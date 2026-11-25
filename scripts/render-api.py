"""Small Render client. Credentials and complete responses stay in ignored local files."""
from pathlib import Path
import json,sys,urllib.request,urllib.error

ROOT=Path(__file__).resolve().parents[1]
def environment():
    return dict(line.split('=',1) for line in (ROOT/'.env').read_text(encoding='utf-8-sig').splitlines() if '=' in line and not line.lstrip().startswith('#'))

def request(path,method='GET',body=None):
    token=environment().get('RENDER_API_KEY','').strip().strip('\"\'')
    if not token:raise RuntimeError('RENDER_API_KEY is missing from the local .env')
    if method=='POST' and body:
        plan=body.get('plan',body.get('serviceDetails',{}).get('plan'))
        if path in ('/services','/postgres','/key-value') and plan!='free':raise RuntimeError('Only explicit free plans are authorized')
    req=urllib.request.Request('https://api.render.com/v1'+path,data=json.dumps(body).encode() if body is not None else None,method=method,headers={'Authorization':'Bearer '+token,'Accept':'application/json','Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=60) as response:return json.load(response)
    except urllib.error.HTTPError as error:
        # Response bodies can echo connection details; keep them out of terminal output.
        (ROOT/'.runtime/render-last-error.private.json').write_bytes(error.read())
        raise RuntimeError(f'Render {method} {path.split("?")[0]} returned HTTP {error.code}') from None

if __name__=='__main__':
    try:
        path=sys.argv[1];method=sys.argv[2] if len(sys.argv)>2 else 'GET';body=json.loads(Path(sys.argv[3]).read_text()) if len(sys.argv)>3 else None
        result=request(path,method,body);output=ROOT/'.runtime/render-last-response.private.json';output.write_text(json.dumps(result))
        item=result.get('service',result) if isinstance(result,dict) else {}
        print(json.dumps({'savedLocally':True,'id':item.get('id'),'name':item.get('name'),'status':item.get('status'),'plan':item.get('plan',item.get('serviceDetails',{}).get('plan')),'items':len(result) if isinstance(result,list) else None}))
    except Exception as error:print(str(error));raise SystemExit(1)
