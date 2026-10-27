"""Guarded publication I/O. Does not merge, push production, or request review."""
from pathlib import Path
import base64,datetime,hashlib,json,os,re,subprocess,sys,time
P=Path(__file__).resolve().parent;R=P.parents[3];Q=P/'publication-final-v4'
read=lambda f:json.loads(Path(f).read_text(encoding='utf8'))
sha=lambda b:hashlib.sha256(b).hexdigest()
plan=read(Q/'publication-plan.json');plan_sha=sha((Q/'publication-plan.json').read_bytes())
assert sha(Path(__file__).read_bytes())==plan['bridge_sha256']
assert sha((P/'publication_orchestrator_v4.js').read_bytes())==plan['orchestrator_sha256']
reviews={};models=set()
for role in ['integration','different-model']:
    f=R/f'work/issue-01/validation/pre-submission-review/metadata-query-20261027/final-{role}.json'
    v=read(f)
    assert v['diagnostic_publication_allowed'] and v['publication_plan_sha256']==plan_sha
    assert v['evidence_manifest_sha256']==plan['evidence_manifest_sha256']
    models.add(v['actual_model_identity']);reviews[f.name]=dict(path=str(f),sha256=sha(f.read_bytes()))
assert models=={'gpt-6.1-sol','gpt-6-astra'}
assets={}
for name,v in plan['assets'].items():
    b=(Q/'assets'/name).read_bytes();assert sha(b)==v['sha256'] and len(b)==v['bytes'];assets[name]=b
for name,v in reviews.items():assets[name]=Path(v['path']).read_bytes()
assets['publication-plan.json']=(Q/'publication-plan.json').read_bytes()
assets['publication-bridge.py']=Path(__file__).read_bytes()
assets['publication-orchestration.js']=(P/'publication_orchestrator_v4.js').read_bytes()
env=os.environ.copy();env['GODEBUG']='http2client=0'
def atomic(path,b):
    path=Path(path);tmp=path.with_name(path.name+'.tmp')
    with open(tmp,'wb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
def get(endpoint):
    for attempt in range(3):
        v=subprocess.run(['C:/Program Files/GitHub CLI/gh.exe','api',endpoint],capture_output=True,env=env,timeout=30)
        if not v.returncode:return json.loads(v.stdout)
        if attempt==2:raise RuntimeError(v.stderr.decode('utf8',errors='backslashreplace'))
        time.sleep(1)
def guard():
    x=get(f"repos/{plan['upstream']}/pulls/{plan['pr_number']}")
    assert x['head']['sha']==plan['head'] and x['state']=='open' and not x['merged']
    return x
def idx():return [dict(name=n,bytes=len(b),sha256=sha(b),base64_characters=len(base64.b64encode(b)),
    git_sha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()) for n,b in assets.items()]
def extract(x):
    if isinstance(x,dict):
        for k in ['sha','commit_sha','tree_sha']:
            if isinstance(x.get(k),str) and re.fullmatch('[0-9a-f]{40}',x[k]):return x[k]
        if 'structuredContent' in x:
            v=extract(x['structuredContent'])
            if v:return v
        for c in x.get('content',[]):
            if c.get('type')=='text':
                try:v=extract(json.loads(c['text']))
                except (ValueError,TypeError):continue
                if v:return v
    if isinstance(x,str) and re.fullmatch('[0-9a-f]{40}',x):return x
    return None
recpath=Q/'execution-receipt.json'
if recpath.exists():rec=read(recpath)
else:rec=dict(publication_plan_sha256=plan_sha,reviews=reviews,blobs={},production_pushed=False,source_submission_gate_passed=False)
assert rec['publication_plan_sha256']==plan_sha and rec['reviews']==reviews
def save():atomic(recpath,(json.dumps(rec,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
action=sys.argv[1]
if action=='metadata':
    assert get('user')['login']==plan['login'];x=guard()
    before=(Q/'assets/previous-public-pr-body.md').read_bytes().decode('utf8');assert sha(before.encode())==plan['before_body_sha256']
    assert x['body']==before and get(f"repos/{plan['fork']}/git/ref/heads/{plan['branch']}")['object']['sha']==plan['parent']
    tree=get(f"repos/{plan['fork']}/git/commits/{plan['parent']}")['tree']['sha']
    entries=get(f"repos/{plan['fork']}/git/trees/{tree}?recursive=1");assert not entries.get('truncated')
    assert not any(x['path']==plan['prefix'] or x['path'].startswith(plan['prefix']+'/') for x in entries['tree'])
    assert not rec.get('commit_unknown') and not rec.get('commit')
    save();print(json.dumps(dict(plan=plan,assets=idx(),base_tree=tree,cached_blobs=rec['blobs'])))
elif action=='chunk':
    name=sys.argv[2];offset=int(sys.argv[3]);assert name in assets and offset>=0
    print(base64.b64encode(assets[name]).decode()[offset:offset+700000])
elif action=='receipt':
    kind,name=sys.argv[2:4];obj=json.loads(sys.argv[4]);assert re.fullmatch('[A-Za-z0-9_.-]+',name)
    folder=Q/'tool-receipts';folder.mkdir(exist_ok=True)
    atomic(folder/f'{kind}-{name}.json',(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
    assert not obj.get('isError'),'Mutation error retained; inspect rather than rerun whole publisher'
    if kind in ['blob','tree','commit']:
        value=extract(obj);assert value,'Unknown result; inspect rather than retry commit'
        if kind=='blob':assert value==next(a for a in idx() if a['name']==name)['git_sha'];rec['blobs'][name]=value
        if kind=='tree':rec['tree']=value
        if kind=='commit':rec['commit']=value;rec['commit_unknown']=False
        save();print(json.dumps(dict(sha=value)))
    else:save();print('{}')
elif action=='begin-commit':
    assert not rec.get('commit') and not rec.get('commit_unknown')
    rec['commit_unknown']=True;save();print('{}')
elif action=='before-ref':
    assert rec.get('commit') and not rec.get('commit_unknown');guard()
    assert get(f"repos/{plan['fork']}/git/ref/heads/{plan['branch']}")['object']['sha']==plan['parent']
    c=get(f"repos/{plan['fork']}/git/commits/{rec['commit']}")
    assert c['tree']['sha']==rec['tree'] and [x['sha'] for x in c['parents']]==[plan['parent']]
    print(json.dumps(dict(commit=rec['commit'])))
elif action in ['verify-assets','publish-body','finish']:
    commit=rec['commit'];assert not rec.get('commit_unknown')
    assert get(f"repos/{plan['fork']}/git/ref/heads/{plan['branch']}")['object']['sha']==commit
    if action=='verify-assets':
        tree=get(f"repos/{plan['fork']}/git/trees/{rec['tree']}?recursive=1");assert not tree.get('truncated')
        seen={x['path'][len(plan['prefix'])+1:]:x['sha'] for x in tree['tree'] if x['type']=='blob' and x['path'].startswith(plan['prefix']+'/')}
        assert seen=={a['name']:a['git_sha'] for a in idx()}
        for a in idx():
            blob=get(f"repos/{plan['fork']}/git/blobs/{a['git_sha']}")
            assert blob['encoding']=='base64' and base64.b64decode(blob['content'])==assets[a['name']]
        rec['all_assets_readback_verified']=True;save();print(json.dumps(dict(verified_assets=len(assets))))
    else:
        assert rec['all_assets_readback_verified']
        template=(Q/'proposed-pr-body.md').read_text(encoding='utf8')
        assert sha(template.encode('utf8'))==plan['body_template_sha256']
        public=f"https://github.com/{plan['fork']}/blob/{commit}/{plan['prefix']}"
        wanted=template.replace('@PUBLIC_ROOT@',public)
        assert wanted.rstrip().endswith(plan['footer'])
        before=(Q/'assets/previous-public-pr-body.md').read_bytes().decode('utf8');x=guard()
        assert x['body'] in [before,wanted],'Concurrent PR body edit; stop'
        if action=='publish-body' and x['body']!=wanted:
            payload=Q/'body-only-patch.json';atomic(payload,json.dumps(dict(body=wanted),ensure_ascii=False).encode('utf8'))
            rec['body_attempt_started']=True;save()
            z=subprocess.run(['C:/Program Files/GitHub CLI/gh.exe','api','--method','PATCH',f"repos/{plan['upstream']}/pulls/{plan['pr_number']}",'--input',str(payload)],capture_output=True,env=env,timeout=90)
            atomic(Q/'body-patch-stdout.json',z.stdout);atomic(Q/'body-patch-stderr.bin',z.stderr)
            rec['body_patch_exit_code']=z.returncode;save();assert z.returncode==0,'Body outcome requires inspection'
            x=guard()
        assert x['body']==wanted
        atomic(Q/'published-pr-body.md',wanted.encode('utf8'))
        rec.update(pr_body_verified=True,pr_body_sha256=sha(wanted.encode('utf8')),ai_disclosure_verified=True,
            report_url=public+'/validation-report.md',evidence_url=public+'/README.md',query_gate_cleared=False,
            source_submission_gate_passed=False,writer_gate_passed=False,source_pushed=False)
        if action=='finish':rec['completed_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        save();print(json.dumps(dict(completed=action=='finish',commit=commit,report_url=rec['report_url'])))
else:raise ValueError(action)
