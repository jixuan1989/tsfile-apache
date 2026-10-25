# PR #1026 CI-only follow-up, 2026-10-25

**Query/source gates remain uncleared.** Public head `f98ff7bd52466dcae2dc8122d847be0de9595d59` is a workflow-only follow-up to `fcab7437130421bed2604311461a7a7aa6e9a255`. The previously measured finite zero-hit FLOAT/DOUBLE NOT latency of 2.6430–2.8513× the prior valid native implementation, six malformed empty/LIMIT0 checks, and local strict sanitizer failure retain their original measured heads and scope. No new local correctness, Java compatibility, coverage, sanitizer, write or query run was performed. Local candidate `2525a557fc1fa67e2c813cc0f42959d499dc2ff6` remains unsubmitted with both earlier final reviews `NOT_READY_TO_PUSH`.

Maintainer ColinLee pinned the Linux C++/Python matrices to Ubuntu 24.04 and explicitly installed `clang-format-17` before configuring alternatives. Exactly two workflow files changed; the standalone `cpp`, `java` and `python` Git trees are identical between the two PR heads (`scope.json`). The previous seven setup failures are historical; all 49 current-head check records are complete: 47 success, one neutral CodeQL record and one skipped codecov job. Success counts are GitHub check records, not test counts. No rerun, source push, upstream merge or Copilot review was requested.

All seven formerly affected Linux matrix replacements reached successful dependency installation and Maven build/test steps. Their actual checkout was synthetic merge `dcd29245266b02f63cd1b5915532fe8e6f922fd6` with parents `eb733133b9eee0b1eb74f7671d809ecd730cedc3` and `f98ff7bd52466dcae2dc8122d847be0de9595d59`. Its C++ and Java trees differ from the standalone PR head; 71 files differ overall. CI results below belong to that merge checkout and its toolchains, not new standalone-head local measurements.

| CI job | Exact visible runner summary |
|---|---|
| [unit-test (ubuntu-24.04, Release, NoAsan)](https://github.com/apache/tsfile/actions/runs/40174679565/job/121112693293) | `[INFO] 100% tests passed, 0 tests failed out of 1365` |
| [unit-test (ubuntu-24.04, Debug, Asan)](https://github.com/apache/tsfile/actions/runs/40174679565/job/121112693234) | `[INFO] 100% tests passed, 0 tests failed out of 1365` |
| [unit-test (ubuntu-24.04, Debug, NoAsan)](https://github.com/apache/tsfile/actions/runs/40174679565/job/121112693190) | `[INFO] 100% tests passed, 0 tests failed out of 1365` |
| [unit-test (ubuntu-24.04, 3.14)](https://github.com/apache/tsfile/actions/runs/40174679545/job/121112693068) | `[INFO] 100% tests passed, 0 tests failed out of 1363`<br>`============================= 602 passed in 16.49s =============================` |
| [unit-test (ubuntu-24.04, 3.11)](https://github.com/apache/tsfile/actions/runs/40174679545/job/121112693028) | `[INFO] 100% tests passed, 0 tests failed out of 1363`<br>`============================= 602 passed in 20.54s =============================` |
| [unit-test (ubuntu-24.04, Release, Asan)](https://github.com/apache/tsfile/actions/runs/40174679565/job/121112693009) | `[INFO] 100% tests passed, 0 tests failed out of 1365` |
| [unit-test (ubuntu-24.04, 3.9)](https://github.com/apache/tsfile/actions/runs/40174679545/job/121112692835) | `[INFO] 100% tests passed, 0 tests failed out of 1363`<br>`======================= 601 passed, 1 skipped in 22.71s ========================` |

Each of the four C++ jobs has 1,362 Passed entries, 3 Skipped and 10 Disabled; the CTest total 1,365 includes the three skipped entries. Each Python job's C++ stage has 1,360 Passed, 3 Skipped and 10 Disabled (CTest total 1,363). Python 3.11/3.14 each reports 602 passed; Python 3.9 reports 601 passed and one skipped. The three skipped C++ entries are GenerateFixtures, ValidateFixtures and OpensExternalIndexWhenConfigured; those entries do not establish fixture cross-reading. These are CTest/pytest entries, not assertion counts. Raw details remain in the logs and `ci-summary.json`.

The two Asan configurations visibly link `-fsanitize=address,undefined`. Their jobs pass, and no sanitizer error marker was found in the visible runner logs; CTest does not retain complete stdout/stderr for passing tests here. This is not proof of an equivalent strict nonrecovering local UBSan run, or a replacement for the earlier all-codec local LZOkay failure. No sanitizer suppression or acceptance gate was changed.

The frozen fcab and local2525 performance rounds, all adverse samples, original coverage denominators, Java oracle limitations and unmeasured query metrics remain intact. There is no new latency ratio, necessity proof, no-regression claim or passing source-submission decision. PR #1018/#1024 evidence gaps and the next issue's independent publication approval are unchanged.

## 完整中文说明

**查询及源码提交门槛仍未通过。** 公开提交 `f98ff7bd52466dcae2dc8122d847be0de9595d59` 仅在 `fcab7437130421bed2604311461a7a7aa6e9a255` 基础上修改工作流。此前测得有限值零命中 FLOAT/DOUBLE NOT 查询延迟为上一正确原生实现的 2.6430–2.8513 倍、6 项空表/LIMIT0 畸形树检查，以及本地严格 sanitizer 失败，均保留原始测量提交及范围。本次没有新运行本地正确性、双向 Java、覆盖率、sanitizer、写入或查询测试。本地候选 `2525a557fc1fa67e2c813cc0f42959d499dc2ff6` 仍未提交，两份此前最终独立审阅的 `NOT_READY_TO_PUSH` 结论保持不变。

维护者 ColinLee 将 Linux C++/Python 矩阵固定为 Ubuntu 24.04，并在设置 alternatives 前显式安装 `clang-format-17`。只修改了两份工作流；两个独立 PR head 的 `cpp`、`java`、`python` Git tree 完全相同，见 `scope.json`。此前 7 项环境准备失败已成为历史记录；当前 head 的 49 条检查均完成：47 成功、1 条 CodeQL 中立、1 项 codecov 跳过。这是 GitHub 检查记录数，不是测试数。未请求重跑、推送源码、合并上游或请求 Copilot 审阅。

原先受影响的 7 项 Linux 矩阵替代任务均已成功完成依赖安装及 Maven 构建/测试。它们实际检出 GitHub 生成的合并提交 `dcd29245266b02f63cd1b5915532fe8e6f922fd6`，父提交为 `eb733133b9eee0b1eb74f7671d809ecd730cedc3` 和 `f98ff7bd52466dcae2dc8122d847be0de9595d59`。该合并提交的 C++、Java tree 与独立 PR head 不同，总计 71 个文件不同。上表逐项链接及原文日志汇总属于这一合并提交及其 CI 工具链，不是本轮新取得的独立 head 本地测量。

4 个 C++ 任务各有 1,362 项 Passed、3 项 Skipped、10 项 Disabled；CTest 汇总的 1,365 包含这 3 项跳过。每个 Python 任务的 C++ 阶段各有 1,360 项 Passed、3 项 Skipped、10 项 Disabled（CTest 汇总 1,363）。Python 3.11/3.14 各报告 602 passed，Python 3.9 为 601 passed、1 skipped。3 项 C++ 跳过条目是 GenerateFixtures、ValidateFixtures、OpensExternalIndexWhenConfigured，这些条目没有证明外部夹具交叉读取。这些是 CTest/pytest 条目数，不是断言数；原始明细保留在日志及 `ci-summary.json`。

两项 Asan 配置的链接参数可见 `-fsanitize=address,undefined`。这些任务已通过，可见 runner 日志未找到 sanitizer 错误标记；但此处 CTest 不保留通过测试的完整 stdout/stderr，不能证明与本地严格、不可恢复的 UBSan 运行等价，也不能替代此前启用全部压缩库的本地 LZOkay 失败。未新增 suppression，也未更改验收门槛。

fcab 与本地2525的冻结性能轮次、全部不利样本、原覆盖率分母、Java oracle 限制及未测查询指标均保留。没有新延迟比率、成本必要性证明、无退化声明或源码提交通过结论。PR #1018/#1024 的证据缺口及下一条 issue 的单独发布批准要求不变。

**AI disclosure:** OpenAI Codex retrieved and checked the reported GitHub evidence and wrote this addendum. CI runs and the new commit were performed/authored by their recorded GitHub actors, not by this agent. This addendum does not claim new local test execution.

**AI 使用说明：** 本附录由 OpenAI Codex 获取、核对 GitHub 证据并编写；CI 运行和新提交分别归属于其 GitHub 记录的执行者及 Git 作者，不归该 AI 代理。本附录不声称执行了新的本地测试。
