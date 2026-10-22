# Local allocation follow-up — NOT READY TO PUSH

> **Query regressions remain unexplained. The source branch has not been pushed.**

> **仍有未解释的查询退化，源码分支尚未推送。**

Public PR source: `11bfc35c99f8e845939a6753f004ecee38c7a2ec`. Local candidate: `45d4d7d5c7182ad7c5208510f6ee33c57670310b`.

The earlier55db repair and all its failed measurements remain frozen. This follow-up only skips unused filter-mask allocation and tests both floating evaluator representations against an independent native oracle. It does not establish a cause for the legacy callback slowdown.

Windows:1,112 passed,3 skipped,10 disabled;207 focused passed. Fresh Linux all-codec ASan/UBSan/LSan:207 focused and369 affected reader tests passed;7 reader tests disabled. Spotless check passed. The full sanitizer suite was not rerun:the prior candidate hit unchanged pinned LZOkay UB. This is not a clean full-suite result.

1,896 complete-file queries were rerun:1,800 floating combinations and96 NULL/BOOLEAN/time/OFFSET/LIMIT queries. Java/baseline/local writer products,Java application predicate,legacy C++,and structured row/batch C++ outputs all match complete deterministic expected sequences and exact defined values,NULLs,signedzero andNaN classes. PLAIN/UNCOMPRESSED only;NaN payload and universal codec compatibility not claimed. Baseline/local C++ writer bytes match.

Coverage scopes:local11b→45d repair lines72/79=91.14%,branches138/191=72.25%;maintainer6f→45d lines887/1058=83.84%,branches885/1441=61.42%;wholePR relative to recorded origin/develop lines966/1139=84.81%,branches1002/1596=62.78%. Selected affected production-file modules:lines3984/4940=80.65%,branches3509/6298=55.72%. These are not whole-library percentages. Seven defensive/unreachable repair lines remain uncovered;no denominator exclusions were used.

## Frozen query results

60 cases,12 initial independent paired blocks,and exactly one24-block confirmation for each of12 predeclared signals. Three neutral image copies and six version orders;verified child affinity4 before resume,parent16;build/sanitizer/coverage jobs finished before timing. All rows were fully consumed and checked. New driver runs3 queries/process;the retained8 noFIELD cases run8. All initial,confirmation and warmup samples retained.

3,456 successful processes. Query counts by phase: `{"warmup": 1320, "initial": 7920, "confirmation_warmup": 306, "confirmation": 3672}`.

|Case|Comparison|Median latency change|Bootstrap95% interval|
|---|---|---:|---|
|callback-w1-p1-b0|fixed/prior|+2.066%|+1.468% to +2.963%|
|callback-w1-p1-b0|fixed/base|+4.153%|+2.846% to +5.319%|
|callback-w1-p1-b1024|fixed/prior|+1.790%|+1.191% to +2.454%|
|callback-w1-p1-b1024|fixed/base|+4.442%|+3.711% to +4.724%|
|callback-w1-p100-b1024|fixed/prior|+1.566%|+1.017% to +2.552%|
|callback-w1-p100-b1024|fixed/base|+2.671%|+2.243% to +3.875%|
|callback-w8-p1-b0|fixed/prior|+2.131%|+1.034% to +3.214%|
|callback-w8-p1-b0|fixed/base|+2.835%|+2.305% to +3.947%|
|callback-w8-p1-b1024|fixed/prior|+1.282%|+0.389% to +2.757%|
|callback-w8-p1-b1024|fixed/base|+1.528%|+1.016% to +2.617%|
|callback-w8-p100-b0|fixed/prior|+0.627%|+0.204% to +0.883%|
|callback-w8-p100-b1024|fixed/prior|+2.210%|+1.302% to +3.015%|
|callback-w8-p100-b1024|fixed/base|+1.894%|+1.084% to +2.672%|
|callback-null-b0|fixed/prior|+2.736%|+2.164% to +3.472%|
|callback-null-b0|fixed/base|+2.628%|+1.709% to +3.564%|
|callback-null-b1024|fixed/prior|+2.111%|+1.100% to +3.497%|
|callback-null-b1024|fixed/base|+2.583%|+1.254% to +3.018%|
|unfiltered-time-b0|fixed/base|+0.995%|+0.295% to +1.676%|

Ten cases still have confirmed increases. No necessary-cost exception is claimed. Narrow low-hit legacy callbacks are about4.44% slower than6f;the unfiltered time-row query is about1.00% slower. Faster structured cases cannot offset these failures. A non-significant comparison does not prove equivalence,and separate candidate sessions do not isolate the effect of the allocation guard.

Structured/base comparisons include an extra projected and verified bucket column in the old reference;this is a materialization-cost comparison,not isolated engine speedup. Prior11b/native vs local45d/native and the separate legacy callback controls have matching physical projections. Open(file handle only),query planning(includes metadata),first row,full teardown latency,throughput,P50/P95 and whole-process peak memory are available for the new driver. The retained noFIELD driver reports total time only;missing phase/memory metrics remain missing.

## 中文说明

公开PR仍为11b，本地45d未推送。相对55db仅减少无结构化过滤时的无用掩码分配，并用独立原生比较期望检查真实TsBlock与ColumnView两条浮点求值路径。该分配不是所有旧回调的实际路径，不能用它解释约4.44%的回退。

本地重新通过Windows1112项、207专项，Linux全压缩依赖下207专项和369reader的ASan/UBSan/LSan检查，以及1896次完整文件Java/C++交叉查询；完整sanitizer未重跑，上一候选的原LZOkay失败保留，不能称全量通过。写入吞吐未重测，互通范围为PLAIN/UNCOMPRESSED，全部行数/顺序/精确值/NULL/负零与NaN类别核对。

本地11b→45d修补行/分支覆盖率91.14%/72.25%；维护者6f→45d为83.84%/61.42%；整个PR修改行/分支84.81%/62.78%；所选受影响生产文件模块80.65%/55.72%。完整PR修改行仍未达到90%，保留未覆盖分支和防御路径，不缩小分母冒充达标。

60场景固定对照和12个预定的一次性复核结束，3456个进程正常退出；全部返回结果消费并核对。10个场景仍确认退化，表格保留18项比较及全部原始样本。查询门槛仍false、必要性未证明；不追加旧候选轮数找通过、不盲调布局。新原生路径更快不能抵销旧回调/无FIELD查询失败，未显著不等同等价，也不能由跨候选轮次比率变化证明优化因果。

**AI disclosure:** OpenAI Codex wrote and ran this local repair,validation and report. The public batch commits were authored by the maintainer.

**AI 使用说明：** 本地修订、验证和报告由OpenAI Codex编写并执行；公开批量提交由维护者编写。
