"""Loopback-only synthetic UI fixture. No telephone calls or production accounts."""
import os,sys,json
from pathlib import Path
from datetime import date,timedelta
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
os.environ['APP_ORIGIN']='http://127.0.0.1:8082'
os.environ['TWILIO_ACCOUNT_SID']=''
from flask import g,request
from app.server import create_app
from contextlib import closing
import sqlite3
app=create_app({'DATA_DIR':'./data/reservation-ui-qa'})
fixture={'id':'synthetic-reservation-route','revision':1,'mode':'Sentetik UI kontrolü — telefon araması kapalı','warnings':[],'notice':'Bu veri gerçek restoran değildir. Arama yapılamaz.','trip':{'city':'Synthetic City, US','start':str(date.today()+timedelta(days=10)),'days':1,'people':3,'categories':['restaurant'],'budget':4,'pace':'Dengeli','transport':'Yürüyüş','notes':'','lodging':'','interests':[]},'days':[{'number':1,'date':str(date.today()+timedelta(days=10)),'stops':[{'id':'synthetic-restaurant','name':'Örnek Restoran · Sentetik QA','category':'restaurant','phone':'+12025550123','address':'Gerçek işletme değil · test verisi','country_code':'US','map_url':'https://example.test/map','website':'https://example.test','tags':[]}]}]}
@app.before_request
def synthetic_identity():
 if hasattr(g,'visitor'):
  g.user={'id':'synthetic-qa-owner','username':'sentetik-qa'}
  with closing(sqlite3.connect(app.config['DATABASE'])) as db, db:
   db.execute('INSERT OR IGNORE INTO drafts VALUES (?,?)',(g.visitor,json.dumps(fixture)))
if __name__=='__main__':app.run(host='127.0.0.1',port=8082,threaded=True)
