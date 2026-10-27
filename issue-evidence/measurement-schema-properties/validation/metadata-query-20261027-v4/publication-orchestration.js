// Execute only after both actual final reviews; no source/merge/review actions.
const bridge='work/issue-01/validation/metadata-query-20261027/publication_bridge_v4.py';
const python='C:/Users/hxd/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
function ps(s){return "'"+s.replace(/'/g,"''")+"'";}
async function local(args,max=10000){
  let r=await tools.exec_command({cmd:'& '+ps(python)+' '+ps(bridge)+' '+args.map(ps).join(' '),max_output_tokens:max,yield_time_ms:1000});
  let output=r.output;
  while(r.session_id){r=await tools.write_stdin({session_id:r.session_id,chars:'',max_output_tokens:max,yield_time_ms:1000});output+=r.output;}
  if(r.exit_code!==0)throw Error('Bridge stopped; inspect rather than rerun writes: '+output);
  return output.trim();
}
async function receipt(kind,name,result){
  store('pr01-publication-'+kind+'-'+name,result);
  const value=kind==='ref'?{isError:Boolean(result.isError),raw_response_in_tool_history:true,characters:JSON.stringify(result).length}:result;
  return JSON.parse(await local(['receipt',kind,name,JSON.stringify(value)]));
}
const m=JSON.parse(await local(['metadata'],16000));
const profile=await tools.mcp__codex_apps__github_get_profile({});
if(profile.isError||profile.structuredContent?.nickname!==m.plan.login)throw Error('Connector identity differs');
const entries=[];
for(const a of m.assets){
  let blob=m.cached_blobs[a.name];
  if(blob&&blob!==a.git_sha)throw Error('Cached blob differs');
  if(!blob){
    let content='';
    for(let off=0;off<a.base64_characters;off+=700000){
      const part=await local(['chunk',a.name,String(off)],500000);
      if(part.length!==Math.min(700000,a.base64_characters-off))throw Error('Truncated base64');content+=part;
    }
    const r=await tools.mcp__codex_apps__github_create_blob({repository_full_name:m.plan.fork,encoding:'base64',content});
    blob=(await receipt('blob',a.name,r)).sha;if(blob!==a.git_sha)throw Error('Blob differs');
  }
  entries.push({path:m.plan.prefix+'/'+a.name,mode:'100644',type:'blob',sha:blob});
}
const tree=(await receipt('tree','tree',await tools.mcp__codex_apps__github_create_tree({repository_full_name:m.plan.fork,base_tree_sha:m.base_tree,tree_elements:entries}))).sha;
await local(['begin-commit']);
const commit=(await receipt('commit','commit',await tools.mcp__codex_apps__github_create_commit({repository_full_name:m.plan.fork,parent_sha:m.plan.parent,tree_sha:tree,message:'Record fixed metadata and OFFSET query diagnostics; preserve unresolved signals'}))).sha;
if(JSON.parse(await local(['before-ref'])).commit!==commit)throw Error('Commit guard differs');
await receipt('ref','ref',await tools.mcp__codex_apps__github_update_ref({repository_full_name:m.plan.fork,branch_name:m.plan.branch,expected_sha:m.plan.parent,sha:commit,force:false}));
text(JSON.parse(await local(['verify-assets'],2000)));
text(JSON.parse(await local(['publish-body'],2000)));
text(JSON.parse(await local(['finish'],2000)));
