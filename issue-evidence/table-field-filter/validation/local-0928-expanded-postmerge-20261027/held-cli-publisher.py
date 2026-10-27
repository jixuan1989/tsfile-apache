"""Publish only independently approved diagnostic assets and guarded existing PR body."""
from pathlib import Path
import base64,hashlib,json,os,subprocess
from datetime import datetime,timezone

root=Path(__file__).resolve().parent.parent
p=root/'work/issue-03/validation/live-type-expanded-query-20261027'
q=p/'publication-after-merge'
r=root/'work/issue-03/validation/pre-submission-review/live-type-expanded-query-20261027'
read=lambda f:json.loads(Path(f).read_text(encoding='utf8'))
sha=lambda b:hashlib.sha256(b).hexdigest()
plan=read(q/'publication-plan.json');ph=sha((q/'publication-plan.json').read_bytes())
assert sha(Path(__file__).read_bytes())==plan['publisher_sha256']
s=read(root/'work/tsfile-contribution-state.json');d=next(x for x in s['drafts'] if x['id']=='03')
for k,v in [('fork',s['fork']),('upstream',s['upstream']),('login',s['github_login']),('pr_number',d['pr_number']),('branch',d['evidence_branch']),('public_head',d['head_commit'])]:assert plan[k]==v,k
assert d['local_live_type_expanded_query']['head']==plan['candidate']
assert sha((p/'final-evidence-manifest-v2.json').read_bytes())==plan['evidence_manifest_sha256']
for k in ['source_submission_gate_passed','query_gate_cleared','writer_gate_passed','ci_gate_cleared']:
    assert plan[k] is False and d['local_live_type_expanded_query'][k] is False
assets={}
for name,x in plan['assets'].items():
    assert Path(name).name==name
    data=(q/'assets'/name).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256'];assets[name]=data
reviews={};models=set()
for role in ['integration','different-model']:
    f=r/f'publication-after-merge-review-{role}.json';x=read(f)
    assert x['publication_plan_sha256']==ph and x['publisher_sha256']==plan['publisher_sha256']
    assert x['diagnostic_publication_allowed'] is True and x['source_submission_gate_passed'] is False
    assert x['baseline_commit']==plan['baseline'] and x['final_commit']==plan['candidate']
    assert x['query_gate_cleared'] is False and x['writer_gate_passed'] is False and x['ci_gate_cleared'] is False
    models.add(x['actual_model_identity']);reviews[f.name]=sha(f.read_bytes());assets[f.name]=f.read_bytes()
assert models=={'gpt-6.1-sol','gpt-6-astra'}
assets['publication-plan.json']=(q/'publication-plan.json').read_bytes()
assets['publication-execution-script.py']=Path(__file__).read_bytes()
before=read(p/'remote-body-update/before.json')['body'];bodytemplate=(q/'proposed-pr-body.md').read_text(encoding='utf8')
assert sha(before.encode('utf8'))==plan['before_body_sha256'] and sha(bodytemplate.encode('utf8'))==plan['body_template_sha256']
rp=q/'publication.json'
record=read(rp) if rp.exists() else {'plan_sha256':ph,'reviews_sha256':reviews,'source_pushed':False}
assert record['plan_sha256']==ph and record['reviews_sha256']==reviews

def atomic(f,data):
    f=Path(f);t=f.with_name(f.name+'.tmp')
    with t.open('wb') as out:out.write(data);out.flush();os.fsync(out.fileno())
    os.replace(t,f)
def save():atomic(rp,(json.dumps(record,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
env=os.environ.copy();env['GODEBUG']='http2client=0';gh='C:/Program Files/GitHub CLI/gh.exe'
def api(endpoint,payload=None,method=None):
    args=[gh,'api',endpoint]
    if payload is not None:
        f=q/'request.json';atomic(f,json.dumps(payload,ensure_ascii=False).encode('utf8'))
        args+=['--method',method or 'POST','--input',str(f)]
    result=subprocess.run(args,capture_output=True,text=True,encoding='utf8',env=env,timeout=90)
    if result.returncode:
        record.setdefault('api_failures',[]).append({'endpoint':endpoint,'stderr':result.stderr});save()
        raise RuntimeError('GitHub API failed; no blind mutation retry: '+endpoint)
    return json.loads(result.stdout)
def guard():
    x=api(f"repos/{plan['upstream']}/pulls/{plan['pr_number']}")
    assert x['head']['sha']==plan['public_head'] and x['state']=='closed' and x['merged'] and x['merge_commit_sha']==plan['merge_commit_sha'],'PR changed'
    return x
fork=plan['fork'];branch=plan['branch'];prefix=plan['prefix']
assert api('user')['login']==plan['login']
guard()
assert record.get('unknown_commit_outcome') is not True,'Commit POST outcome unknown; inspect record before any continuation'
if 'commit' not in record:
    parent=api(f'repos/{fork}/git/ref/heads/{branch}')['object']['sha']
    if 'parent' not in record:record['parent']=parent;save()
    assert parent==record['parent'],'Concurrent evidence branch change'
    base_tree=api(f'repos/{fork}/git/commits/{parent}')['tree']['sha']
    prior=api(f'repos/{fork}/git/trees/{base_tree}?recursive=1')
    assert not prior.get('truncated')
    assert not any(x['path']==prefix or x['path'].startswith(prefix+'/') for x in prior['tree']),'Evidence destination already exists'
    entries=[]
    for name,data in assets.items():
        cached=record.setdefault('blobs',{}).get(name)
        if cached:
            assert cached['sha256']==sha(data);gitsha=cached['git_sha']
        else:
            gitsha=api(f'repos/{fork}/git/blobs',{'content':base64.b64encode(data).decode('ascii'),'encoding':'base64'})['sha']
            record['blobs'][name]={'sha256':sha(data),'git_sha':gitsha};save()
        entries.append({'path':prefix+'/'+name,'mode':'100644','type':'blob','sha':gitsha})
    tree=api(f'repos/{fork}/git/trees',{'base_tree':base_tree,'tree':entries})['sha']
    record['tree']=tree;record['unknown_commit_outcome']=True;save()
    commit=api(f'repos/{fork}/git/commits',{'message':'Record unpublished local candidate expanded-query diagnostics; gates remain failed','tree':tree,'parents':[parent]})['sha']
    record.update(commit=commit,unknown_commit_outcome=False);save()
commit=record['commit']
c=api(f'repos/{fork}/git/commits/{commit}')
assert c['tree']['sha']==record['tree'] and [x['sha'] for x in c['parents']]==[record['parent']]
current=api(f'repos/{fork}/git/ref/heads/{branch}')['object']['sha']
if current!=commit:
    assert current==record['parent'],'Concurrent evidence branch change'
    guard()
    try:api(f'repos/{fork}/git/refs/heads/{branch}',{'sha':commit,'force':False},'PATCH')
    except (RuntimeError,subprocess.TimeoutExpired):
        assert api(f'repos/{fork}/git/ref/heads/{branch}')['object']['sha']==commit
assert api(f'repos/{fork}/git/ref/heads/{branch}')['object']['sha']==commit
tree=api(f"repos/{fork}/git/trees/{record['tree']}?recursive=1")
assert not tree.get('truncated')
observed={x['path'][len(prefix)+1:]:x['sha'] for x in tree['tree'] if x['type']=='blob' and x['path'].startswith(prefix+'/')}
assert observed=={n:x['git_sha'] for n,x in record['blobs'].items()}
for name,data in assets.items():
    obj=api(f"repos/{fork}/git/blobs/{record['blobs'][name]['git_sha']}")
    assert obj['encoding']=='base64' and base64.b64decode(obj['content'])==data,name
record['readback_all_assets_verified']=True;save()
public=f'https://github.com/{fork}/blob/{commit}/{prefix}'
wanted=bodytemplate.replace('@PUBLIC_ROOT@',public)
footer=s['workflow']['ai_disclosure']['pr_footer']
assert wanted.rstrip().endswith(footer) and '@PUBLIC_ROOT@' not in wanted
observed=guard();assert observed['body'] in [before,wanted],'Concurrent PR body edit'
if observed['body']!=wanted:
    try:api(f"repos/{plan['upstream']}/pulls/{plan['pr_number']}",{'body':wanted},'PATCH')
    except (RuntimeError,subprocess.TimeoutExpired):
        assert guard()['body']==wanted
assert guard()['body']==wanted
atomic(q/'published-pr-body.md',wanted.encode('utf8'))
record.update(completed_at=datetime.now(timezone.utc).isoformat(),report_url=public+'/validation-report.md',
              evidence_url=public+'/README.md',pr_url=plan['pr_url'],pr_body_verified=True,
              pr_body_sha256=sha(wanted.encode('utf8')),ai_disclosure_verified=True,
              query_gate_cleared=False,source_submission_gate_passed=False,writer_gate_passed=False,ci_gate_cleared=False)
save();print(json.dumps({k:record[k] for k in ['commit','report_url','evidence_url','completed_at']}))
