# PR #1024: calibrated event-address diagnostic

**Publication update:** Complete original evidence is now public as9 fixed parts, downloaded and reassembled to the original SHA-256. Single-file API upload remains unavailable; browser extension file access is no longer required. [Parts and SHA-checking reassembly script](https://github.com/jixuan1989/tsfile-apache/tree/7a8abd77296d4296b274f39f95b01b0b2c4c6a16/issue-evidence/ts2diff-writer-precision/validation/query-event-address/complete-evidence-parts). Analysis/gates are unchanged.

**公开状态更新：** 原完整证据已按9片公开，下载重组后与原ZIP的SHA-256一致；单文件API上传仍失败，但无需浏览器文件权限。分析结果及未通过的查询门槛不变。


**Query-performance gate: UNCLEARED. Necessity of the query slowdown: NOT PROVEN.** This is a completed new event-address capture, distinct from the earlier completed switch-counter recording. It identifies a narrower observational hotspot, not a repair or proof of a necessary performance trade-off. Production head remains `75592b89d1523a96090e8bca1dcb4cd2180162e5`.

## Completed collection and integrity

Captured `capture-20261018-145427`, with32 measured original-program children ×256 fully consumed and checked dense aligned DOUBLE precision2 four-field batch queries: **8,192 verified queries**. Excluded192 warmup and12 preflight queries;16 separate calibration children in four position-rotated rounds. Original executable/source/fixture hashes match the frozen plan. Baseline/fixed writer products for this case are byte-identical. All32 native outputs match65,536 rows/query,4 fields, no NULLs and the independently recomputed checksum `70368140197888` per256 queries.

WPR saved/stopped its unique owned instance successfully. The ETL stays local:225,443,840 bytes, SHA-256 `66cbaf0cf8514286776f014dc69de6205c3682caec1a7927dbbd69e77f136826`. Native ProcessTrace returned0; no reported lost events/buffers, malformed PMC payloads or callback errors. Trace confirms source9 interval16,384 and source25 interval4,194,304. There are **160,111 target PMC address samples**:25,289 source9 and134,822 source25.159,491 samples have same-timestamp target stacks (99.6128%);620 do not. There are zero multi-sample timestamp keys. All matched stacks have the expected PID and all samples/stacks fit a unique main-TID plus child-time window; two main TIDs are reused across the48 children.

The reader's raw thread-start summary is51, versus48 ends/children. Its start counter tests membership without the exact child window and must **not** be presented as51 distinct target main threads or as a validated lifecycle balance. Sample/stack association is independently checked against each child's recorded PID/TID and QPC interval. No context-switch counter or periodic CPU profile was requested: no sibling-busy or query CPU-cycle result is claimed.

## Calibration observations

Only native computation-body QPC windows are counted below; startup, initialization, reference calculation and output are excluded. Each code mode performs the same verified xorshift/multiply arithmetic across134,217,728 steps; loop selection differs.256 independently linked code functions span461,040 bytes; same-code folding is disabled only for this private calibration target. Data modes traverse4KiB/64MiB random single-cycle lists for16,777,216 steps. All checksums match. Local topology reports32KiB L1I/48KiB L1D.

| Mode | Source9 body samples, four rounds | Source25 body samples, four rounds |
|---|---|---|
| code_hot | [2, 1, 2, 2] | [132, 132, 132, 132] |
| code_stream | [69, 70, 72, 69] | [133, 133, 133, 133] |
| data_hot | [1, 1, 1, 0] | [28, 29, 29, 28] |
| data_stream | [10, 8, 11, 8] | [32, 29, 31, 30] |

The streaming-code mode produces more source9 events than the hot-code mode in all four rounds, while source25 counts stay close. This supports using the requested source for a **directional code-locality diagnostic**. Long data traversal also accumulates source9 samples; calibration is not an independent proof of a specific AMD event encoding, cache level or exact instruction-miss count. Do not label it a calibrated L1I counter.

## Paired diagnostic results

Four labels include two copies of each original executable. They rotate over four common executable identities and occupy each execution position twice in8 rounds. Parent mask16, child mask12 before resume; mask12 selects two SMT threads on one physical core. Pool2, parallel=false, warm filesystem.8 descriptive round ratios, **not new performance acceptance intervals**; no extra rounds or rejection of adverse samples.

| Metric | Median F/B change | Range of8 round changes |
|---|---:|---:|
| Source9, whole target main-thread samples | +6.7769% | -1.3132% to +16.1873% |
| Source25, whole target main-thread samples | -0.0122% | -0.1458% to +0.1339% |
| Source9/Source25 ratio | +6.7443% | -1.1929% to +16.1732% |
| Source9, query-frame-associated samples | +7.3122% | -1.7519% to +17.6303% |
| Source25, query-frame-associated samples | -0.0305% | -0.1466% to +0.3302% |
| Native full-query time under sampling | +1.8501% | +0.8602% to +5.0515% |

Query-frame membership means the sampled address or a same-timestamp stack contains the exact PE runtime range of `read_fixture`; it includes setup, decoding, inlined verification and cleanup. It is not an exact per-query QPC interval. The caller itself receives about39% of source25 query-frame samples; inlined verification and other caller work cannot be separated with public MAP symbols. Nearest public symbol names are descriptive, not PDB line/inline attribution. Sidecar `.text` and `.pdata` exactly match each original measured executable.

Within-version copy2/copy1 negative controls:

| Version | Metric | Median change | Range of8 changes |
|---|---|---:|---:|
| baseline | source9 | -0.4000% | -3.0708% to +8.0601% |
| baseline | source25 | -0.0608% | -0.1459% to +0.1219% |
| baseline | native_full_query_sum | +0.0771% | -2.7167% to +0.8711% |
| fixed | source9 | +2.3733% | -16.1905% to +13.1043% |
| fixed | source25 | +0.0487% | -0.2915% to +0.2190% |
| fixed | native_full_query_sum | +0.2186% | -4.0933% to +6.4758% |

The sampled +1.8501% native latency is **not** a replacement for the earlier unsampled acceptance evidence: administrator execution, active sampling and256 in-process queries differ. Its wide per-round and same-binary control spreads remain visible. Sampling perturbation was not measured with a matched no-sampling run here. Memory, cold-cache behavior, quantile non-inferiority and query-only cycles remain unmeasured in this diagnostic. The original32-case matrix,7 independent confirmations and three residual scenarios are retained.

## Narrower hotspot, not causality

The largest absolute source9 query-associated leaf-count increase is inside the actual runtime function range of **`common::ByteStream::read_buf`**:346→540 samples, +194. Baseline per-round counts `[45,46,37,52,42,44,40,40]`; fixed `[77,82,59,65,54,75,65,63]`. All eight fixed counts are larger. Stacks include TS2DIFF headers/batch decoding, page statistics/chunk headers and metadata reads, so this is not exclusively the value-decoding stage or verifier.

This function is **299 bytes in both original COFF objects**, with identical SHA-256 `c7187b279c96e594750ba8b6a8f06c3f588bdcc3f61fe89e61a12a9f8997b10c` and identical relocation triples (one memcpy call). Its selected COMDAT comes from page_writer.obj in both builds. Baseline startRVA `0x25f30` (mod64=48), fixed `0x263c0` (mod64=0). Changed placement with identical code is a concrete investigation lead, **not proof** that that alignment/cache mapping caused the slowdown. No linker/source/layout intervention was run in this follow-up.

Source9 kernel leaves are5,093/5,206 query-frame-associated samples; ntdll leaves2,031/2,122. The event excess is distributed across library/runtime/kernel paths; `read_buf` does not explain all extra events or measured latency. Hardware sample IPs may skid. Source25 sampling is periodic and function sample shares are not exact instruction counts. Do not infer extra required work, exact miss penalties or unavoidable cost from these samples.

## Decision and next step

The new administrator action is fulfilled; do not request another execution of either completed capture script. Keep the original query gate uncleared and the prominent top-of-PR warning. A compatibility fix is required, but this does not prove its query slowdown necessary under the human-approved exception. No production source changed, so previous correctness/bidirectional Java/changed-line/module/branch coverage/write evidence retains its original scope; no fresh production suite, coverage or throughput result is claimed.

Use the saved per-IP read_buf samples and caller contexts to design one bounded observational/direct-call comparison with same-image controls before any source remedy. Do not blindly vary padding, linker order or arithmetic, extend rounds seeking a pass, or repeat the full acceptance matrix without a new tested causal hypothesis. Any adopted source change still requires affected correctness, bidirectional Java, coverage, write and query validation before push.

The ZIP contains every target sample normalized to module/RVA, all native workload outputs, calibration counts, per-round ratios and copy controls, static audit, sources and a standalone verifier. It excludes the system-wide ETL, absolute runtime addresses and unrelated process/thread payloads. Run `python verify_public.py` after extraction to recompute counts, checksums, query membership, calibration counts, pairing and controls; local-only ETL reprocessing additionally requires the captured ETL and original build sidecars.

## 中文说明

新的管理员采集已成功保存并停止：32个正式进程、8192次查询全部完整核对，192次预热和12次预检另计，另有16个校准进程。取得160111个目标事件地址样本，159491个能匹配同时间戳栈；未报告事件/缓冲区丢失或畸形负载。TID实际复用两次，按目标PID/TID与时间窗核对。原解析器的启动汇总51没有按时间窗筛选，不能冒充48个主线程生命周期平衡；样本关联另行逐条验证。系统ETL和绝对运行地址仅留本地。

代码流式校准的源9事件明显高于热点校准，源25接近，支持继续观察代码局部性；这不证明微架构事件编码或精确L1I语义。8轮配对中位数：源9约+6.78%，源25约−0.01%；含查询调用栈的源9约+7.31%，源25约−0.03%。采样下完整查询约+1.85%，但条件不同、负对照波动及采样开销未测，不能替代原验收结果。

新线索是ByteStream::read_buf范围内的源9样本346→540，8轮均增加，是本轮最大叶节点增量。函数在两版均为299字节，原COFF机器码及重定位完全相同，链接位置不同；调用栈横跨解码、页头/统计和元数据读取。内核/运行库也有明显样本，不能把全部退化归因于此函数或缓存对齐，更不能据此宣称是必要代价。未改源码、未进行新的布局干预、未重跑矩阵寻找通过样本。

用户这次环境操作已经完成，无需再运行采集。下一步利用已有地址/调用栈准备有停止规则、含同二进制对照的针对性观察，先验证原因再提源码方案。查询门槛仍未通过，PR顶部警示继续保留；既有Java互通、覆盖率和写入证据保留原范围，不冒充本轮重测。第4条issue仍待单独批准。

References: [Microsoft PMU collection](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/recording-pmu-events), [Microsoft WPR examples](https://devblogs.microsoft.com/performance-diagnostics/recording-hardware-performance-pmu-events-with-complete-examples/), [Microsoft PerfView event definitions](https://raw.githubusercontent.com/microsoft/perfview/main/src/TraceEvent/Parsers/KernelTraceEventParser.cs), [AMD hardware sampling/skid](https://docs.amd.com/r/en-US/68658-uProf-getting-started-guide/Hardware-Counters). The source-list file records conflicting interval-unit wording on an element reference page; this capture validates actual configured interval metadata rather than deriving elapsed time from the interval.

**AI disclosure:** The implementation, tests and description in this pull request were written by an AI coding agent (OpenAI Codex), which also performed the reported local validation.

**AI 使用说明：** 本 PR 的代码修改、测试和正文由 AI 编程代理（OpenAI Codex）编写，文中报告的本地验证也由该 AI 代理执行。
