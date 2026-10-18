# TsFile PR 03 本地验证报告

Issue：https://github.com/apache/tsfile/issues/1025。独立分支 `cpp/fix-table-field-filter`，基线 `1180b13675e11a0230708af2cc70d037e0e12623`，验证提交 `e2e9c3786f9753ec5d5c1b813fd2f1fb0d71d5b8`。

## 修改为何正确

原对齐批路径跳过 FIELD 回调；稀疏合并路径的 TODO 在非空过滤器下既不输出也不推进。现在非空过滤器走独立列上下文的时间合并路径：先形成保留实际类型、NULL、二进制长度和 64 位时间戳的借用行视图，再调用谓词。不能复用 TAG 的字符串段回调，也不能把共享向量上下文的首列值当作所有字段的值。

谓词的返回码与匹配布尔值分离：`E_OK` 加 `false` 是正常拒绝，非零返回码才是失败。`RET_FAIL(expr)` 将返回码赋给 `ret` 并判断其是否非零，不把匹配结果当成错误码。只有接受的行才消耗 OFFSET/LIMIT；拒绝行也必须推进，跨页、chunk 和设备继续读。回调或读取失败由既有 ResultSet 错误锁存机制传播。未过滤查询保留原有共享向量和批复制路径，接受行也保留原来的填充/推进循环。

新增 TableFieldFilter 没有修改 Filter 的虚函数表。旧 Filter 支持单个整数/布尔或字符串字段，NULL 不匹配；旧接口的浮点和多字段形态返回 E_NOT_SUPPORT，应使用带类型行回调。未投影字段自动加载、谓词下推和向量化过滤不在本项范围。视图只在回调内有效。

## 正确性与兼容性

50 项新增专项全部通过；Windows 全量 955 通过、3 跳过；Linux 全量 976 通过、1 跳过。两侧各有 10 项已有 disabled 测试，未将其算作通过。完整库及专项均使用 MSVC ASan 插桩，重复 5 轮，共 250 次通过。

原 issue 的 12 次 Java/C++ 自身和交叉读取全部一致，直接验证 Java 原生 ExpressionTree 常量回调。多类型文件有 24 次逐行对照，包含两种 writer、两种 reader、NULL、二进制、浮点及过滤后的 OFFSET/LIMIT。复杂条件的 Java 答案由 Java 原生解码后的应用层谓词计算，没有冒充 Java 原生字段表达式接口。上游验证器还验证 Java 读取 117 个 C++ 文件、C++ 读取 135 个 Java 文件，Linux 启用了六种可选压缩库。

## 覆盖率

新增/修改生产行 75/77（97.40%），分支 85/109（77.98%）。两条未覆盖行是读取当前上下文时的防御性错误返回。以下同时报告整文件覆盖率，不将局部覆盖率当成整个模块的覆盖率。

| Production file | Whole-file lines | Whole-file branches |
|---|---:|---:|
| `cpp/src/reader/block/single_device_tsblock_reader.cc` | 629/756 (83.20%) | 605/1008 (60.02%) |
| `cpp/src/reader/block/single_device_tsblock_reader.h` | 29/29 (100.00%) | 10/14 (71.43%) |
| `cpp/src/reader/filter/table_field_filter.cc` | 24/24 (100.00%) | 16/19 (84.21%) |
| `cpp/src/reader/filter/table_field_filter.h` | 16/16 (100.00%) | 19/20 (95.00%) |

GCC/gcovr 原始计数使用 atomic profiling；源文件与 CMake 复制头文件先核对 SHA，再按物理行和分支标识合并。没有排除分支或忽略解析失败。覆盖率来自完整 Linux 测试的计数快照；之后又单独验证了新生成的 Java fixture。

## 性能

300,000 行 × 8 个 INT64 字段，每进程 8 次完整查询；双方每一行和校验和均校验。每场景 2 轮预热、25 对交替独立进程、CPU affinity=4。计时含打开/查询/扫描/释放结果，不含生成 fixture。基线源快照的 255 个文件已逐一核对 Git blob。

| Scenario | Fixed / baseline latency | 95% bootstrap interval | Baseline / fixed p95 (s) |
|---|---:|---|---|
| `all_row` | 0.9955 | [0.9856, 1.0047] | 0.362647 / 0.353376 |
| `all_batch` | 0.9945 | [0.9891, 1.0157] | 0.144448 / 0.147937 |
| `time_row` | 1.0063 | [0.9946, 1.0148] | 0.239114 / 0.253533 |
| `time_batch` | 1.0136 | [1.0008, 1.0281] | 0.101074 / 0.103562 |
| `offset_row` | 0.9947 | [0.9806, 1.0096] | 0.162534 / 0.163275 |
| `offset_batch` | 0.9814 | [0.9609, 0.9987] | 0.112986 / 0.117022 |
| `sparse_row` | 1.0033 | [0.9983, 1.0119] | 0.672574 / 0.706775 |
| `sparse_batch` | 0.9801 | [0.9713, 0.9998] | 0.464649 / 0.480847 |

The initial `time_batch` estimate was 1.0136 [1.0008, 1.0281]. It was investigated with 300 additional independent alternating process pairs, grouped into 75 blocks of four pairs: the median block ratio was 0.9961, 95% interval [0.9882, 1.0011]. The slowdown did not reproduce consistently. Both datasets are retained; no production change was made between these measurements.

首轮时间过滤批查询偏慢的结果没有删除。追加 300 对、按每 4 对形成 75 个区块后，没有复现稳定退化；两个阶段使用完全相同的源提交和测量程序。原有有效查询路径的结果不能证明所有场景永不退化；此前忽略过滤器或卡住的实现也不是实际执行过滤的等价性能基线。

## 保留的失败与限制

1. Windows 关闭可选压缩库时额外启用 fixture 生成测试会失败；未修改基线和修复版的 336 个断言值序列完全一致。已保留两个日志，不计入默认套件通过数；压缩兼容性结论使用全部压缩库开启的 Linux 结果。
2. Windows Java 生成的 CSV manifest 使用 CRLF，Linux 上游测试工具逐字比较表头而失败。只将辅助 CSV 转为 LF，135 个 TsFile 的 SHA 全部不变，保留原 CSV、失败日志和转换脚本。
3. 显式投影 time 在基线表 schema 中已经返回列不存在，本项测试隐式时间戳和 TAG-only 投影。该限制未作为本项修改内容。
4. 初次批模式测试工具错误使用了不存在的显式 time 列索引，修正为表块固定的时间列 0。ASan 工具初次链接了未插桩 GTest，出现链接注解不匹配；已改为同选项编译 GTest，最终插桩测试通过。这些是验证工具修正，没有更改生产逻辑来绕过断言。
5. WSL/NTFS 构建曾提示约 0.2 秒时间偏差；最终重建未改变已验证可执行文件的 SHA，重建日志和前后 SHA 保留。

## 可复查材料

证据包包含生产 diff、五个修改文件、独立跨语言源码、CMake/PowerShell/WSL 构建脚本、原始测试 XML 和日志、覆盖率原始 JSON/汇总、全部性能样本与确认样本、基线文件核验、manifest 转换与 TsFile SHA。机器路径保留实际执行位置。主要入口为 final-native.ps1、build-asan.ps1、build-linux.sh、final-linux-extra.sh、check_compatibility.py、benchmark.py、confirm_performance.py。

**AI disclosure:** The implementation, tests and description in this pull request were written by an AI coding agent (OpenAI Codex), which also performed the reported local validation.

**AI 使用说明：** 本 PR 的代码修改、测试和正文由 AI 编程代理（OpenAI Codex）编写，文中报告的本地验证也由该 AI 代理执行。
