# Maintainer develop merge and CI setup failure

**Latest public head `eee39799` supersedes the c01 validation below.** The maintainer merged develop `ef1107d1` into the PR:82files differ from standalone c01, including7 C++ production files and Java changes. Current CI is46success/1neutral/1skip/1failure. The Windows Python3.14 failure is a Chocolatey LLVM17.0.6 HTTP504 during dependency installation; project build/test was skipped. The unchanged Windows install command and raw log support this setup-failure assessment; no retry or workflow change was requested. **This new merged source has not completed fresh local correctness/Java/coverage/sanitizer/query validation. Neither green checks nor c01 results pass its gates.** The c01 report below is completed historical-head evidence. Its query acceptance remains UNCLEARED. #1038 separately tracks pre-existing TimeIn row loss after a fully rejected page; upstream requests separate tracking. Source inspection finds the status conversion in base/c01/current/develop; no new local runtime reproduction or fix is claimed.

**最新公开head `eee39799` 已取代下方c01验证。** 维护者合入develop `ef1107d1`，相对独立c01有82文件不同，含7个C++生产文件及Java修改。当前CI46成功/1中立/1跳过/1失败。Windows Python3.14在依赖安装时获取Chocolatey LLVM17.0.6收到HTTP504，项目构建/测试被跳过；Windows安装命令未改，原始日志支持环境失败判断，未请求重跑或修改workflow。**新合并源码尚未完成新本地正确性/Java/覆盖率/sanitizer/查询验证，不因绿check或c01旧结果通过门槛。** 下方c01是已完成的历史head证据，查询验收仍未通过。上游 #1038 单独跟踪完全过滤页后TimeIn漏行，要求分开处理；源码检查在base/c01/current/develop均找到状态转换，不声称新本地运行复现或已修复。


## English

Head `eee39799948699c58e292ee6361f1da8154378c2` has parents `c01ee105d397b1ed16a4daf335db9d8176036bac` and `ef1107d1fc681066cdd99e6f2c55fa2ec67393fe`. C++ imports change var-string length preservation, oversized PageArena allocation/accounting and ownership of metadata-index lookup copies; Java also imports encryption changes. AlignedChunkReader.cc remains byte-identical to c01, but that does not make its linked executable, metadata lifetime or Java compatibility equivalent. All c01 correctness, coverage, sanitizer and timing results retain exact original commit/protocol boundaries. No source push is made by Codex.

The failed job is [unit-test (windows-latest, 3.14)](https://github.com/apache/tsfile/actions/runs/40262386602/job/121377331843), started `2026-10-26T03:06:19Z`, completed `2026-10-26T03:08:43Z`. Its actual checkout is synthetic merge `e6abb45c64fd56b42c47d5be65465418ac404edd`, not presumed standalone head. Its Git tree is independently verified identical to standalone eee39799; the failure stage still precedes project build/test. Original log is `47003` bytes, SHA256 `d39655d9b60c1497e2220ea0b6ae865c8ae26c2edfa9675827b6e97f99d80f8c`. Dependency installation fails with `504 (Gateway Timeout)` for `Packages(Id='llvm',Version='17.0.6')`; Maven build/test and wheel upload are skipped. This is not a C++/Python test failure or evidence that tests passed. No production fix is supported by this trace and no automated rerun was requested. Earlier c01 CI47success is historical, not the new head's current count.

Upstream issue1038 reports21rather than27TimeIn rows, losing19/20after a fully rejected14–18page despite unread time data. Its reproducer has4096byte internal TsBlock capacity and terminates, distinct from1035's128byte hang. The shared empty-result-to-E_NO_MORE_DATA status conversion exists at originalPRbase1180,c01,currenteee and importeddevelopef1107. This is source evidence, not a local execution claim. Issue1034's dictionary fix is now imported by this merge; it remains separately authored. Existing1035/1038bugs are separately tracked, not folded into this PR or used to clear its gaps.

The prospective publication only archives completed c01 diagnostics and this remote observation, then updates the existing PR/reply with the latest-head limitation above. Both actual independent reviewers must approve diagnostic wording on exact manifests; neither source/query gate passes. No new issue, upstream merge, production push, Copilot request or review-setting change. Issue04 still needs separate explicit approval.

Read-only setup failures: direct job-log GET transport failed on signed redirect; the CLI run-log endpoint succeeded (47003bytes). A mistakenly supplied unsupported run-view flag and local default-GBK display errors did not change raw saved inputs. No credentials are included in diagnostic records. Complete raw CI log includes normal masked checkout setup; signed redirect errors are excluded.

## 完整中文译稿

提交 `eee39799948699c58e292ee6361f1da8154378c2` 的父提交为 `c01ee105d397b1ed16a4daf335db9d8176036bac` 和 `ef1107d1fc681066cdd99e6f2c55fa2ec67393fe`。C++合入变长字符串长度保留、超大PageArena分配/计数、元数据索引查找副本所有权修改，Java还合入加密修改。AlignedChunkReader.cc与c01字节相同，不代表链接镜像、元数据生命周期或Java兼容等效。c01正确性/覆盖/sanitizer/性能均保留原提交和协议范围，Codex没有生产源码推送。

失败job为 [unit-test (windows-latest, 3.14)](https://github.com/apache/tsfile/actions/runs/40262386602/job/121377331843)，实际开始 `2026-10-26T03:06:19Z`，完成 `2026-10-26T03:08:43Z`，检出的是合成合并提交 `e6abb45c64fd56b42c47d5be65465418ac404edd`，不假定等于独立head；现已独立核对该合并提交Git tree与独立eee39799完全相同，失败阶段仍早于项目构建/测试。原始日志 `47003` bytes，SHA256 `d39655d9b60c1497e2220ea0b6ae865c8ae26c2edfa9675827b6e97f99d80f8c`。获取 `Packages(Id='llvm',Version='17.0.6')` 收到 `504 (Gateway Timeout)` 导致依赖安装失败，Maven构建/测试和wheel上传均跳过。这不是C++/Python测试失败，也不证明测试通过；该日志不支持生产修补，未自动重跑。先前c01的47成功属于历史，并非新head当前计数。

上游1038报告TimeIn仅21行而非27行，在完全过滤14–18页后漏掉仍未读的19/20。其内部TsBlock4096bytes且正常结束，与1035内部128bytes卡住不同。空结果转E_NO_MORE_DATA的源码同时存在于原PRbase1180、c01、当前eee、合入的developef1107；这是源码证据，不是本地运行复现。1034的字典修复已随合并引入，作者归属单独保留。既有1035/1038独立跟踪，不夹带本PR或用来豁免缺口。

本次拟发布只归档已完成c01诊断及新远端观察，并以顶部最新head限制更新原PR/回复。两位实际独立审阅均须复核精确manifest和文字，仅允许诊断公开，源码/查询门槛不通过。没有新issue、上游合并、生产推送、Copilot请求或审阅设置修改；issue04仍须单独明确批准。

只读setup失败保留：直接job-log GET在签名重定向上transport失败，CLI run-log接口成功（47003bytes）；一次误加不支持的run-view flag及本地默认GBK显示错误未改原始保存输入。诊断不包含凭据，完整CI日志仅有正常已遮盖的checkout设置，签名重定向错误排除出公开证据。

**AI disclosure:** OpenAI Codex wrote this validation report and reply and performed the reported local validation. Maintainer commits retain their Git authorship.

**AI 使用说明：** 本验证报告与回复由OpenAI Codex编写，报告的本地验证由该AI代理执行；维护者提交保留Git作者归属。
