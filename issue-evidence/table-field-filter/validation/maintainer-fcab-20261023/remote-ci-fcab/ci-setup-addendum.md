# Current fcab CI setup failures / 当前 fcab 的 CI 环境失败

The original frozen local validation report did not include these CI records. This addendum documents records obtained and assessed after that report was published; the jobs themselves completed between `2026-10-23T11:27:44Z` and `2026-10-23T11:28:21Z`, earlier than the final review freeze. It records the same public `fcab7437130421bed2604311461a7a7aa6e9a255` and does not change or upgrade the original local gates.

All7failed job logs, job step metadata and check annotations were downloaded and hashed. Six jobs fail in `Install dependencies` because `/usr/bin/clang-format-17` is absent; one fails in `Set up Python` because setup-python has no Python3.9 x64 for Ubuntu26.04. Every later noncleanup step is skipped. No project compilation/tests ran in these7jobs. The exact workflow diff11b→fcab is empty. These are runner/toolchain provisioning failures, not evidence of a new C++ test regression; the separate22query-regression cases, malformed6 and full local LZOkay sanitizer failure remain unresolved. No CI rerun, shared workflow change, source push, issue/PR creation or Copilot request was made.

原冻结本地验证报告没有包含这些CI记录。本附录补记原报告发布后才获取并核对的记录；任务本身于 `2026-10-23T11:27:44Z` 至 `2026-10-23T11:28:21Z` 完成，早于最终审阅冻结时间。附录对应同一公开提交 `fcab7437130421bed2604311461a7a7aa6e9a255`，不改变或升级原有本地门槛。

7个失败任务的实际日志、各步骤元数据及check注解均已下载并计算哈希。6个任务在 `Install dependencies` 阶段因缺少 `/usr/bin/clang-format-17` 失败；另1个在 `Set up Python` 阶段因setup-python没有适用于Ubuntu26.04的Python3.9 x64而失败。后续非清理步骤全部跳过，这7项均没有执行项目编译或测试。workflow在11b→fcab间的精确diff为空。这属于runner/工具链环境失败，不能据此认定新增C++测试回归，也不抵销另行确认的22个查询退化场景、6项畸形树错误一致性问题及本地全量LZOkay sanitizer失败。没有请求重跑CI、修改共享workflow、推送源码、创建issue/PR或请求Copilot。

| Job / 任务 | Failed stage / 失败阶段 | Actual reason / 实际原因 |
|---|---|---|
| [unit-test (ubuntu-latest, 3.14)](https://github.com/apache/tsfile/actions/runs/39931228111/job/120339717916) | Install dependencies | clang-format-17 missing |
| [unit-test (ubuntu-latest, 3.11)](https://github.com/apache/tsfile/actions/runs/39931228111/job/120339717863) | Install dependencies | clang-format-17 missing |
| [unit-test (ubuntu-latest, 3.9)](https://github.com/apache/tsfile/actions/runs/39931228111/job/120339717640) | Set up Python | Python3.9 unavailable on Ubuntu26.04 |
| [unit-test (ubuntu-latest, Release, NoAsan)](https://github.com/apache/tsfile/actions/runs/39931228083/job/120339717530) | Install dependencies | clang-format-17 missing |
| [unit-test (ubuntu-latest, Release, Asan)](https://github.com/apache/tsfile/actions/runs/39931228083/job/120339717511) | Install dependencies | clang-format-17 missing |
| [unit-test (ubuntu-latest, Debug, NoAsan)](https://github.com/apache/tsfile/actions/runs/39931228083/job/120339717478) | Install dependencies | clang-format-17 missing |
| [unit-test (ubuntu-latest, Debug, Asan)](https://github.com/apache/tsfile/actions/runs/39931228083/job/120339717188) | Install dependencies | clang-format-17 missing |

Actual error strings / 实际错误原文：

```text
update-alternatives: error: alternative path /usr/bin/clang-format-17 does not exist
The version '3.9' with architecture 'x64' was not found for Ubuntu 26.04.
```

The first log-download attempt was refused by the current GH CLI's ANSI-output guard. Runtime help confirmed `gh api --allow-escape-sequences`; it was enabled only when capturing raw log bytes to files, without displaying or executing ANSI content. The initial retrieval failure is preserved in `retrieval-note.json` and is not a test failure. Check-run/step JSON and original logs are included in `ci-setup-evidence.zip`, with every entry bound by the manifest.

首次下载日志被当前GH CLI的ANSI输出保护拒绝；本机help确认 `gh api --allow-escape-sequences` 后，只在捕获原始日志字节到文件时启用，未展示或执行ANSI内容。初次下载失败保留在 `retrieval-note.json`，不算测试失败。check/步骤JSON及原始日志包含于 `ci-setup-evidence.zip`，各条目由清单绑定。

**AI disclosure:** OpenAI Codex downloaded and classified the actual CI records and wrote this addendum. No production changes or test reruns are attributed to this diagnostic.

**AI 使用说明：** OpenAI Codex下载、判断实际CI记录并编写本附录；本诊断没有生产代码修改或测试重跑。
