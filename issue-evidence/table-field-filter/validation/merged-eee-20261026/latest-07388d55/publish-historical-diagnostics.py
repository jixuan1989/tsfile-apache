"""Publish historical eee results and current80b pending scope; evidence refs only."""
from pathlib import Path
from datetime import datetime,timezone
import base64,hashlib,json,os,re,subprocess,time
w=Path(__file__).resolve().parent;r=w.parents[3];v=w.parent/'maintainer-head-eee39799-20261026'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
f=read(w/'followup-summary.json');state=read(r/'work/tsfile-contribution-state.json');item=next(x for x in [state['active'],*state['drafts']] if x['id']=='03');oldpub=read(v/'publication.json')
record_path=w/'publication.json';record=read(record_path) if record_path.exists() else {'source_pushed':False}
env=os.environ.copy();env['GODEBUG']='http2client=0';gh='C:/Program Files/GitHub CLI/gh.exe';fork=state['fork'];branch=item['evidence_branch'];prefix=branch+'/validation/merged-eee-20261026/latest-07388d55'
def save():record_path.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def api(endpoint,payload=None,method=None):
 args=[gh,'api',endpoint]
 if payload is not None:
  p=w/'request.json';p.write_text(json.dumps(payload,ensure_ascii=False),encoding='utf-8');args+=['--method',method or 'POST','--input',str(p)]
 tries=3 if payload is None or endpoint.endswith(('/git/blobs','/git/trees')) else 1
 for n in range(tries):
  proc=subprocess.run(args,env=env,capture_output=True,text=True,encoding='utf-8',timeout=90)
  if proc.returncode==0:return json.loads(proc.stdout)
  record.setdefault('api_failures',[]).append({'endpoint':endpoint,'stderr':proc.stderr});save()
  if n+1<tries:time.sleep(2)
 raise RuntimeError(proc.stderr)
def patch(endpoint,wanted,before):
 current=api(endpoint)
 if current['body']==wanted:return
 assert current['body']==before,'Concurrent edit preserved; stop'
 try:api(endpoint,{'body':wanted},'PATCH')
 except RuntimeError:
  current=api(endpoint)
  if current['body']!=wanted:
   assert current['body']==before;api(endpoint,{'body':wanted},'PATCH')
 assert api(endpoint)['body']==wanted
if record.get('completed_at'):
 print(json.dumps({'already_completed':True}));raise SystemExit(0)
assert api('user')['login']==state['github_login']
pull=api('repos/'+state['upstream']+'/pulls/'+str(item['pr_number']));assert pull['head']['sha']==f['head'] and not pull['merged']
assert oldpub['all_assets_readback_verified'] and not oldpub.get('pr_body_and_reply_verified')
oldmanifest=read(v/'final-evidence-manifest.json');oldhash=sha((v/'final-evidence-manifest.json').read_bytes());assert oldhash==f['historical_manifest_sha256']
for name,x in oldmanifest['files'].items():assert sha((v/name).read_bytes())==x['sha256'],name
manifest=read(w/'diagnostic-publication-manifest.json');mh=sha((w/'diagnostic-publication-manifest.json').read_bytes());files={name:(w/name).read_bytes() for name in manifest['files']}
for name,data in files.items():assert sha(data)==manifest['files'][name]['sha256'],name
reviews={}
for name in ['independent-review-integration.json','independent-review-different-model.json']:
 data=(w/name).read_bytes();x=json.loads(data);assert mh in json.dumps(x) and x['source_submission_gate_passed'] is False and x['diagnostic_publication_allowed'] is True
 files[name]=data;reviews[name]=sha(data)
files['diagnostic-publication-manifest.json']=(w/'diagnostic-publication-manifest.json').read_bytes()
files['historical-eeefinal-review-outcome.json']=(v/'final-review-outcome.json').read_bytes()
record.update(historical_publication_commit=oldpub['commit'],historical_manifest_sha256=oldhash,diagnostic_manifest_sha256=mh,reviews=reviews,report_url=oldpub['report_url'],evidence_url=oldpub['evidence_url'],latest_public_head=f['head']);save()
if 'commit' not in record:
 parent=api('repos/'+fork+'/git/ref/heads/'+branch)['object']['sha'];tree=api('repos/'+fork+'/git/commits/'+parent)['tree']['sha'];entries=[]
 for name,data in files.items():
  cached=record.setdefault('uploaded',{}).get(name)
  if cached and cached['sha256']==sha(data):gitsha=cached['git_sha']
  else:
   gitsha=api('repos/'+fork+'/git/blobs',{'content':base64.b64encode(data).decode(),'encoding':'base64'})['sha'];record['uploaded'][name]={'sha256':sha(data),'git_sha':gitsha};save()
  entries.append({'path':prefix+'/'+name,'mode':'100644','type':'blob','sha':gitsha})
 tree=api('repos/'+fork+'/git/trees',{'base_tree':tree,'tree':entries})
 commit=api('repos/'+fork+'/git/commits',{'message':'Record latest NOT-operand head and historical eee validation scope','tree':tree['sha'],'parents':[parent]})
 record.update(commit=commit['sha'],parent=parent);save()
ref=api('repos/'+fork+'/git/ref/heads/'+branch)['object']['sha'];assert ref in [record['parent'],record['commit']]
if ref!=record['commit']:
 try:api('repos/'+fork+'/git/refs/heads/'+branch,{'sha':record['commit'],'force':False},'PATCH')
 except RuntimeError:
  ref=api('repos/'+fork+'/git/ref/heads/'+branch)['object']['sha']
  if ref!=record['commit']:
   assert ref==record['parent'];api('repos/'+fork+'/git/refs/heads/'+branch,{'sha':record['commit'],'force':False},'PATCH')
for name,data in files.items():
 got=api('repos/'+fork+'/contents/'+prefix+'/'+name+'?ref='+record['commit']);assert base64.b64decode(got['content'])==data,name
 record.setdefault('verified',{})[name]={'sha256':sha(data),'bytes':len(data)};save()
record.update(all_assets_readback_verified=True,annex_url='https://github.com/'+fork+'/blob/'+record['commit']+'/'+prefix+'/new-head-scope-annex.md');save()
endpoint='repos/'+state['upstream']+'/pulls/'+str(item['pr_number']);pull=api(endpoint);assert pull['head']['sha']==f['head'] and not pull['merged']
footer=state['workflow']['ai_disclosure']['pr_footer'];assert footer in pull['body'];original=read(w/'pull-before-patch.json')['body']
marker='<!-- codex-073-current-historical-eee-20261026 -->'
notice=(w/'current-head-notice.md').read_text(encoding='utf-8').replace('{{ANNEX_URL}}',record['annex_url']);assert '{{' not in notice
status=marker+'\n'+notice+'\n\n'+(v/'performance-warning-bilingual.md').read_text(encoding='utf-8')+'\n\n'
if marker not in pull['body']:
 assert pull['body']==original,'Concurrent PR edit preserved'
 wanted=status+'<details>\n<summary>Historical heads and diagnostics / 历史提交和诊断</summary>\n\n'+original.rsplit(footer,1)[0].rstrip()+'\n\n</details>\n\nMaintainer commits retain Git authorship; OpenAI Codex authored validation/reply.\n\n维护者提交保留Git作者，OpenAI Codex编写验证/回复。\n\n'+footer+'\n'
 assert len(wanted)<65000;(w/'published-pr-body.md').write_text(wanted,encoding='utf-8');patch(endpoint,wanted,original)
else:assert status in pull['body']
reply_url=item['reviewed_batch_findings_publication']['reply_url'];replyid=reply_url.rsplit('-',1)[1];endpoint='repos/'+state['upstream']+'/issues/comments/'+replyid;reply=api(endpoint);assert reply['user']['login']==state['github_login'];original=read(w/'reply-before-patch.json')['body']
if marker not in reply['body']:
 assert reply['body']==original,'Concurrent reply edit preserved'
 history=original.rsplit(footer,1)[0].rstrip() if footer in original else original.rstrip()
 wanted=status+'<details>\n<summary>Historical diagnostics / 历史诊断</summary>\n\n'+history+'\n\n</details>\n\n'+footer+'\n';assert len(wanted)<65000
 (w/'published-review-reply.md').write_text(wanted,encoding='utf-8');patch(endpoint,wanted,original)
else:assert status in reply['body']
record.update(pr_body_and_reply_verified=True,reply_url=reply_url,completed_at=datetime.now(timezone.utc).isoformat());save()
print(json.dumps({k:record[k] for k in ['source_pushed','commit','report_url','annex_url','pr_body_and_reply_verified']}))
