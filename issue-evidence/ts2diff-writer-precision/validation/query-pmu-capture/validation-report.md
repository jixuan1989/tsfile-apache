# PR #1024: captured hardware-counter diagnosis

Source head: `75592b89d1523a96090e8bca1dcb4cd2180162e5`. **The query-performance gate remains uncleared.** Production source is clean and unchanged. This report supersedes the earlier pending administrator-capture status, without replacing any earlier measurements.

## Capture and result integrity

The completed capture is `capture-20261018-104907`: 8 position-balanced rounds, four labels (two copies each of the exact original baseline/fixed mixed binaries), 1024 fully consumed and checked queries per child: **32 measured children, 32768 queries**. Its 64 warmup children (192 queries) and four preflight children (12 queries) are excluded. An earlier capture `capture-20261018-104843` has four measured children but no completion marker; it remains local and is excluded, not silently combined or replaced.

The scenario is dense aligned DOUBLE, TS_2DIFF precision2, two devices ×32768 rows, four projected fields, batch consumption, pool2, parallel=false. Both writer products are byte identical. Native verification checks values, timestamps, ordering, types, NULLs and checksums. All native outputs and timings are retained. Original image and fixture SHA-256 values are checked before analysis. The previous Java audit remains applicable to the unchanged fixture; no new Java, source-coverage, unit-suite, sanitizer or write-throughput run is claimed.

The system ETL is **local only**, 293601280 bytes, SHA-256 `5b85ce18fcb774792ca4b8927a263b7196c3d7c6018e558db8f168b252b8a17a`. Stop succeeded; no WPR session remains active. `ProcessTrace` succeeded: 2855423 total events, 1985359 PMC-bearing switches, **zero reported lost events/buffers**, no invalid target intervals and no CPU2/3 switch-chain errors. PID plus time-window filtering gives exactly32 target-main-thread starts/ends,510 closed valid counter intervals,88135 CPU samples and93109 stack records. A previous derivative counted reused warmup thread IDs outside target windows; the final v4 reader explicitly checks PID and time. No workload was rerun to fix the analysis. Two stack records may belong to one sample (kernel/user stacks); stacks join by thread and event timestamp, not arrival order. [Microsoft StackWalk event format](https://learn.microsoft.com/en-us/windows/win32/etw/stackwalk-event).

Counter order is read from the trace's `PerfInfo/PmcCtrConfig`, **not the requested XML order**: `BranchMispredictions, DcacheMisses, IcacheMisses, InstructionRetired, TotalCycles`. Source IDs are11,8,9,25,19. The24 CPU status records each carry five raw64-bit values, all0; these opaque raw statuses are preserved rather than assigned undocumented semantics. `DcacheMisses` is zero throughout the target records and is **unusable/uninterpretable**. It does not demonstrate an absence of data-cache misses. Nonzero monotonic counters are plausible, but HAL event semantics have not been independently calibrated on this Ryzen9 9900X. [Microsoft PMU recording documentation](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/recording-pmu-events).

## Descriptive paired results

Each round sums its two fixed counts and divides by its two baseline counts; CPI uses each version's summed cycles/instructions. The table reports the median of8 ratios and the full observed round range. It is not an acceptance confidence interval. Counts cover **scheduled main-thread intervals**, including startup, kernel/interrupt work, queries, printing and teardown; exact per-query QPC boundaries are not instrumented. Elevated execution, active WPR and1024 in-process queries differ from the original three-query acceptance protocol.

| Metric | Median fixed/baseline change | Full eight-round range |
|---|---:|---:|
| InstructionRetired | +0.0171% | -0.1318% to +0.0747% |
| TotalCycles | +1.2106% | +0.7273% to +2.5838% |
| CPI | +1.2002% | +0.7072% to +2.5072% |
| IcacheMisses | +9.1903% | -2.0976% to +17.3680% |
| BranchMispredictions | -1.1713% | -2.7558% to +1.5496% |
| native_full_query_time | +0.8800% | -0.2299% to +3.1824% |
| DcacheMisses | unavailable: all zero | unavailable |

The approximately unchanged retired instruction count, higher cycles/CPI and higher reported instruction-cache event count support investigating instruction locality/front-end effects. They **do not establish causality** or identify which instruction caused a miss. Eight rounds cover only two complete image/order cycles. All raw samples and contrary rounds remain retained.

Within-version negative controls compare copy2/copy1 of the same payload, also without trimming:

| Version | Metric | Median change | Full range |
|---|---|---:|---:|
| baseline | TotalCycles | +0.4668% | -1.4341% to +2.6760% |
| baseline | IcacheMisses | -5.0800% | -14.3853% to +5.2925% |
| baseline | native_full_query_time | +0.6441% | -1.5921% to +3.7746% |
| fixed | TotalCycles | -0.4959% | -1.2635% to +2.1484% |
| fixed | IcacheMisses | +1.4824% | -4.3008% to +9.9517% |
| fixed | native_full_query_time | -0.4667% | -2.2811% to +2.3075% |

Those control spreads are material, particularly for instruction-cache events, and limit causal strength. Affinity12 permits logical CPUs2 and3, SMT siblings on **one physical core**. Median scheduled sibling non-idle exposure is1.6968% baseline and1.4964% fixed; the fixed run does not have more median measured sibling contention. CPU2 residency medians are39.61%/58.94%. This does not control IRQ/DPC, other-core shared-cache traffic, frequency, power or the complete host workload.

## Sample attribution and a rejected source candidate

Query-call frames occur in43689/43808 baseline and44225/44327 fixed CPU samples (87914/88135 combined). Nearest-public-symbol leaf shares within query-frame samples put `multi_DECODE_TV_BATCH` at6.716% baseline and8.075% fixed. Symbols come from public linker maps and PE ranges, not full PDB line/inline attribution. The function's **5608 COFF code bytes and every relocation (offset,type,target-symbol) tuple are identical** in the original baseline/fixed objects. This is an attribution lead, not evidence of an added reader operation.

A private source candidate moved the property-aware encoder factory from its inline header into a compiled translation unit, aiming to reduce writer-initialization code footprint. It was built beside an unchanged control from the same source path and options. The matched control reproduces the original fixed `.text` and `.pdata` bytes exactly; `.rdata` differs and is not claimed identical. Candidate `.text` grows from651603 to653443 virtual bytes (**+1840**) and `.rdata` from133750 to134678 (**+928**). The intended footprint reduction failed. The candidate was **rejected at this screen**: no timing search, production change, source push, compatibility/coverage claim or full quality-gate run. Its diff and binary section/hash records remain in the archive, so this failed attempt is visible.

The original32-case matrix and7 independent confirmations still leave dense DOUBLE row (+1.06%), dense DOUBLE batch (+1.27%) and sparse DOUBLE batch (+0.45%) end-to-end residuals under their original protocol. This one-case diagnostic neither replaces those results nor fills controlled cold-cache/P99/native FIELD/all-NULL/general-parallel and other declared scope gaps. Next work must form a maintainable source-level/code-generation hypothesis before further timing; no linker-order/padding search or repeated full matrix to obtain a pass.

## Reanalysis and privacy

Extract the evidence ZIP and run `python verify_public_pmu.py`. It recomputes the510 target interval totals,32 child result checks and paired medians/ranges from public normalized events and native outputs. The public archive includes all88135 samples and93109 stacks with target module/RVA locations; kernel/unresolved addresses and unrelated switch thread identities are removed. Original absolute addresses and the system-wide ETL stay local. Analyzer/reader/capture sources are supplied for audit; exported source-path roots are redacted and require local configuration before recollecting. No ETL file is packaged.

## 中文说明

管理员录制已成功完成，32768次查询全部完整核对；预热192次和预检12次另计。另一次只有4个测量进程、缺少完成标记的录制被保留并排除。ETL停止成功，当前没有WPR录制。系统ETL只保存在本地，公开包仅含目标进程过滤、模块/RVA标准化的数据及所有原始查询输出。

最终解析无报告的事件/缓冲区丢失、无无效目标区间和CPU切换链错误；32个目标主线程、510个完整计数区间、88135个CPU样本、93109个栈记录。修正了暖机线程ID复用导致的派生计数错误，未重跑测量。计数器顺序取自trace配置事件，不能沿用XML顺序。数据缓存计数全为0，不可解释，不能据此说没有缓存未命中；CPU硬件事件语义尚未独立校准。

8轮配对中位数：退休指令+0.0171%，周期+1.2106%，CPI+1.2002%，指令缓存事件+9.1903%，分支误预测−1.1713%，本地完整查询耗时+0.8800%。这是包含初始化/内核/输出/退出的主线程计数，不是精确query-only计数；仅8轮、两次完整身份/顺序周期，负对照波动也明显，不能作为原验收协议的通过结果或缓存因果证明。亲和性12为同一物理核两个SMT线程；修复版并无更多中位同核兄弟线程运行暴露，但IRQ/DPC、其他核共享缓存和功耗频率仍未控制。

批量对齐解码样本占比约6.716%/8.075%，其5608字节机器码与全部重定位目标完全一致。为降低写入初始化代码体积，尝试把带属性的encoder工厂移到独立编译单元，结果`.text`反增1840字节、`.rdata`反增928字节，已在体积筛查阶段放弃；没有继续挑选计时、没有推送生产源码，也没有宣称它完成兼容性/覆盖率/性能验证。失败候选的diff、哈希和区段数据均公开保留。

原完整矩阵的三项残留退化及历史相反结果全部保留，查询门槛仍未通过。现有正确性、Java双向兼容、覆盖率和写入证据沿用原范围，本轮未冒充重新验证；冷缓存、P99等既有缺口不变。后续针对可维护的源码/代码生成原因继续定位，不用padding、链接排列或反复跑分清除门槛。

**AI disclosure:** The implementation, tests and description in this pull request were written by an AI coding agent (OpenAI Codex), which also performed the reported local validation.

**AI 使用说明：** 本 PR 的代码修改、测试和正文由 AI 编程代理（OpenAI Codex）编写，文中报告的本地验证也由该 AI 代理执行。
