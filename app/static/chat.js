'use strict';
let conversation={revision:0,messages:[],trip:{}},chatSending=false,chatRetry=null,chatEpoch=0,chatPending=null,chatSendError='';
const fieldLabels={...tasteFieldLabels,persistence:'Hatırlama'};
function chatProfile(){
  const p=state.profile;if(!p)return;
  const values=[...p.themes,...p.cuisines.map(id=>tasteView.options?.cuisines.find(x=>x.id===id)?.name||id.split(':').pop()),...(p.profile_version?[p.pace]:[])];
  $('chat-memory').textContent=values.length?values.join(' · '):'Seni tanıdıkça burada birikecek.';
  $('chat-storage').textContent=state.user?'Tercihler hesabında · son 100 mesaj':p.persistence==='device'?'Bu cihazda hatırlanır · son 100 mesaj':'Misafir oturumu · son 100 mesaj';
}
function renderChat(welcome){
  const messages=conversation.messages.length?[...conversation.messages]:[{role:'assistant',text:welcome||"Let us explore your next journey. What excites you most when you travel?"}];
  if(chatPending&&!conversation.messages.some(m=>m.turn_id===chatPending.turn_id))messages.push(chatPending);
  $('chat-messages').innerHTML=messages.map((m,i)=>`<article data-message-index="${i}" class="chat-message ${m.role==='user'?'chat-user':'chat-assistant'}"><span class="chat-avatar" aria-hidden="true">${m.role==='user'?'S':'✦'}</span><div class="chat-bubble"><p class="chat-author">${m.role==='user'?'You':'TasteTrip'}</p><div class="chat-text">${esc(m.text)}</div>${m.pending?`<small class="muted">${chatSendError?'Could not send; your message is preserved.':'Sending…'}</small>`:''}${m.saved?.length?`<div class="chat-receipt">✓ Profile kaydedildi: ${m.saved.map(k=>esc(fieldLabels[k]||k)).join(', ')} <button type="button" data-chat-edit>İncele / düzelt</button></div>`:''}${(m.actions||[]).map((a,j)=>`${a.type==='plan'?`<p class="chat-trip-preview">${esc(a.trip.city)} · ${esc(a.trip.start)} · ${esc(a.trip.days)} gün · ${esc(a.trip.people)} kişi · ${esc(a.trip.pace)}</p>`:''}<button type="button" class="secondary chat-action" data-chat-action="${i}:${j}">${a.type==='plan'?'Bu bilgilerle rotamı oluştur ↗':a.type==='revise'?'Rotaya bu değişikliği uygula ↗':a.type==='lookup'?'Qloo’da eşleşmeleri bul: '+esc(a.query):esc(({current_route:'Rotamı konuşmada göster',listen_call:'Canlı görüşmeyi aç',stop_call:'Aramayı durdurma kontrolünü aç',call_status:'Görüşme durumunu göster',profile:'Tercihlerimi göster',saved:'Rotalarımı göster',save:'Rotayı hesabıma kaydet',reservations:'Rezervasyonlarımı göster',flights:'Uçuş seçeneklerini bul',media:'Bu mola için öneri al',reserve:'Rezervasyon koşullarını incele',reset_profile:'Profil sıfırlamasını incele',logout:'Çıkış yap',forget:'Cihaz verisini temizlemeyi incele'})[a.type]||'Devam et')}</button>`).join('')}</div></article>`).join('');
  $('chat-messages').lastElementChild?.scrollIntoView({block:'nearest',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});chatProfile();window.dispatchEvent(new Event('chat-rendered'));
}
async function loadChat(){const epoch=chatEpoch;const data=await api('chat');if(epoch!==chatEpoch)return;conversation=data.thread;state.profile=data.profile;renderChat(data.welcome);}
async function sendChat(text,context={}){
  if(chatSending||!text.trim())return;chatSending=true;$('chat-send').disabled=true;$('chat-status').textContent='Thinking about your preferences and your trip…';
  const epoch=chatEpoch;const pending=chatRetry?.text===text?chatRetry:{text,id:crypto.randomUUID().replaceAll('-',''),context};chatRetry=pending;chatPending={role:'user',text,turn_id:pending.id,pending:true};chatSendError='';renderChat();
  try{const result=await api('chat',{message:text,turn_id:pending.id,revision:conversation.revision,has_route:!!state.plan,...(pending.context||context)});if(epoch!==chatEpoch)return;conversation=result.thread;state.profile=result.profile;chatRetry=null;chatPending=null;if($('chat-input').value===text)$('chat-input').value='';renderChat(result.welcome);await refreshTasteProfile();chatProfile();$('chat-status').textContent='';}
  catch(e){if(epoch!==chatEpoch)return;chatSendError=e.message;renderChat();$('chat-status').textContent=e.message+' Mesajın giriş alanında korundu.';if(e.message.includes('değişti'))await loadChat();}
  finally{chatSending=false;$('chat-send').disabled=false;$('chat-input').focus();}
}
async function chatAction(button){
 const [i,j]=button.dataset.chatAction.split(':').map(Number),action=conversation.messages[i]?.actions?.[j];if(!action)return;
 await busy(button,async()=>{
  if(action.type==='plan'){const result=await api('plan',action.trip);state.plan=result.plan;state.day=0;applyTrip(result.plan.trip);renderRoute();$('route-area').scrollIntoView({block:'start',behavior:'smooth'});return;}
  if(action.type==='revise'){if(!state.plan)throw new Error('Önce bir rota oluştur.');const result=await api('revise',{revision:state.plan.revision,instruction:action.instruction});if(result.clarification){notify(result.clarification);return;}state.plan=result.plan;renderRoute();return;}
  const result=action.mode==='cuisine'?await api('profile/cuisines',{query:action.query}):action.mode==='topic'?await api('content/topics',{query:action.query,kind:action.kind}):await api('interests/search',{query:action.query,kind:action.kind});
  const container=document.createElement('div');container.className='chat-matches';container.textContent='Seni anlatan gerçek kaydı seç; seçimin genel profiline kaydedilecek.';button.after(container);
  for(const item of (result.results||result.topics||[])){const choice=document.createElement('button');choice.className='result-button';choice.textContent=[item.name,item.disambiguation].filter(Boolean).join(' · ');choice.addEventListener('click',()=>busy(choice,async()=>{
    await refreshTasteProfile();const p=state.profile;let changes;
    if(action.mode==='cuisine')changes={cuisines:[...new Set([...p.cuisines,item.id])]};
    else if(action.mode==='topic'){const entry=p.content[action.kind]||{};changes={content:{[action.kind]:{...entry,tastes:[...(entry.tastes||[]).filter(x=>x.id!==item.id),item].slice(-5),query:action.query}}};}
    else changes={favorites:[...p.favorites.filter(x=>x.id!==item.id),item].slice(-20)};
    await api('profile',{profile_version:p.profile_version,changes},'PATCH');await refreshTasteProfile();chatProfile();container.textContent='✓ '+item.name+' genel profiline kaydedildi. Tercihlerim’den değiştirebilirsin.';
  }));container.append(choice);}
  if(!(result.results||result.topics||[]).length)container.textContent='Qloo’da eşleşme bulunamadı. Başka bir isim veya konu deneyebilirsin.';
 },'Hazırlanıyor…');
}
window.addEventListener('DOMContentLoaded',async()=>{
 document.body.classList.add('chat-first');
 const discover=$('discover'),legacy=document.createElement('div');legacy.hidden=true;legacy.id='legacy-planner';
 for(const element of [...discover.children])if(element.id!=='route-area')legacy.append(element);
 discover.prepend(legacy);
 const chat=document.createElement('section');chat.id='chat-experience';chat.innerHTML=`<div class="chat-cover"><div><p class="eyebrow">SEN ANLAT. YOLCULUĞUN ŞEKİLLENSİN.</p><h1>Dünyayı <em>kendi zevkinle</em> keşfet.</h1><p>Birkaç güzel sohbet. Sana benzeyen duraklar. Birlikte çizdiğimiz bir rota.</p></div><img src="/static/atmosphere.jpg" alt="Akdeniz terası; temsili seyahat fotoğrafı"></div><div class="chat-workspace"><section class="chat-thread" aria-label="Chat with your travel assistant"><div id="chat-messages" role="log" aria-label="Conversation messages" aria-live="polite"></div><div class="chat-suggestions"><button type="button" data-prompt="I love local food and quiet cafes.">☕ Local flavors and little breaks</button><button type="button" data-prompt="I enjoy museums and art.">◈ Art and culture</button><button type="button" data-prompt="I would like to skip introductions and plan my trip.">↗ Let's plan my trip</button></div><form id="chat-form"><label class="sr-only" for="chat-input">Your message</label><textarea id="chat-input" rows="2" maxlength="2000" placeholder="Tell me about yourself or your dream trip…" required></textarea><button type="submit" class="primary" id="chat-send" aria-label="Send message">Send ↗</button></form><p id="chat-status" role="status"></p><p class="chat-disclosure">Your assistant saves preferences you explicitly share to your profile. Trip-specific requests stay separate. You can change them anytime.</p></section><aside class="chat-context"><span class="chat-compass">✦</span><p class="eyebrow">SENİN SEYAHAT İZİN</p><h2>Biraz daha sen.</h2><p id="chat-memory"></p><button type="button" id="chat-profile" class="text-button">Tercihlerimi incele ↗</button><p id="chat-storage" class="muted"></p><button type="button" id="chat-remember" class="secondary">Bu cihazda beni hatırla</button><button type="button" id="chat-clear" class="text-button">Sohbeti temizle</button><p class="muted">Sohbet ve tercihler sunucuda saklanır. Cookie yalnız tanıma kimliğini taşır. Etkin olmayan sohbetler 30 gün sonra servis başlangıcında temizlenir. Şifre veya ödeme bilgisi paylaşma.</p></aside></div>`;
 const flights=legacy.querySelector('.flight-panel');if(flights)chat.append(flights);
 discover.insertBefore(chat,$('route-area'));$('route-area').classList.add('chat-route');$('revision-form').closest('.revision-panel').hidden=true;
 $('chat-form').addEventListener('submit',e=>{e.preventDefault();sendChat($('chat-input').value);});
 $('chat-input').addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault();sendChat(e.target.value);}});
 chat.addEventListener('click',e=>{const prompt=e.target.closest('[data-prompt]'),action=e.target.closest('[data-chat-action]');if(prompt){$('chat-input').value=prompt.dataset.prompt;sendChat(prompt.dataset.prompt);}if(action)chatAction(action);if(e.target.closest('[data-chat-edit]'))$('taste-nav').click();});
 $('chat-profile').onclick=()=>$('taste-nav').click();
 $('chat-remember').onclick=()=>busy($('chat-remember'),async()=>{await refreshTasteProfile();const p=state.profile;await api('profile',{profile_version:p.profile_version,changes:{persistence:p.persistence==='device'?'session':'device'}},'PATCH');await refreshTasteProfile();chatProfile();$('chat-remember').textContent=state.profile.persistence==='device'?'Bu cihazda hatırlama açık · kapat':'Bu cihazda beni hatırla';});
 $('chat-clear').onclick=()=>busy($('chat-clear'),async()=>{const data=await api('chat/clear',{revision:conversation.revision});conversation=data.thread;renderChat(data.welcome);});
 // Ownership changes replace the visible conversation; anonymous history is never silently imported.
 for(const id of ['auth-dialog','taste-dialog','taste-import-dialog'])$(id).addEventListener('close',()=>loadChat().catch(e=>notify(e.message)));
 window.addEventListener('taste-profile',chatProfile);
 window.addEventListener('taste-identity',()=>{chatEpoch++;chatPending=null;chatSendError='';conversation={revision:0,messages:[],trip:{}};$('chat-messages').replaceChildren();loadChat().catch(e=>notify(e.message));});
});
