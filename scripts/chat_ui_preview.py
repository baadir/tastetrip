"""Isolated conversational QA; provider call credentials are explicitly disabled."""
import os
import sys
import json
import sqlite3
from contextlib import closing
from datetime import date, timedelta
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ['APP_ORIGIN'] = 'http://127.0.0.1:8083'
os.environ['TWILIO_ACCOUNT_SID'] = ''
os.environ['TWILIO_AUTH_TOKEN'] = ''
from flask import g
from app.server import create_app
app = create_app({'DATA_DIR': './data/full-chat-ui-qa'})
day = str(date.today() + timedelta(days=10))
fixture = {'id':'synthetic-chat-route','revision':1,'mode':'Sentetik QA — telefon kapalı',
 'warnings':[],'notice':'Gerçek rezervasyon yapılamaz.',
 'trip':{'city':'Synthetic City, US','start':day,'days':1,'people':3,'categories':['restaurant'],
 'budget':4,'pace':'Dengeli','transport':'Yürüyüş','notes':'','lodging':'','interests':[]},
 'days':[{'number':1,'date':day,'stops':[{'id':'synthetic-restaurant',
 'name':'Örnek Restoran · Sentetik QA','category':'restaurant','phone':'+12025550123',
 'address':'Sentetik test adresi','country_code':'US','timezone':'America/New_York',
 'map_url':'https://example.test/map','website':'https://example.test','tags':[]}]}]}
@app.before_request
def fixture_route():
 if hasattr(g, 'visitor'):
  with closing(sqlite3.connect(app.config['DATABASE'])) as connection:
   connection.execute('INSERT OR IGNORE INTO drafts VALUES (?,?)', (g.visitor,json.dumps(fixture)))
   connection.commit()
if __name__ == '__main__':
 app.run(host='127.0.0.1', port=8083, threaded=True)
