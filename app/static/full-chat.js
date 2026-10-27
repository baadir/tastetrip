'use strict';
// A single conversation hosts every result and every consequential approval.
const chatCards=[],baseChatAction=chatAction,baseRenderRoute=renderRoute,baseOpenReservation=openReservation,baseOpenAttempt=openReservationAttempt;
let fullChatReady=false,fullChatOwner=null;const conversationNodes={};
const originalBusy=busy;busy=async function(button,action,label='Hazırlanıyor…'){return originalBusy(button,async()=>{const epoch=chatEpoch;try{return await action();}catch(error){if(fullChatReady&&epoch===chatEpoch)sayInChat(error.message+' Önceki seçimlerin korundu; ilgili karttan yeniden deneyebilir veya mesajla değiştirebilirsin.');throw error;}},label);};
function lastTurn(){return [...conversation.messages].reverse().find(m=>m.role==='user')?.turn_id||null;}
function reflowChatTools(){
 if(!fullChatReady)return;
 if(conversation.messages.length){const suggestions=$('chat-experience').querySelector('.chat-suggestions');suggestions.innerHTML=['Show my itinerary', 'Find flights', 'Show my preferences'].map(text=>`<button type="button" data-prompt="${text}">${text}</button>`).join('');}
 for(const card of chatCards){
  const index=card.turn?conversation.messages.findIndex(m=>m.turn_id===card.turn):-1;
  const target=index>=0?$('chat-messages').querySelector(`[data-message-index="${index+1}"] .chat-bubble`):$('chat-messages').querySelector('.chat-assistant .chat-bubble');
  if(target)target.append(card.element);else $('conversation-scroll')?.append(card.element);
 }
}
function chatCard(title,content=null,key=null){
 let card=key&&chatCards.find(c=>c.key===key);
 if(card){card.turn=lastTurn();card.element.hidden=false;reflowChatTools();return card.element;}
 const el=document.createElement('section');el.className='conversation-card';el.setAttribute('aria-label',title);
 const heading=document.createElement('h3');heading.textContent=title;el.append(heading);if(content)el.append(content);
 card={element:el,turn:lastTurn(),key};chatCards.push(card);reflowChatTools();requestAnimationFrame(()=>{if(el.isConnected&&!el.hidden)el.scrollIntoView({block:'nearest'});});return el;
}
function sayInChat(text){const p=document.createElement('p');p.className='chat-text';p.textContent=text;return chatCard('TasteTrip',p);}
function chatButton(parent,label,action,primary=false){const b=document.createElement('button');b.type='button';b.className=primary?'primary':'secondary';b.textContent=label;b.addEventListener('click',()=>busy(b,action));parent.append(b);return b;}
function askInChat(text,context={}){$('chat-input').value=text;return sendChat(text,context);}
savePlan=async function(){try{await api('plans/save',{});sayInChat('Rotan hesabına kaydedildi. Rotalarım’dan yeniden açabilirsin.');}catch(e){if(e.code==='login_required'){state.user=null;needAuth(savePlan);}else throw e;}};
function showProfileInChat(){
 const p=state.profile;if(!p)return;const content=document.createElement('div');
 const options=tasteView.options||{};
 for(const key of ['themes','cuisines','atmosphere','required_atmosphere','dietary','favorites','excluded']){
  if(!p[key]?.length)continue;
  const row=document.createElement('div');row.className='profile-chat-row';const label=document.createElement('strong');label.textContent=fieldLabels[key];row.append(label);
  for(const item of p[key]){const id=typeof item==='string'?item:item.id;const display=typeof item==='object'?item.name:(options[key==='required_atmosphere'?'atmosphere':key]||[]).find(x=>(typeof x==='string'?x:x.id)===id);const name=typeof display==='object'?display.name:display||id.split(':').pop();
   chatButton(row,name+' ×',async()=>{const current=state.profile;const changes={[key]:current[key].filter(x=>(typeof x==='string'?x:x.id)!==id)};const result=await api('profile',{profile_version:current.profile_version,changes},'PATCH');state.profile=result.profile;await refreshTasteProfile();showProfileInChat();});}
  content.append(row);
 }
 const info=document.createElement('p');info.textContent=`Tempo: ${p.pace} · Bütçe: ${['','Ekonomik','Orta','Yüksek','Esnek'][p.budget]} · Ulaşım: ${p.transport} · Ana dil: ${reservationLanguageLabel(p.locale.native_language)}`;content.append(info);
 for(const [kind,entry] of Object.entries(p.content)){const line=document.createElement('p');line.textContent=`${mediaLabels[kind]?.[1]||kind}: ${[entry.query,...(entry.tastes||[]).map(x=>x.name),entry.language&&reservationLanguageLabel(entry.language)].filter(Boolean).join(' · ')}`;content.append(line);}
 if(p.special_requirements){const condition=document.createElement('p');condition.textContent='Özel koşul: '+p.special_requirements;content.append(condition);chatButton(content,'Özel koşulu genel profilden kaldır',async()=>{await api('profile',{profile_version:state.profile.profile_version,changes:{special_requirements:''}},'PATCH');await refreshTasteProfile();showProfileInChat();});}
 const help=document.createElement('p');help.textContent='Değiştirmek istediğini mesajla söyle: “Genel gezi tempomu yoğun yap” veya “Podcastleri İngilizce dinlemek isterim.” Yukarıdaki × yalnız o tercihi kaldırır.';content.append(help);
 const card=chatCard('Seni nasıl tanıyorum?',null,'profile');card.replaceChildren(document.createElement('h3'),content);card.firstChild.textContent='Seni nasıl tanıyorum?';
 chatButton(card,p.persistence==='device'?'Bu cihazda hatırlamayı kapat':'Bu cihazda beni hatırla',async()=>{$('chat-remember').click();});
 chatButton(card,'Zevk profilimi sıfırlamayı incele',async()=>confirmProfileReset());
}
function confirmProfileReset(){const card=chatCard('Zevk profilini sıfırla');const note=document.createElement('p');note.textContent='Genel tercihlerin sıfırlanacak. Rotaların ve restoran rezervasyonların korunur.';card.append(note);chatButton(card,'Evet, genel tercihlerimi sıfırla',async()=>{await api('profile/reset',{profile_version:state.profile.profile_version});await refreshTasteProfile();card.textContent='Genel tercihlerin sıfırlandı. Seni yeniden tanıyabiliriz.';},true);chatButton(card,'Vazgeç',async()=>{card.hidden=true;});}
function confirmNewConversation(){const card=chatCard('Yeni bir sohbet');card.append(document.createTextNode('Mevcut sohbet metni silinecek. Genel tercihlerin, kayıtlı rotaların ve rezervasyonların korunur. Devam eden telefon araması bu işlemle durmaz.'));chatButton(card,'Sohbeti temizle ve yenisini başlat',async()=>{disconnectReservationAudio();const data=await api('chat/clear',{revision:conversation.revision});for(const node of Object.values(conversationNodes))$('legacy-planner').append(node);for(let i=chatCards.length-1;i>=0;i--){if(chatCards[i].key?.startsWith('dialog:'))chatCards[i].element.hidden=true;else{chatCards[i].element.remove();chatCards.splice(i,1);}}conversation=data.thread;renderChat(data.welcome);},true);chatButton(card,'Vazgeç',async()=>{card.hidden=true;});}
function inlineDialog(id,title){
 const dialog=$(id);dialog.classList.add('conversation-dialog');dialog.hidden=true;
 const card=chatCard(title,dialog,'dialog:'+id);card.hidden=true;
 dialog.showModal=function(){card.hidden=false;this.hidden=false;this.open=true;chatCards.find(c=>c.key==='dialog:'+id).turn=lastTurn();show('discover');reflowChatTools();this.scrollIntoView({block:'nearest'});};
 dialog.close=function(){this.open=false;this.hidden=true;card.hidden=true;this.dispatchEvent(new Event('close'));};
 return dialog;
}
async function showSavedInChat(){needAuth(async()=>{const epoch=chatEpoch;const result=await api('plans');if(epoch!==chatEpoch)return;const card=chatCard('Kaydettiğin rotalar');if(!result.plans.length){card.append(document.createTextNode('Henüz kayıtlı rotan yok. Birlikte bir yolculuk planlayalım.'));return;}
 for(const plan of result.plans)chatButton(card,`${plan.trip.city} · ${plan.trip.start} · ${plan.trip.days} gün`,async()=>{const result=await api('plans/open',{id:plan.id});state.plan=result.plan;state.day=0;applyTrip(result.plan.trip);renderRoute();});});}
async function showReservationsInChat(){needAuth(async()=>{const epoch=chatEpoch;await refreshReservations();if(epoch!==chatEpoch)return;const card=chatCard('Rezervasyonların',null,'reservation-list');card.append($('reservation-list'));$('reservation-list').hidden=false;});}
async function startReservationConversation(stopId,retryOf=null){
 const stop=getStop(stopId);if(!stop)return;
 if(stop.reservation_id&&!retryOf){needAuth(()=>openReservationAttempt(stop.reservation_id));return;}
 reservationUI.retryOf=retryOf;
 await askInChat(`${stop.name} için rezervasyon planlamak istiyorum. Eksik bilgileri konuşarak tamamlayalım.`,{task_mode:'reserve',stop_id:stopId});
}
async function reviewReservationInChat(draft){
 const stop=getStop(draft.stop_id);if(!stop)throw new Error('Bu durak artık açık rotanda değil. Güncel rotadan seç.');
 return needAuth(async()=>{
  // Reuse the production validation/review/start path; no model output can check these boxes.
  const epoch=chatEpoch;await baseOpenReservation(stop.id,reservationUI.retryOf);if(epoch!==chatEpoch){$('reservation-dialog').close();return;}
  const form=$('reservation-form');for(const [key,value] of Object.entries(draft)){const field=form.elements.namedItem(key);if(field&&key!=='phone_verified'&&key!=='timezone_verified')field.value=value??'';}
  form.hidden=true;$('reservation-review').hidden=true;
  let intake=$('chat-reservation-intake');if(!intake){intake=document.createElement('section');intake.id='chat-reservation-intake';$('reservation-dialog').insertBefore(intake,$('reservation-error'));}
  intake.hidden=false;intake.replaceChildren();const summary=document.createElement('p');summary.className='chat-text';summary.textContent=`${stop.name}\n${draft.local_date} · ${draft.local_time} · ${draft.timezone}\n${draft.people} kişi · ${draft.booking_name}\nTelefon: ${stop.phone}\nGörüşme: ${reservationLanguageLabel(draft.conversation_language)} · Altyazı/özet: ${reservationLanguageLabel(draft.native_language)}\n${draft.notes||'Özel istek yok.'}`;intake.append(summary);
  const disclosure=document.createElement('p');disclosure.textContent='Ülke, görüşme dili ve saat dilimi başlangıç önerisidir. Kaynak bağlantısından işletme/telefon eşleşmesini ve restoranın yerel saatini kontrol et. Rota hesabına kaydedilir. Konuşma metni ve özet 30 gün tutulur.';intake.append(disclosure);
  for(const [key,text] of [['phone_verified','Telefonun bu işletmeye ait olduğunu kaynakta kontrol ettim.'],['timezone_verified','Tarih, saat ve saat diliminin restoranın yerel saatine uygunluğunu kontrol ettim.']]){const label=document.createElement('label');label.className='register-label';const check=document.createElement('input');check.type='checkbox';check.addEventListener('change',()=>{form.elements[key].checked=check.checked;});form.elements[key].checked=false;label.append(check,document.createTextNode(text));intake.append(label);}
  chatButton(intake,'Bu koşulları doğrula ve arama özetini hazırla',async()=>{if(!form.elements.phone_verified.checked||!form.elements.timezone_verified.checked)throw new Error('İşletme/telefon ve yerel saat kontrolünü açıkça onayla.');if(!form.reportValidity())throw new Error('Eksik veya desteklenmeyen bir alan var. Düzeltmeyi sohbetle belirt.');form.requestSubmit($('reservation-prepare'));},true);
  chatButton(intake,'Koşulları sohbetle düzelt',async()=>{sayInChat('Neyi değiştirmek istersin? Örneğin “Saati 20:00 yap, aynı gün ve kişi sayısı kalsın.”');$('chat-input').focus();});
 });
}
async function flightsInChat(draft){
 const epoch=chatEpoch;const card=chatCard('Uçuşun için havalimanını seç');const result=await Promise.all([api('airports',{query:draft.origin_query}),api('airports',{query:draft.destination_query})]);if(epoch!==chatEpoch)return;
 let chosen={};const groups=[];
 for(let i=0;i<2;i++){const group=document.createElement('div');const title=document.createElement('p');title.textContent=(i?'Varış: ':'Kalkış: ')+(i?draft.destination_query:draft.origin_query);group.append(title);card.append(group);groups.push(group);
  for(const row of result[i].results){const choice=chatButton(group,`${row.name} · ${row.country} · ${row.code}`,async()=>{chosen[i]=row.code;for(const b of group.querySelectorAll('button'))b.setAttribute('aria-pressed',String(b===choice));if(chosen[0]&&chosen[1])search.disabled=false;});}
  if(!result[i].results.length)group.append(document.createTextNode('Eşleşme bulunamadı; şehir adını sohbetten düzelt.'));
 }
 const search=chatButton(card,`${draft.departure}${draft.return?' → '+draft.return:' · Tek yön'} için fiyatları ara`,async()=>{const data=await api('flights',{origin:chosen[0],destination:chosen[1],departure:draft.departure,return:draft.return||null});if(epoch!==chatEpoch)return;const resultCard=chatCard('Uçuş seçeneklerin');const content=document.createElement('div');content.innerHTML=`<p class="notice">${esc(data.notice)}</p>`+link(data.search_url,'Aviasales’te fiyatı incele ↗')+(data.results.length?data.results.map(f=>`<article class="flight-card"><strong>${esc(f.origin)} → ${esc(f.destination)} · ${esc(f.price)} ${esc(f.currency)}</strong><p>${esc(f.departure)}${f.return?' → '+esc(f.return):' · Tek yön'} · ${esc(f.transfers)} aktarma · ${esc(f.airline)}</p></article>`).join(''):'<p>Tam bu tarihlerde önbellek fiyatı bulunamadı. Bu, uçuş olmadığı anlamına gelmez.</p>');resultCard.append(content);},true);search.disabled=true;
}
async function mediaInChat(draft){
 const epoch=chatEpoch;const stop=getStop(draft.stop_id);if(!stop)throw new Error('Öneri alacağın durağı güncel rotandan seç.');
 const kind=draft.kind,card=chatCard(`${stop.name} · ${mediaLabels[kind]?.[1]||kind} keşfi`);
 const saved=state.profile.content[kind]||{};let tastes=saved.tastes||[];
 if(draft.query){const topic=kind==='podcast'||kind==='book'&&draft.mode!=='title';const data=topic?await api('content/topics',{query:draft.query,kind}):await api('interests/search',{query:draft.query,kind});if(epoch!==chatEpoch)return;const matches=topic?data.topics:data.results;tastes=[];
  const note=document.createElement('p');note.textContent='Zevkini anlatan gerçek Qloo eşleşmelerini seç. Bunlar bu öneriye özeldir.';card.append(note);
  for(const item of matches){const choice=chatButton(card,item.name,async()=>{const found=tastes.findIndex(x=>x.id===item.id);if(found>=0)tastes.splice(found,1);else if(tastes.length<5)tastes.push({id:item.id,name:item.name});else throw new Error('En fazla 5 eşleşme seçebilirsin.');choice.setAttribute('aria-pressed',String(tastes.some(x=>x.id===item.id)));});}
  if(!matches.length)card.append(document.createTextNode('Qloo eşleşmesi bulunamadı. Başka bir konu söyle veya tercihsiz öneri al.'));
 }
 const options=document.createElement('p');const language=['book','podcast'].includes(kind)?draft.language||saved.language||'any':'any';options.textContent='İçerik dili: '+(language==='any'?'Dil fark etmez':reservationLanguageLabel(language))+'. Konu veya dili değiştirmek için mesaj yazabilirsin.';card.append(options);
 chatButton(card,'Seçimlerimle öneri al',async()=>{const data=await api('recommend',{stop_id:stop.id,kind,tastes,skip_taste:!tastes.length,language,remember_profile:false});if(epoch!==chatEpoch)return;const result=chatCard('Bu molaya eşlik etsin');const content=document.createElement('div');content.innerHTML=`<p>${esc(data.basis)}</p>`+(data.language_status?`<p>${esc(data.language_status.matched)} dil eşleşmesi · ${esc(data.language_status.unknown)} adayın dili doğrulanamadı.</p>`:'')+(data.results.length?data.results.map(item=>`<article class="media-card">${safeURL(item.image)?`<img src="${esc(item.image)}" alt="${esc(item.name)} kapağı" loading="lazy">`:''}<div><h3>${esc(item.name)}</h3>${link(kind==='podcast'?item.apple_url:item.website,kind==='podcast'?'Apple Podcasts’te aç ↗':'Kaynakta incele ↗')}</div></article>`).join(''):'<p>Bu koşullarla sonuç bulunamadı. Dili veya konuyu sohbetten değiştirebilirsin.</p>');result.append(content);},true);
 chatButton(card,'Seçtiğim zevki genel profilime de kaydet',async()=>{const p=state.profile;const entry={tastes,query:draft.query||'',...(['book','podcast'].includes(kind)?{language}:{})};await api('profile',{profile_version:p.profile_version,changes:{content:{[kind]:entry}}},'PATCH');await refreshTasteProfile();sayInChat('Seçtiğin içerik zevki genel profiline kaydedildi.');});
}
chatAction=async function(button){
 const [i,j]=button.dataset.chatAction.split(':').map(Number),a=conversation.messages[i]?.actions?.[j];if(!a)return;
 if(['plan','revise','lookup'].includes(a.type))return baseChatAction(button);
 return busy(button,async()=>{
  if(a.type==='current_route'){if(!state.plan)throw new Error('Henüz bir rotan yok. Nereye gitmek istersin?');renderRoute();return;}
  if(['listen_call','stop_call','call_status'].includes(a.type)){return needAuth(async()=>{await refreshReservations();const item=reservationUI.attempt||reservationUI.items[0];if(!item){sayInChat('Henüz rezervasyon girişimin yok. Rota kartından başlayabiliriz.');return;}await openReservationAttempt(item.id);});}
  if(a.type==='profile')return showProfileInChat();if(a.type==='saved')return showSavedInChat();if(a.type==='save')return needAuth(savePlan);if(a.type==='reservations')return showReservationsInChat();
  if(a.type==='flights')return flightsInChat(a.draft);if(a.type==='media')return mediaInChat(a.draft);if(a.type==='reserve')return reviewReservationInChat(a.draft);if(a.type==='reset_profile')return confirmProfileReset();
  if(a.type==='logout'){$('account').click();return;}if(a.type==='forget'){const card=chatCard('Cihazdaki veriyi temizle');card.append(document.createTextNode('Bu cihazın anonim tercihleri, taslağı ve anonim sohbeti silinir. Hesap verilerin korunur.'));chatButton(card,'Evet, cihazdaki veriyi temizle',async()=>{$('forget').click();card.hidden=true;});}
 });
};
renderRoute=function(){baseRenderRoute();if(fullChatReady){chatCard('Yolculuğun',null,'route').append($('route-area'));reflowChatTools();}};
openReservation=startReservationConversation;
openReservationAttempt=async function(id){if($('chat-reservation-intake'))$('chat-reservation-intake').hidden=true;return baseOpenAttempt(id);};
openMedia=function(stopId){const stop=getStop(stopId);if(stop)askInChat(`${stop.name} durağındaki molam için içerik önerisi almak istiyorum.`,{task_mode:'media',stop_id:stopId});};
openMenu=function(stopId){const stop=getStop(stopId);if(!stop||!safeURL(stop.menu_url))return;const card=chatCard(stop.name+' · Menü');const frame=document.createElement('iframe');frame.title=stop.name+' menüsü';frame.src=safeURL(stop.menu_url);frame.setAttribute('sandbox','allow-scripts allow-same-origin allow-popups');frame.className='conversation-menu';card.append(frame);const links=document.createElement('div');links.innerHTML='<p>Kaynak site gömülmeyi engellerse menüyü kaynakta açabilirsin.</p>'+link(stop.menu_url,'Menüyü kaynakta aç ↗');card.append(links);};
window.addEventListener('chat-rendered',reflowChatTools);
window.addEventListener('DOMContentLoaded',()=>{
 fullChatReady=true;document.body.classList.add('full-chat');conversationNodes.route=$('route-area');conversationNodes.reservations=$('reservation-list');
 const header=document.createElement('header');header.className='conversation-header';header.innerHTML='<a class="brand" href="/">taste<span>trip</span></a><span>A journey shaped around you.</span><div id="conversation-shortcuts"></div>';
 $('chat-experience').prepend(header);
 const shortcuts=$('conversation-shortcuts');for(const [label,action] of [['My preferences',showProfileInChat],['My trips',showSavedInChat],['My reservations',showReservationsInChat],['Find flights',()=>askInChat("I would like to find flights. Let us work out the origin, destination and dates.")],['My account',()=>{$('account').click();}],['New chat',async()=>confirmNewConversation()],['Fresh session',async()=>{await api('session/new',{});location.reload();}]])chatButton(shortcuts,label,async()=>action());
 const accountButton=[...shortcuts.querySelectorAll('button')].find(b=>b.textContent==='My account');if(accountButton){accountButton.dataset.account='1';accountButton.textContent=state.user?state.user.username+' · Sign out':'Sign in';}
 const scroller=document.createElement('div');scroller.id='conversation-scroll';$('chat-messages').before(scroller);scroller.append($('chat-messages'));
 for(const [id,title] of [['auth-dialog','Güvenli hesap adımı'],['taste-import-dialog','Cihaz tercihlerini hesabına taşı'],['reservation-dialog','Rezervasyon görüşmesi']])inlineDialog(id,title);
 // Keep passwords out of the conversation and the model context, even with inline account UI.
 $('auth-dialog').querySelector('.muted').textContent='Bu güvenli kartta giriş yap. Parolan sohbet geçmişine veya DeepSeek’e gönderilmez. İşlemden sonra konuşmaya devam edeceğiz.';
 $('taste-dialog').showModal=showProfileInChat;
 $('chat-profile').onclick=showProfileInChat;
 $('reservation-edit').addEventListener('click',()=>{ $('reservation-form').hidden=true;$('reservation-review').hidden=true;if($('chat-reservation-intake'))$('chat-reservation-intake').hidden=true;sayInChat('Rezervasyon koşullarında neyi değiştirmek istersin? Mesajla söyleyebilirsin.');$('chat-input').focus();});
 new MutationObserver(()=>{if(!$('reservation-review').hidden&&$('chat-reservation-intake'))$('chat-reservation-intake').hidden=true;}).observe($('reservation-review'),{attributes:true,attributeFilter:['hidden']});
 const oldShow=show;show=function(view){oldShow('discover');};
 // Navigation buttons from earlier modules now resolve to conversation cards.
 showSaved=showSavedInChat;
 const originalRender=renderReservationList;renderReservationList=function(){originalRender();if(chatCards.some(c=>c.key==='reservation-list'))reflowChatTools();};
 window.addEventListener('taste-identity',()=>{const account=[...$('conversation-shortcuts').querySelectorAll('button')].find(b=>b.dataset.account==='1');if(account)account.textContent=state.user?state.user.username+' · Sign out':'Sign in';const owner=state.user?.id||'visitor';if(fullChatOwner!==owner){fullChatOwner=owner;for(const node of Object.values(conversationNodes))$('legacy-planner').append(node);for(let i=chatCards.length-1;i>=0;i--){const card=chatCards[i];if(card.key?.startsWith('dialog:')){card.element.hidden=true;card.turn=null;const d=card.element.querySelector('dialog');if(d){d.open=false;d.hidden=true;}}else{card.element.remove();chatCards.splice(i,1);}}reflowChatTools();} });
 if(state.plan)renderRoute();
});
