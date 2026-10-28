'use strict';
// Conversation hosts travel planning; reservation approval and live calls use a modal.
const chatCards=[],baseChatAction=chatAction,baseRenderRoute=renderRoute,baseOpenReservation=openReservation,baseOpenAttempt=openReservationAttempt;
let fullChatReady=false,fullChatOwner=null;const conversationNodes={};
const originalBusy=busy;busy=async function(button,action,label='Preparing…'){return originalBusy(button,async()=>{const epoch=chatEpoch;try{return await action();}catch(error){if(fullChatReady&&epoch===chatEpoch){if(button.closest('#reservation-dialog'))$('reservation-error').textContent=error.message;else sayInChat(error.message+' Your previous selections were kept; you can try again from the relevant card or change it via message.');}throw error;}},label);};
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
savePlan=async function(){try{await api('plans/save',{});sayInChat('Your route has been saved to your account. You can reopen it from My Routes.');}catch(e){if(e.code==='login_required'){state.user=null;needAuth(savePlan);}else throw e;}};
function showProfileInChat(){
 const p=state.profile;if(!p)return;const content=document.createElement('div');
 const options=tasteView.options||{};
 for(const key of ['themes','cuisines','atmosphere','required_atmosphere','dietary','favorites','excluded']){
  if(!p[key]?.length)continue;
  const row=document.createElement('div');row.className='profile-chat-row';const label=document.createElement('strong');label.textContent=fieldLabels[key];row.append(label);
  for(const item of p[key]){const id=typeof item==='string'?item:item.id;const display=typeof item==='object'?item.name:(options[key==='required_atmosphere'?'atmosphere':key]||[]).find(x=>(typeof x==='string'?x:x.id)===id);const name=typeof display==='object'?display.name:display||id.split(':').pop();
   chatButton(row,uiLabel(name)+' ×',async()=>{const current=state.profile;const changes={[key]:current[key].filter(x=>(typeof x==='string'?x:x.id)!==id)};const result=await api('profile',{profile_version:current.profile_version,changes},'PATCH');state.profile=result.profile;await refreshTasteProfile();showProfileInChat();});}
  content.append(row);
 }
 const info=document.createElement('p');info.textContent=`Pace: ${uiLabel(p.pace)} · Budget: ${['','Budget','Mid-range','High','Flexible'][p.budget]} · Transport: ${uiLabel(p.transport)} · Native language: ${reservationLanguageLabel(p.locale.native_language)}`;content.append(info);
 for(const [kind,entry] of Object.entries(p.content)){const line=document.createElement('p');line.textContent=`${mediaLabels[kind]?.[1]||kind}: ${[entry.query,...(entry.tastes||[]).map(x=>x.name),entry.language&&reservationLanguageLabel(entry.language)].filter(Boolean).join(' · ')}`;content.append(line);}
 if(p.special_requirements){const condition=document.createElement('p');condition.textContent='Custom condition: '+p.special_requirements;content.append(condition);chatButton(content,'Remove custom condition from general profile',async()=>{await api('profile',{profile_version:state.profile.profile_version,changes:{special_requirements:''}},'PATCH');await refreshTasteProfile();showProfileInChat();});}
 const help=document.createElement('p');help.textContent='Tell me in a message what you want to change: “Make my general travel pace packed” or “I\'d like to listen to podcasts in English.” The × above only removes that preference.';content.append(help);
 const card=chatCard('How do I know you?',null,'profile');card.replaceChildren(document.createElement('h3'),content);card.firstChild.textContent='How do I know you?';
 chatButton(card,p.persistence==='device'?'Turn off remembering on this device':'Remember me on this device',async()=>{$('chat-remember').click();});
 chatButton(card,'Review resetting my taste profile',async()=>confirmProfileReset());
}
function confirmProfileReset(){const card=chatCard('Reset taste profile');const note=document.createElement('p');note.textContent='Your general preferences will be reset. Your routes and restaurant reservations are kept.';card.append(note);chatButton(card,'Yes, reset my general preferences',async()=>{await api('profile/reset',{profile_version:state.profile.profile_version});await refreshTasteProfile();card.textContent='Your general preferences have been reset. We can get to know you again.';},true);chatButton(card,'Cancel',async()=>{card.hidden=true;});}
function confirmNewConversation(){const card=chatCard('New chat');card.append(document.createTextNode('The current chat text will be deleted. Your general preferences, saved routes and reservations are kept. An ongoing phone call will not stop with this action.'));chatButton(card,'Clear chat and start a new one',async()=>{disconnectReservationAudio();const data=await api('chat/clear',{revision:conversation.revision});for(const node of Object.values(conversationNodes))$('legacy-planner').append(node);for(let i=chatCards.length-1;i>=0;i--){if(chatCards[i].key?.startsWith('dialog:'))chatCards[i].element.hidden=true;else{chatCards[i].element.remove();chatCards.splice(i,1);}}conversation=data.thread;renderChat(data.welcome);},true);chatButton(card,'Cancel',async()=>{card.hidden=true;});}
function inlineDialog(id,title){
 const dialog=$(id);dialog.classList.add('conversation-dialog');dialog.hidden=true;
 const card=chatCard(title,dialog,'dialog:'+id);card.hidden=true;
 dialog.showModal=function(){card.hidden=false;this.hidden=false;this.open=true;chatCards.find(c=>c.key==='dialog:'+id).turn=lastTurn();show('discover');reflowChatTools();this.scrollIntoView({block:'nearest'});};
 dialog.close=function(){this.open=false;this.hidden=true;card.hidden=true;this.dispatchEvent(new Event('close'));};
 return dialog;
}
async function showSavedInChat(){needAuth(async()=>{const epoch=chatEpoch;const result=await api('plans');if(epoch!==chatEpoch)return;const card=chatCard('Your saved routes');if(!result.plans.length){card.append(document.createTextNode('You don\'t have any saved routes yet. Let\'s plan a journey together.'));return;}
 const source=document.createElement('div');source.innerHTML=qlooAttribution();card.append(source);
 for(const plan of result.plans)chatButton(card,`${plan.trip.city} · ${plan.trip.start} · ${plan.trip.days} days`,async()=>{const result=await api('plans/open',{id:plan.id});state.plan=result.plan;state.day=0;applyTrip(result.plan.trip);renderRoute();});});}
async function showReservationsInChat(){needAuth(async()=>{const epoch=chatEpoch;await refreshReservations();if(epoch!==chatEpoch)return;const card=chatCard('Your reservations',null,'reservation-list');card.append($('reservation-list'));$('reservation-list').hidden=false;});}
async function startReservationConversation(stopId,retryOf=null){
 const stop=getStop(stopId);if(!stop)return;
 if(stop.reservation_id&&!retryOf){needAuth(()=>openReservationAttempt(stop.reservation_id));return;}
 reservationUI.retryOf=retryOf;
 await askInChat(`${stop.name} I want to plan a reservation for. Let's complete the missing details by talking.`,{task_mode:'reserve',stop_id:stopId});
}
async function reviewReservationInChat(draft){
 const stop=getStop(draft.stop_id);if(!stop)throw new Error('This stop is no longer in your active route. Select from the current route.');
 return needAuth(async()=>{
  // Reuse the production validation/review/start path; no model output can check these boxes.
  const epoch=chatEpoch;await baseOpenReservation(stop.id,reservationUI.retryOf);if(epoch!==chatEpoch){$('reservation-dialog').close();return;}
  const form=$('reservation-form');for(const [key,value] of Object.entries(draft)){const field=form.elements.namedItem(key);if(field&&key!=='phone_verified'&&key!=='timezone_verified')field.value=value??'';}
  form.hidden=true;$('reservation-review').hidden=true;
  let intake=$('chat-reservation-intake');if(!intake){intake=document.createElement('section');intake.id='chat-reservation-intake';$('reservation-dialog').insertBefore(intake,$('reservation-error'));}
  intake.hidden=false;intake.replaceChildren();const summary=document.createElement('p');summary.className='chat-text';summary.textContent=`${stop.name}\n${draft.local_date} · ${draft.local_time} · ${draft.timezone}\n${draft.people} people · ${draft.booking_name}\nPhone: ${stop.phone}\nCall: ${reservationLanguageLabel(draft.conversation_language)} · Transcript/summary: ${reservationLanguageLabel(draft.native_language)}\n${draft.notes||'No special requests.'}`;intake.append(summary);
  const disclosure=document.createElement('p');disclosure.textContent='Country, call language and time zone are initial suggestions. Check the business/phone match and the restaurant\'s local time from the source link. It is saved to the route calculation. The call transcript and summary are kept for 30 days.';intake.append(disclosure);
  for(const [key,text] of [['phone_verified','I have verified from the source that the phone belongs to this business.'],['timezone_verified','I have verified that the date, time and time zone match the restaurant\'s local time.']]){const label=document.createElement('label');label.className='register-label';const check=document.createElement('input');check.type='checkbox';check.addEventListener('change',()=>{form.elements[key].checked=check.checked;});form.elements[key].checked=false;label.append(check,document.createTextNode(text));intake.append(label);}
  chatButton(intake,'Verify these conditions and prepare the call summary',async()=>{if(!form.elements.phone_verified.checked||!form.elements.timezone_verified.checked)throw new Error('Explicitly confirm the business/phone and local time check.');if(!form.reportValidity())throw new Error('There is a missing or unsupported field. State the correction in chat.');form.requestSubmit($('reservation-prepare'));},true);
  chatButton(intake,'Correct the conditions in chat',async()=>{$('reservation-dialog').close('edit');sayInChat('What would you like to change? For example, "Make the time 20:00, keep the same day and number of people."');$('chat-input').focus();});
 });
}
async function flightsInChat(draft){
 const epoch=chatEpoch;const card=chatCard('Select the airport for your flight');const result=await Promise.all([api('airports',{query:draft.origin_query}),api('airports',{query:draft.destination_query})]);if(epoch!==chatEpoch)return;
 let chosen={};const groups=[];
 for(let i=0;i<2;i++){const group=document.createElement('div');const title=document.createElement('p');title.textContent=(i?'Arrival: ':'Departure: ')+(i?draft.destination_query:draft.origin_query);group.append(title);card.append(group);groups.push(group);
  for(const row of result[i].results){const choice=chatButton(group,`${row.name} · ${row.country} · ${row.code}`,async()=>{chosen[i]=row.code;for(const b of group.querySelectorAll('button'))b.setAttribute('aria-pressed',String(b===choice));if(chosen[0]&&chosen[1])search.disabled=false;});}
  if(!result[i].results.length)group.append(document.createTextNode('No match found; correct the city name in chat.'));
 }
 const search=chatButton(card,`${draft.departure}${draft.return?' → '+draft.return:' · One way'} — search prices`,async()=>{const data=await api('flights',{origin:chosen[0],destination:chosen[1],departure:draft.departure,return:draft.return||null});if(epoch!==chatEpoch)return;const resultCard=chatCard('Your flight options');const content=document.createElement('div');content.innerHTML=`<p class="notice">${esc(data.notice)}</p>`+link(data.search_url,'Check price on Aviasales ↗')+(data.results.length?data.results.map(f=>`<article class="flight-card"><strong>${esc(f.origin)} → ${esc(f.destination)} · ${esc(f.price)} ${esc(f.currency)}</strong><p>${esc(f.departure)}${f.return?' → '+esc(f.return):' · One way'} · ${esc(f.transfers)} transfer · ${esc(f.airline)}</p></article>`).join(''):'<p>No cached price was found for exactly these dates. This does not mean there are no flights.</p>');resultCard.append(content);},true);search.disabled=true;
}
async function mediaInChat(draft){
 const epoch=chatEpoch;const stop=getStop(draft.stop_id);if(!stop)throw new Error('Select the stop you want a suggestion for from the current route.');
 const kind=draft.kind,card=chatCard(`${stop.name} · ${mediaLabels[kind]?.[1]||kind} discovery`);
 const saved=state.profile.content[kind]||{};let tastes=saved.tastes||[];
 if(draft.query){const topic=kind==='podcast'||kind==='book'&&draft.mode!=='title';const data=topic?await api('content/topics',{query:draft.query,kind}):await api('interests/search',{query:draft.query,kind});if(epoch!==chatEpoch)return;const matches=topic?data.topics:data.results;tastes=[];
  const note=document.createElement('p');note.textContent='Select the real Qloo matches that describe your taste. These are specific to this suggestion.';card.append(note);
  for(const item of matches){const choice=chatButton(card,item.name,async()=>{const found=tastes.findIndex(x=>x.id===item.id);if(found>=0)tastes.splice(found,1);else if(tastes.length<5)tastes.push({id:item.id,name:item.name});else throw new Error('You can select up to 5 matches.');choice.setAttribute('aria-pressed',String(tastes.some(x=>x.id===item.id)));});}
  if(!matches.length)card.append(document.createTextNode('No Qloo match found. Mention another topic or get a suggestion without preferences.'));
 }
 const options=document.createElement('p');const language=['book','podcast'].includes(kind)?draft.language||saved.language||'any':'any';options.textContent='Content language: '+(language==='any'?'Language doesn\'t matter':reservationLanguageLabel(language))+'. You can type a message to change the topic or language.';card.append(options);
 chatButton(card,'Get a suggestion with my choices',async()=>{const data=await api('recommend',{stop_id:stop.id,kind,tastes,skip_taste:!tastes.length,language,remember_profile:false});if(epoch!==chatEpoch)return;const result=chatCard('Accompany this break');const content=document.createElement('div');content.innerHTML=`<p>${esc(data.basis)}</p>`+(data.language_status?`<p>${esc(data.language_status.matched)} language match · ${esc(data.language_status.unknown)} candidates' language could not be verified.</p>`:'')+(data.results.length?data.results.map(item=>`<article class="media-card">${safeURL(item.image)?`<img src="${esc(item.image)}" alt="${esc(item.name)} cover" loading="lazy">`:''}<div><h3>${esc(item.name)}</h3>${link(kind==='podcast'?item.apple_url:item.website,kind==='podcast'?'Open in Apple Podcasts ↗':'View at source ↗')}${qlooAttribution()}</div></article>`).join(''):'<p>No results were found with these conditions. You can change the language or topic in chat.</p>');result.append(content);},true);
 chatButton(card,'Also save the taste I selected to my general profile',async()=>{const p=state.profile;const entry={tastes,query:draft.query||'',...(['book','podcast'].includes(kind)?{language}:{})};await api('profile',{profile_version:p.profile_version,changes:{content:{[kind]:entry}}},'PATCH');await refreshTasteProfile();sayInChat('The content taste you selected has been saved to your general profile.');});
}
chatAction=async function(button){
 const [i,j]=button.dataset.chatAction.split(':').map(Number),a=conversation.messages[i]?.actions?.[j];if(!a)return;
 if(['plan','revise','lookup'].includes(a.type))return baseChatAction(button);
 return busy(button,async()=>{
  if(a.type==='current_route'){if(!state.plan)throw new Error('You don\'t have a route yet. Where do you want to go?');renderRoute();return;}
  if(['listen_call','stop_call','call_status'].includes(a.type)){return needAuth(async()=>{await refreshReservations();const item=reservationUI.attempt||reservationUI.items[0];if(!item){sayInChat('You don\'t have any reservation entries yet. We can start from a route card.');return;}await openReservationAttempt(item.id);});}
  if(a.type==='profile')return showProfileInChat();if(a.type==='saved')return showSavedInChat();if(a.type==='save')return needAuth(savePlan);if(a.type==='reservations')return showReservationsInChat();
  if(a.type==='flights')return flightsInChat(a.draft);if(a.type==='media')return mediaInChat(a.draft);if(a.type==='reserve')return reviewReservationInChat(a.draft);if(a.type==='reset_profile')return confirmProfileReset();
  if(a.type==='logout'){$('account').click();return;}if(a.type==='forget'){const card=chatCard('Clear data on the device');card.append(document.createTextNode('This device\'s anonymous preferences, draft and anonymous chat will be deleted. Your account data is preserved.'));chatButton(card,'Yes, clear data on the device',async()=>{$('forget').click();card.hidden=true;});}
 });
};
renderRoute=function(){baseRenderRoute();if(fullChatReady){chatCard('Your journey',null,'route').append($('route-area'));reflowChatTools();}};
openReservation=startReservationConversation;
openReservationAttempt=async function(id){if($('chat-reservation-intake'))$('chat-reservation-intake').hidden=true;return baseOpenAttempt(id);};
openMedia=function(stopId){const stop=getStop(stopId);if(stop)askInChat(`${stop.name} I'd like to get a content suggestion for my break at the stop.`,{task_mode:'media',stop_id:stopId});};
openMenu=function(stopId){const stop=getStop(stopId);if(!stop||!safeURL(stop.menu_url))return;const card=chatCard(stop.name+' · Menu');const frame=document.createElement('iframe');frame.title=stop.name+' menu';frame.src=safeURL(stop.menu_url);frame.setAttribute('sandbox','allow-scripts allow-same-origin allow-popups');frame.className='conversation-menu';card.append(frame);const links=document.createElement('div');links.innerHTML='<p>If the source site blocks embedding, you can open the menu at the source.</p>'+link(stop.menu_url,'Open the menu at the source ↗');card.append(links);};
window.addEventListener('chat-rendered',reflowChatTools);
window.addEventListener('DOMContentLoaded',()=>{
 fullChatReady=true;fullChatOwner=state.user?.id||'visitor';document.body.classList.add('full-chat');conversationNodes.route=$('route-area');conversationNodes.reservations=$('reservation-list');
 const header=document.createElement('header');header.className='conversation-header';header.innerHTML='<a class="brand" href="/">taste<span>trip</span></a><span>A journey shaped around you.</span><div id="conversation-shortcuts"></div>';
 $('chat-experience').prepend(header);
 const shortcuts=$('conversation-shortcuts');for(const [label,action] of [['My preferences',showProfileInChat],['My trips',showSavedInChat],['My reservations',showReservationsInChat],['Find flights',()=>askInChat("I would like to find flights. Let us work out the origin, destination and dates.")],['My account',()=>{$('account').click();}],['Sign up',()=>openAuth('signup')],['New chat',async()=>confirmNewConversation()],['Fresh session',async()=>{await api('session/new',{});location.reload();}]])chatButton(shortcuts,label,async()=>action());
 const accountButton=[...shortcuts.querySelectorAll('button')].find(b=>b.textContent==='My account');if(accountButton){accountButton.dataset.account='1';accountButton.textContent=state.user?state.user.username+' · Sign out':'Sign in';}
 const signupButton=[...shortcuts.querySelectorAll('button')].find(b=>b.textContent==='Sign up');if(signupButton){signupButton.dataset.signup='1';signupButton.hidden=!!state.user;signupButton.classList.add('signup-shortcut');}
 setupReservationModal();
 const scroller=document.createElement('div');scroller.id='conversation-scroll';$('chat-messages').before(scroller);scroller.append($('chat-messages'));
 for(const [id,title] of [['auth-dialog','Secure account step'],['taste-import-dialog','Move device preferences to your account']])inlineDialog(id,title);
 // Keep passwords out of the conversation and the model context, even with inline account UI.
 $('taste-dialog').showModal=showProfileInChat;
 $('chat-profile').onclick=showProfileInChat;
 $('reservation-edit').addEventListener('click',()=>{ $('reservation-dialog').close('edit');$('reservation-form').hidden=true;$('reservation-review').hidden=true;if($('chat-reservation-intake'))$('chat-reservation-intake').hidden=true;sayInChat('What would you like to change in the reservation terms? You can tell me in a message.');$('chat-input').focus();});
 new MutationObserver(()=>{if(!$('reservation-review').hidden&&$('chat-reservation-intake'))$('chat-reservation-intake').hidden=true;}).observe($('reservation-review'),{attributes:true,attributeFilter:['hidden']});
 const oldShow=show;show=function(view){oldShow('discover');};
 // Navigation buttons from earlier modules now resolve to conversation cards.
 showSaved=showSavedInChat;
 const originalRender=renderReservationList;renderReservationList=function(){originalRender();if(chatCards.some(c=>c.key==='reservation-list'))reflowChatTools();};
 window.addEventListener('taste-identity',()=>{const signup=$('conversation-shortcuts').querySelector('[data-signup]');if(signup)signup.hidden=!!state.user;const account=[...$('conversation-shortcuts').querySelectorAll('button')].find(b=>b.dataset.account==='1');if(account)account.textContent=state.user?state.user.username+' · Sign out':'Sign in';const owner=state.user?.id||'visitor';if(fullChatOwner!==owner){fullChatOwner=owner;for(const node of Object.values(conversationNodes))$('legacy-planner').append(node);for(let i=chatCards.length-1;i>=0;i--){const card=chatCards[i];if(card.key?.startsWith('dialog:')){card.element.hidden=true;card.turn=null;const d=card.element.querySelector('dialog');if(d){d.open=false;d.hidden=true;}}else{card.element.remove();chatCards.splice(i,1);}}reflowChatTools();} });
 if(state.plan)renderRoute();
});
