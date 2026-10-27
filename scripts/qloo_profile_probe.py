"""Small read-only target-server contract probe; never writes keys or venue records."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / '.env')
from app.providers import qloo
from app.profiles import OPTIONS
out=[]
for group in ('cuisines','atmosphere','dietary'):
    for choice in OPTIONS[group]:
        params={'filter.type':'urn:entity:place','filter.location.query':'Rome','filter.tags':'urn:tag:category:place:restaurant','signal.interests.tags':choice['id'],'take':2}
        try:
            entities=qloo('/v2/insights',params).get('entities',[])
            out.append({'option':choice['id'],'mode':'soft','success':True,'count':len(entities)})
        except Exception as e:
            out.append({'option':choice['id'],'mode':'soft','success':False,'error_type':type(e).__name__})
params={'filter.type':'urn:entity:place','filter.location.query':'Rome','filter.tags':'urn:tag:category:place:restaurant,'+OPTIONS['dietary'][0]['id'],'operator.filter.tags':'intersection','take':3}
rows=qloo('/v2/insights',params).get('entities',[])
out.append({'mode':'required_vegan','count':len(rows),'all_tagged':all(OPTIONS['dietary'][0]['id'] in [t['id'] for t in e.get('tags',[])] for e in rows)})
if rows:
    params['filter.exclude.entities']=rows[0]['entity_id']
    check=qloo('/v2/insights',params).get('entities',[])
    out.append({'mode':'exclude_entity','count':len(check),'excluded_absent':all(e['entity_id']!=params['filter.exclude.entities'] for e in check)})
path=Path(__file__).resolve().parents[1]/'docs/validation/qloo-profile-contract-2026-10-22.json'
path.write_text(json.dumps({'date':'2026-10-22','checks':out},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=True))
