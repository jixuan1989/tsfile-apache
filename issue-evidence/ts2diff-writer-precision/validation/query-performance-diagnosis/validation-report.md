# TsFile PR #1024: query signal diagnosis

Tested head `75592b89d1523a96090e8bca1dcb4cd2180162e5`; baseline `1180b13675e11a0230708af2cc70d037e0e12623`. Production code, the six measured original binaries, and their source checkouts remain unchanged/clean. This report supplements the previous query backfill and preserves its small dense-DOUBLE slowdown and later contradictory controls. The query gate remains qualified; no universal or zero-regression claim is made.

## Retained measurements: where was the earlier difference?

Retrospective decomposition uses every original 192-quartet confirmation sample, with 24 chronological blocks of eight. `consume_validate_close` is full-result time minus open, explicit cached schema lookup and plan time. It combines native read/decode, application materialization/verification and cleanup; it is not pure decoder timing. Component medians are not additive. These exploratory subcomponents reuse the same processes and do not form independent confirmation evidence.

| Case | Contrast | Full paired median delta/query (µs) | Consume/validate/close delta/query (µs) | Open delta/query (µs) |
|---|---|---:|---:|---:|
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` | `reader_on_fixed_file` | 25.383 | 24.917 | -0.767 |
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` | `end_to_end` | 13.517 | 13.650 | -1.317 |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` | `reader_on_fixed_file` | 13.817 | 16.100 | -0.333 |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` | `end_to_end` | 12.517 | 13.633 | 0.367 |

The retained difference predominantly occurs after query construction (roughly 13–25 µs/query in these comparisons), rather than a stable file-open increase. It remains incorrect to replace these original observations with the later opposite-direction samples.

## What actually differs in linked reader code?

Linker-map sidecars are generated from the original single reader object and pinned libraries. Their `.text` and `.pdata` are asserted byte-identical to the previously measured executables; `.rdata` differences are verified to occur only in PE debug-directory build timestamps. The maps therefore describe those original code layouts. All 60 differing `.text` bytes lie in **52 instructions**. MSVC dumpbin decoding verifies each changed instruction has the same operation/operand form and references at least one common, exact-target linker symbol in both executables. Examples are shifted `__imp_free` import slots and metadata vtable addresses. This is stronger evidence than comparing raw, pre-relocation COFF sections alone. It does not establish identical referenced runtime data, memory/cache behavior, imported function runtime placement, or wall time.

For the original mixed caller, 30 selected query/verification/main/cleanup function sections also have identical raw code and relocation `(offset, type, target symbol)` triples. Writer functions and all other helper functions are outside that selection. Earlier seven-reader-object raw code equality remains in the preceding evidence. These checks narrow the investigation to linked references/layout and execution conditions; they do not identify a causal fix or justify modifying production alignment/padding.

## Fixed diagnostic protocol

The finite protocol was saved before samples: two dense aligned DOUBLE cases (row and batch), three binary mappings (actual baseline/fixed, baseline/baseline, fixed/fixed), and two launch methods. Each of the **12 cells** runs **96 four-label process quartets**, after two warmups per label. Each child executes three complete verified queries. Both original precision-2 products are byte-identical; every label reads the same fixed-produced file, so this is a same-file reader diagnosis, not writer-product performance.

The `after_create` mode sets affinity immediately after CreateProcess returns. The `before_resume` mode creates the process suspended, sets and checks affinity, then resumes its initial thread. The latter removes the opportunity for child initialization to run before affinity is set. This experiment does not prove that such a race occurred in old runs. Both modes use the same Windows CreateProcess wrapper, redirects, binary arguments, affinity mask 12 and pool size 2. Execution positions are asserted balanced for labels and cells before measurement.

AMD Ryzen 9 9900X, Windows, MSVC 14.50 Release/static and CPython 3.12.14. The recorded topology confirms logical processors 2 and 3 (mask 12) are **SMT siblings on one physical core**. Previous reports correctly named logical CPUs; this is not two-physical-core scaling. The filesystem cache is warm. The interactive host is not an isolated laboratory; background load, clock/power state and cache effects are not controlled hardware-counter measurements.

Each child checks all 65,536 rows × four projected fields, timestamps, types, values and NULL positions. Python independently checks aggregate rows and checksum. The same original, Java-audited input file is used; this round does not add a Java-writer matrix, production coverage run, sanitizer suite or writer benchmark.

Main-thread lifetime cycle count, OS-accounted main-thread/process CPU time and whole child-process wall time are additional diagnostics. They include initialization, printing and exit; they are **not query-only CPU costs**. QueryThreadCycleTime is hardware-dependent and is not retired instruction count or a calibrated clock-frequency estimate. Some short processes have zero OS-accounted CPU time, so any CPU-time contrast containing such samples is unavailable as a whole; no nonzero-only estimate is substituted. The first post-collection analyzer divided by such a zero: its failure log is retained, then analysis was repaired without launching any additional children or replacing any samples. Full-result timing remains the unchanged driver measurement. Confidence intervals resample 12 chronological blocks of eight quartets (10,000 bootstrap draws). All initial, outlier and negative-control samples are retained. No multiplicity-adjusted inference or formal non-inferiority test is claimed.

## Diagnostic results

Ratios are later-label/earlier-label time. For actual A/B mappings this is fixed/baseline; for A/A and F/F both labels execute the very same binary. Brackets are block-bootstrap 95% intervals. A negative-control interval excluding one demonstrates uncertainty in this measurement setup; it cannot be a production source regression.

| Case | Launch affinity | Binary mapping | First label-pair full latency | Second label-pair full latency | End-label full latency | End-label main-thread lifetime cycles |
|---|---|---|---|---|---|---|
| row | `after_create` | `baseline_vs_fixed` | 1.00529 [1.00161, 1.00673] | 1.00741 [1.00293, 1.01123] | 1.00512 [1.00315, 1.00943] | 1.00200 [0.99549, 1.01204] |
| row | `after_create` | `baseline_vs_baseline` | 0.99827 [0.99713, 1.00422] | 0.99969 [0.99681, 1.00584] | 0.99835 [0.99591, 1.00433] | 1.00156 [0.99503, 1.00423] |
| row | `after_create` | `fixed_vs_fixed` | 0.99813 [0.99399, 1.00180] | 1.00045 [0.99637, 1.00390] | 0.99744 [0.99535, 1.00244] | 1.00293 [0.99289, 1.01031] |
| row | `before_resume` | `baseline_vs_fixed` | 1.00537 [1.00276, 1.00948] | 1.00557 [1.00144, 1.01004] | 1.00640 [1.00426, 1.01112] | 1.00580 [0.99949, 1.00915] |
| row | `before_resume` | `baseline_vs_baseline` | 1.00088 [0.99574, 1.00446] | 1.00174 [0.99836, 1.00348] | 1.00121 [0.99788, 1.00257] | 1.00086 [0.99587, 1.00406] |
| row | `before_resume` | `fixed_vs_fixed` | 1.00016 [0.99631, 1.00382] | 1.00150 [0.99805, 1.00323] | 1.00273 [0.99666, 1.00609] | 1.00125 [0.99721, 1.00731] |
| batch | `after_create` | `baseline_vs_fixed` | 1.00792 [1.00448, 1.00955] | 1.00707 [1.00488, 1.01199] | 1.00760 [1.00455, 1.01232] | 0.99745 [0.99413, 1.00562] |
| batch | `after_create` | `baseline_vs_baseline` | 0.99931 [0.99761, 1.00358] | 1.00199 [0.99404, 1.00486] | 0.99939 [0.99707, 1.00401] | 0.99978 [0.99842, 1.00557] |
| batch | `after_create` | `fixed_vs_fixed` | 0.99809 [0.99590, 1.00269] | 1.00064 [0.99866, 1.00423] | 0.99957 [0.99651, 1.00316] | 0.99546 [0.99014, 0.99877] |
| batch | `before_resume` | `baseline_vs_fixed` | 1.00791 [1.00493, 1.01030] | 1.01036 [1.00746, 1.01524] | 1.00982 [1.00554, 1.01220] | 1.00792 [1.00253, 1.01118] |
| batch | `before_resume` | `baseline_vs_baseline` | 1.00329 [0.99924, 1.00567] | 0.99897 [0.99387, 1.00105] | 1.00075 [0.99955, 1.00544] | 1.00440 [1.00192, 1.00556] |
| batch | `before_resume` | `fixed_vs_fixed` | 1.00359 [0.99932, 1.00432] | 1.00073 [0.99901, 1.00362] | 1.00121 [0.99593, 1.00601] | 1.00127 [0.99443, 1.00731] |

Across **24 negative-control latency contrasts**, 0 intervals lie wholly above 1 and 0 wholly below 1. Across 12 actual A/B latency contrasts, 12 lie wholly above 1 and 0 wholly below 1. These are correlated exploratory contrasts, not independent hypothesis tests. The complete CPU-time/cycle and per-query arrays are included in the archive.

In particular, all four actual-A/B **end-label** latency comparisons have confidence intervals wholly above one: row queries increase approximately 0.5–0.6%, and batch queries approximately 0.8–1.0% by block medians. Both post-create and pre-resume affinity modes show this direction, so affinity timing alone does not explain the signal in this round. Same-binary controls must be consulted alongside those comparisons; these diagnostics do not justify dismissing the actual difference as noise. The original opposite-direction factorial measurements are also retained, so stability across sessions remains a limit.

## Disposition and limits

The new evidence narrows the code differences and quantifies same-binary/launch controls. It neither erases the earlier 0.4–0.7% signal nor establishes a specific query-source defect. No speculative production change is made. **The strict query gate stays qualified and uncleared** pending a justified resolution/acceptance criterion; earlier correctness, compatibility, coverage and write-performance evidence retains its original scope. New upstream source submission is not justified by these diagnostics alone.

This is a finite diagnostic experiment rather than repeated sampling until a passing result appears. Further timing should have a stated causal hypothesis and stopping rule. An engineering acceptance margin would require an explicit decision and prospective validation; this report does not silently introduce one. Cold-cache behavior, P99, broad parallel scaling, compressed-query performance and large-corpus generalization remain outside this experiment.

## Reproduction and artifacts

The archive includes the fixed pre-sample plan, all raw diagnostic arrays and execution order, stage analysis/source, code/relocation comparisons, original linked-address maps and dumpbin output, environment/binary integrity checks, the retained original confirmation input, and the same actual DOUBLE input file. It references the previously published full backfill for the pinned static-library builds and earlier correctness/Java/coverage/write results. Build the map helper with CMake Release using the original compiled reader object; its exact-code assertion must pass. Run `analyze_history.py`, `map_differences.py`, `normalize_disassembly.py`, `compare_driver_code.py`, `capture_environment.py`, then `launch_control.py` with CPython on Windows. `launch_control.py --smoke` validates the two launch modes first. Local source/library/tool paths are preserved and need adaptation on another machine; any recompiled driver is a new measurement artifact.

## 中文说明

本轮没有生产代码修改，原有六个查询程序哈希及两个源码目录状态均核对一致。历史复查中的约 0.4%–0.7% 差异主要位于读取/解码、物化校验与关闭阶段，约每次 13–25 微秒；打开文件没有稳定变慢。该分项不是纯 decoder 计时，也不是独立于旧数据的新证据。

通过保持原始 `.text`/`.pdata` 字节一致的旁路链接生成地址映射，确认独立 reader 的 60 个差异字节位于 52 条指令，全部只改变引用地址、仍指向同名符号（如 `__imp_free` 与元数据虚表）。原混合程序选查的 30 个查询/校验/main/清理函数，链接前代码及重定位目标一致。该结果缩小了排查范围，但不能证明缓存、导入函数运行地址和数据布局性能一致，也没有确认根因。

诊断计划在采样前固定：行/批两场景 × 真实前后版本/原版自身/修复版自身三种映射 × 启动后绑核/恢复执行前绑核两种方法，共 12 组，每组 96 轮四标签、每进程三次完整结果核验。总计 4,608 个计时子进程、13,824 次查询；另有各标签两轮预热。位置均衡先断言通过，所有样本保留。同一文件由两版读取，未重复冒充 writer 产物对照；亲和性 12 对应同一物理核的两个 SMT 逻辑处理器。

主线程生命周期周期数/CPU 时间包含初始化、输出和退出，不能替代查询区间 CPU 计时或退休指令数。短进程的部分 OS CPU 计时为零，对应 CPU 时间比较整体标为不可用，不剔除零值再作估计。最初分析在全部采样结束后因此出现除零，失败日志保留；修正后仅重新分析，没有重跑子进程或替换样本。上述表格保留全部同版本负对照与真实比较，置信区间按 12 个连续时间块重采样，未做多重比较校正。24 个同版本延迟比较中 0 个区间完全大于 1、0 个完全小于 1；12 个真实前后版本比较中分别为 12、0 个。不能把同一二进制自身出现的测量差异解释为生产代码退化。

旧的小幅差异及相反方向结果始终保留，**查询性能门槛仍有保留，未标为通过**。本轮辅助诊断不产生新的覆盖率、完整 sanitizer、Java writer 或写入性能结论。进一步测量应围绕可验证的因果假设并设定停止规则；若采用工程允许误差，须明确决定后再预先定义验证标准，不能为得到通过结果事后改变标准。

本轮四项真实前后版本的末标签延迟比较，其置信区间均完全大于 1：行模式区块中位数约慢 0.5%–0.6%，批模式约慢 0.8%–1.0%；两种绑核方法均存在。因此，启动绑核时机不能单独解释这批样本，不能把差异直接归为噪声。旧的反向控制结果也继续保留，不因此声称所有轮次稳定一致。

**AI disclosure:** The implementation, tests and description in this pull request were written by an AI coding agent (OpenAI Codex), which also performed the reported local validation.

**AI 使用说明：** 本 PR 的代码修改、测试和正文由 AI 编程代理（OpenAI Codex）编写，文中报告的本地验证也由该 AI 代理执行。
