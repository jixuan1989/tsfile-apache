// Execute once after two actual connector-transport reviews. No source/merge/review actions.
const bridge = 'work/expanded_publication_connector_bridge_v3.py';
const python = 'C:/Users/hxd/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
function ps(s) { return "'" + s.replace(/'/g, "''") + "'"; }
async function local(args, max = 10000) {
  const cmd = '& ' + ps(python) + ' ' + ps(bridge) + ' ' + args.map(ps).join(' ');
  let r = await tools.exec_command({cmd, max_output_tokens:max, yield_time_ms:1000});
  let output = r.output;
  while (r.session_id) {
    r = await tools.write_stdin({session_id:r.session_id,chars:'',max_output_tokens:max,yield_time_ms:1000});
    output += r.output;
  }
  if (r.exit_code !== 0) throw Error('Bridge failed; inspect instead of repeating writes: ' + output);
  return output.trim();
}
async function receipt(kind, name, result) {
  store('tsfile-connector-response-'+kind+'-'+name, result);
  const payload = ['ref','body'].includes(kind) ? {isError:Boolean(result.isError), actual_raw_response_retained_in_tool_history:true, response_characters:JSON.stringify(result).length} : result;
  return JSON.parse(await local(['receipt', kind, name, JSON.stringify(payload)]));
}
const m = JSON.parse(await local(['metadata'], 16000));
const profile = await tools.mcp__codex_apps__github_get_profile({});
if (profile.isError || profile.structuredContent?.nickname !== m.plan.login) throw Error('Wrong connector identity');
const entries = [];
for (const a of m.assets) {
  const cached=m.cached_blobs[a.name];
  if (cached) {
    if (cached.git_sha!==a.git_sha || cached.sha256!==a.sha256) throw Error('Cached blob mismatch');
    entries.push({path:m.plan.prefix+'/'+a.name,mode:'100644',type:'blob',sha:a.git_sha});
    continue; // Actual prior create_blob receipt is retained; final remote readback remains mandatory.
  }
  let content = '';
  for (let offset=0; offset<a.base64_characters; offset+=700000) {
    const chunk = await local(['chunk', a.name, String(offset)], 500000);
    if (chunk.length !== Math.min(700000, a.base64_characters-offset)) throw Error('Truncated asset chunk');
    content += chunk;
  }
  const result = await tools.mcp__codex_apps__github_create_blob({repository_full_name:m.plan.fork, encoding:'base64', content});
  const stored = await receipt('blob', a.name, result);
  if (stored.sha !== a.git_sha) throw Error('Blob identity mismatch');
  entries.push({path:m.plan.prefix+'/'+a.name, mode:'100644', type:'blob', sha:stored.sha});
}
const tr = await tools.mcp__codex_apps__github_create_tree({repository_full_name:m.plan.fork, base_tree_sha:m.base_tree, tree_elements:entries});
const tree = (await receipt('tree','tree',tr)).sha;
await local(['begin-commit']);
const cr = await tools.mcp__codex_apps__github_create_commit({repository_full_name:m.plan.fork, parent_sha:m.parent, tree_sha:tree,
  message:'Record unpublished local expanded-query diagnostics after upstream merge; local gates remain failed'});
const commit = (await receipt('commit','commit',cr)).sha;
const refguard = JSON.parse(await local(['before-ref']));
if (refguard.commit !== commit) throw Error('Wrong commit before ref update');
const rr = await tools.mcp__codex_apps__github_update_ref({repository_full_name:m.plan.fork, branch_name:m.plan.branch, expected_sha:m.parent, sha:commit, force:false});
await receipt('ref','ref',rr);
const verified = JSON.parse(await local(['verify-assets'],20000));
if (!verified.already_updated) {
  const br = await tools.mcp__codex_apps__github_update_pull_request({repository_full_name:m.plan.upstream, pr_number:m.plan.pr_number, body:verified.body});
  await receipt('body','body',br);
}
const final = JSON.parse(await local(['finish'],2000));
text(final);
