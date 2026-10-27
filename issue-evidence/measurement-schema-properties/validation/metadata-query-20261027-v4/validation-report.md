# PR01 metadata and OFFSET/LIMIT query validation — diagnostic scope

**English warning:** This fixed60-case round has 5 repeated primary comparison signals and 0 repeated same-reader copy/identity signals (counts of contrasts, not unique cases). All effects and pointwise intervals are retained below. A repeated signal is not a source cause; necessary/minimal extra cost is unproved. This report does not clear the expanded query gate or authorize a production revision/push. The historical16-case measured scope stays separate.

**中文性能说明：** 固定60场景中，主要比较有5项重复上升信号，同reader文件/镜像身份对照有0项重复上升信号（按比较项计数，非去重场景）。全部比值和逐项区间保留如下。重复信号不证明源码原因，必要最小额外成本未证实；本报告不解除扩展查询门槛或授权生产修订/推送。历史16场景仍独立保留。

Baseline `12e39fe9d9dace63cc0ad39664aa0fbf5e29f52f`; final `5fb363774ed7b492252d2933707545edca5ca981`. Production diff is the original one-line MeasurementSchema serializer fix; no new production changes. Original frozen MSVC static libraries plus matching baseline schema.h overlay were reused; helper-only builds are not fresh production/full-suite/coverage/sanitizer/write acceptance. Final4199-input protocol `9d92c0e81bfcb0fd3f6b85ae3951b012e365f667f1bf1f6c2f1e88d79712a7aa`; final integrity rechecked every input and clean source head. See protocol-notes-v4.md and full provenance/manifest.

18432 child processes, 55296 measured complete queries, 18432 complete excluded warmup queries; 203079168 measured returned rows and 779069952 measured non-NULL FIELD points. All raw outputs independently rechecked.24 initial blocks for60 cases; 18 cases selected once for48 new confirmation blocks. Two correlated crossed executable assignments per block, per-child first-of4 warmup excluded, median of measured3.12000 paired-block bootstrap pointwise95%, no familywise correction/equivalence/causality or pooling. Initial-only and confirmation-only effects retained; no extensions.

## Comparison scope and results

BA/FA/BB/FB are baseline-A/fixed-A/baseline-B/fixed-B. reader_A=FA/BA, reader_B=FB/BB, crossed_A_B=FB/BA. Empty-property A/B old/new writer files have identical bytes; nonempty A/B both copy the same valid fixed-writer file. Four malformed old products/eight code6 negatives are excluded. Nonempty crossed comparison is reader+copy, never old-writer end-to-end. baseline_copy=BB/BA and fixed_copy=FB/FA hold reader fixed. baseline_identity/fixed_identity compare assignment1/0 within the same version across A/B; they include parent-path/basename/assignment effects, not a filename mechanism.

| Contrast | Repeated | Initial only | Confirmation only | Worst repeated confirmation ratio [pointwise95%] |
|---|---:|---:|---:|---|
| reader_A | 3 | 3 | 2 | 1.018810236 [1.003194774, 1.036945600] `f128-p64-a0-scan1-b1024-par0` |
| reader_B | 0 | 7 | 1 | — |
| crossed_A_B | 2 | 1 | 1 | 1.023036959 [1.010517284, 1.036602305] `f128-p64-a0-tag1-b0-par1` |
| baseline_copy | 0 | 2 | 2 | — |
| fixed_copy | 0 | 2 | 0 | — |
| baseline_identity | 0 | 3 | 0 | — |
| fixed_identity | 0 | 1 | 0 | — |

Every one of420 case/contrast rows, including non-significant estimates, is in comparisons-v4.tsv and report-metrics-v4.json. Initial/confirmation outputs are independent; raw process and assignment data are retained. No post-hoc layout tuning, CPU attribution or regression exception is claimed.

## Metrics, data and compatibility boundaries

16/0,16/64,128/64 FIELD/property sizes × two layouts × ten scan/time/TAG/slice/empty row/batch combinations. Two devices ×4096 timestamps;2048-row flushed chunks,127-point page cap, UNCOMPRESSED/PLAIN/FLOAT; projections1/8 fields include v0 anchor, internal NULL and all-NULL v7. Time1027–3077; TAG=d1 is50% of devices/rows; OFFSET4093/LIMIT11 crosses devices, OFFSET8195 empty. A limited result is completely consumed, not every file row. Time/TAG request parallel read, thread_count2; no scaling claim.

report-metrics-v4.json has every stage/case/role/assignment: open, first_schema_load, plan, first_result, close, full latency min/P50/P95/max and counts; rows/s, non-NULL FIELD points/s and whole-process PeakWorkingSet. Each raw4-query counter is divided by4 for per-query counts before measured3 accounting. Samples within process/block are correlated. Opening is handle/reader initialization; first schema timing includes lazy metadata load+lookup, not cached getter/isolated deserialization; plan may read other metadata. first_result is successful next readiness before checks: row or batch block, null for empty. Full includes result verification/cleanup, expected-vector allocation outside clock. Whole-process peak includes startup/oracle and all4queries; no query-only heap claim.

Final crossed-path qualification480 native and240 Java-file→C++ full queries passed. V3 hash-bound8 C++ products→Java and6 Java-own per-series reads directly validate metadata name/type/category/properties, every non-NULL point and NULL absence. This is a raw-series oracle, not native Java Table or original wide-projection acceptance, and no Java timing. Original oracle failed at32 requested→30 returned paths due nonaligned all-NULL v7 path bloom pruning; original failure/GBK stdout text-capture loss retained, later exact bytes/JVM UTF8 capture retained. There were no new production tests/coverage/sanitizer or write-throughput measurements.

Historical coverage only, not rerun: changed production line1/1=100%; serializer13/13 lines100%,10/18 branches55.56%; MeasurementSchema62/64 lines96.875%,32/54 branches59.26%; full schema.h249/259 lines96.14%,158/244 branches64.75%. Original write metrics remain unchanged/separate: empty serializer ratio0.999289538 [0.995451006,1.001920973], empty table writer0.991458638 [0.974894021,1.010871491]; nonempty comparisons use valid manual references, not invalid old output. No new writer throughput or module coverage acceptance inferred.

Unmeasured: controlled cold cache/P99/native FIELD selectivity/sole all-NULL projection/compressed queries/special float/general large-file or parallel scaling/all tree APIs/query-only memory. Ambient OS cache/no eviction, normal priority/noaffinity/shared host; executable copy balancing cannot prove all OS effects disappear. The old16-case round is not pooled. PR02 stopped directions, PR03 unresolved local candidate signals and issue04 per-issue approval remain unchanged.

## 中文完整说明

本轮未改生产源码，仍比较原基线与最终提交，复用已冻结MSVC Release旧静态库及匹配基线头文件覆盖，只新构建验证程序。18432个进程，共55296次正式完整查询和18432次固定排除预热；正式返回203079168行及779069952个非NULL FIELD点，全部原始值/顺序/NULL/count/checksum复核。初测60场景各24块，按七项预定比较逐项下界>1一次选18场景另48块确认，两套交换assignment在块内聚合，仅块bootstrap，不将进程内3次或assignment冒充独立样本；逐项95%无多重校正、等价性或因果承诺。420条比较及所有分项/P50/P95/吞吐/峰值和各自样本数量见JSON/TSV，初测单独/确认单独及所有对照上升保留，禁止扩样或混历史16轮。

空属性A/B为原/新writer字节相同文件；非空旧writer的四个损坏产物及8次code6负控不计时，A/B同为有效新writer副本，不能叫旧writer端到端。reader_A/B和crossed关系如上；两个copy对照固定reader，两个identity对照比较同版本不同assignment，含父路径/文件名/先后组合影响，不能仅归为文件名。重复未解释增幅及必要成本均未闭环，查询/生产提交/写入门槛不因该诊断通过，不进行盲目布局修改或生产推送。

范围为16/0、16/64、128/64字段/属性、对齐与非对齐、扫描/时间/TAG/跨设备OFFSET/LIMIT及空结果、行/批接口；投影1或8字段包含v0锚点、内部NULL和全NULL v7。两设备各4096时间戳、2048行chunk及127点页上限；UNCOMPRESSED/FLOAT/PLAIN。时间1027–3077、TAG50%设备/行、OFFSET4093/LIMIT11及8195空结果。完整消费受限结果不表示返回全文件。并行只请求时间/TAG启用、thread_count2，不代表一般扩展性。

open仅打开/reader初始化；first_schema_load是懒加载及查找，不是缓存getter或独立反序列化。plan可能继续读元数据。首结果为next成功后的行/块就绪、核值前，空结果null；full包括逐值核对和资源清理，expected-vector分配在计时外。进程4-query累计点先除4求每query，再统计正式3次。整体峰值含启动、oracle和全部4次，不能叫查询专属内存。环境为共享Windows主机、普通优先级、无affinity、OS缓存无清空/冷保证。

新最终路径资格480次原生及240次Java文件→C++通过；V3同文件/字节码8个C++产物→Java及6次Java自读为逐序列与NULL缺席参考，并直接核schema名字/类型/类别/属性，不是Java原生Table/原wide投影验收或Java计时。原32→30全NULL路径bloom裁剪导致的oracle失败、最初GBK stdout丢失及之后原始字节日志完整保留。新全生产测试、覆盖率、sanitizer及写吞吐均未做，历史数据不挪为新结果。历史改动行1/1=100%；serializer13/13行100%、10/18分支55.56%；类62/64行96.875%、32/54分支59.26%；schema.h249/259行96.14%、158/244分支64.75%。历史空serializer比0.999289538、空表writer0.991458638及各自上列区间单独保留，非空比较只对有效人工参考，非无效旧输出，不代表新writer吞吐通过。

仍未测冷缓存/P99/FIELD原生过滤命中率/单独全NULL投影/压缩/特殊浮点/一般大文件与并行扩展/所有树接口/查询专属内存。旧16独立不混合，PR02停止方向、PR03本地未解信号及issue04逐条审批不变。两实际独立模型的协议/最终审阅记录附于pre-submission-review，不能代替真实实验或追认历史PR通过新门槛。

**AI disclosure:** The implementation, tests and description in this pull request were written by an AI coding agent (OpenAI Codex), which also performed the reported local validation.

**AI 使用说明：** 本 PR 的代码修改、测试和正文由 AI 编程代理（OpenAI Codex）编写，文中报告的本地验证也由该 AI 代理执行。
