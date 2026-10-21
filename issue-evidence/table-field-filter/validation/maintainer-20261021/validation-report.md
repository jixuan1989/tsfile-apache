# PR #1026 maintainer follow-up validation

> **WARNING — query acceptance is not cleared.** Three initially flagged comparisons remain positive in the predeclared independent confirmation. Their necessity is unproven. The complete combined ASan/UBSan run is also not clean because unchanged-code diagnostics aborted it. Functional validation below must not be read as whole-PR acceptance.
>
> **警告——查询性能尚未验收通过。** 三个初测上升项在事先规定的独立复核中仍为正向，尚未证明其必要性。完整 ASan/UBSan 检查也因未改动代码的诊断而中止，不能称为全量通过。下述功能验证结果不代表整个 PR 已满足全部门槛。

| Comparison | Confirmed median latency change | Bootstrap 95% interval |
|---|---:|---:|
| `null_w4_p1_b1024_tag0_parallel0` | +0.826% | [+0.125%, +1.454%] |
| `dense_w4_p10_b1024` | +0.902% | [+0.528%, +1.321%] |
| `dense_w4_p100_b1024` | +1.433% | [+0.380%, +1.998%] |

The NULL comparisons above use a correct application-level reference, including an extra dense `anchor` projection and its materialization. The formerly incorrect native query returns no rows and is not a valid fast baseline. Across the 30 initial NULL cases, native-after / old correct-reference median ratios range from 0.6479 to 1.7273; the largest is `null_w4_p100_b1024_tag1_parallel0`. Different execution plans, projection, predicate and verification work are included, so these ratios do not isolate reader-engine cost. The worst cost difference is still disclosed rather than called an unavoidable regression.

上述 NULL 对照使用能返回正确结果的应用层过滤参考，包含额外稠密 `anchor` 列的投影和物化。旧原生查询漏掉所有行，不能用它作为快速基线。30 个 NULL 初测场景中，新原生路径/旧正确参考的延迟比为 0.6479–1.7273，最高出现在 `null_w4_p100_b1024_tag1_parallel0`。执行计划、投影、谓词和验证开销不同，不能由此单独归因于 reader 引擎；最大差距仍明确披露，不擅称其不可避免。

## Reviewed source and correctness

Frozen old head: `249b0d51a6bfe202185aa21b794ff21ccdfafcf3`. Frozen final head: `6f4a971eefffcc81cf62a75b6ad8bc91460b0fa6`. The two new commits were authored by maintainer ColinLee/ColinLeeo; Codex fetched and fast-forwarded the clean local topic branch, without authoring or pushing production changes.

`f2e157ed3` correctly replaces a whole-series non-NULL-count test with an aligned-source test in the empty-value-context fallback. A series may have non-NULL values only before the selected time window. Its shared aligned timestamps must still reach a NULL-aware FIELD predicate. The non-aligned shortcut and prior hard-error propagation remain. The new maintainer regression fails 6/6 on the old library and passes on the final head. Additional local-only tests cover multiple/duplicate projected fields, TAG exclusion from FIELD rows, OFFSET/LIMIT across devices, rejecting/error callbacks, outside-window and mixed present/missing fields.

Three further local-only cases exercise the retained non-aligned guard using real points at times 0 and 100: querying the gap [50,60] returns no rows and invokes no predicate, while [0,0] returns the first value. Row, batch-1 and batch-4 modes pass under ASan/UBSan. These cover the previously missed changed guard line without a production edit.

`6f4a971e` removes a private non-virtual INT32 helper with only a declaration/definition and no call sites at the old head. Active dispatch already calls `decode_tv_batch<int32_t>`. The separately used non-aligned `ChunkReader` method was not removed.

冻结的旧、新提交分别如上。两次新生产提交由维护者 ColinLee/ColinLeeo 编写；Codex 只获取并快进同步干净的本地分支，没有编写或推送新的生产代码。第一项修正正确地区分了“整列有值”与“选中时间范围有值”：第一 chunk 有值、第二 chunk 全 NULL 时仍须以共享时间轴向谓词提供 NULL 行，非对齐保护和既有硬错误传播保留。维护者新回归在旧库 6/6 失败、最终提交通过；本地额外用例覆盖多字段/重复投影、TAG 不进入 FIELD 行、跨设备 OFFSET/LIMIT、拒绝/错误回调、窗口外和有值/无值列混合。

另有三个本地辅助用例使用时间 0、100 的真实非对齐数据：查询间隙 [50,60] 返回零行且不调用谓词，[0,0] 返回首值。行模式、batch-1、batch-4 均在 ASan/UBSan 下通过，补到了此前未覆盖的修改保护行，没有为覆盖率修改生产代码。第二项删除的是无调用点的私有非虚 INT32 辅助函数；实际分派已使用 `decode_tv_batch<int32_t>`，仍在使用的非对齐 `ChunkReader` 同名函数保留。

| Local test record | Passed | Failed | Skipped | Disabled |
|---|---:|---:|---:|---:|
| `before-new-regression.xml` | 0 | 6 | 0 | 0 |
| `after-field-filter.xml` | 80 | 0 | 0 | 0 |
| `extended-windows.xml` | 24 | 0 | 0 | 0 |
| `windows-full.xml` | 985 | 0 | 3 | 10 |
| `linux-field-filter.xml` | 80 | 0 | 0 | 0 |
| `extended-linux.xml` | 24 | 0 | 0 | 0 |
| `linux-reader-scope.xml` | 343 | 0 | 2 | 9 |
| `nonaligned-linux.xml` | 3 | 0 | 0 | 0 |

Windows Release uses the same codecs-off static configuration as the retained old Windows library. Linux focused/reader checks use all six compression codecs and combined ASan/UBSan with leak detection. Ten upstream disabled tests remain disabled. Full failed runs are preserved as `linux-full.log` and `linux-remainder.log`. The first hits `ts2diff_decoder.h:508` signed overflow; exact old/new Git blobs have the same SHA256 and a valid two-value raw page reproduces the overflow with both. The separately filtered remainder later hits an unaligned read in the unchanged pinned LZOkay dependency. No sanitizer suppression or production fix was added. The reader-scope run covers suites named in `cpp/test/reader`, with unconfigured external fixtures explicitly skipped; it cannot replace those two failed broader runs.

Windows 配置与保存的旧 Windows 静态库一致，关闭可选压缩库；Linux 专项/reader 使用六种压缩库，并同时开启 ASan、UBSan 和泄漏检测。上游 10 个禁用测试仍禁用。两个失败的扩大检查原日志完整保留：第一次在 `ts2diff_decoder.h:508` 触发有符号溢出，旧、新 Git 原始头文件 SHA256 一致，合法双值原始页在两版均复现；单独排除该夹具测试的剩余检查又在未改动的固定版本 LZOkay 中遇到未对齐读取。没有新增 sanitizer suppression 或生产修正。reader 范围按 `cpp/test/reader` 的测试套件提取，未配置的外部夹具明确记为跳过，不能代替前述两个失败的扩大检查。

## Java compatibility and coverage

48 final-C++/Java own or cross reads match exact timestamps, order, NULL cells and BOOLEAN output across Java, old-C++ and final-C++ writer products. Twenty-four old reads retain six expected failures in the newly exposed NULL-window/slice cases. Both C++ writer products are byte-identical for the small and large NULL fixtures. Java/C++ whole-file byte equality is not claimed. Java performs its native time-filtered read and application-level IS NULL / OFFSET/LIMIT; final C++ performs native FIELD filtering. No new general Java/C++ equivalence claim is made.

新增 48 次最终 C++/Java 自身或交叉读取逐项一致，覆盖时间、顺序、NULL 和 BOOLEAN 输出；24 次旧读回保留新增 NULL 时间窗口/切片中的六次预期失败。小型和大型 NULL 夹具由旧、新 C++ 写出时字节完全一致，不宣称 Java/C++ 整文件字节一致。Java 使用原生时间过滤并在应用层执行 IS NULL 和 OFFSET/LIMIT，最终 C++ 使用原生 FIELD 回调；不扩大为全库互通保证。

Added/changed production executable lines: **4/4 (100.00%)**; changed branches **5/6 (83.33%)**. Affected reader files combined: **79.81% lines / 55.92% branches**. Deleted dead lines are not added executable lines. Native GCC11 gcov JSON counters are merged only for byte-identical source/header copies; branch identities retain mangled function and line-ordinal distinctions. `coverage-filtered-inputs.json`, native-report hashes and collector preserve the inputs and method. Earlier gcovr tooling failures are retained; no ignore-errors flags were used. Coverage does not turn aborted sanitizer runs into correctness passes.

本次新增/修改生产可执行行覆盖率 **4/4（100.00%）**，修改分支覆盖率 **5/6（83.33%）**；受影响 reader 文件合计行/分支覆盖率 **79.81% / 55.92%**。删除的死代码不作为新增可执行行。仅合并字节相同的源码/复制头文件，分支保留函数与行内序号身份；过滤后的原始输入、原生报告哈希和采集器保留。先前 gcovr 工具失败也保留，没有忽略解析错误，更不把覆盖率当成中止的 sanitizer 全量通过。

## Query and write measurement scope

68 initial cases: eight existing aligned scan/time/OFFSET/sparse cases, 30 dense FIELD width/selectivity cases and 30 NULL-in-range cases. Two warmup blocks and 24 balanced measurement blocks per case, then one independent 48-block confirmation for each of seven predeclared initial flags. **20,928 formal checked queries**, plus **1,456 warmup queries**, in 5,084 child processes. Every command, result, affinity and frozen input hash was independently rechecked. All initial/confirmation arrays and outliers remain. New local verifier copies check all projected cells/order; their absolute times cannot be compared with the older weaker verifier's historical times.

MSVC Release, PLAIN/UNCOMPRESSED, warm filesystem cache. Children start suspended, receive and verify affinity mask4 before resume; parent mask16. No exclusive-core or controlled-cold-cache claim. Dense/NULL datasets report open, plan/metadata, first-returned-row, complete-query p50/p95, throughput and whole-process peak working set. Zero-hit queries have no first-row latency. The eight existing cases retain only total eight-query time/throughput; missing open/first-row/memory metrics stay missing. Driver families have different first-row observation points. Only the explicit TAG/parallel settings in the protocol are measured, not a complete parallel matrix. P99, cold cache, compressed query latency, broad non-aligned FIELD performance and general parallel scaling remain unmeasured.

共 68 个初测场景，分别为原有 8 项扫描/时间/OFFSET/稀疏查询、30 项稠密 FIELD 投影/命中率和 30 项时间范围内全 NULL 查询。每项两组预热、24 组平衡顺序正式测量，七个触发项各做一次独立 48 组复核；**20,928 次正式完整核对查询**，另有 **1,456 次预热**，合计 5,084 个子进程。原始记录、哈希、命令、亲和性和结果离线复核，初测/复核及异常样本全部保留。加强后的本地验证驱动逐项核对投影值和顺序，其绝对耗时不能直接与旧弱校验驱动的历史耗时比较。

使用 MSVC Release、PLAIN/UNCOMPRESSED、暖文件系统缓存。子进程暂停创建后设置并核对亲和性 mask4 再恢复，父进程 mask16；不声称独占核心或受控冷缓存。稠密/NULL 数据单列打开、元数据/计划、首个匹配行、完整查询 p50/p95、吞吐和整个进程峰值工作集；零命中没有首行指标。原有八项只记录八次查询总耗时/吞吐，缺失的打开/首行/内存仍明确缺失。不同驱动的首行观测点不同，不能跨组比较其绝对值。仅测协议内实际 TAG/并行设置；P99、冷缓存、压缩查询、大范围非对齐 FIELD 性能和通用并行扩展仍未测。

Write throughput was not rerun for this reader-only change. Old/new writer product bytes were compared and both products queried. Historical write evidence remains at its recorded head/scope. No source push, upstream merge or Copilot review request was made. A read-only independent agent reviewed local source and validation; two protocol findings were corrected before measurement. Actual model identity and a different-model final evidence review remain unverified/not run, so the complete new pre-submission review gate is not passed.

本次仅涉及 reader，没有重测写入吞吐；已比较两版写出字节并查询两版产物，旧写入证据保留其提交和范围。本轮未推生产代码、未合并上游、未请求 Copilot。独立 agent 对本地源码和验证做了只读审阅，两条协议意见已在计时前修正；实际模型身份及另一模型最终证据审阅尚未核实/运行，完整的新提交前审阅门槛未通过。

## Complete query table

`after/before - 1`; NULL `before/after` are correct application references. Native ratios and all metric arrays are in `benchmark-results.json`.

| Case | Initial median change | Initial 95% interval | Independent confirmation |
|---|---:|---:|---:|
| `existing_all_0` | +0.022% | [-0.538%, +1.587%] | not triggered |
| `existing_all_1024` | +0.513% | [-0.784%, +1.009%] | not triggered |
| `existing_time_0` | +0.612% | [+0.092%, +1.316%] | +0.237% [-0.102%, +0.602%] |
| `existing_time_1024` | +0.315% | [-0.931%, +1.064%] | not triggered |
| `existing_offset_0` | +0.753% | [-0.203%, +1.283%] | not triggered |
| `existing_offset_1024` | -0.919% | [-2.267%, +1.319%] | not triggered |
| `existing_sparse_0` | +0.409% | [-0.674%, +0.756%] | not triggered |
| `existing_sparse_1024` | +0.231% | [-0.488%, +0.903%] | not triggered |
| `dense_w1_p0_b0` | +0.208% | [-0.257%, +1.099%] | not triggered |
| `null_w1_p0_b0_tag0_parallel0` | +0.047% | [-0.787%, +0.906%] | not triggered |
| `dense_w1_p0_b1024` | -0.152% | [-2.031%, +1.184%] | not triggered |
| `null_w1_p0_b1024_tag0_parallel0` | -0.763% | [-1.110%, +0.303%] | not triggered |
| `dense_w1_p1_b0` | +1.339% | [-0.917%, +1.764%] | not triggered |
| `null_w1_p1_b0_tag1_parallel0` | -0.571% | [-0.867%, +0.281%] | not triggered |
| `dense_w1_p1_b1024` | +0.059% | [-0.708%, +1.622%] | not triggered |
| `null_w1_p1_b1024_tag1_parallel0` | -0.440% | [-1.558%, +0.336%] | not triggered |
| `dense_w1_p10_b0` | +0.256% | [-1.129%, +1.533%] | not triggered |
| `null_w1_p10_b0_tag0_parallel0` | +0.303% | [-0.428%, +0.874%] | not triggered |
| `dense_w1_p10_b1024` | +0.113% | [-0.785%, +1.261%] | not triggered |
| `null_w1_p10_b1024_tag0_parallel0` | +0.247% | [-1.154%, +0.740%] | not triggered |
| `dense_w1_p50_b0` | +1.009% | [-0.726%, +1.865%] | not triggered |
| `null_w1_p50_b0_tag0_parallel0` | +0.298% | [-0.563%, +0.949%] | not triggered |
| `dense_w1_p50_b1024` | +0.310% | [-1.168%, +2.491%] | not triggered |
| `null_w1_p50_b1024_tag0_parallel0` | +0.312% | [-0.264%, +0.817%] | not triggered |
| `dense_w1_p100_b0` | +0.639% | [-0.930%, +1.952%] | not triggered |
| `null_w1_p100_b0_tag0_parallel0` | +0.685% | [+0.102%, +0.945%] | -0.197% [-0.415%, +0.092%] |
| `dense_w1_p100_b1024` | +0.675% | [-0.957%, +1.811%] | not triggered |
| `null_w1_p100_b1024_tag0_parallel0` | -0.820% | [-1.270%, +0.029%] | not triggered |
| `dense_w4_p0_b0` | -0.000% | [-1.422%, +1.107%] | not triggered |
| `null_w4_p0_b0_tag1_parallel0` | -0.291% | [-0.649%, -0.038%] | not triggered |
| `dense_w4_p0_b1024` | +0.394% | [-0.649%, +1.167%] | not triggered |
| `null_w4_p0_b1024_tag1_parallel0` | -0.083% | [-1.157%, +0.826%] | not triggered |
| `dense_w4_p1_b0` | +0.612% | [-0.260%, +1.477%] | not triggered |
| `null_w4_p1_b0_tag0_parallel0` | -0.054% | [-0.418%, +0.249%] | not triggered |
| `dense_w4_p1_b1024` | +0.956% | [+0.277%, +1.923%] | +0.432% [-0.394%, +0.959%] |
| `null_w4_p1_b1024_tag0_parallel0` | +1.457% | [+0.664%, +1.832%] | +0.826% [+0.125%, +1.454%] |
| `dense_w4_p10_b0` | +0.349% | [-0.875%, +1.343%] | not triggered |
| `null_w4_p10_b0_tag1_parallel0` | -0.377% | [-0.806%, -0.056%] | not triggered |
| `dense_w4_p10_b1024` | +0.983% | [+0.045%, +1.574%] | +0.902% [+0.528%, +1.321%] |
| `null_w4_p10_b1024_tag1_parallel0` | +0.247% | [-0.367%, +1.836%] | not triggered |
| `dense_w4_p50_b0` | +0.344% | [-0.273%, +1.239%] | not triggered |
| `null_w4_p50_b0_tag1_parallel0` | -0.139% | [-0.492%, +0.089%] | not triggered |
| `dense_w4_p50_b1024` | +0.676% | [+0.383%, +2.418%] | +0.852% [-0.018%, +1.674%] |
| `null_w4_p50_b1024_tag1_parallel0` | +0.181% | [-0.678%, +0.748%] | not triggered |
| `dense_w4_p100_b0` | +0.339% | [-0.877%, +0.667%] | not triggered |
| `null_w4_p100_b0_tag1_parallel0` | -0.254% | [-0.946%, +0.290%] | not triggered |
| `dense_w4_p100_b1024` | +1.698% | [+0.602%, +2.488%] | +1.433% [+0.380%, +1.998%] |
| `null_w4_p100_b1024_tag1_parallel0` | +0.194% | [-0.348%, +0.523%] | not triggered |
| `dense_w8_p0_b0` | -0.862% | [-2.631%, +0.108%] | not triggered |
| `null_w8_p0_b0_tag1_parallel0` | +0.122% | [-0.300%, +0.560%] | not triggered |
| `dense_w8_p0_b1024` | +0.473% | [-0.989%, +2.259%] | not triggered |
| `null_w8_p0_b1024_tag1_parallel1` | -40.781% | [-41.301%, -40.566%] | not triggered |
| `dense_w8_p1_b0` | +0.190% | [-0.869%, +1.851%] | not triggered |
| `null_w8_p1_b0_tag0_parallel0` | +0.108% | [-0.061%, +0.613%] | not triggered |
| `dense_w8_p1_b1024` | -0.291% | [-1.367%, +0.412%] | not triggered |
| `null_w8_p1_b1024_tag0_parallel1` | -3.111% | [-3.879%, -2.085%] | not triggered |
| `dense_w8_p10_b0` | -0.352% | [-1.918%, +1.286%] | not triggered |
| `null_w8_p10_b0_tag1_parallel0` | -0.015% | [-0.725%, +0.535%] | not triggered |
| `dense_w8_p10_b1024` | -0.799% | [-1.225%, +0.106%] | not triggered |
| `null_w8_p10_b1024_tag1_parallel1` | -0.432% | [-0.661%, +0.445%] | not triggered |
| `dense_w8_p50_b0` | +0.744% | [-1.446%, +2.322%] | not triggered |
| `null_w8_p50_b0_tag1_parallel0` | -0.330% | [-0.645%, +0.103%] | not triggered |
| `dense_w8_p50_b1024` | -1.053% | [-2.004%, -0.252%] | not triggered |
| `null_w8_p50_b1024_tag1_parallel1` | -0.121% | [-0.705%, +0.437%] | not triggered |
| `dense_w8_p100_b0` | -0.189% | [-1.286%, +0.704%] | not triggered |
| `null_w8_p100_b0_tag1_parallel0` | +0.228% | [-0.216%, +0.933%] | not triggered |
| `dense_w8_p100_b1024` | +1.005% | [-0.337%, +3.303%] | not triggered |
| `null_w8_p100_b1024_tag1_parallel1` | -0.038% | [-0.556%, +0.313%] | not triggered |

**AI disclosure:** The analysis, local validation, reproduction helpers and report were prepared by OpenAI Codex. The two reviewed production commits were authored by maintainer ColinLee/ColinLeeo.

**AI 使用说明：** 本分析、本地验证、复现辅助代码和报告由 OpenAI Codex 完成；本次审阅的两次生产代码提交由维护者 ColinLee/ColinLeeo 编写。
