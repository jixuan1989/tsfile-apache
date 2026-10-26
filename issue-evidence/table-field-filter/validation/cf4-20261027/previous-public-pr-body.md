<!-- codex-073-current-historical-eee-20261026 -->
**Public head `07388d55`: fresh local validation PENDING.** Maintainer ColinLee added `80bdef8d` (Java-style FIELD numeric binding/conversions), then `07388d55` (retain invalid missing NOT operands through repeated rewriting). The latest commit has parent80b and changes2production/2testfiles; cumulative sinceeee:3production reader/filter files and2testfiles. Exact clean source and870production-input freeze are saved;610Java inputs are unchanged. No local tests/timings have run for either new head; historical eee correctness, Java, coverage and performance results do not transfer. CI snapshot 2026-10-26T06:37:24.324696+00:00: `{"in_progress": 29, "success": 16, "neutral": 1, "skipped": 1}`; pending checks are neither failures nor acceptance. No new review was observed. Next scope includes numeric low-bit narrowing, NaN/infinity/saturation/rounding boundaries, schema binding and failed/reused/shared predicates, orderedNOT/statistics, missing operands/repeated negation, empty/LIMIT0/allNULL and row/batch execution, then affected bidirectionalJava/coverage/sanitizer/write/query checks and actual independent final reviews.

**Historical eee validation completed; quality gates remain UNCLEARED.**21cases/23repeated latency comparisons plus4confirmation-only signals;7repeat/3only versus precedingc01. The predeclared writer/arena supplement stopped before accepted timing: all5files with2048byteFIELDnames passJava4000row/order/NULL/value checks, bothc01/eeeC++readers fail10/10 `E_PARTIAL_READ=6`; the valid2056byteheader exceeds the initial1024read. Low-budget files differ75,617→98,037bytes. Strict full sanitizer retains unchangedLZOkay34failure. Windows1138pass/Java139tests,1,896compatibilityqueries and freshC++/Java coverage remain historicaleee; broader coverage is below90%. Two actual independent reviewers approve diagnostic publication only. First publisher readback verified32assets before the new80bhead guard stopped PR/reply edits. The80b annex publisher then stopped at its initialhead guard when073appeared, before uploads or PR/reply edits. [Full bilingual historical report](https://github.com/jixuan1989/tsfile-apache/blob/1b7b3e5e790b59c80814b322622093c02b12cac8/issue-evidence/table-field-filter/validation/merged-eee-20261026/validation-report.md) · [Immutable evidence and reviews](https://github.com/jixuan1989/tsfile-apache/tree/1b7b3e5e790b59c80814b322622093c02b12cac8/issue-evidence/table-field-filter/validation/merged-eee-20261026) · [Current scope annex](https://github.com/jixuan1989/tsfile-apache/blob/6ab9c92298431d0da32ab1346a7bea3ced761714/issue-evidence/table-field-filter/validation/merged-eee-20261026/latest-07388d55/new-head-scope-annex.md).

**公开head `07388d55`：本地新验证待执行。** 维护者ColinLee先加入`80bdef8d`（Java风格FIELD数值绑定/转换），再加入`07388d55`（缺失NOT操作数在重复重写后仍保留为无效谓词）。最新提交父为80b，修改2项生产/2项测试文件；相对eee累计3项生产reader/filter文件和2项测试文件。独立干净源码及870生产输入已冻结，610项Java输入未变。两个新head均未运行本地测试/计时，eee的正确性、Java、覆盖和性能结果不转记。CI快照2026-10-26T06:37:24.324696+00:00：`{"in_progress": 29, "success": 16, "neutral": 1, "skipped": 1}`；待执行不等于失败或验收，无新审阅。后续范围含数值低位窄化、NaN/无穷/饱和/舍入边界、schema绑定及失败/复用/共享谓词、有序NOT/统计、缺失操作数/重复否定、空表/LIMIT0/全NULL、行/批执行，再做受影响双向Java/覆盖/sanitizer/写入查询及实际独立最终复核。

**历史eee验证已完成，质量门槛仍未通过。**21场景/23项比较重复延迟上升，另4项仅确认轮信号；对前版c01为7重复/3仅确认。事前writer/arena补测在验收计时前中止：2048字节FIELD名五份文件均通过Java4000行/顺序/NULL/值检查，两版C++读者10/10失败`E_PARTIAL_READ=6`，初读1024不足有效2056字节header；低预算文件75,617→98,037字节。严格全量仍有未改LZOkay34失败。Windows1138通过/Java139项、1,896互通查询及新C++/Java覆盖均仅属历史eee，较广覆盖低于90%。两位实际独立审阅只批准诊断。首轮发布32项资产回读完成后因新80b停止PR/回复修改；随后80b附录发布在最初head检查发现073，尚未上传或修改PR/回复。[历史完整中英文报告](https://github.com/jixuan1989/tsfile-apache/blob/1b7b3e5e790b59c80814b322622093c02b12cac8/issue-evidence/table-field-filter/validation/merged-eee-20261026/validation-report.md) · [不可变证据与审阅](https://github.com/jixuan1989/tsfile-apache/tree/1b7b3e5e790b59c80814b322622093c02b12cac8/issue-evidence/table-field-filter/validation/merged-eee-20261026) · [当前范围附录](https://github.com/jixuan1989/tsfile-apache/blob/6ab9c92298431d0da32ab1346a7bea3ced761714/issue-evidence/table-field-filter/validation/merged-eee-20261026/latest-07388d55/new-head-scope-annex.md)。


**Query acceptance: UNCLEARED.** Fresh exact merged eee39799 samples: 21cases/23comparisons repeat an increase; 4confirmation-only comparisons remain unresolved. Largest repeat: `callback-w8-p1-b1024` fixed/base: 1.0517087 (+5.171%), pointwise95 [1.0432711,1.0608423]. Against preceding c01: 7repeated and 3confirmation-only comparisons. `callback-w1-p100-b0` fixed/public: 1.0115275 (+1.153%), pointwise95 [1.0076397,1.0188672]; `float-not-t1-mixed1-cut50-b0` fixed/public: 1.0072373 (+0.724%), pointwise95 [1.0033128,1.0106933]; `float-not-t1-mixed0-cut50-b0` fixed/public: 1.0065595 (+0.656%), pointwise95 [1.0034455,1.0099957]; `unfiltered-time-b0` fixed/public: 1.0038816 (+0.388%), pointwise95 [1.0006250,1.0058125]; `float-not-t1-mixed1-cut50-b1024` fixed/public: 1.0031530 (+0.315%), pointwise95 [1.0004637,1.0063783]; `long-n1-b0-parallel0-early` fixed/public: 1.0156498 (+1.565%), pointwise95 [1.0093514,1.0238755]; `long-n0-b1024-parallel0` fixed/public: 1.0079208 (+0.792%), pointwise95 [1.0007978,1.0188438]; `callback-w1-p100-b1024` fixed/public: 1.0087204 (+0.872%), pointwise95 [1.0020374,1.0146030]; `unfiltered-all-b0` fixed/public: 1.0028930 (+0.289%), pointwise95 [1.0008056,1.0110444]; `unfiltered-sparse-b0` fixed/public: 1.0036016 (+0.360%), pointwise95 [1.0001186,1.0069600] Necessary/minimized extra cost and complete causal attribution are not established. Separate affected writer/arena scope stopped on a pre-existing long-header correctness failure; no write acceptance. Full strict sanitizer fails in unchanged LZOkay. No old samples were extended, removed or pooled; no arbitrary tolerance. This is diagnostic publication only.

**查询验收：尚未通过。** 精确合入提交eee39799的新样本有21场景/23比较重复上升，另4项仅确认轮信号仍待解决。最大重复信号：`callback-w8-p1-b1024` fixed/base: 1.0517087 (+5.171%), pointwise95 [1.0432711,1.0608423]。相对前一c01有7项重复、3项仅确认轮信号。`callback-w1-p100-b0` fixed/public: 1.0115275 (+1.153%), pointwise95 [1.0076397,1.0188672]; `float-not-t1-mixed1-cut50-b0` fixed/public: 1.0072373 (+0.724%), pointwise95 [1.0033128,1.0106933]; `float-not-t1-mixed0-cut50-b0` fixed/public: 1.0065595 (+0.656%), pointwise95 [1.0034455,1.0099957]; `unfiltered-time-b0` fixed/public: 1.0038816 (+0.388%), pointwise95 [1.0006250,1.0058125]; `float-not-t1-mixed1-cut50-b1024` fixed/public: 1.0031530 (+0.315%), pointwise95 [1.0004637,1.0063783]; `long-n1-b0-parallel0-early` fixed/public: 1.0156498 (+1.565%), pointwise95 [1.0093514,1.0238755]; `long-n0-b1024-parallel0` fixed/public: 1.0079208 (+0.792%), pointwise95 [1.0007978,1.0188438]; `callback-w1-p100-b1024` fixed/public: 1.0087204 (+0.872%), pointwise95 [1.0020374,1.0146030]; `unfiltered-all-b0` fixed/public: 1.0028930 (+0.289%), pointwise95 [1.0008056,1.0110444]; `unfiltered-sparse-b0` fixed/public: 1.0036016 (+0.360%), pointwise95 [1.0001186,1.0069600] 尚未证明额外成本的必要性、最小性和完整因果。受影响writer/arena补测因既有长header正确性失败中止，写入验收未通过；严格全量sanitizer仍在未改LZOkay失败。未追加、删除或混合旧样本，也未自定容差。本次只发布诊断。


<details>
<summary>Historical heads and diagnostics / 历史提交和诊断</summary>

**Latest public head `eee39799` supersedes the c01 validation below.** The maintainer merged develop `ef1107d1` into the PR:82files differ from standalone c01, including7 C++ production files and Java changes. Current CI is46success/1neutral/1skip/1failure. The Windows Python3.14 failure is a Chocolatey LLVM17.0.6 HTTP504 during dependency installation; project build/test was skipped. The unchanged Windows install command and raw log support this setup-failure assessment; no retry or workflow change was requested. **This new merged source has not completed fresh local correctness/Java/coverage/sanitizer/query validation. Neither green checks nor c01 results pass its gates.** The c01 report below is completed historical-head evidence. Its query acceptance remains UNCLEARED. #1038 separately tracks pre-existing TimeIn row loss after a fully rejected page; upstream requests separate tracking. Source inspection finds the status conversion in base/c01/current/develop; no new local runtime reproduction or fix is claimed.

**最新公开head `eee39799` 已取代下方c01验证。** 维护者合入develop `ef1107d1`，相对独立c01有82文件不同，含7个C++生产文件及Java修改。当前CI46成功/1中立/1跳过/1失败。Windows Python3.14在依赖安装时获取Chocolatey LLVM17.0.6收到HTTP504，项目构建/测试被跳过；Windows安装命令未改，原始日志支持环境失败判断，未请求重跑或修改workflow。**新合并源码尚未完成新本地正确性/Java/覆盖率/sanitizer/查询验证，不因绿check或c01旧结果通过门槛。** 下方c01是已完成的历史head证据，查询验收仍未通过。上游 #1038 单独跟踪完全过滤页后TimeIn漏行，要求分开处理；源码检查在base/c01/current/develop均找到状态转换，不声称新本地运行复现或已修复。


<!-- codex-c01-maintainer-lifetime-20261026 -->
**Performance acceptance: UNCLEARED.** These are new samples for public c01ee105, not transferred c8b/5db results. Across the96+14 predeclared cases, 7 cases/8 comparisons repeat an increase in both initial and confirmation phases; 4 additional confirmation-only comparisons remain unresolved. Worst repeat: `callback-w8-p1-b1024` fixed/base: ratio 1.0603646 (+6.036%), pointwise95 [1.0495569, 1.0653652]. Against immediately preceding public c8b: 0 repeated comparisons, but 2 confirmation-only increases remain unresolved: `callback-null-b1024` fixed/public: ratio 1.0081152 (+0.812%), pointwise95 [1.0011798, 1.0161548]; `unfiltered-all-b0` fixed/public: ratio 1.0075084 (+0.751%), pointwise95 [1.0041994, 1.0119992]. Zero repeats does not establish equivalence. Necessary/minimized extra cost and causal attribution have not been established. Known-leaking c8b is a latency observation, not a memory-safe quality-equivalent baseline; correct release cannot be rejected solely for costing more than a leak. No old round was extended, no sample removed, and no arbitrary tolerance was introduced. Full raw ratios/metrics and comparison boundaries are supplied below.

**查询性能验收：尚未通过。** 本轮是公开 c01ee105 的新样本，不移植 c8b/5db 旧结果。预先声明的96+14场景中，7个场景/8项比较在初测和确认轮均重复上升，另4项仅确认轮出现的信号仍未解决。最大重复信号：`callback-w8-p1-b1024` fixed/base: ratio 1.0603646 (+6.036%), pointwise95 [1.0495569, 1.0653652]。相对紧邻的公开 c8b，有0项重复比较，但仍有2项仅确认轮出现的上升尚未解决：`callback-null-b1024` fixed/public: ratio 1.0081152 (+0.812%), pointwise95 [1.0011798, 1.0161548]; `unfiltered-all-b0` fixed/public: ratio 1.0075084 (+0.751%), pointwise95 [1.0041994, 1.0119992]。没有重复信号不代表等效。尚未证明额外成本的必要性、已尽量降低或完整因果。已知泄漏的 c8b 只提供延迟观察，不是内存安全的质量等价基线；不能只因正确释放比泄漏更慢就拒绝释放。未追加旧轮次、删除样本或自定容差。下文提供全部原始比率、指标及比较边界。


**Validated previous public head `c01ee105`: maintainer header-name cleanup, CI47success/1neutral/1skip.** ColinLee's two empty-string swaps release the owned time/value ChunkHeader names in terminal placement-new-reader cleanup. They preserve subobject lifetime; chunk reuse remains reset, not destroy. The existing FIELD predicate implementation retains filter-before-projection semantics, NULL rows, ordered comparison/NOT handling and page progress as verified in the declared tests. No new source was pushed by OpenAI Codex in this follow-up; old local5db and its extra test assertions remain separate and unpushed.

Fresh standalone Windows focused224/full1129pass,3skip/10disabled;Spotless clang-format17.0.6 passes. Linux build enables all6codec dependencies;strict ASan/UBSan/LSan focused224/reader291 and independent180dual-evaluator combinations(360evaluations)+24file controls per platform pass. All6long-name lifecycle oldc8b negatives leak;all6c01 positives exit0 clean,including reset/reload,error after allocation and early close. **Full strict Linux still exits1 at unchanged pinned LZOkay34;no suppression/full pass.** Remote Ubuntu Asan jobs actually check out merge3dcb84ad,71files different from standalone,each1387Passed/3Skipped/10Disabled;green CI does not replace local gates.

Fresh1896Java/C++complete queries,2752integer+2160floating preflight,10Java40000row scans and context216full+36early C++queries/3Java scans pass. Java inputs frozen before corresponding first execution;C++writerproducts byte-equal within declared fixtures,Java whole-file equality unclaimed. New96round:13,584processes,42,816formal queries,18one-shot confirmations;new14longname:828processes,2,304formal,1confirmations. Protocols reviewed before timing;no previous frozen samples appended/pooled.

Incremental lines2/2=100%,branches0/0=N/A;wholePR lines/branches85.98%/63.24%;selected16files75.88%/52.67%,fresh isolatedc01profile. Original8lack phase/perqueryquantile/memory;newtests are warmcache,valuesPLAIN/defaulttimeTS_2DIFF/UNCOMPRESSED. Cold/P99/compressed/generalnonalignedFIELD/parallelscaling/query-onlymemory/currentwrite throughput remain unmeasured. Full includes validation+teardown;context close only times destroy_query_data_set,headerrelease can also occur during iteration. Early-closefull is firstrow+cleanup,notfullscan. Known-leakingc8b is not a memory-safe equivalent baseline. Integerstructured/base6fmaterializes extra bucket inside fulltime and is excluded from the gate;incorrect mixedNaN oldnative is excluded. Reader-only writes not retimed;first2PRquery gaps unchanged.

Upstream #1034 tracks a historical DICTIONARY/NUL bug already fixed independently on develop by #1022. #1035 tracks a pre-existing small-internal-TsBlock hang separately;no extra fix is folded into this PR. These findings and exact source/CI boundaries are documented. Both actual independent final reviews are published with their model/runtime provenance and exact evidence hashes. Source/query gates are not waived. [Complete English/Chinese report](https://github.com/jixuan1989/tsfile-apache/blob/d7b99b409eab1cf6dfc2ce98f3cc99c03444f1a0/issue-evidence/table-field-filter/validation/lifetime-c01-20261026/validation-report.md) · [Raw diagnostics and final reviews](https://github.com/jixuan1989/tsfile-apache/tree/d7b99b409eab1cf6dfc2ce98f3cc99c03444f1a0/issue-evidence/table-field-filter/validation/lifetime-c01-20261026).

**已验证的历史公开head `c01ee105`：维护者清理header列名，CI47成功/1中立/1跳过。** ColinLee的两次空字符串swap在placement-new reader终止清理时释放time/value ChunkHeader列名，并保持子对象存活；跨chunk复用仍走reset，不是destroy。现有FIELD实现的先过滤后投影、NULL行、有序比较/NOT及页进展由声明范围内测试验证。本轮OpenAI Codex没有生产源码推送，旧本地5db及额外测试断言仍分开保留、未推送。

新独立Windows专项224/全量1129通过、3跳过10禁用，clang-format17.0.6下Spotless通过。Linux启用全部6项codec依赖，严格ASan/UBSan/LSan专项224/reader291及两平台各180种双求值器组合（实际360次）、24项文件控制通过。6项长名生命周期旧c8b负控均泄漏，6项c01正向均exit0且干净，覆盖reset重载、分配后错误和提前关闭。**严格全量仍在未改固定LZOkay34处exit1，无suppression或总通过声明。** 远程Ubuntu Asan实际检出3dcb84ad合并提交，与独立head71文件不同，各1387Passed/3Skipped/10Disabled，绿CI不替代本地门槛。

新1896次Java/C++完整查询、2752整数/2160浮点预检、10次Java40000行扫描及长名216次完整/36次提前关闭C++查询和3次Java扫描通过。Java输入在首次对应执行前冻结，声明夹具内C++writer产物字节相同，不声称Java整文件相同。新96轮13,584进程、正式42,816次、18项一次确认；新14项长名828进程、正式2,304次、1项确认。协议均计时前独立审阅，不追加或混合历史冻结样本。

本次修改行2/2=100%、分支0/0=N/A；整个PR行/分支85.98%/63.24%，所选16文件75.88%/52.67%，均新隔离c01profile。旧8项仍缺分项/单次分位数/内存；新驱动暖缓存、值PLAIN/默认时间TS_2DIFF/UNCOMPRESSED。冷/P99/压缩/广泛非对齐FIELD/并行扩展/查询专属内存/当前写吞吐未测。full包含核对和销毁，close只计destroy_query_data_set，header也可在遍历中释放；提前关闭full是首行和清理，不是完整扫描。仍泄漏的c8b不是内存安全等价基线；整数结构化/base6f额外物化bucket且成本计入full，排除出门槛，错误混合NaN旧原生同样排除。reader-only未重测写入，前两PR查询缺口保持。

上游 #1034 记录DICTIONARY/NUL历史问题，develop已由 #1022 独立修复；#1035 单独跟踪既有小容量内部TsBlock卡住，本PR不夹带修补。报告明确源码及CI比较范围。两位实际独立最终审阅与模型/runtime身份、精确证据哈希一并公开，不豁免源码/查询门槛。[完整中英文报告](https://github.com/jixuan1989/tsfile-apache/blob/d7b99b409eab1cf6dfc2ce98f3cc99c03444f1a0/issue-evidence/table-field-filter/validation/lifetime-c01-20261026/validation-report.md) · [原始诊断和最终审阅](https://github.com/jixuan1989/tsfile-apache/tree/d7b99b409eab1cf6dfc2ce98f3cc99c03444f1a0/issue-evidence/table-field-filter/validation/lifetime-c01-20261026)。



[Latest merge and setup-failure evidence / 最新合并与环境失败证据](https://github.com/jixuan1989/tsfile-apache/tree/d7b99b409eab1cf6dfc2ce98f3cc99c03444f1a0/issue-evidence/table-field-filter/validation/lifetime-c01-20261026/ci-and-source-report.md).

<details>
<summary>Historical heads, CI and validation / 历史提交、CI及验证</summary>

<!-- codex-c8b-lifetime-20261025 -->
**Source submission gate remains false.** The local lifetime repair is unpushed. Both predeclared rounds completed: 21 repeated latency increases across 18 cases; largest confirmed median increase 3.96%. 6 confirmation-only signals remain. Necessary/minimized extra cost is unproven; no numerical tolerance or faster unrelated case is used to waive the gate. See all-query-ratios.md for every initial/confirmation comparison. Four of these comparisons are against current public c8b, with a maximum +2.87%; the overall maximum is against base6f. These observations do not establish the source-level cause of the cost.

**源码提交门槛仍为false，本地生命周期修复未推送。**两套预声明轮次均完成：18场景、21项比较确认延迟上升，最大中位数增加3.96%；另有6项仅确认轮出现的信号。额外成本的必要性及已尽量降低仍未证明，不设数值容忍线，也不用其他场景更快抵销。所有初测与唯一确认比较见all-query-ratios.md。 其中4项比较相对当前公开c8b，最高+2.87%；总体最大项相对base6f。这些观察尚不能确定源码层面的成本原因。


**Current public head `c8b27546` has two real Debug/Release Asan failures.** CI syntheticmerge90db2294 (not standalonehead;71files differ) leaks62bytes/2alloc in each of six long-FIELD cases. Standalonec8b reproduces224functional passes but process exit1,360bytes/12alloc on local libstdc++. OpenAI Codex local `5db66cd7` completes terminal time/value ChunkHeader destruction and adds two nonnull result assertions; the long-name regression remains. It is unpushed. Maintainerc8b already restores NaN-safe finite statistics and strict empty-path validation; olderfcab's2.6430–2.8513×/six-malformed findings are historical,not transferred to this head.

**当前公开head `c8b27546` 有两项真实Debug/Release Asan失败。** CI实际为合并提交90db2294（与独立head71文件不同），6组长FIELD用例各泄漏62bytes/2alloc；本地独立c8b虽224功能通过，进程仍exit1、360bytes/12alloc。OpenAI Codex本地 `5db66cd7` 补齐终止式time/value ChunkHeader析构并加两处nonnull断言，长名回归保留，尚未推送。维护者c8b已恢复NaN安全有限统计和严格空路径验证，旧fcab的2.6430–2.8513倍及6项畸形检查属于历史，不套用到新head。

Fresh local Windows focused224/full1129pass,3skip/10disabled;Linux all6codec ASan/UBSan/LSan focused224/reader291 and independent180dual-evaluator+24file controls pass. Full strict Linux sanitizer still exits1 in unchanged LZOkay34 during LZOTest.TestBytes1;no suppression/full pass. Standard1896Java/C++queries,2752integer+2160float preflight and10Java scans pass;long-name supplement216queries+3Java scans pass. Java class/jar/oracle inputs frozen before first corresponding Java execution. New96round:13,784processes,42,432formal queries,19one-shot confirmations;new12longname:624processes,1,728formal,0confirmations. Both exact24/48bounded protocols reviewed independently before timing;no old frozen-round extension.

新本地Windows专项224/全量1129通过、3跳过10禁用；Linux全6codec下ASan/UBSan/LSan专项224/reader291及独立180双求值器+24文件控制通过。严格全量仍在未修改LZOkay34的LZOTest.TestBytes1中exit1，无suppression或总通过声明。标准1896次Java/C++、2752整数+2160浮点预检、10次Java扫描，新增长名216次查询+3次Java扫描通过；各Java class/jar/oracle在首次对应Java执行前冻结。新96轮13,784进程、正式42,432次、19项一次确认；新长名12轮624进程、正式1,728次、0项确认；两套固定24/48协议均计时前独立审阅，不追加历史冻结轮次。

Changed lines2/2=100%,branches0/0=N/A;wholePR85.98%/63.24%,selected16files75.80%/52.59% lines/branches,fresh isolated final5db profile. The module percentage is lower than prior cumulative profile;denominators/scope disclosed. Warmcache,new PLAIN/defaulttimeTS_2DIFF/UNCOMPRESSED data;requested parallel flag is not actual fallback scaling proof. Full latency includes actual ownership release which may occur during iteration;close_seconds only times destroy_query_data_set. Known-leaking publicc8b is not a memory-safe quality-equivalent baseline. Old8still lack phases/perqueryquantiles/memory;cold/P99/compressed/generalnonalignedFIELD/scaling/query-onlymemory/currentwrite throughput unmeasured. Reader-only writes not retimed;first2PRquery gaps unchanged.

修改行2/2=100%、分支0/0=N/A；整个PR行/分支85.98%/63.24%，所选16文件75.80%/52.59%，均新隔离最终5db profile，模块率低于历史累计profile，分母及范围如实公开。暖缓存，新增数据值PLAIN/默认时间TS_2DIFF/UNCOMPRESSED；parallel参数不证明fallback扩展性。实际释放可在迭代中发生且包含在完整延迟，close_seconds只计destroy_query_data_set。仍泄漏的公开c8b不是内存安全质量等价基线。旧8项仍缺分项/单次分位数/内存；冷/P99/压缩/广泛非对齐FIELD/扩展/查询专属内存/当前写吞吐未测，reader-only未重测写，前两PR查询缺口保持。

Both actual independent final reviewers,gpt-6.1-sol agent and different gpt-6-astra model(runtime verified),reviewed exact source and frozen evidence:NOT_READY_TO_PUSH. Diagnostic publication allowed;source/query gates not waived. [Full bilingual report](https://github.com/jixuan1989/tsfile-apache/blob/b15cccd4d9f895def65739b519f41e8d79031954/issue-evidence/table-field-filter/validation/lifetime-c8b-20261025/validation-report.md) · [Raw evidence and final reviews](https://github.com/jixuan1989/tsfile-apache/tree/b15cccd4d9f895def65739b519f41e8d79031954/issue-evidence/table-field-filter/validation/lifetime-c8b-20261025).

实际独立agent gpt-6.1-sol及不同模型gpt-6-astra（runtime核实）分别复核精确源码及冻结证据，均NOT_READY_TO_PUSH，仅允许发布诊断，不豁免源码/查询门槛。[完整中英文报告](https://github.com/jixuan1989/tsfile-apache/blob/b15cccd4d9f895def65739b519f41e8d79031954/issue-evidence/table-field-filter/validation/lifetime-c8b-20261025/validation-report.md) · [原始证据及最终审阅](https://github.com/jixuan1989/tsfile-apache/tree/b15cccd4d9f895def65739b519f41e8d79031954/issue-evidence/table-field-filter/validation/lifetime-c8b-20261025)。

<details>
<summary>Historical heads,CI and validation / 历史提交、CI及验证</summary>

<!-- codex-ci-recovery-f98-20261025 -->
> **CI recovery only; query/source gates remain uncleared.** Current public head `f98ff7bd` changes only the two C++/Python workflows on `fcab7437`; standalone C++/Java/Python trees are identical. Current checks: 47 success / 1 neutral / 1 skipped. The seven previously affected Linux jobs now complete setup, build and tests, but actually test merge `dcd29245` (with develop `eb733133`), whose C++/Java trees differ from the PR head. Their Asan job success does not replace earlier strict local sanitizer failures or clear performance/invalid-tree findings. No local test/timing rerun or source submission occurred. [Scoped bilingual CI addendum](https://github.com/jixuan1989/tsfile-apache/blob/0919def5313ddf8179dfecc862c328251a96c68c/issue-evidence/table-field-filter/validation/ci-f98-20261025/ci-followup-report.md).
>
> **仅 CI 恢复，查询及源码门槛仍未通过。** 当前公开 `f98ff7bd` 只在 `fcab7437` 上修改 C++/Python 两份工作流；独立 head 的 C++/Java/Python tree 相同。当前检查 47 成功、1 中立、1 跳过。原先受影响的 7 项 Linux 任务已完成环境准备、编译和测试，但实际测试合并提交 `dcd29245`（合入 develop `eb733133`），其 C++/Java tree 与 PR head 不同。Asan 任务通过不能替代此前本地严格 sanitizer 失败，也不能清除性能及畸形树问题。未重跑本地测试/计时，未提交源码。[完整中英文 CI 附录](https://github.com/jixuan1989/tsfile-apache/blob/0919def5313ddf8179dfecc862c328251a96c68c/issue-evidence/table-field-filter/validation/ci-f98-20261025/ci-followup-report.md)。

<!-- codex-finite-stats-local2525-20261023 -->
> **Current public PR head is f98ff7bd (CI-only follow-up on fcab7437); the local repair below has not been submitted.** Its earlier, separate frozen96-case validation retains finite zero-hit FLOAT/DOUBLE NOT latency2.6430–2.8513×the valid prior11b native path, plus the six malformed empty/LIMIT0 checks. Those findings remain applicable to the unchanged public source; the new local candidate's smaller residual flags do not replace the public-head warning. [Public-head evidence](https://github.com/jixuan1989/tsfile-apache/blob/a1e854ae1ea161e77b65ce9cfbea2dabca8b3259/issue-evidence/table-field-filter/validation/maintainer-fcab-20261023/validation-report.md).
>
> **当前公开PR为f98ff7bd（fcab7437上的纯CI后续提交），下述本地修补尚未提交。**公开源码此前独立冻结96场景验证中，有限值零命中FLOAT/DOUBLE NOT延迟仍为正确的上一版11b原生路径的2.6430–2.8513倍，另有6项空表/LIMIT0畸形树检查。公开源码未变，这些发现继续适用；新本地候选较小的剩余信号不能代替公开head的警告。[公开head证据](https://github.com/jixuan1989/tsfile-apache/blob/a1e854ae1ea161e77b65ce9cfbea2dabca8b3259/issue-evidence/table-field-filter/validation/maintainer-fcab-20261023/validation-report.md)。

> **Performance gate not cleared for local candidate2525:** 96 cases, 13,584 successful processes and 18 predeclared one-shot confirmations retain 15 cases / 15 repeated increases, all against base6f; the largest is +2.94% (ratio interval1.02149–1.03652). No confirmation-only signals remain. No repeated increase against publicfcab or prior11b was found in this bounded round; this is not equivalence. Finite zero-hit FLOAT/DOUBLE queries have initial latency ratios 0.3363–0.3485 versus publicfcab and 0.9881–1.0089 versus prior11b. Extra-cost necessity remains unproven. Full sanitizer still fails in unchanged LZOkay. Source is unpushed and the submission gate remains false.
>
> **本地候选2525的性能门槛未通过：**96场景、13,584个成功进程及18项预定一次性确认后，15场景/15项比较保留重复延迟上升，均相对base6f，最高+2.94%（比率区间1.02149–1.03652）。没有只在确认轮出现的剩余信号。本次有界测量未确认相对公开fcab或上一版11b的重复上升，不表示等效。有限值零命中FLOAT/DOUBLE初测延迟为公开fcab的0.3363–0.3485倍、上一版11b的0.9881–1.0089倍。额外成本必要性仍未证明；全量sanitizer仍在未修改的LZOkay失败。源码未推送，提交门槛仍为false。

**This candidate is local and unsubmitted. Public PR head is `f98ff7bd`, with the same standalone production sources as `fcab7437`.** OpenAI Codex authored local `2525a557` from the maintainer head: NaN-safe ordered statistics shortcuts, whole-tree checks before empty-table/LIMIT0 returns, and mask lifecycle work. These repairs have not been applied to the public branch. Against frozen fcab, seven regression groups fail; local final Windows focused214/full1119 and Linux ASan/UBSan/LSan focused214/reader376 pass. Both evaluators and24 independent file-query controls pass;1,896 standard Java/C++ file queries plus2,160 floating and2,752 integer preflight queries and ten Java scans pass. Generated four-version C++ writer products are byte-identical. Full Linux sanitizer still fails at unchanged pinned LZOkay; no full pass is claimed.

**候选仅在本地，尚未提交，公开PR为 `f98ff7bd`，独立生产源码与 `fcab7437` 相同。** OpenAI Codex从维护者提交编写本地 `2525a557`，恢复NaN安全的有序统计快捷路径、在空表/LIMIT0返回前检查整树，并修正掩码生命周期；这些修补尚未应用到公开分支。冻结fcab上7组回归失败，本地最终Windows专项214/全量1119及Linux ASan/UBSan/LSan专项214/reader376通过；两条求值器与24项独立文件查询控制通过，1,896次标准Java/C++查询、2,160次浮点及2,752次整数预检查询、10次Java全读均通过；四版C++写入产物字节一致。Linux全量sanitizer仍在未修改的固定LZOkay失败，不能称总通过。

The new frozen96-case four-version round completed13,584 children and43,776 formal plus3,136 warmup queries, with18 predeclared one-shot confirmations. Fifteen comparisons against6f retain increases: floating callbacks up to+2.94%, narrow integer callbacks up to+1.86%, sparse noFIELD batch+0.62%. The largest pointwise95 ratio interval is1.02149–1.03652. No repeated publicfcab/prior11b increase was found in this bounded round; this is not equivalence. Finite zero-hit floating queries are0.3363–0.3485×publicfcab in initial blocks and0.9881–1.0089×prior11b; no old-round ratios were divided or pooled. Necessary extra cost remains unproved; gates remainfalse. Both actual independent reviewers (`gpt-6.1-sol`, `gpt-6-astra`, runtime-verified) completed final source/evidence review and conclude `NOT_READY_TO_PUSH`. No Copilot review was requested.

新冻结的96场景四版本计时完成13,584进程，正式43,776次及预热3,136次查询，18项各一次预定确认。相对6f的15项比较保留上升：浮点同回调最高+2.94%、窄投影整数回调最高+1.86%、无FIELD稀疏批查询+0.62%；最大项逐项95比率区间1.02149–1.03652。本次有界轮次未确认相对公开fcab/上一版11b的重复上升，不表示等效。有限值零命中浮点初测延迟为公开fcab的0.3363–0.3485倍、11b的0.9881–1.0089倍，没有跨旧轮求比率或池化。尚未证明额外成本必要，门槛保持false。独立agent和另一实际模型（`gpt-6.1-sol`、`gpt-6-astra`，runtime身份已核实）完成最终源码及证据审阅，均判定 `NOT_READY_TO_PUSH`；没有请求Copilot审阅。

Changed-line/branch coverage for fcab→local2525 is97.92%/71.90%; **wholePR1180→local2525 remains85.64%/62.57%**; selected16 affected files80.81%/55.65%. Coverage accumulates3ce/2525 test runs on260 byte-identical production inputs; it is not a cleared isolated final-test profile. Final test pass counts use fresh final XML. Warm cache, PLAIN/default timeTS_2DIFF/UNCOMPRESSED generated data; original8 retain old configuration and lack phases, per-query quantiles and memory. Cold cache/P99/compressed/general nonaligned FIELD/parallel scaling/query-only memory remain unmeasured. Reader-only writes were not retimed; earlier PR1018/1024 gaps remain. Old45d and all prior samples stay intact; no extra timing rounds were added. The first spotless missingPATH raw log was accidentally overwritten and is explicitly disclosed in the report.

fcab→本地2525的修改行/分支覆盖率97.92%/71.90%；**整个PR1180→本地2525仍为85.64%/62.57%**，所选16文件80.81%/55.65%。覆盖率累积3ce/2525两个测试提交在260项逐字节相同生产输入上的运行，不是清零后最终测试提交的独立profile；最终测试通过数来自全新最终XML。生成数据为暖缓存、值PLAIN/时间默认TS_2DIFF/UNCOMPRESSED；原8项保持旧配置，仍缺分项、单次分位数和内存。冷缓存/P99/压缩/广泛非对齐FIELD/并行扩展/查询专属内存仍未测，reader-only未重测写入，前两个PR的缺口未补齐。旧45d及全部旧样本保持原样，没有增加计时轮次。首次spotless缺PATH失败的原始日志被意外覆盖，报告已明确披露。

[Current bilingual report / 当前中英文报告](https://github.com/jixuan1989/tsfile-apache/blob/eba6ca392583fede0bc3a2864665bb7ab0247912/issue-evidence/table-field-filter/validation/finite-stats-20261023/validation-report.md) · [All raw evidence and both final reviews / 全部原始证据及两份最终审阅](https://github.com/jixuan1989/tsfile-apache/tree/eba6ca392583fede0bc3a2864665bb7ab0247912/issue-evidence/table-field-filter/validation/finite-stats-20261023)

<details>
<summary>Earlier publicfcab and local45d evidence / 公开fcab及本地45d的先前证据</summary>

<!-- codex-maintainer-fcab-20261023 -->
> **Performance gate failed on public maintainer head `fcab7437`:** 96 cases, 5,826 successful processes and 23 predeclared one-shot confirmations retain 22 cases / 28 comparisons with pointwise confirmed latency increases. Finite FLOAT/DOUBLE `NOT(x < 100)` zero-hit row/batch queries are 2.6430–2.8513× prior valid native `11b` (maximum +185.13%, bootstrap95 ratio 2.7587–2.8947); finite full-hit queries increase 12.70–30.57%. Same-callback floating controls increase up to 8.22% against `6f` and 3.32% against `11b`; an integer callback is +1.00% against `6f`, sparse noFIELD batch is +1.32% against `11b`. This warm-cache MSVC Release uncompressed scope does not prove the extra cost necessary or minimized. No production patch is submitted; query/source gates remain false. Faster native-vs-opaque results do not cancel these regressions.
>
> **公开维护者提交 `fcab7437` 的性能门槛未通过：**96个场景、5,826个成功进程和23项预定的一次性独立复核后，22个场景、28项比较仍保留逐项区间确认的延迟上升。有限值FLOAT/DOUBLE的 `NOT(x < 100)` 零命中行/批查询，是结果正确的上一公开原生实现 `11b` 的2.6430–2.8513倍（最高增加185.13%，bootstrap95比率区间2.7587–2.8947）；有限值全命中查询增加12.70–30.57%。同一回调的浮点控制场景相对 `6f` 最高增加8.22%、相对 `11b` 最高增加3.32%；整数回调相对 `6f` 增加1.00%，无FIELD的稀疏批查询相对 `11b` 增加1.32%。这些结果仅适用于暖缓存、MSVC Release、无压缩测试范围，未证明额外成本必要或已尽量降低。没有提交生产补丁，查询及源码提交门槛仍为false；原生路径相对应用层参考更快也不能抵销这些退化。

<!-- codex-ci-provisioning-fcab-20261023 -->
> **Current fcab CI setup blocker:** all7failed Ubuntu jobs were checked using actual logs, step metadata and annotations. Six lack `/usr/bin/clang-format-17`; Python3.9 x64 is unavailable for Ubuntu26.04. All later noncleanup steps were skipped; none reached project compilation/tests. Workflow11b→fcab is unchanged. This does not clear the independent local query, invalid-tree or sanitizer findings. No rerun or shared workflow edit was requested.
>
> **当前 fcab 的CI环境阻塞：**已逐一核对7个Ubuntu失败任务的实际日志、步骤元数据与注解。6项缺少 `/usr/bin/clang-format-17`，另1项在Ubuntu26.04上没有Python3.9 x64。后续非清理步骤全部跳过，均未执行项目编译或测试；workflow在11b→fcab间未改。此判断不抵销本地查询退化、畸形树和sanitizer问题；未请求重跑或修改共享workflow。

[Current-head CI logs and bilingual diagnosis / 当前提交CI日志及中英文判断](https://github.com/jixuan1989/tsfile-apache/blob/852fe30285d547aab85afd6d290d4388671e9925/issue-evidence/table-field-filter/validation/maintainer-fcab-20261023/remote-ci-fcab/ci-setup-addendum.md)


Maintainer ColinLee's new public commit `fcab7437` fixes ordered FLOAT/DOUBLE NOT with NaN by complementing only nonNULL comparisons in both evaluators, guards malformed nonempty aligned plans, and releases owned mask storage during manual destroy. Valid-query evidence: Windows1104full/199focused passed; Linux ASan/UBSan/LSan199focused+361reader passed;1896complete-file Java/C++ queries plus864floating C++ queries and6Java full scans passed. Two actual independent reviewers (`gpt-6.1-sol`, `gpt-6-astra`, verified runtime identities) completed source/protocol/final-evidence reviews and conclude `NOT_READY_TO_PUSH`.

维护者ColinLee的新公开提交 `fcab7437` 在两条求值路径中仅对非NULL比较结果取反，修复FLOAT/DOUBLE有序NOT与NaN语义，保护非空对齐计划的畸形树检查，并在手动destroy时释放掩码所有权存储。合法查询证据：Windows全量1104/专项199通过；Linux ASan/UBSan/LSan专项199及reader361通过；1896次完整文件Java/C++查询、864次浮点C++查询和6次Java全量扫描通过。两个实际独立审阅会话（`gpt-6.1-sol`、`gpt-6-astra`，runtime身份已核实）完成源码、协议和最终证据审阅，均判定 `NOT_READY_TO_PUSH`。

Remaining limits:6 schema-only/LIMIT0 malformedOR checks return E_OK/empty rather than strict expected E_INVALID_ARG;12valid controls pass. Fresh full Linux sanitizer exits in unchanged pinned LZOkay; no full pass. Current11b→fcab changed-line/branch coverage91.67%/70.27%; **wholePR1180→fcab84.26%/61.56%**, selected affected files80.54%/55.41%. Conservative negated statistics and preexisting duplicate lazy-mask evaluation are source observations, not proof of complete slowdown causality or necessity. ValuesPLAIN/timeTS_2DIFF/UNCOMPRESSED for generated matrices; original8 keep original configuration. Cold cache/P99/compressed/general nonaligned FIELD/parallel scaling remain unmeasured. Writes were not retimed for this reader-only revision. Historical local45d stays unmerged/unpushed, without transferring its results tofcab.

剩余限制：空表/LIMIT0的6项畸形OR仍返回E_OK/空结果，未按严格期望返回E_INVALID_ARG；12个合法控制通过。新全量Linux sanitizer仍在未修改的固定LZOkay中止，不能称总通过。本轮11b→fcab修改行/分支覆盖91.67%/70.27%；**整个PR1180→fcab为84.26%/61.56%**，所选受影响文件80.54%/55.41%。保守取反统计及原有lazy-mask重复求值是源码观察，未证明完整退化因果或必要性。生成矩阵的值为PLAIN、时间TS_2DIFF、UNCOMPRESSED；原8项保留原配置。冷缓存/P99/压缩/广泛非对齐FIELD/并行扩展仍未测；仅reader修订没有重测写入吞吐。历史本地45d仍未合入或推送，其结果不转移到fcab。

[Current bilingual report / 当前中英文报告](https://github.com/jixuan1989/tsfile-apache/blob/a1e854ae1ea161e77b65ce9cfbea2dabca8b3259/issue-evidence/table-field-filter/validation/maintainer-fcab-20261023/validation-report.md) · [All raw evidence and both final reviews / 全部原始证据与两份最终审阅](https://github.com/jixuan1989/tsfile-apache/tree/a1e854ae1ea161e77b65ce9cfbea2dabca8b3259/issue-evidence/table-field-filter/validation/maintainer-fcab-20261023)

<details>
<summary>Historical evidence through public11b and unpushed local45d / 公开11b及未推送本地45d的历史证据</summary>

<!-- codex-local45d-diagnostics-20261022 -->
> **Latest local candidate `45d4d7d5` remains unpushed:** 60 query cases, 3,456 successful processes and 12 bounded confirmations still show 10 cases with confirmed regressions, including up to +4.44% for narrow legacy callback queries and +1.00% for unfiltered time-row query latency versus `6f4a971e`. Necessity is unproven; the query gate remains failed.
>
> **最新本地候选 `45d4d7d5` 仍未推送：**60 个查询场景、3,456 个成功进程和 12 次有界复核后，10 个场景仍确认退化；相对 `6f4a971e`，窄投影旧回调查询延迟最高增加 4.44%，无 FIELD 过滤的时间行查询延迟增加 1.00%。退化的必要性尚未证明，查询门槛仍未通过。

This candidate passed 1,112 Windows tests, scoped Linux ASan/UBSan/LSan runs with 207 and 369 passing tests, and 1,896 complete-file Java/C++ queries. Local repair line/branch coverage is 91.14%/72.25%; **whole-PR changed-line/branch coverage is 84.81%/62.78%**, and coverage of the selected affected production files is 80.65%/55.72%. Full sanitizer testing was not rerun; the earlier failure in unchanged LZOkay code remains. Both independent source/evidence reviewers conclude `NOT_READY_TO_PUSH`. The mask-allocation guard has not been shown to explain the legacy callback regressions.

该候选已通过 1,112 项 Windows 测试、分别有 207 和 369 项通过的 Linux 专项 ASan/UBSan/LSan 检查，以及 1,896 次完整文件 Java/C++ 查询。本地修补行/分支覆盖率为 91.14%/72.25%；**整个 PR 修改行/分支覆盖率为 84.81%/62.78%**，所选受影响生产文件的行/分支覆盖率为 80.65%/55.72%。全量 sanitizer 未重跑，先前未修改的 LZOkay 代码失败记录仍保留。两位独立源码及证据审阅者均判定 `NOT_READY_TO_PUSH`；尚无证据证明掩码分配优化能解释旧回调的性能退化。

[Latest bilingual report / 最新中英文报告](https://github.com/jixuan1989/tsfile-apache/blob/a0783a71c07c82e4ec41cd52b23fdb80d90d571c/issue-evidence/table-field-filter/validation/allocation-followup-20261022/validation-report.md) · [Scoped diagnostics and all timing records / 分项诊断及全部计时记录](https://github.com/jixuan1989/tsfile-apache/tree/a0783a71c07c82e4ec41cd52b23fdb80d90d571c/issue-evidence/table-field-filter/validation/allocation-followup-20261022)

The earlier `55db175d` measurements and findings for public head `11bfc35c` below retain their original source scopes. 以下 `55db175d` 的旧测量和公开提交 `11bfc35c` 的问题记录保留各自的原始提交范围及失败证据。

<!-- codex-ci-provisioning-11b-20261022 -->
> **CI setup blocker at11b:** six Ubuntu jobs cannot find clang-format17;Python3.9 is unavailable for Ubuntu26.04. These seven jobs fail before project compilation/tests. This does not clear the separate local correctness/performance findings below.
>
> **11b 的CI环境阻塞：**6项Ubuntu任务缺少clang-format17，Python3.9任务在Ubuntu26.04上无对应运行时，7项均在项目编译/测试前失败；此说明不抵销下面独立的本地正确性和性能问题。

> **Current public head `11bfc35c`: local validation still finds floating `NOT` result errors, malformed-OR validation bypass, and new mask-storage leaks. A local repair (`55db175d`) has NOT been pushed because its query-performance gate failed.**

> **当前公开 head `11bfc35c`：本地仍复现浮点 `NOT` 结果错误、畸形 OR 绕过检查和新增掩码泄漏。本地修订 `55db175d` 因查询性能门槛未通过，尚未推送。**

The local repair passed Windows 1,112 tests and Linux ASan/UBSan/LSan focused207 plus reader369 tests;1,896 complete-file Java/C++ queries match an independent complete oracle. However, its confirmed dense width4/100%-hit row query is **+2.56% vs11b**, and narrow low-hit legacy callbacks are **up to+5.05% vs6f**. Other confirmed increases are retained. Necessity has not been demonstrated; no performance exception is claimed. Full sanitizer still aborts in unchanged pinned LZOkay; local11b→55db changed-line/branch coverage is89.47%/68.78%.

本地修订的Windows1112项及Linux207专项、369reader检查在ASan/UBSan/LSan下通过，1896次完整文件Java/C++查询与独立完整期望一致。但确认的4列/100%命中行查询相对11b **慢2.56%**，窄投影低命中旧回调相对6f **最高慢5.05%**，其它确认退化均保留。必要性未证明，不使用性能例外；全量sanitizer仍在未修改的LZOkay中止。本地11b→55db修补差异的行/分支覆盖率为89.47%/68.78%。

[Bilingual report / 中英文报告](https://github.com/jixuan1989/tsfile-apache/blob/058e80e4349a5307e9e6870bc5563ec8e631b886/issue-evidence/table-field-filter/validation/aligned-batch-20261022/validation-report.md) · [Complete retained diagnostics / 完整保留的诊断证据](https://github.com/jixuan1989/tsfile-apache/tree/058e80e4349a5307e9e6870bc5563ec8e631b886/issue-evidence/table-field-filter/validation/aligned-batch-20261022)

The batch commits f5d1243a/11bfc35c were authored by the maintainer. The repair is local AI-authored work; source submission remains blocked by unresolved validation. Earlier measurements below retain their original commits and scopes.

批量实现f5d1243a/11bfc35c由维护者编写；本地修订由AI编写，源分支仍须满足验证门槛。下面早期记录仅适用于其原提交和范围。

<details><summary>Historical validation before the current batch implementation / 当前批量实现之前的历史验证</summary>

<!-- codex-maintainer-followup-20261021 -->
Fixes #1025.

> **PERFORMANCE WARNING — query acceptance remains NOT cleared at `6f4a971ee`.** Three comparisons still show higher median complete-query latency after the predeclared independent confirmation (table below). Their necessity has **not** been demonstrated; they are not accepted as an unavoidable correctness cost. The worst native NULL-query / old correct application-reference ratio is **1.7273×**; those plans include different projection/materialization and predicate work, so it does not isolate engine regression. Full combined ASan/UBSan validation is also **not clean**: unchanged TS2DIFF and pinned LZOkay diagnostics aborted broader runs. Earlier passing measurements below apply only to the historical heads stated there.
>
> **性能警告——`6f4a971ee` 的查询验收仍未通过。** 三个场景在事先规定的独立复核中仍有完整查询延迟上升，见下表；尚未证明这些代价必要，不能按“正确性必需开销”验收。原生 NULL 查询/旧正确应用层参考的最大延迟比为 **1.7273 倍**，两者投影、物化及谓词工作不同，不能单独归因于引擎退化。完整 ASan/UBSan 也**不能称为通过**：未改动的 TS2DIFF 和固定版本 LZOkay 问题中止了扩大检查。下方旧的通过记录仅适用于其明确注明的历史提交。

| Comparison / 场景 | Confirmed median change / 复核延迟变化 | Bootstrap 95% interval / 区间 |
|---|---:|---:|
| `null_w4_p1_b1024_tag0_parallel0` | +0.826% | [+0.125%, +1.454%] |
| `dense_w4_p10_b1024` | +0.902% | [+0.528%, +1.321%] |
| `dense_w4_p100_b1024` | +1.433% | [+0.380%, +1.998%] |

### Current behavior and maintainer follow-up

The PR executes FIELD predicates on aligned table rows, including NULL rows that must reach the predicate before OFFSET/LIMIT. Maintainer [ColinLeeo's follow-up](https://github.com/apache/tsfile/pull/1026#issuecomment-6307669660) adds two commits, `f2e157ed3` and `6f4a971e`; these were authored by the maintainer, not Codex.

* Whole-column non-NULL count is not a safe test for whether selected aligned timestamps exist: values may occur only before the requested time range. When no selected value context remains, the fallback now checks whether the requested sources are aligned and uses their shared time context for a non-null FIELD predicate. The new range regression fails all six configurations on `249b0d51a` and passes on the new head. The non-aligned empty-context shortcut and hard-error handling remain.
* The removed private non-virtual INT32 decoder helper had no call sites. Active aligned INT32 decoding already uses `decode_tv_batch<int32_t>`. The used non-aligned `ChunkReader` helper remains.

Local validation against frozen `249b0d51a` / `6f4a971ee`:

* 80 focused permanent tests pass, plus 24 local boundary cases and three non-aligned gap cases. Windows Release: **985 passed, 3 skipped, 10 disabled**, codecs off to match the retained Windows baseline.
* All-codec Linux combined ASan/UBSan: **80 focused + 24 boundary + 3 gap** cases pass. Reader-suite scope: **343 passed, 2 external-fixture skips, 9 disabled**. This does not establish a clean full sanitizer run. The aborted broader logs and the exact old/new TS2DIFF raw-page reproduction remain in the evidence.
* **48** final-C++/Java own/cross reads match exact times, order, NULL and BOOLEAN values. Java uses native time filtering plus application-level IS NULL/OFFSET/LIMIT; this is a result comparison, not equivalent native FIELD execution. Small and large NULL fixtures written by old/new C++ are byte-identical; Java/C++ whole-file byte equality is not claimed.
* Maintainer-delta executable lines **4/4 (100%)**, branches **5/6 (83.33%)**. Affected reader files overall: **79.81% lines / 55.92% branches**; these are not whole-library percentages.
* Query protocol: **68 initial cases**, seven one-time independent confirmations, **20,928 fully consumed and checked formal queries** plus 1,456 warmups. Projection 1/4/8, FIELD hit rates 0/1/10/50/100%, row/batch and NULL-in-range cases are included. Warm-cache MSVC Release PLAIN/UNCOMPRESSED results do not establish cold-cache, compressed-query, broad non-aligned FIELD or general parallel-scaling behavior. Initial data and outliers are retained.
* This follow-up changes reader paths only; writing was not retimed. Historical write evidence retains its original head/scope. An independent agent reviewed local source/protocol, but actual serving-model identity and a different-model final-evidence review are unverified/not run. The complete new pre-submission review gate is **not passed**. Codex made no new production-code push.

### 当前行为和维护者修正

本 PR 使对齐表数据逐行执行 FIELD 谓词，包括应先进入谓词、再应用 OFFSET/LIMIT 的 NULL 行。维护者上述两次提交修正“整列有值、所选时间范围全 NULL”的漏行，并删除无调用的私有辅助函数；实际 INT32 解码走既有模板，非对齐保护及硬错误传播保留。

新增范围回归在旧库六种配置全部失败，在新提交全部通过。本地永久专项 80 项、额外边界 24 项和非对齐间隙 3 项通过；Windows Release 985 项通过、3 项跳过、10 项禁用。Linux 六压缩库的 ASan/UBSan 专项和额外用例通过，reader 范围 343 项通过、2 项外部夹具跳过、9 项禁用；两个扩大检查仍中止，不能替代为全量 sanitizer 通过。

48 次最终 C++/Java 自身或交叉读取逐项一致；Java 使用时间过滤后应用层 IS NULL/OFFSET/LIMIT，不宣称原生 FIELD 执行路径相同。旧、新 C++ 两种规模的 NULL 文件字节一致，不宣称 Java/C++ 整文件一致。本次维护者修改行覆盖率 100%、分支 83.33%，受影响 reader 文件合计为 79.81%/55.92%，不是全库覆盖率。

查询包含 68 项初测、七项一次性独立复核，正式完整核对 20,928 次，另有 1,456 次预热，涵盖不同投影、命中率和 NULL 范围；仅测暖缓存、MSVC Release、无压缩数据，冷缓存、压缩查询、广泛非对齐 FIELD 和通用并行扩展仍未测。原始数据和异常样本保留。此次仅改 reader，没有重测写入吞吐。另一模型最终证据审阅尚未运行，完整提交前独立审阅门槛未通过；Codex 没有新增生产代码推送。

[Current bilingual validation report](https://github.com/jixuan1989/tsfile-apache/blob/146680b0eecc3db6501d46ed697d145db462baef/issue-evidence/table-field-filter/validation/maintainer-20261021/validation-report.md) · [Raw sources, results and evidence download instructions](https://github.com/jixuan1989/tsfile-apache/tree/146680b0eecc3db6501d46ed697d145db462baef/issue-evidence/table-field-filter/validation/maintainer-20261021)

<!-- /codex-maintainer-followup-20261021 -->

<details>
<summary>Historical implementation and validation through 249b0d51a / 历史提交说明与验证</summary>

Fixes #1025.

With a one-row aligned table (`time=1, v=42`), an always-false FIELD predicate currently returns the row without invoking the predicate. This change makes Java and C++ return zero rows and invoke their callbacks once; the null-filter and always-true controls still return the row.

### Why the current paths are wrong

`init_internal()` enables the aligned bulk path even when `field_filter` is non-null. That path copies decoded batches directly into the result and never evaluates the predicate. The scalar merge path also has an unfinished FIELD-filter condition: with a non-null filter, it neither appends nor advances the current row, so sparse selections can loop indefinitely.

### How the change preserves row semantics

* Non-null FIELD filters use individual column contexts and the existing timestamp merge path. The shared vector context exposes only its first current value through `get_current_value()`, so reusing that accessor for several FIELDs would silently bind the wrong values. The unfiltered shared-vector and bulk-copy paths stay enabled.
* Build a borrowed, typed view of the projected FIELDs at the candidate timestamp. Fields absent at that timestamp are NULL. Names are normalized and unique; their order is unspecified. The timestamp remains signed 64-bit, primitive access checks the exact type and byte length, and binary views preserve empty values and embedded NUL bytes.
* Evaluate before appending a row and before consuming OFFSET/LIMIT. Rejected rows, including the last row of a page, still advance all contexts at that timestamp. OFFSET/LIMIT therefore count matching rows across pages, chunks and devices. Accepted unfiltered rows keep their existing append/advance loop.
* Keep callback status separate from acceptance: `E_OK` plus `accepted=false` means reject; a nonzero status is an error. `RET_FAIL(expr)` assigns `ret` and tests `ret != E_OK`, so callback/read failures return their original error and the existing `TableResultSet` failure latch prevents resuming a partially consumed read as EOF.

### Predicate API and boundaries

Add `TableFieldFilter::satisfy_row(const TableFieldRow&, bool&)` without changing `Filter`'s vtable. Its views are valid only during the callback. This avoids treating FIELDs as TAG string segments: the existing `satisfyRow(int, segments)` callback is for TAGs and also narrows timestamps to 32 bits.

Ordinary `Filter` subclasses remain usable for one selected integer/Boolean or string-like FIELD through their existing value overloads. NULL does not match these legacy predicates. Legacy FLOAT/DOUBLE or multiple-FIELD shapes return `E_NOT_SUPPORT`; use the typed row callback for those shapes and NULL-aware predicates. TAG filtering remains separate. Unprojected FIELD loading, predicate pushdown/vectorization, and new C/Python wrapper APIs are outside this change.

```cpp
struct Positive : storage::TableFieldFilter {
  int satisfy_row(const storage::TableFieldRow& row,
                  bool& accepted) const override {
    const auto* field = row.find("v");
    int64_t value = 0;
    accepted = field != nullptr && field->get(value) && value > 0;
    return common::E_OK;
  }
};
// query() owns the allocated predicate through the result reader.
executor.query("t", {"v"}, nullptr, nullptr, new Positive(), result);
```

### Review revision: aligned NULLs and time predicates

All three Copilot findings were reproduced against prior PR head `e2e9c3786f9753ec5d5c1b813fd2f1fb0d71d5b8`. Four new cases × six row/batch/parallel configurations failed before the revision (24/24) and pass afterward.

* An aligned value page's statistics cover non-NULL values only. Its last value timestamp can precede NULL timestamps still present in the shared time page. Page rejection now uses the shared time-page statistics only; an absent statistic conservatively keeps the page. For `(t0,42),(t1,NULL),(t2,NULL)`, a query restricted to `[t1,t2]` must still present both NULL rows to a NULL-aware FIELD predicate.
* The scalar BOOLEAN decoder previously appended a NULL before applying the time predicate. It now tests the decoded timestamp and backs off the provisional row before continuing when the time does not match. No value decoder advances for a NULL. This prevents an out-of-window NULL from reaching FIELD evaluation or consuming OFFSET/LIMIT.
* A sole all-NULL selected aligned FIELD has no value context. For a non-null FIELD predicate and an aligned value index with count zero, the reader now uses the existing time-only context to supply candidate timestamps and typed NULL values. Other empty-value queries retain the existing empty-result shortcut, including non-aligned sources and nonzero-value series eliminated by the time filter. Unfiltered behavior is unchanged.
* The Linux ASan CI failures were a separate test ownership error: TAG predicates are borrowed, so the combined-filter test now passes a stack-owned TAG predicate instead of leaking an allocation. The old test reproduced 480 leaked bytes in six allocations locally. Linux ASan/UBSan with leak detection enabled now passes the focused 74 tests and the full suite, with no suppressed sanitizer diagnostics.

The before/after C++ results on **both Java-written and C++-written files** are:

| Query | Prior PR C++ rows | Revised C++ rows | Java reference rows |
|---|---:|---:|---:|
| trailing NULLs, time window, `IS NULL` | 0 | 4 | 4 |
| nullable BOOLEAN, time window, accept-all | 6 | 4 | 4 |
| sole all-NULL FIELD, `IS NULL` | 0 | 28 | 28 |
| sole all-NULL FIELD, time/OFFSET/LIMIT | 0 | 2 | 2 |
| outside time window | 0 | 0 | 0 |

Twenty revised C++/Java own/cross-reader results match exactly. Ten prior-PR C++ reads are retained, including eight mismatches. Java performs native time filtering and projected reads, followed by application-level `IS NULL` and OFFSET/LIMIT; this is a result oracle, not a native Java FIELD callback performance baseline. Full source and actual row outputs are in the revision evidence.

### Validation after review

Base: `1180b13675e11a0230708af2cc70d037e0e12623`; previous PR head: `e2e9c3786f9753ec5d5c1b813fd2f1fb0d71d5b8`; revised head: `249b0d51a6bfe202185aa21b794ff21ccdfafcf3`.

* 74 focused tests pass: row/batch sizes 1 and 4, parallel on/off, typed/legacy predicates, NULL/binary/primitive boundaries, timestamp width, combined time/TAG/FIELD filtering, page/chunk/device transitions, OFFSET/LIMIT and terminal errors. The 24 new review regressions fail before and pass after.
* Windows Release: **979 passed**, 3 opt-in skipped; Linux GCC C++11 with all six optional codecs: **1000 passed**, 1 external-index skipped. Both have 10 pre-existing disabled tests.
* Linux Debug ASan/UBSan with leak detection: **74 focused and 999 full-suite tests passed**, 2 opt-in skipped and 10 pre-existing disabled. The full run validates the 135 fresh Java fixtures; C++ fixture generation is opt-in and disabled for this sanitizer run. No runtime-error or sanitizer diagnostics in the full log.
* Original 12 Java native callback own/cross-reads and 24 multi-type comparisons still match. Added 20 NULL-boundary comparisons match. With all six codecs enabled, C++ validates 135 Java fixtures and Java validates 117 C++ fixtures generated by this revision.
* Whole-PR changed/new executable lines: **87/89 (97.75%)**; branches **105/133 (78.95%)**. Review-only changed lines: **12/12 (100.00%)**; branches **20/24 (83.33%)**. Two whole-PR uncovered lines are defensive current-context error returns. GCC attributes generated decoder macro bodies to their expansion/physical lines; this is executable-line coverage, not a claim to cover every generated instruction. Source/copied-header hashes match; normal compiler branches are included without exclusions.

| Production file | Whole-file lines | Whole-file branches |
|---|---:|---:|
| `cpp/src/reader/aligned_chunk_reader.cc` | 1283/1651 (77.71%) | 998/1766 (56.51%) |
| `cpp/src/reader/block/single_device_tsblock_reader.cc` | 637/764 (83.38%) | 617/1024 (60.25%) |
| `cpp/src/reader/block/single_device_tsblock_reader.h` | 29/29 (100.00%) | 10/14 (71.43%) |
| `cpp/src/reader/filter/table_field_filter.cc` | 24/24 (100.00%) | 16/19 (84.21%) |
| `cpp/src/reader/filter/table_field_filter.h` | 16/16 (100.00%) | 19/20 (95.00%) |

Windows optional-codec fixture generation still has the documented untouched-baseline failure (336 matching assertion values), so compressed-file compatibility is validated by the all-codec Linux build. The earlier CRLF fixture-manifest normalization and unchanged 135 TsFile hashes remain documented in the original report. Explicit `"time"` projection remains an existing table-schema limitation; ordinary implicit timestamps and TAG-only projection are tested.

### Query performance after review

Query and write scope are reported separately. This revision changes reader paths and test ownership only; no writer, encoder, Java source or on-disk format changed. Existing write results are retained, and writing was not retimed for this reader revision.

**Existing eight query cases: develop base versus revised head.** Same verified 300,000-row × 8 INT64 PLAIN/UNCOMPRESSED files, same MSVC Release static configuration, eight fully consumed/checksummed queries per process, two warmups then 25 alternating process pairs, CPU affinity mask 4. The p95 below is **process time for eight queries**, not individual-request p95. Timing includes open/setup/read/checksum/cleanup; no cold-cache claim. The original initial and 300-pair confirmation measurements remain linked and preserved.

| Case | After / baseline median paired latency | 95% bootstrap interval | Baseline / after p95 (s) |
|---|---:|---|---|
| `all_row` | 1.0063 | [0.9976, 1.0118] | 0.355794 / 0.363827 |
| `all_batch` | 0.9961 | [0.9867, 1.0109] | 0.145429 / 0.148665 |
| `time_row` | 0.9986 | [0.9876, 1.0118] | 0.238007 / 0.240857 |
| `time_batch` | 0.9912 | [0.9796, 1.0050] | 0.099348 / 0.098299 |
| `offset_row` | 0.9948 | [0.9759, 1.0025] | 0.163547 / 0.159783 |
| `offset_batch` | 0.9915 | [0.9769, 0.9984] | 0.118996 / 0.112900 |
| `sparse_row` | 0.9906 | [0.9869, 1.0000] | 0.676885 / 0.685464 |
| `sparse_batch` | 0.9861 | [0.9806, 0.9946] | 0.469320 / 0.488395 |

**FIELD selectivity and projection: prior PR head versus revised head.** Thirty cases cover 1/4/8 projected FIELDs, 0/1/10/50/100% accepted rows and row/batch-1024 APIs. The identical dense file has 40,000 rows × 8 INT64 PLAIN/UNCOMPRESSED fields. Prior PR head correctly executes the same native callback on these non-NULL inputs, so it is a valid baseline for this revision's filtering cost. The upstream ignored/hanging implementation is not used as an equivalent filtering baseline.

Two warmups and 25 alternating process pairs per case, four queries/process, CPU affinity mask 4; every cell, returned row count, checksum and 160,000 callbacks/process are checked. Raw per-query arrays provide file-open time, metadata/query-plan time, first-row time (unavailable at 0% results), complete query latency and throughput; peak working set is the **whole process**, not incremental query memory. Per-query p50/p95 use 100 queries per variant/case clustered in 25 processes; bootstrap ratios resample the 25 process pairs. No P99 or controlled cold-cache result is claimed.

| Case | After / baseline median paired latency | 95% bootstrap interval | Baseline / after p95 (s) |
|---|---:|---|---|
| `fields1_accept0_row` | 1.0005 | [0.9896, 1.0116] | 0.004989 / 0.004881 |
| `fields1_accept0_batch` | 0.9924 | [0.9872, 1.0163] | 0.004910 / 0.004868 |
| `fields1_accept1_row` | 1.0029 | [0.9957, 1.0232] | 0.004834 / 0.004927 |
| `fields1_accept1_batch` | 0.9968 | [0.9735, 1.0231] | 0.004832 / 0.004854 |
| `fields1_accept10_row` | 0.9925 | [0.9806, 1.0049] | 0.004905 / 0.004824 |
| `fields1_accept10_batch` | 0.9946 | [0.9843, 1.0110] | 0.004938 / 0.004938 |
| `fields1_accept50_row` | 1.0046 | [0.9850, 1.0148] | 0.005369 / 0.005270 |
| `fields1_accept50_batch` | 0.9960 | [0.9911, 1.0135] | 0.005241 / 0.005232 |
| `fields1_accept100_row` | 0.9992 | [0.9847, 1.0109] | 0.005555 / 0.005555 |
| `fields1_accept100_batch` | 0.9945 | [0.9889, 1.0036] | 0.005469 / 0.005533 |
| `fields4_accept0_row` | 0.9933 | [0.9833, 1.0133] | 0.013445 / 0.013155 |
| `fields4_accept0_batch` | 0.9872 | [0.9834, 0.9998] | 0.013141 / 0.012938 |
| `fields4_accept1_row` | 1.0021 | [0.9906, 1.0222] | 0.013353 / 0.013523 |
| `fields4_accept1_batch` | 1.0000 | [0.9879, 1.0123] | 0.013175 / 0.013138 |
| `fields4_accept10_row` | 1.0024 | [0.9858, 1.0156] | 0.013289 / 0.013406 |
| `fields4_accept10_batch` | 1.0141 | [0.9972, 1.0225] | 0.013354 / 0.013456 |
| `fields4_accept50_row` | 1.0032 | [0.9889, 1.0095] | 0.014865 / 0.014117 |
| `fields4_accept50_batch` | 0.9923 | [0.9789, 1.0169] | 0.014246 / 0.014134 |
| `fields4_accept100_row` | 0.9903 | [0.9761, 1.0012] | 0.015026 / 0.014867 |
| `fields4_accept100_batch` | 0.9990 | [0.9912, 1.0087] | 0.014602 / 0.014524 |
| `fields8_accept0_row` | 0.9988 | [0.9910, 1.0069] | 0.025107 / 0.025277 |
| `fields8_accept0_batch` | 0.9940 | [0.9875, 1.0029] | 0.025044 / 0.024810 |
| `fields8_accept1_row` | 0.9993 | [0.9924, 1.0069] | 0.025470 / 0.025153 |
| `fields8_accept1_batch` | 0.9935 | [0.9835, 1.0070] | 0.025466 / 0.024971 |
| `fields8_accept10_row` | 1.0002 | [0.9922, 1.0070] | 0.025557 / 0.025438 |
| `fields8_accept10_batch` | 0.9988 | [0.9831, 1.0175] | 0.025595 / 0.025505 |
| `fields8_accept50_row` | 1.0039 | [0.9990, 1.0112] | 0.026570 / 0.027005 |
| `fields8_accept50_batch` | 0.9955 | [0.9872, 1.0077] | 0.027299 / 0.027576 |
| `fields8_accept100_row` | 0.9990 | [0.9901, 1.0060] | 0.028741 / 0.028654 |
| `fields8_accept100_batch` | 0.9900 | [0.9725, 0.9971] | 0.028858 / 0.027890 |

Full metrics and every initial sample, including outliers, are retained in `field-query-performance.json` and `existing-query-performance.json`. NULL/page/chunk/device and parallel boundaries are covered by correctness tests; the new FIELD timing matrix is dense, one-device, single-reader, uncompressed. It does not measure a TAG selectivity matrix, FIELD-filtered sparse/NULL latency, non-aligned FIELD performance, compressed-query performance, or parallel scaling. Those scopes remain explicitly unmeasured. Original and revised query comparisons do not prove universal Java/C++ performance equivalence.

No case in either new dataset has its paired-median 95% interval wholly above 1. The measured scope shows no statistically clear slowdown; this does not establish an absolute absence of regressions or a p95 non-inferiority guarantee. Individual higher p95 samples and outliers are preserved in the tables and raw data.

[Review revision validation report](https://github.com/jixuan1989/tsfile-apache/blob/0c9b74499e362321b62e27f21f97df61fdc3f378/issue-evidence/table-field-filter/validation/review-null-rows/validation-report.md) · [Revision sources, scripts, raw logs and measurements](https://raw.githubusercontent.com/jixuan1989/tsfile-apache/0c9b74499e362321b62e27f21f97df61fdc3f378/issue-evidence/table-field-filter/validation/review-null-rows/validation-evidence.zip)

[Original validation report](https://github.com/jixuan1989/tsfile-apache/blob/f93a65a0bab8cd0fda3f255fb7f8b95f74beb3d9/issue-evidence/table-field-filter/validation/validation-report.md) · [Original evidence, including all initial and confirmation performance samples](https://raw.githubusercontent.com/jixuan1989/tsfile-apache/f93a65a0bab8cd0fda3f255fb7f8b95f74beb3d9/issue-evidence/table-field-filter/validation/validation-evidence.zip)

</details>

</details>

</details>

Authorship clarification: the original implementation and validation were written by OpenAI Codex; subsequent maintainer commits, including `fcab7437`, retain their Git authorship. The original required disclosure is preserved below.

作者说明：原始实现及验证由OpenAI Codex编写；后续维护者提交（含 `fcab7437`）保留各自Git作者归属。以下保留原有规定的AI说明。

</details>

Authorship: OpenAI Codex wrote the original PR and this unsubmitted local repair; maintainer commits including publicfcab retain their Git authorship. The required original disclosure follows.

作者说明：OpenAI Codex编写原PR和本次未提交本地修补；包括公开fcab在内的维护者提交保留Git作者归属。以下保留规定的原AI说明。

</details>

Authorship:maintainerc8b retains its Git author;OpenAI Codex authored originalPR and unsubmitted local5db.

作者归属：维护者c8b保留Git作者，OpenAI Codex编写原PR及未提交本地5db。

</details>

Authorship: maintainer c01 retains its Git author; OpenAI Codex authored the original PR and this validation/reply.

作者归属：维护者c01保留Git作者，OpenAI Codex编写原PR及本轮验证/回复。

</details>

Maintainer commits retain Git authorship; OpenAI Codex authored validation/reply.

维护者提交保留Git作者，OpenAI Codex编写验证/回复。

**AI disclosure:** The implementation, tests and description in this pull request were written by an AI coding agent (OpenAI Codex), which also performed the reported local validation.

**AI 使用说明：** 本 PR 的代码修改、测试和正文由 AI 编程代理（OpenAI Codex）编写，文中报告的本地验证也由该 AI 代理执行。
