"""Isolated popup UI fixture on 8085. All reservation endpoints are simulated; no calls."""
import os, sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
for key in ['TWILIO_ACCOUNT_SID','TWILIO_AUTH_TOKEN','LLM_API_KEY','QLOO_API_KEY','ELEVENLABS_API_KEY']:
    os.environ[key]=''
os.environ['APP_ORIGIN']='http://127.0.0.1:8085'
from flask import g, request, jsonify
from app.server import create_app
app=create_app({'DATA_DIR':'./artifacts/call-popup-qa','COOKIE_SECURE':False})
terms={'restaurant':'Synthetic Garden · QA only','address':'Synthetic City, US','phone':'+12025550123','map_url':'https://example.test','local_date':'2026-11-10','local_time':'19:00','timezone':'America/New_York','people':3,'booking_name':'Synthetic Guest','conversation_language':'en','native_language':'en','country_code':'US','notes':'','alternatives':'Exact terms only'}
attempt={'id':'qa-call','plan_id':'qa-plan','stop_id':'qa-stop','terms':terms,'status':'queued','result':'pending','summary_status':'pending','events':[]}
starts=0
@app.before_request
def fixture():
    global starts
    if hasattr(g,'visitor'):g.user={'id':'qa-owner','username':'QA only'}
    path=request.path
    if path.startswith('/api/reservations'):
        if path.endswith('/options'):return jsonify(languages=['en'],countries=['US'],country_timezones={'US':'America/New_York'},country_languages={'US':'en'},worker_available=True)
        if path.endswith('/prepare'):return jsonify(request_id='qa-request',digest='synthetic-digest',terms=terms)
        if path.endswith('/start'):
            starts+=1
            return jsonify(reservation=attempt)
        if path=='/api/reservations':return jsonify(reservations=[attempt] if starts else [])
        if path.endswith('/listen'):return jsonify(error='Synthetic fixture: audio is disabled.'),400
        if path.endswith('/stop'):
            attempt['status']='canceled'
            return jsonify(reservation=attempt)
        return jsonify(reservation=attempt)
@app.get('/qa')
def preview():
    html=Path('app/static/index.html').read_text(encoding='utf-8')
    return html.replace('</head>','<script src="/qa-controls.js" defer></script></head>')
@app.get('/qa-controls.js')
def controls():
    return """window.addEventListener('load',()=>{const box=document.createElement('aside');box.style='position:fixed;bottom:0;left:0;z-index:99999;background:#ffe9a9;padding:6px;font:12px sans-serif';box.textContent='SIMULATION — no telephone calls ';for(const [label,action] of [['Review popup',async()=>{state.user={id:'qa-owner',username:'QA only'};state.plan={id:'qa-plan',revision:1,warnings:[],notice:'Synthetic QA only',trip:{city:'Synthetic City',start:'2026-11-10',days:1,people:3,pace:'Dengeli',transport:'Yürüyüş'},days:[{number:1,date:'2026-11-10',stops:[{id:'qa-stop',name:'Synthetic Garden · QA only',category:'restaurant',phone:'+12025550123',address:'Synthetic City',country_code:'US'}]}]};await reviewReservationInChat({stop_id:'qa-stop',local_date:'2026-11-10',local_time:'19:00',people:3,booking_name:'Synthetic Guest',country_code:'US',timezone:'America/New_York',conversation_language:'en',native_language:'en',notes:''});}]]){const b=document.createElement('button');b.textContent=label;b.onclick=action;box.append(b);}document.body.append(box);});""",200,{'Content-Type':'text/javascript'}
@app.get('/qa/control')
def control():
    return '<h1>Simulation controls — no telephone calls</h1><script src=/qa-state-controls.js defer></script>'+''.join(f'<button data-phase={phase}>{phase}</button>' for phase in ['connected','ended','ready'])
@app.get('/qa-state-controls.js')
def state_controls():
    return "document.querySelectorAll('[data-phase]').forEach(b=>b.onclick=async()=>{const r=await fetch('/qa-state/'+b.dataset.phase,{method:'POST',headers:{'X-TasteTrip':'1','Content-Type':'application/json'},body:'{}'});document.querySelector('h1').textContent=await r.text();});",200,{'Content-Type':'text/javascript'}
@app.post('/qa-state/<phase>')
def phase(phase):
    if phase=='ready':
        attempt['summary_status']='ready';attempt['summary']={'text':'Anna introduced herself as a digital assistant and requested a table for three at 19:00. The restaurant asked to verify the date. No confirmed reservation was recorded. (Synthetic QA)'};attempt['result']='unknown'
    else:
        attempt['status']=phase
        attempt['events']=[{'event_id':'qa1','role':'assistant','text':'Hello, I am a digital assistant calling on behalf of Synthetic Guest. May I request a table for three?','translation_status':'ready','translation':'Hello, I am a digital assistant calling on behalf of Synthetic Guest. May I request a table for three?'},{'event_id':'qa2','role':'restaurant','text':'Certainly. Could you confirm the date and time?','translation_status':'ready','translation':'Certainly. Could you confirm the date and time?'}]
    return jsonify(status=attempt['status'],starts=starts)
if __name__=='__main__':app.run(host='127.0.0.1',port=8085,threaded=True)
