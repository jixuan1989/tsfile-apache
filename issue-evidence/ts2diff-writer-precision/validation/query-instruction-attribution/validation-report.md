# PR #1024: limits of the read_buf hotspot attribution

**The original query-performance gate remains uncleared. No necessary-cost or cache-alignment cause has been established.** This is an offline partition of the existing original-image event capture, not another acceptance run or a new production candidate.

## Original-image observations

All 160,111 target samples were consumed. The 32 measured children still represent 8,192 fully consumed/checked queries, with the original 192 warmup queries and 16 calibration children separate. Both original executable hashes match the capture. No queries or administrator captures were launched for this analysis.

MSVC disassembly of the two original read_buf functions covers all 299 bytes; all attributed read_buf sample IPs fall on decoded instruction starts. Original COFF code and relocation targets are equal. The largest single instruction-address increase is at offset234, `add dword ptr [r14],edi`, immediately after the memcpy call: source9 104→155, source25 495→524. PMU IP skid means these are **not 51 proven misses caused by that add instruction or memcpy**. That address accounts for 51/194 of the function's extra source9 observations; the rest are distributed across other instructions.

Query-frame source9 samples total 11,186→11,991 (+805). read_buf contributes 346→540 (+194), or 24.10% of that raw sample-count difference. This percentage is not a fraction of latency or an estimate of attainable speedup.

Caller grouping below uses the nearest public MAP stack frames, including up to three executable callers; it is heuristic and may omit inline frames. It is not an exact query-phase boundary or dynamic invocation count. Source25 means sampled retired-instruction events, not time or CPI.

| Caller group | source9 baseline | source9 fixed | source25 baseline | source25 fixed |
| --- | ---: | ---: | ---: | ---: |
| ts2diff_value_or_time_decode | 102 | 220 | 613 | 625 |
| page_header_or_statistics | 121 | 205 | 632 | 739 |
| chunk_header | 35 | 43 | 14 | 19 |
| floating_precision_page_header | 22 | 25 | 168 | 166 |
| metadata_or_other_caller | 66 | 47 | 72 | 79 |

The increase is spread through existing TS2DIFF decoding and page-header/statistics paths. The floating-precision page-header group is only 22→25 source9 samples. The current PR does not change byte_stream.h, ts2diff_decoder.h or ts2diff_wire_format.h relative to its recorded upstream base. These observations do not support attributing the overall slowdown to added precision arithmetic.

Both CPU2 and CPU3 show higher descriptive read_buf source9/source25 ratios: fixed/baseline 1.4398 and 1.4338 respectively. Query-frame ratios on those CPUs are 1.0821 and 1.0513. The signal is therefore visible within both observed CPU partitions, rather than appearing only after pooling unequal CPU sample shares. Conditioning on CPU is observational and cannot isolate scheduling/SMT or sampling bias. The sparse stream contains 105 sample-to-sample CPU changes over 32 measured children; these are **not context-switch counts** and do not measure migration cost. Mask12 contains two SMT logical processors on one physical core.

## Stopped private probe, retained separately

The prior private direct-call probe selected the same 299-byte COFF body but changed the caller/data/link context; both probe functions had the same static RVA. Its predeclared 32-quartet whole-query guard completed 384 fully checked measured queries and 768 excluded warmups. The fixed/baseline chronological block-median change was +0.5347%, bootstrap95% [-0.1736%,+1.8029%]. Same-binary controls also shifted. Since the guard did not retain an upward signal, the direct-call timings were **not executed**, no rounds were added and no layout variant was selected. This neither clears the original regression nor establishes that equal placement fixes it.

## Reproducibility and remaining limits

The separate offline verifier replays all 160,111 samples, checks child QPC windows, independently reconstructs query-frame membership, recomputes per-CPU/per-instruction/per-round counts and checks caller-count conservation. Exact caller classification remains a MAP heuristic. All original observations and negative controls are retained. The machine-readable attribution-summary.json accompanies this report. Local analyzer, verifier, original disassembly and complete arrays remain in work/query-backfill/instruction-attribution.

The full normalized event ZIP is still **unpublished**, with SHA-256 `80b7373e253d0a0572d3cc5293d3a6c7938c7849a70a72b61abade68d36b9421`; earlier network uploads failed and the optional browser file-access permission remains pending. System ETL and absolute runtime addresses stay local. This small report/summary does not constitute publication of all raw samples. No new production correctness/Java/coverage/write/full-query acceptance is claimed; earlier results retain their original scope.

## 中文说明

**原查询性能门槛仍未通过，尚未证明必要代价或缓存对齐因果。** 本轮只离线细分原图像已有的160111个目标样本，没有运行新查询或管理员采集。两个原始可执行文件SHA与采集一致；反汇编覆盖read_buf全部299字节，所有相关采样IP均落在指令起始位置。

最大单地址增量位于memcpy返回后的offset234（`add dword ptr [r14],edi`），源9为104→155、源25为495→524。但采样IP会偏移，不能认定新增51个样本由该add或memcpy引起。查询调用帧中源9总计11186→11991，read_buf的194个增量仅占805个总增量的24.10%，不是查询耗时占比或可优化幅度。上表按最多三个可见公共MAP调用者粗分；解码和页头/统计均有增量，浮点精度页头仅22→25。该PR相对记录基线未修改byte_stream.h、ts2diff_decoder.h及ts2diff_wire_format.h，不能据此归因于新增精度运算。

CPU2/CPU3各自的read_buf源9/源25描述性比值均上升，fixed/baseline分别1.4398和1.4338；查询帧对应比值1.0821和1.0513。因此信号不是仅在混合不同CPU样本份额后出现，但按CPU分组仍不能隔离调度、SMT或采样偏差。稀疏样本间观察到105次CPU编号变化，不是上下文切换计数，也没有测迁移开销；mask12是同一物理核的两个SMT逻辑处理器。

此前私有探针虽然选中了相同299字节函数，但整体上下文改变。固定32轮/384次正式查询与768次预热后，区块中位数+0.5347%、bootstrap95%[-0.1736%,+1.8029%]，且同二进制对照也偏移；按事先规则停止，未运行直接调用计时、未追加轮数或换布局。不能凭探针区间跨1清除原退化，也不能证明相同位置解决问题。

离线复核重新检查全部样本时间窗、查询帧、CPU/指令/轮次计数及调用者计数守恒。完整标准化ZIP仍未公开（SHA见上），小报告及summary不是完整原始样本包；系统ETL和运行时绝对地址仅保留本地。本轮没有生产修改，没有新增Java互通、覆盖率、写入或完整查询验收的通过声明。原验收信号、全部异常/相反样本和未测范围均保留。
