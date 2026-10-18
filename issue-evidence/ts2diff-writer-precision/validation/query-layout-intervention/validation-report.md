# PR #1024: four-image crossover and private function-order experiment

Source head: `75592b89d1523a96090e8bca1dcb4cd2180162e5`. Production source is unchanged and clean. **The query gate remains uncleared.** This diagnostic cannot turn the original production binaries into passing artifacts. It retains all earlier sessions, including the three corrected-matrix residuals (+1.06%, +1.27%, +0.45% end-to-end).

## Protocol and scope

The three selected cases are the previously retained DOUBLE aligned precision-2 scenarios: dense scan with four projected fields in row and 1024-row batch modes, and a sparse file with one projected anchor field and a 50% application predicate. The anchor has no NULLs; other fields in that file do. Application filtering consumes and verifies the complete native scan; it is not FIELD pushdown. Two devices, 65,536 input rows, 256-row pages and multiple chunks use the same earlier fixtures. Baseline/fixed writer products in ALL THREE cases are SHA-256 and byte identical. Their earlier Java audit is retained; no new Java run is claimed.

Each stage fixes 192 matched rounds/scenario, four images/round and three complete verified queries/child. CPU affinity mask12 is applied before the initial thread resumes (logical CPUs2,3, SMT siblings on one physical core); pool2, parallel=false, warm filesystem cache. Interactive-host power/background is not controlled. All four executable payloads rotate over the SAME four neutral paths every eight-round block; every path carries every payload six times. Query inputs use one common file identity/scenario. After each copy block, each image/scenario gets two untimed warmups. Round/image and scenario positions are balanced. No sample trimming, adaptive extension or relaxed margin.

Two stages total 4,608 measured children / 13,824 checked queries, plus 1,152 separately excluded warmup children. Every timestamp, NULL, value, ordering, row count and checksum is verified. Full latency includes open/internal metadata, query construction, complete materialization/verification/application filtering, destruction and close. Ratios use the median of 24 chronological block medians, eight matched rounds/block; 20,000 fixed-seed bootstrap draws. Interaction is formed per matched round before block aggregation. Ratios below use F/B (fixed/baseline); values above1 are slower. These diagnostic intervals are not proof of equivalence when they include1, and are not multiplicity-adjusted.

## Stage1: all four original images on common neutral identities

The original combined writer/reader images and single-object reader-only images are unchanged. The primary interaction compares mixed F/B against reader-only F/B in the same matched rounds. This corrects the earlier caller test's separate image paths.

| Scenario | mixed F/B | reader_only F/B | mixed/reader_only interaction |
|---|---|---|---|
| dense row | 1.009011 [1.003393, 1.013019] | 1.002614 [0.997474, 1.005238] | 1.009160 [0.998831, 1.014704] |
| dense batch | 1.010039 [1.006835, 1.014846] | 1.002685 [1.000028, 1.006105] | 1.007309 [1.002259, 1.014690] |
| sparse app50 batch | 1.004146 [1.000907, 1.008777] | 0.998178 [0.993810, 1.000551] | 1.003081 [0.995447, 1.012515] |

The dense batch primary interval is above1. Row and sparse interactions include1. This establishes a measured caller/link-contents dependence for dense batch under this protocol; it does not prove that all reader-only costs are zero or that only the mixed caller can show a signal.

## Stage2: private three-function order intervention

Reuse the EXACT original mixed caller objects and baseline/fixed static libraries. Relink with the same three decorated query-function names in `/ORDER`: `TableResultSet::next`, `DoubleTS2DIFFDecoder::read_batch_double`, `DoubleTS2DIFFDecoder::read_double`. There is no source edit or recompilation. The selected RVAs become equal across versions: `0x76d0`, `0x7720`, `0x7910`. Original RVAs and the new map files are retained. [Microsoft documents /ORDER as controlling COMDAT function placement](https://learn.microsoft.com/en-us/cpp/build/reference/order-put-functions-in-order?view=msvc-170).

Original and ordered baseline/fixed images share the same four counterbalanced paths. The primary interaction is original F/B divided by ordered F/B. Other function/data locations and relocations can change with relinking; this does not isolate an individual hardware-cache or branch-predictor mechanism. No hardware counters or loaded image bases were collected. A private benchmark link option is not an upstream production repair and cannot establish no regression for other builds/workloads.

| Scenario | original F/B | ordered F/B | original/ordered interaction |
|---|---|---|---|
| dense row | 1.008783 [1.002322, 1.012308] | 1.012057 [1.008611, 1.014287] | 0.996571 [0.991203, 1.000537] |
| dense batch | 1.009181 [1.006200, 1.013389] | 1.014273 [1.011184, 1.017978] | 0.993632 [0.989698, 0.999289] |
| sparse app50 batch | 1.000906 [0.997488, 1.004979] | 1.000027 [0.997172, 1.004156] | 1.001576 [0.992421, 1.005009] |

The intervention failed to eliminate the dense-query cost. Dense batch ordered F/B is 1.014273 [1.011184, 1.017978], versus original 1.009181 [1.006200, 1.013389]. The original/ordered interaction interval is wholly below1: the relative penalty increases under this intervention. Dense row ordered F/B also remains above1; its interaction includes1. Sparse intervals include1, which does not establish equivalence. Equalizing these three function RVAs is therefore insufficient. No production change follows from this experiment, and no further layout/padding search is justified without a new profile-based hypothesis.

## Absolute query metrics

Raw JSON retains every sample: open, cached metadata lookup, plan construction, first decoded row, first accepted row, complete latency, process peak working set and main-thread lifetime cycles. The latter covers startup/printing/exit and is not query-only cycles or retired instructions. P95 is descriptive, not an inferential tail guarantee. Cold cache, P99, compressed files, broad parallel scaling, special-value latency and the other previously stated unmeasured scopes remain untested. No new production coverage/full unit/ASan/write-throughput results are claimed; earlier correctness, bidirectional compatibility, coverage and write results retain their original scope.

| Stage | Scenario | Variant | Full p50 ms | Full p95 ms | Decoded rows/s | Process peak working set median MiB |
|---|---|---|---:|---:|---:|---:|
| joint | dense row | mixed_baseline | 3.3717 | 4.2732 | 19436792 | 5.434 |
| joint | dense row | mixed_fixed | 3.3965 | 4.2967 | 19295441 | 5.418 |
| joint | dense row | reader_only_baseline | 3.3566 | 4.2207 | 19524519 | 5.357 |
| joint | dense row | reader_only_fixed | 3.3674 | 4.2432 | 19461899 | 5.355 |
| joint | dense batch | mixed_baseline | 2.8289 | 3.7232 | 23167011 | 5.434 |
| joint | dense batch | mixed_fixed | 2.8626 | 3.7504 | 22894273 | 5.418 |
| joint | dense batch | reader_only_baseline | 2.8301 | 3.6888 | 23156779 | 5.352 |
| joint | dense batch | reader_only_fixed | 2.8321 | 3.7145 | 23140426 | 5.359 |
| joint | sparse app50 batch | mixed_baseline | 1.2329 | 2.1097 | 53158134 | 5.371 |
| joint | sparse app50 batch | mixed_fixed | 1.2352 | 2.1066 | 53056995 | 5.359 |
| joint | sparse app50 batch | reader_only_baseline | 1.2308 | 2.0766 | 53246669 | 5.297 |
| joint | sparse app50 batch | reader_only_fixed | 1.2291 | 2.0756 | 53320316 | 5.301 |
| order | dense row | original_baseline | 3.3556 | 4.2396 | 19530338 | 5.434 |
| order | dense row | original_fixed | 3.3825 | 4.2811 | 19374732 | 5.422 |
| order | dense row | ordered_baseline | 3.4434 | 4.3208 | 19032628 | 5.426 |
| order | dense row | ordered_fixed | 3.4914 | 4.4439 | 18770425 | 5.424 |
| order | dense batch | original_baseline | 2.8250 | 3.7089 | 23198584 | 5.438 |
| order | dense batch | original_fixed | 2.8522 | 3.7328 | 22976948 | 5.418 |
| order | dense batch | ordered_baseline | 2.9125 | 3.7955 | 22501631 | 5.430 |
| order | dense batch | ordered_fixed | 2.9581 | 3.8551 | 22154387 | 5.426 |
| order | sparse app50 batch | original_baseline | 1.2291 | 2.0796 | 53322489 | 5.373 |
| order | sparse app50 batch | original_fixed | 1.2329 | 2.0994 | 53158130 | 5.359 |
| order | sparse app50 batch | ordered_baseline | 1.2516 | 2.1193 | 52359685 | 5.367 |
| order | sparse app50 batch | ordered_fixed | 1.2591 | 2.1077 | 52049877 | 5.367 |

## 中文说明

本轮没有修改 PR 源码。三个残留场景的输入文件在修复前后逐字节相同，可排除文件内容/大小变化。第一阶段把四个原程序放到共同的中性路径上轮换；密集 DOUBLE 批查询的调用程序交互区间高于1，行查询和稀疏场景的交互区间包含1，不能把后者解释为已证明性能等价。

第二阶段仅在私有诊断构建中重排三个查询函数，使修复前后热点函数地址一致；目标文件和静态库复用原件。表中保留原始构建与重排构建的比率、交互区间和全部原始样本。其他代码/数据位置也随链接变化，不能直接归因于某个硬件缓存机制。这个实验并非上游实现修复，不能据此把查询门槛标成通过，也不能丢弃先前测到的退化。

这次干预失败：密集批查询原构建的相对成本约+0.92%，重排后约+1.43%，交互区间表明相对代价进一步增大；行查询重排后也仍有增大信号，稀疏查询区间包含1但未证明等价。三个热点的地址一致仍不足以消除问题，不应继续盲目搜索 padding/排列参数。下一步应根据实际查询采样/计数器提出新的可检验原因，再选择有维护价值的源码修改。

两阶段共4608个计时子进程、13824次完整查询，另有1152个预热子进程。每次均完整消费并核对结果。CPU设置、缓存状态、统计方法、吞吐、内存和未测范围见上文；没有新增完整 Java/单测/ASan/覆盖率/写入性能验证的声明。

**AI disclosure:** The implementation, tests and description in this pull request were written by an AI coding agent (OpenAI Codex), which also performed the reported local validation.

**AI 使用说明：** 本 PR 的代码修改、测试和正文由 AI 编程代理（OpenAI Codex）编写，文中报告的本地验证也由该 AI 代理执行。
