"""Monitor source text for changes; never fabricate a profile review or rewrite facts."""
import json,hashlib,datetime,urllib.request,os
from pathlib import Path
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[1]
class Text(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.parts=[]
 def handle_starttag(self,t,a):
  if t in ('script','style','nav','footer'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style','nav','footer'):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip and d.strip():self.parts.append(d.strip())
def run():
 path=ROOT/'data/local-source-status.json';old=json.loads(path.read_text()) if path.exists() else {'sources':{}}
 places=json.loads((ROOT/'data/local-places.json').read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
 def one(url):
  prev=old.get('sources',{}).get(url,{})
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'LoudLocalSourceMonitor/1.0 (weekly reference checks)'})
   with urllib.request.urlopen(req,timeout=18) as res:raw=res.read(3_000_000).decode('utf-8',errors='replace')
   parser=Text();parser.feed(raw);plain=' '.join(parser.parts)
   if len(plain)<150:raise ValueError('Insufficient source text; manual review needed')
   digest=hashlib.sha256(plain.encode()).hexdigest()
   changed=bool(prev.get('sha256') and prev['sha256']!=digest)
   return url,{'status':'changed' if changed or prev.get('status')=='changed' else 'ok','checked_at':now,'last_success':now,'sha256':digest,'changed_at':now if changed else prev.get('changed_at')}
  except Exception as ex:return url,{**prev,'status':'error','checked_at':now,'error':str(ex)[:200]}
 urls=list(dict.fromkeys(p['source'] for p in places));sources=dict(ThreadPoolExecutor(max_workers=5).map(one,urls))
 result={'checked_at':now,'sources':sources};tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2));os.replace(tmp,path)
 print(json.dumps({'sources':len(sources),'ok':sum(s['status']=='ok' for s in sources.values()),'changed':sum(s['status']=='changed' for s in sources.values()),'errors':sum(s['status']=='error' for s in sources.values())}))
if __name__=='__main__':run()
