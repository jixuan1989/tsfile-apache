"""Local bounded I/O and read-only verification for the connector transport."""
from pathlib import Path
import base64,hashlib,json,os,re,subprocess,sys,time

ROOT=Path(__file__).resolve().parent.parent
P=ROOT/'work/issue-03/validation/live-type-expanded-query-20261027'
Q=P/'publication-after-merge';R=ROOT/'work/issue-03/validation/pre-submission-review/live-type-expanded-query-20261027'
read=lambda f:json.loads(Path(f).read_text(encoding='utf8'))
sha=lambda b:hashlib.sha256(b).hexdigest()
plan=read(Q/'publication-plan.json');ph=sha((Q/'publication-plan.json').read_bytes())
annex=read(Q/'connector-execution-plan-v3.json')
assert annex['publication_plan_sha256']==ph
assert annex['bridge_sha256']==sha(Path(__file__).read_bytes())
js=ROOT/'work/expanded_publication_connector_v3.js'
assert annex['orchestrator_sha256']==sha(js.read_bytes())
assets={}
for n,x in plan['assets'].items():
    b=(Q/'assets'/n).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'];assets[n]=b
# Full metrics remain byte-exact inside the reviewed ZIP; omit only the duplicate uncompressed Git blob.
assert sha(assets['metrics.json'])==annex['full_metrics_sha256']
assets.pop('metrics.json')
models=set();reviews={}
for role in ['integration','different-model']:
    f=R/f'publication-after-merge-review-{role}.json';v=read(f)
    assert v['diagnostic_publication_allowed'] and v['publication_plan_sha256']==ph
    assert v['publisher_sha256']==plan['publisher_sha256'];models.add(v['actual_model_identity'])
    reviews[f.name]=sha(f.read_bytes());assets[f.name]=f.read_bytes()
assert models=={'gpt-6.1-sol','gpt-6-astra'}
transport_reviews={};models=set()
for role in ['integration','different-model']:
    f=R/f'connector-execution-v3-review-{role}.json';v=read(f)
    assert v['connector_execution_plan_sha256']==sha((Q/'connector-execution-plan-v3.json').read_bytes())
    assert v['diagnostic_publication_allowed'] and v['source_submission_gate_passed'] is False
    models.add(v['actual_model_identity']);transport_reviews[f.name]=sha(f.read_bytes());assets[f.name]=f.read_bytes()
assert models=={'gpt-6.1-sol','gpt-6-astra'}
for n,f in [('publication-plan.json',Q/'publication-plan.json'),('connector-execution-plan.json',Q/'connector-execution-plan-v3.json'),
            ('actual-connector-orchestration.js',js),('actual-connector-bridge.py',Path(__file__)),
            ('held-cli-publisher.py',ROOT/'work/publish_live_type_expanded_diagnostics_after_merge.py')]:assets[n]=f.read_bytes()
before=assets['previous-public-pr-body.md'].decode('utf8')
assert sha(before.encode('utf8'))==plan['before_body_sha256']
bodytemplate=(Q/'proposed-pr-body.md').read_text(encoding='utf8')
assert sha(bodytemplate.encode('utf8'))==plan['body_template_sha256']
recpath=Q/'connector-publication-v3.json';rec=read(recpath)
assert rec['plan_sha256']==ph and rec['reviews_sha256']==reviews and not rec.get('commit')
assert not rec.get('unknown_commit_outcome')
if 'connector_transport_reviews' in rec:assert rec['connector_transport_reviews']==transport_reviews
rec['connector_transport_reviews']=transport_reviews
rec['actual_transport']='GitHub connector after CLI blob POST HTTP401; original CLI attempts retained'
parent=rec['parent'];assert re.fullmatch('[0-9a-f]{40}',parent)
env=os.environ.copy();env['GODEBUG']='http2client=0'
def atomic(f,b):
    f=Path(f);t=f.with_name(f.name+'.connector.tmp')
    with t.open('wb') as out:out.write(b);out.flush();os.fsync(out.fileno())
    os.replace(t,f)
def save():atomic(recpath,(json.dumps(rec,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
def get(endpoint):
    for attempt in range(3):
        z=subprocess.run(['C:/Program Files/GitHub CLI/gh.exe','api',endpoint],capture_output=True,text=True,encoding='utf8',env=env,timeout=30)
        if not z.returncode:return json.loads(z.stdout)
        if attempt==2:raise RuntimeError(z.stderr)
        time.sleep(1)
def guard():
    x=get(f"repos/{plan['upstream']}/pulls/{plan['pr_number']}")
    assert x['head']['sha']==plan['public_head'] and x['merged'] and x['state']=='closed' and x['merge_commit_sha']==plan['merge_commit_sha']
    return x
def asset_index():return [{'name':n,'sha256':sha(b),'bytes':len(b),'base64_characters':len(base64.b64encode(b)),
                            'git_sha':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()} for n,b in assets.items()]
def connector_sha(x):
    if isinstance(x,dict):
        for k in ['sha','commit_sha','tree_sha']:
            if isinstance(x.get(k),str) and re.fullmatch('[0-9a-f]{40}',x[k]):return x[k]
        if 'structuredContent' in x:
            a=connector_sha(x['structuredContent'])
            if a:return a
        for v in x.get('content',[]):
            if v.get('type')=='text':
                try:a=connector_sha(json.loads(v['text']))
                except (ValueError,TypeError):continue
                if a:return a
    if isinstance(x,str) and re.fullmatch('[0-9a-f]{40}',x):return x
    return None
action=sys.argv[1]
if action=='metadata':
    assert get('user')['login']==plan['login'];x=guard()
    assert x['body']==before
    ref=get(f"repos/{plan['fork']}/git/ref/heads/{plan['branch']}")['object']['sha'];assert ref==parent
    tree=get(f"repos/{plan['fork']}/git/commits/{parent}")['tree']['sha']
    old=get(f"repos/{plan['fork']}/git/trees/{tree}?recursive=1");assert not old.get('truncated')
    assert not any(t['path']==plan['prefix'] or t['path'].startswith(plan['prefix']+'/') for t in old['tree'])
    save();print(json.dumps({'plan':plan,'parent':parent,'base_tree':tree,'assets':asset_index(),'cached_blobs':rec.get('connector_blobs',{})}))
elif action=='chunk':
    n=sys.argv[2];offset=int(sys.argv[3]);assert n in assets and offset>=0
    print(base64.b64encode(assets[n]).decode('ascii')[offset:offset+700000])
elif action=='receipt':
    kind=sys.argv[2];name=sys.argv[3];assert re.fullmatch('[A-Za-z0-9_.-]+',name)
    assert kind in ['blob','tree','commit','ref','body','error']
    obj=json.loads(sys.argv[4]);folder=Q/'connector-receipts';folder.mkdir(exist_ok=True)
    atomic(folder/f'{kind}-{name}.json',(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
    assert not obj.get('isError'), 'Connector returned error; stop and inspect receipt'
    if kind in ['blob','tree','commit']:
        value=connector_sha(obj);assert value, 'Unknown connector result shape; inspect receipt, do not retry commit'
        if kind=='blob':
            expected=next(x for x in asset_index() if x['name']==name);assert value==expected['git_sha']
            rec.setdefault('connector_blobs',{})[name]={'git_sha':value,'sha256':expected['sha256']}
        elif kind=='tree':rec['connector_tree']=value
        else:rec['connector_commit']=value;rec['connector_commit_outcome_unknown']=False
        save();print(json.dumps({'sha':value}))
    else:print('{}')
elif action=='begin-commit':
    assert not rec.get('connector_commit') and not rec.get('connector_commit_outcome_unknown')
    rec['connector_commit_outcome_unknown']=True;save();print('{}')
elif action=='before-ref':
    assert not rec.get('connector_commit_outcome_unknown');commit=rec['connector_commit'];guard()
    assert get(f"repos/{plan['fork']}/git/ref/heads/{plan['branch']}")['object']['sha']==parent
    c=get(f"repos/{plan['fork']}/git/commits/{commit}")
    assert c['tree']['sha']==rec['connector_tree'] and [x['sha'] for x in c['parents']]==[parent]
    print(json.dumps({'commit':commit}))
elif action in ['verify-assets','finish']:
    commit=rec['connector_commit'];assert get(f"repos/{plan['fork']}/git/ref/heads/{plan['branch']}")['object']['sha']==commit
    tree=get(f"repos/{plan['fork']}/git/trees/{rec['connector_tree']}?recursive=1");assert not tree.get('truncated')
    observed={t['path'][len(plan['prefix'])+1:]:t['sha'] for t in tree['tree'] if t['type']=='blob' and t['path'].startswith(plan['prefix']+'/')}
    assert observed=={x['name']:x['git_sha'] for x in asset_index()}
    for idx in asset_index():
        b=get(f"repos/{plan['fork']}/git/blobs/{idx['git_sha']}");assert b['encoding']=='base64' and base64.b64decode(b['content'])==assets[idx['name']]
    public=f"https://github.com/{plan['fork']}/blob/{commit}/{plan['prefix']}"
    wanted=bodytemplate.replace('@PUBLIC_ROOT@',public)
    assert sha(bodytemplate.encode('utf8'))==plan['body_template_sha256']
    x=guard();before=assets['previous-public-pr-body.md'].decode('utf8');assert x['body'] in [before,wanted]
    if action=='verify-assets':print(json.dumps({'body':wanted,'already_updated':x['body']==wanted}))
    else:
        assert x['body']==wanted
        footer=read(ROOT/'work/tsfile-contribution-state.json')['workflow']['ai_disclosure']['pr_footer'];assert wanted.rstrip().endswith(footer)
        atomic(Q/'published-pr-body.md',wanted.encode('utf8'))
        from datetime import datetime,timezone
        rec.update(commit=commit,tree=rec['connector_tree'],readback_all_assets_verified=True,pr_body_verified=True,
                   pr_body_sha256=sha(wanted.encode('utf8')),ai_disclosure_verified=True,completed_at=datetime.now(timezone.utc).isoformat(),
                   report_url=public+'/validation-report.md',evidence_url=public+'/README.md',pr_url=plan['pr_url'],
                   source_pushed=False,source_submission_gate_passed=False,query_gate_cleared=False,writer_gate_passed=False,ci_gate_cleared=False)
        save();print(json.dumps({'completed':True,'commit':commit,'report_url':rec['report_url']}))
else:raise ValueError('Unsupported bridge action')
