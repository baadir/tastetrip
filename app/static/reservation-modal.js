'use strict';

function reservationNeedsPolling(){
 const a=reservationUI.attempt;
 return !!a&&($('reservation-dialog').open||!endedReservations.has(a.status)||['pending','working'].includes(a.summary_status));
}

function updateCallPopup(){
 const dialog=$('reservation-dialog'),a=reservationUI.attempt;
 const live=!$('reservation-live').hidden&&a;
 $('call-popup-stage').textContent=live?(endedReservations.has(a.status)?'Call details':'3 · Live call'):!$('reservation-review').hidden?'2 · Approve the call':'1 · Verify reservation details';
 $('call-popup-disclosure').textContent=live&&!endedReservations.has(a.status)?'Closing this window stops listening, not the phone call. Use Stop the call to request a stop. You can reopen this window from the call button.':live?'Review the transcript and reservation outcome. Viewing this record does not start another call.':'Review the details before approving a paid phone call. No call starts without your explicit approval.';
 const reopen=$('call-reopen');
 reopen.hidden=!a||endedReservations.has(a.status)||dialog.open;
 reopen.textContent=a?(callStatusNames[a.status]||'Call in progress')+' · Reopen':'';
}

function showCallSummaryInChat(a){
 const key='call-summary:'+a.id;
 const existing=chatCards.find(card=>card.key===key);
 const card=existing?existing.element:chatCard('Call summary',null,key);
 const snapshot=JSON.stringify([a.terms,a.status,a.result,a.confirmation_source,a.summary_status,a.summary?.text]);
 if(card.dataset.callSnapshot===snapshot)return;
 card.dataset.callSnapshot=snapshot;
 card.classList.add('reservation-call-summary');
 const title=document.createElement('h3');title.textContent='Call summary';
 const venue=document.createElement('p');venue.textContent=a.terms.restaurant+' · '+a.terms.local_date+' '+a.terms.local_time+' · '+a.terms.people+' people';
 const outcome=document.createElement('p');outcome.className='notice';
 outcome.textContent=(callStatusNames[a.status]||a.status)+' · '+(a.result==='confirmed'&&a.confirmation_source==='restaurant_exact_reply'?'Restaurant confirmed the exact terms':reservationResultNames[a.result]||a.result);
 const summary=document.createElement('p');summary.className='chat-text';summary.setAttribute('role','status');
 summary.textContent=a.summary?.text||({failed:'The summary could not be generated. You can retry without making another call.',insufficient:'There was not enough conversation data to generate a summary.',expired:'The transcript and summary retention period has expired.'})[a.summary_status]||'The call has ended. Your conversation summary is being prepared…';
 const note=document.createElement('p');note.className='muted';note.textContent='An automatic summary is not proof of a confirmed reservation. Review the restaurant’s exact response if the outcome is uncertain.';
 card.replaceChildren(title,venue,outcome,summary,note);
 chatButton(card,'View transcript and review outcome',()=>openReservationAttempt(a.id));
 if(['failed','insufficient'].includes(a.summary_status))chatButton(card,'Retry summary only',async()=>{await api('reservations/'+a.id+'/summary/retry',{});await openReservationAttempt(a.id);reservationUI.attempt.summary_status='pending';summary.textContent='Preparing the summary again. No new phone call will be made.';});
}

const renderCallBeforePopup=renderReservationLive;
renderReservationLive=function(){
 renderCallBeforePopup();
 const a=reservationUI.attempt;if(!a||!$('call-popup-stage'))return;
 if(endedReservations.has(a.status)){
  showCallSummaryInChat(a);
  if(reservationUI.followAttempt===a.id){
   reservationUI.followAttempt=null;
   if($('reservation-dialog').open)$('reservation-dialog').close('completed');
  }
 }
 updateCallPopup();
};

function setupReservationModal(){
 const dialog=$('reservation-dialog');
 document.body.append(dialog);dialog.classList.add('reservation-popup');
 const stage=document.createElement('p');stage.id='call-popup-stage';stage.className='call-popup-stage';stage.setAttribute('role','status');dialog.prepend(stage);
 const disclosure=document.createElement('p');disclosure.id='call-popup-disclosure';disclosure.className='muted';dialog.querySelector('.dialog-top').after(disclosure);
 const reopen=document.createElement('button');reopen.id='call-reopen';reopen.type='button';reopen.className='primary call-reopen';reopen.hidden=true;
 reopen.addEventListener('click',()=>{if(reservationUI.attempt)openReservationAttempt(reservationUI.attempt.id).catch(e=>notify(e.message));});document.body.append(reopen);
 const nativeShow=dialog.showModal.bind(dialog);
 dialog.showModal=function(){updateCallPopup();nativeShow();updateCallPopup();};
 dialog.addEventListener('close',()=>{updateCallPopup();if(dialog.returnValue==='completed')$('chat-input').focus();});
 new MutationObserver(updateCallPopup).observe(dialog,{subtree:true,attributes:true,attributeFilter:['hidden']});
 let owner=state.user?.id||'visitor';
 window.addEventListener('taste-identity',()=>{const next=state.user?.id||'visitor';if(next===owner)return;owner=next;reservationUI.followAttempt=null;if(dialog.open)dialog.close('identity');reopen.hidden=true;});
 updateCallPopup();
}
