# PR #1026 aligned batch follow-up validation

> **NOT READY TO PUSH — performance regressions remain unexplained; complete sanitizer suite is not clean; changed-line coverage is89.47%.**

> **暂不推送：仍有未解释的查询退化；完整 sanitizer 未通过；修改行覆盖率为89.47%。**

Public maintainer source: `11bfc35c99f8e845939a6753f004ecee38c7a2ec`. Local AI-authored candidate: `55db175d6c999ceab731955b3697a467a3a9a587`. Baseline: `6f4a971eefffcc81cf62a75b6ad8bc91460b0fa6`. The candidate has not been pushed to the PR.

## Confirmed defects and local fixes

- The maintainer fixed the earlier f5 lazy-page continuation crash and NaN EQ/NE statistics pruning. Standalone final controls return300/300 large-page rows,4/6 EQ rows and2/6 NE rows. Earlier failed source/logs are retained separately.
- On public11b, NOT implemented by reversing ordered floating operators loses IEEE NaN truth. With NaN values,32 operator/literal combinations omit NaN rows;8 with NaN literal incorrectly return empty instead of all32 nonNULL rows. All3 writer products reproduce40 exact mismatches with normal exit0. The candidate complements the original comparison only for nonNULL values, retains finite statistics pruning, handles doubleNOT and conservatively evaluates NaN statistics/literals.
- Incomplete OR could prove FULL_PASS before evaluation rejected its missing child. Candidate validates the complete tree before task iteration/statistics, so malformed predicates returnE_INVALID_ARG even for empty time windows.14 added configurations fail against pristine11b and pass after repair.
- AlignedChunkReader is placement-allocated and manually destroyed. Its new vector owners were not released by destroy():pristine11b focused functional tests pass but LSan exits1 with16152bytes/2019allocations. Candidate releases both mask owners in destroy(). Focused207 and expandedreader369 now exit0 underASan+UBSan+LSan.
- Lazy decoding already computed the page selection; clearing its validity afterwards caused a second evaluation. Candidate invalidates before decode, retains the produced mask and skips an empty mask without reevaluation.

## Actual verification

- Windows Release: 1112 passed,3 skipped,10 disabled;focused207 passed. MSVC14.50,x64,static,threads/memstatON,SIMD/codecsOFF.
- Linux GCC11 Debug,O0,atomicgcov,all6codecsON:207 focused and369 reader tests pass with leak detection. Full and separately filtered remainder stop on the same pinnedLZOkay undefined behavior;this is not a clean full-suite claim.
-1896 positive complete-file queries:1800 FLOAT/DOUBLE comparisons plus96 NULL/BOOLEAN/time/OFFSET/LIMIT queries. Java,oldC++ and localC++ products read by Java public projected query+application predicate,oldlegacyC++,locallegacyC++,and localstructured row/batch APIs. The deterministic complete expected sequence checks row count/order,timestamps,all defined fixture values,NULL,signedzero andNaN class;NaN payload bits are not checked.
- Both C++ writer products are byteidentical for NULL and floating fixtures. Java full-file equality is not claimed. PLAIN/UNCOMPRESSED is the measured compatibility scope;not a new universal encoding/compression compatibility pass. Initial Java fixture omitted the global UNCOMPRESSED time compressor and failed on both codec-disabled Windows readers;initial failed evidence retained. Two independently found oracle weaknesses were corrected before final rerun.
- Local11b→55db repair-diff production lines68/76=89.47%,branches130/189=68.78%;selected affected reader/file modules3923/4938=79.45%,branches3461/6298=54.95%. All counters and uncoveredlines retained;this is not whole-library coverage. A real directTsBlock evaluator path still needs a regression,besides defensive/unreachable paths.

## Query performance: failed

Frozen60case protocol:42 structured,10 equivalent legacycallback controls,and retained8 noFIELD queries.12 paired independent processblocks;exactly one24block confirmation when predeclared signals trigger;3neutralimagecopies and6 processorders;warm filesystemcache,suspendedchild verifiedaffinity4,parent16;no builds/sanitizerjobs during timing. Every result is completely consumed and checked. Structured/callback driver3 queries/process;retainednoFIELD driver8. Phase distributions correlate within each process.

3378 successful processes. Complete query counts by phase: `{"warmup": 1320, "initial": 7920, "confirmation_warmup": 258, "confirmation": 3096}`. This contains all initial,confirmation and warmup samples;no outliers discarded and no extra rounds to obtain a pass.

| Case | Comparison | Confirmed median latency change | Bootstrap95% interval |
|---|---|---:|---|
|dense-w4-p100-b0|fixed/prior|+2.563%|+1.724% to +3.016%|
|callback-w1-p1-b0|fixed/prior|+2.207%|+1.626% to +3.144%|
|callback-w1-p1-b0|fixed/base|+4.710%|+3.853% to +5.610%|
|callback-w1-p1-b1024|fixed/prior|+2.402%|+1.174% to +3.569%|
|callback-w1-p1-b1024|fixed/base|+5.050%|+3.667% to +5.542%|
|callback-w1-p100-b0|fixed/base|+0.750%|+0.097% to +1.507%|
|callback-w1-p100-b1024|fixed/prior|+1.284%|+0.850% to +1.941%|
|callback-w1-p100-b1024|fixed/base|+3.237%|+1.296% to +4.472%|
|callback-w8-p1-b0|fixed/prior|+0.986%|+0.182% to +2.826%|
|callback-w8-p1-b0|fixed/base|+1.104%|+0.345% to +2.281%|
|callback-w8-p100-b1024|fixed/prior|+0.928%|+0.117% to +1.486%|
|callback-w8-p100-b1024|fixed/base|+0.642%|+0.065% to +1.952%|
|callback-null-b0|fixed/prior|+1.813%|+1.114% to +2.294%|
|callback-null-b0|fixed/base|+1.365%|+0.527% to +2.393%|
|callback-null-b1024|fixed/prior|+1.733%|+0.953% to +2.889%|
|callback-null-b1024|fixed/base|+1.018%|+0.206% to +2.387%|
|unfiltered-offset-b1024|fixed/prior|+1.107%|+0.020% to +2.142%|
|unfiltered-offset-b1024|fixed/base|+1.569%|+0.748% to +2.542%|

Most structured cases are materially faster than the oldcallback reference,but that reference also materializes/verifies an extra bucket output while native paths load it as hiddenfiltercolumn. Such ratios include reduced materialization and are not isolatedengine speedups. Prior11b/native vs local55db/native has the same physical projection;legacy controls have the same callback projection across all3versions. Confirmed increases above remain unexplained;necessary-cost exception is not invoked. No-confirmed-increase is not proof of equivalence.

Metrics: filehandleopen,queryplan(includesmetadata),first returned row,fullquery includingteardown,rows/s,P50/P95,wholeprocesspeakworkingset for newdriver. OldnoFIELD driver reports totalonly;no missing phase/memory claims. No coldcache,P99,compressedquery,broadnonaligned FIELD or parallel scaling claims. Writer throughput not retimed for this reader-only delta;bothbaseline/fixed C++ products read and bytecompared.

## 中文说明

维护者11b已修复此前大页续读崩溃和NaN等于/不等于统计裁剪；本轮仍复现浮点否定、畸形OR及掩码资源泄漏。NOT不能简单把浮点<反转为>=，因为NaN参与时两者都为false；局部修订保留原运算并仅对非NULL取反，同时保持保守统计裁剪。畸形树在扫描前统一返回E_INVALID_ARG；手动destroy显式释放新增拥有的vector；延迟解码生成的掩码不再重复计算。

本地Windows全量1112通过、3跳过、10禁用；Linux全压缩依赖的207专项和369reader检查在ASan/UBSan/LSan下均正常退出。全量仍在字节相同的固定LZOkay依赖中遇到未对齐读取，未添加suppression，不能称全量sanitizer通过。

修正两项独立审阅发现的验证脚本缺口后，1800次浮点和96次NULL相关完整文件查询全部与独立完整期望一致；Java和C++分别写文件并交叉读，明确区分Java应用层谓词和C++原生结构化谓词。检查NaN类别、无穷、负零、全部定义的有限值、NULL、完整行数与顺序，不宣称NaN payload一致。当前双向互通范围为PLAIN/UNCOMPRESSED，未替换原编码压缩矩阵结论。本地11b→55db修补差异的修改行89.47%、修改分支68.78%；所选模块行79.45%、分支54.95%，不冒称全库覆盖。

60场景查询计时及预定的一次性复核已结束，共3378个成功进程；所有返回结果完整消费并核对，原始异常波动和全部样本保留。上表是确认退化：结构化dense-w4-p100-row相对11b约+2.56%，窄投影低命中旧回调相对6f约+5%，其它确认项亦不掩盖。必要性尚未证明，未使用允许必要代价的例外，查询门槛未通过；更快的其它结构化场景不能冲销旧回调或无FIELD退化。旧参考额外输出bucket，收益含物化减少；不能全部归因于批量算法。

下一步仅处理经源码审阅确认的无用掩码分配及真实TsBlock evaluator测试缺口。无结构化过滤时的分配并不处于所有legacy回调路径中，因此不能据此解释约5%回退。新候选必须单独冻结并验证，不延长本候选跑分、不盲调布局。源分支尚未推送，不主动请求Copilot或合并上游。

**AI disclosure:** Local repairs, validation drivers and this report were written by OpenAI Codex; the public11b batch changes were authored by the maintainer. Reported runs were performed locally by Codex.

**AI 使用说明：** 本地修订、验证程序和本报告由OpenAI Codex编写并执行；公开11b批量实现由维护者编写。
