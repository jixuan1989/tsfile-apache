# TsFile PR #1024: query performance backfill

Baseline `1180b13675e11a0230708af2cc70d037e0e12623`; tested PR head `75592b89d1523a96090e8bca1dcb4cd2180162e5`. No production code or new upstream source commit was made for this backfill. Existing correctness, bidirectional interoperability, coverage and write-performance results remain in the earlier reports, with their original limits. This follow-up adds query timings rather than treating untimed readback as performance evidence.

## 数据与独立校验

Each file contains 2 devices × 32,768 rows × 4 FLOAT/DOUBLE FIELDs, plus a STRING TAG in table metadata. The writer flushes every 8,192 rows/device (4 value chunks per field/device; 32 value chunks/file). Page limit is 256 rows. Java independently reads every value, NULL position, timestamp and type, and audits actual chunk compression, page count and precision. Dense/aligned files have 1,024 value pages; sparse non-aligned files have 976. All values use UNCOMPRESSED; the time codec is also configured UNCOMPRESSED. Multi-device aligned/non-aligned files carry an explicit table schema and are queried through the native table row/batch APIs; this is not a benchmark of every tree-query API.

Nullable FIELDs v1–v3 omit `(row+column)%11==0`; v0 remains present as the row anchor. Precision-2 data uses exact `.25` fractions; precision-0 data uses integer-valued inputs, so the original default-2 writer and revised precision-0 writer return identical logical values. Both versions write their own products; both reader versions fully read each valid product before timings. Across this backfill there are 29 valid C++ products audited in Java and 58 successful native cross/own read preflights. The single malformed original property-file control is expected to fail in both readers and is excluded from timing.

## 测量定义与条件

MSVC 14.50 Release/static, identical native driver source/options, threads enabled, two-worker pool, optional codecs/ANTLR/SIMD disabled. Two warmups per variant then **32 independent position-balanced process quartets** (pairs for the one valid property-file comparison). Each process runs 3 complete queries, so per-query p50/p95 use **96 queries clustered in 32 processes**, not 96 independent processes. The bootstrap median latency ratios resample processes. Every label occupies every execution position equally. Full-result latency includes open/header/footer initialization, explicit schema lookup, query setup, decoded-cell validation/materialization, optional application filtering, result destruction and close. Fixture generation and process startup are excluded.

`open_seconds` measures `TsFileReader::open`, including its internal initialization; `metadata_seconds` measures the subsequent native schema lookup and may reuse metadata loaded during open. `plan_seconds` is query construction. `first_decoded_row_seconds` measures first native row/block availability. `first_row_seconds` measures the first accepted, validated application row (N/A for app0). Full query latency, decoded/accepted row throughput, projected-cell throughput and whole-process peak working set are retained. Peak memory includes the process/thread pool and is not incremental query allocation. Filesystem cache is warmed; fresh processes do not establish cold-cache measurements. No P99, controlled cold-cache, or p95 non-inferiority guarantee is claimed.

The initial mixed driver uses affinity mask 12 (two logical CPUs) for all cases. Parallel read configuration is reported in each scenario; this is not a general parallel-scaling study. The later reader-only controls below refine caller/CPU placement explicitly.

Native TAG equality selects device d1 (50% of input rows); the time window is `[8195,24581]`. `app0`, `app1`, `app50` apply `floor(v0/8)%100 < percent` **after fully materializing and validating the native scan**. Their cost includes reading all input rows/cells. The old native FIELD paths ignored the predicate or hung, so those paths are not used as an equivalent fast filtering baseline. Application filtering is clearly a materializing reference, not native predicate pushdown. Both input and accepted counts/checksums are independently checked in Python; every cell is also checked in the driver.

## 原始顺序检查

A first, interrupted attempt had an ordering bug (cyclic rotation followed by odd-round reversal). For two variants it always ran baseline first; four variants also did not occupy all positions evenly. These samples and their original script/plan are preserved under `protocol-order-initial/` and are **not used for the performance conclusions**. The replacement 32-round order is checked for equal label/position counts before measurement. No samples or outliers from the valid replacement runs are removed.

## 原有 writer + reader 混合程序结果

Ratios below are fixed/baseline; brackets are process-cluster bootstrap 95% intervals. The columns separately isolate reader cost on an identical baseline/fixed file, changed writer product cost through the fixed reader, and end-to-end original-writer/original-reader versus revised-writer/revised-reader cost.

| Scenario | Reader on baseline file | Reader on fixed file | Writer products, fixed reader | End-to-end |
|---|---|---|---|---|
| `FLOAT_aligned_p2_null0_props0_all_w4_row_parallel0` | 0.9700 [0.9680, 0.9764] | 0.9745 [0.9710, 0.9774] | 1.0015 [0.9986, 1.0058] | 0.9728 [0.9679, 0.9760] |
| `FLOAT_aligned_p2_null0_props0_all_w4_batch_parallel0` | 0.9667 [0.9628, 0.9730] | 0.9684 [0.9628, 0.9749] | 1.0018 [0.9958, 1.0049] | 0.9678 [0.9649, 0.9715] |
| `FLOAT_aligned_p0_null1_props0_time_w1_row_parallel1` | 0.9926 [0.9840, 1.0008] | 0.9833 [0.9766, 0.9949] | 0.9958 [0.9877, 1.0052] | 0.9911 [0.9819, 0.9986] |
| `FLOAT_aligned_p0_null1_props0_time_w1_batch_parallel1` | 0.9795 [0.9718, 0.9972] | 0.9914 [0.9790, 1.0017] | 0.9924 [0.9840, 1.0020] | 0.9818 [0.9740, 0.9933] |
| `FLOAT_aligned_p0_null1_props0_app1_w4_row_parallel1` | 0.9794 [0.9667, 0.9967] | 0.9925 [0.9876, 1.0064] | 0.9238 [0.9047, 0.9296] | 0.8995 [0.8901, 0.9059] |
| `FLOAT_aligned_p0_null1_props0_app1_w4_batch_parallel1` | 0.9763 [0.9665, 0.9944] | 1.0041 [0.9968, 1.0103] | 0.9188 [0.9049, 0.9264] | 0.8986 [0.8876, 0.9108] |
| `FLOAT_nonaligned_p2_null0_props0_all_w4_row_parallel0` | 0.9877 [0.9759, 1.0053] | 0.9887 [0.9715, 0.9977] | 1.0002 [0.9900, 1.0119] | 0.9896 [0.9826, 1.0001] |
| `FLOAT_nonaligned_p2_null0_props0_all_w4_batch_parallel0` | 0.9865 [0.9725, 0.9907] | 0.9981 [0.9819, 1.0062] | 1.0070 [0.9958, 1.0137] | 0.9951 [0.9810, 1.0032] |
| `FLOAT_nonaligned_p0_null1_props0_time_w1_row_parallel1` | 0.9909 [0.9792, 0.9976] | 0.9945 [0.9846, 0.9980] | 0.9965 [0.9907, 1.0016] | 0.9863 [0.9800, 0.9976] |
| `FLOAT_nonaligned_p0_null1_props0_time_w1_batch_parallel1` | 1.0011 [0.9878, 1.0220] | 0.9974 [0.9884, 1.0112] | 0.9949 [0.9866, 1.0059] | 0.9920 [0.9885, 1.0014] |
| `FLOAT_nonaligned_p0_null1_props0_app1_w4_row_parallel1` | 0.9775 [0.9727, 0.9933] | 0.9901 [0.9848, 0.9980] | 0.9763 [0.9610, 0.9893] | 0.9611 [0.9524, 0.9686] |
| `FLOAT_nonaligned_p0_null1_props0_app1_w4_batch_parallel1` | 0.9887 [0.9756, 0.9973] | 0.9784 [0.9751, 0.9844] | 0.9691 [0.9660, 0.9783] | 0.9603 [0.9564, 0.9674] |
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` | 1.0063 [1.0018, 1.0113] | 1.0042 [0.9995, 1.0072] | 0.9999 [0.9961, 1.0038] | 1.0064 [1.0014, 1.0123] |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` | 1.0058 [1.0013, 1.0112] | 1.0059 [1.0017, 1.0078] | 0.9983 [0.9945, 1.0036] | 1.0017 [0.9989, 1.0061] |
| `DOUBLE_aligned_p0_null1_props0_time_w1_row_parallel1` | 0.9959 [0.9919, 1.0036] | 0.9991 [0.9927, 1.0108] | 1.0005 [0.9900, 1.0090] | 0.9977 [0.9931, 1.0040] |
| `DOUBLE_aligned_p0_null1_props0_time_w1_batch_parallel1` | 0.9997 [0.9938, 1.0039] | 0.9963 [0.9848, 1.0091] | 0.9970 [0.9925, 1.0026] | 1.0006 [0.9911, 1.0049] |
| `DOUBLE_aligned_p0_null1_props0_app1_w4_row_parallel1` | 0.9905 [0.9802, 0.9974] | 1.0053 [0.9918, 1.0130] | 0.9252 [0.9148, 0.9478] | 0.9186 [0.9119, 0.9390] |
| `DOUBLE_aligned_p0_null1_props0_app1_w4_batch_parallel1` | 0.9992 [0.9877, 1.0113] | 1.0043 [0.9969, 1.0097] | 0.9120 [0.8991, 0.9216] | 0.9128 [0.8990, 0.9181] |
| `DOUBLE_nonaligned_p2_null0_props0_all_w4_row_parallel0` | 1.0013 [0.9907, 1.0096] | 0.9983 [0.9888, 1.0078] | 1.0046 [0.9872, 1.0096] | 1.0012 [0.9977, 1.0065] |
| `DOUBLE_nonaligned_p2_null0_props0_all_w4_batch_parallel0` | 0.9948 [0.9871, 1.0058] | 0.9978 [0.9872, 1.0061] | 1.0007 [0.9941, 1.0104] | 1.0009 [0.9848, 1.0084] |
| `DOUBLE_nonaligned_p0_null1_props0_time_w1_row_parallel1` | 0.9866 [0.9759, 1.0062] | 0.9957 [0.9879, 1.0003] | 0.9998 [0.9947, 1.0118] | 0.9902 [0.9840, 1.0031] |
| `DOUBLE_nonaligned_p0_null1_props0_time_w1_batch_parallel1` | 0.9958 [0.9875, 1.0043] | 0.9925 [0.9807, 1.0133] | 1.0053 [0.9970, 1.0139] | 0.9971 [0.9945, 1.0088] |
| `DOUBLE_nonaligned_p0_null1_props0_app1_w4_row_parallel1` | 0.9950 [0.9809, 1.0003] | 0.9977 [0.9880, 1.0010] | 0.9747 [0.9679, 0.9824] | 0.9631 [0.9588, 0.9737] |
| `DOUBLE_nonaligned_p0_null1_props0_app1_w4_batch_parallel1` | 0.9916 [0.9843, 0.9976] | 0.9919 [0.9871, 0.9990] | 0.9765 [0.9698, 0.9869] | 0.9659 [0.9563, 0.9761] |
| `FLOAT_aligned_p2_null1_props0_tag_w4_row_parallel1` | 0.9760 [0.9674, 0.9851] | 0.9819 [0.9708, 0.9862] | 1.0036 [0.9934, 1.0156] | 0.9793 [0.9712, 0.9857] |
| `FLOAT_aligned_p2_null1_props0_tag_w4_batch_parallel1` | 0.9756 [0.9606, 0.9850] | 0.9741 [0.9658, 0.9817] | 1.0033 [0.9920, 1.0095] | 0.9738 [0.9591, 0.9821] |
| `DOUBLE_nonaligned_p2_null1_props0_tag_w4_row_parallel0` | 0.9874 [0.9763, 1.0012] | 0.9944 [0.9859, 1.0071] | 1.0032 [0.9982, 1.0126] | 0.9944 [0.9868, 1.0018] |
| `DOUBLE_nonaligned_p2_null1_props0_tag_w4_batch_parallel0` | 0.9930 [0.9795, 0.9982] | 0.9916 [0.9816, 1.0029] | 0.9995 [0.9870, 1.0107] | 0.9897 [0.9786, 0.9969] |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_row_parallel0` | 0.9994 [0.9941, 1.0049] | 0.9970 [0.9856, 1.0075] | 1.0015 [0.9936, 1.0107] | 1.0037 [0.9945, 1.0100] |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_batch_parallel0` | 1.0009 [0.9925, 1.0064] | 1.0060 [1.0017, 1.0080] | 1.0000 [0.9909, 1.0108] | 1.0026 [0.9931, 1.0086] |
| `FLOAT_nonaligned_p0_null1_props0_app0_w1_row_parallel0` | 0.9874 [0.9796, 0.9916] | 0.9897 [0.9844, 0.9975] | 1.0031 [0.9987, 1.0104] | 0.9939 [0.9849, 1.0011] |
| `FLOAT_nonaligned_p0_null1_props0_app0_w1_batch_parallel0` | 0.9953 [0.9859, 1.0023] | 0.9910 [0.9782, 1.0049] | 0.9946 [0.9837, 1.0070] | 0.9904 [0.9750, 0.9997] |

| Scenario | Baseline / fixed full p50 (ms) | Baseline / fixed full p95 (ms) | Baseline / fixed first accepted p50 (ms) | Baseline / fixed peak working set median (MiB) |
|---|---|---|---|---|
| `FLOAT_aligned_p2_null0_props0_all_w4_row_parallel0` | 3.562 / 3.454 | 4.412 / 4.281 | 0.179 / 0.182 | 5.484 / 5.477 |
| `FLOAT_aligned_p2_null0_props0_all_w4_batch_parallel0` | 2.992 / 2.881 | 3.731 / 3.633 | 0.178 / 0.177 | 5.475 / 5.471 |
| `FLOAT_aligned_p0_null1_props0_time_w1_row_parallel1` | 0.907 / 0.895 | 1.641 / 1.645 | 0.142 / 0.141 | 5.383 / 5.355 |
| `FLOAT_aligned_p0_null1_props0_time_w1_batch_parallel1` | 0.785 / 0.765 | 1.528 / 1.500 | 0.146 / 0.145 | 5.371 / 5.361 |
| `FLOAT_aligned_p0_null1_props0_app1_w4_row_parallel1` | 13.440 / 11.900 | 14.302 / 13.277 | 1.049 / 0.879 | 6.193 / 6.176 |
| `FLOAT_aligned_p0_null1_props0_app1_w4_batch_parallel1` | 12.868 / 11.600 | 13.609 / 13.008 | 1.046 / 0.883 | 6.189 / 6.178 |
| `FLOAT_nonaligned_p2_null0_props0_all_w4_row_parallel0` | 15.283 / 15.154 | 16.327 / 16.128 | 0.428 / 0.424 | 5.521 / 5.541 |
| `FLOAT_nonaligned_p2_null0_props0_all_w4_batch_parallel0` | 14.818 / 14.664 | 15.654 / 16.505 | 0.428 / 0.429 | 5.531 / 5.525 |
| `FLOAT_nonaligned_p0_null1_props0_time_w1_row_parallel1` | 2.705 / 2.648 | 3.545 / 3.475 | 0.171 / 0.168 | 5.348 / 5.334 |
| `FLOAT_nonaligned_p0_null1_props0_time_w1_batch_parallel1` | 2.535 / 2.527 | 3.340 / 3.293 | 0.166 / 0.168 | 5.350 / 5.316 |
| `FLOAT_nonaligned_p0_null1_props0_app1_w4_row_parallel1` | 16.451 / 15.803 | 17.425 / 16.827 | 0.449 / 0.436 | 5.582 / 5.531 |
| `FLOAT_nonaligned_p0_null1_props0_app1_w4_batch_parallel1` | 15.805 / 15.131 | 16.686 / 16.210 | 0.446 / 0.433 | 5.553 / 5.490 |
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` | 3.350 / 3.367 | 4.122 / 4.117 | 0.163 / 0.167 | 5.441 / 5.422 |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` | 2.818 / 2.829 | 3.576 / 3.586 | 0.163 / 0.162 | 5.443 / 5.426 |
| `DOUBLE_aligned_p0_null1_props0_time_w1_row_parallel1` | 0.873 / 0.877 | 1.610 / 1.635 | 0.142 / 0.148 | 5.398 / 5.355 |
| `DOUBLE_aligned_p0_null1_props0_time_w1_batch_parallel1` | 0.747 / 0.743 | 1.480 / 1.481 | 0.143 / 0.140 | 5.393 / 5.355 |
| `DOUBLE_aligned_p0_null1_props0_app1_w4_row_parallel1` | 13.618 / 12.438 | 14.515 / 14.375 | 1.073 / 0.970 | 6.357 / 6.342 |
| `DOUBLE_aligned_p0_null1_props0_app1_w4_batch_parallel1` | 13.216 / 11.964 | 14.470 / 12.887 | 1.072 / 0.944 | 6.348 / 6.361 |
| `DOUBLE_nonaligned_p2_null0_props0_all_w4_row_parallel0` | 14.808 / 14.893 | 16.114 / 15.959 | 0.408 / 0.410 | 5.496 / 5.471 |
| `DOUBLE_nonaligned_p2_null0_props0_all_w4_batch_parallel0` | 14.296 / 14.277 | 15.596 / 15.593 | 0.407 / 0.403 | 5.488 / 5.467 |
| `DOUBLE_nonaligned_p0_null1_props0_time_w1_row_parallel1` | 2.620 / 2.601 | 3.456 / 3.385 | 0.170 / 0.166 | 5.352 / 5.312 |
| `DOUBLE_nonaligned_p0_null1_props0_time_w1_batch_parallel1` | 2.480 / 2.504 | 3.244 / 3.246 | 0.166 / 0.170 | 5.352 / 5.312 |
| `DOUBLE_nonaligned_p0_null1_props0_app1_w4_row_parallel1` | 16.125 / 15.581 | 17.253 / 16.495 | 0.461 / 0.450 | 5.492 / 5.449 |
| `DOUBLE_nonaligned_p0_null1_props0_app1_w4_batch_parallel1` | 15.445 / 15.007 | 16.492 / 16.282 | 0.434 / 0.430 | 5.492 / 5.445 |
| `FLOAT_aligned_p2_null1_props0_tag_w4_row_parallel1` | 6.765 / 6.625 | 7.575 / 7.436 | 1.055 / 1.010 | 6.133 / 6.139 |
| `FLOAT_aligned_p2_null1_props0_tag_w4_batch_parallel1` | 6.589 / 6.386 | 8.279 / 7.445 | 1.056 / 1.007 | 6.105 / 6.133 |
| `DOUBLE_nonaligned_p2_null1_props0_tag_w4_row_parallel0` | 8.110 / 8.015 | 8.894 / 8.834 | 0.433 / 0.438 | 5.490 / 5.469 |
| `DOUBLE_nonaligned_p2_null1_props0_tag_w4_batch_parallel0` | 7.888 / 7.817 | 9.024 / 8.579 | 0.439 / 0.436 | 5.494 / 5.465 |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_row_parallel0` | 1.469 / 1.474 | 2.179 / 2.190 | 0.118 / 0.119 | 5.379 / 5.361 |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_batch_parallel0` | 1.229 / 1.227 | 1.966 / 1.972 | 0.123 / 0.122 | 5.381 / 5.367 |
| `FLOAT_nonaligned_p0_null1_props0_app0_w1_row_parallel0` | 5.167 / 5.089 | 5.952 / 5.851 | N/A (zero accepted rows) | 5.340 / 5.311 |
| `FLOAT_nonaligned_p0_null1_props0_app0_w1_batch_parallel0` | 4.917 / 4.828 | 5.736 / 5.640 | N/A (zero accepted rows) | 5.334 / 5.311 |

## 初测信号与独立复测

Three initial DOUBLE cases triggered confirmation. With the **unchanged mixed caller and two-CPU affinity**, 192 independent quartets/case were then measured (3 queries/process). The primary confirmation CI resamples 24 chronological blocks of 8 complete order cycles. The two dense aligned DOUBLE full scans retain approximately 0.4–0.7% increases in some comparisons; the sparse application-filter case does not reproduce its initial signal. These observations are retained as **confirmed mixed-caller measurements**, not silently relabeled as passing.

| Case / contrast | Confirmatory block-median ratio [95% CI] |
|---|---|
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` / `reader_on_baseline_file` | 1.0028 [1.0000, 1.0050] |
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` / `reader_on_fixed_file` | 1.0072 [1.0055, 1.0091] |
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` / `writer_products_fixed_reader` | 1.0004 [0.9982, 1.0030] |
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` / `end_to_end` | 1.0041 [1.0030, 1.0056] |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` / `reader_on_baseline_file` | 1.0057 [1.0024, 1.0082] |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` / `reader_on_fixed_file` | 1.0051 [1.0028, 1.0065] |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` / `writer_products_fixed_reader` | 0.9978 [0.9967, 0.9995] |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` / `end_to_end` | 1.0040 [1.0011, 1.0062] |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_batch_parallel0` / `reader_on_baseline_file` | 0.9960 [0.9922, 1.0001] |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_batch_parallel0` / `reader_on_fixed_file` | 0.9968 [0.9946, 0.9993] |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_batch_parallel0` / `writer_products_fixed_reader` | 1.0002 [0.9983, 1.0061] |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_batch_parallel0` / `end_to_end` | 0.9950 [0.9922, 0.9978] |

## 查询代码与调用程序隔离

No reader/decoder source changed in PR #1024. For seven reader object files, the multisets of raw `.text` section payloads match (13,672 sections); this comparison is before relocation/linking and does **not** prove identical runtime addresses. The mixed caller also compiles writer/encoder helpers against different headers, so its linked code layout differs widely. A separate reader-only caller is compiled **once against baseline public reader headers**, then that exact same object is linked with each library. The two reader-only binaries have matching `.pdata` and only 60 differing bytes in their 491,008-byte `.text` sections; relocation targets/constants are not claimed identical.

The 32-case reader-only matrix pins serial cases to one logical CPU (mask 4); parallel-enabled cases retain mask 12. This changes both caller and serial CPU placement, so it is shown as a separate control rather than overwriting the mixed-caller data.

| Scenario | Reader on baseline file | Reader on fixed file | Writer products, fixed reader | End-to-end |
|---|---|---|---|---|
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` | 0.9995 [0.9955, 1.0050] | 0.9980 [0.9940, 1.0047] | 1.0028 [0.9991, 1.0090] | 1.0034 [0.9990, 1.0105] |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` | 0.9997 [0.9941, 1.0053] | 1.0053 [1.0002, 1.0105] | 1.0029 [0.9958, 1.0088] | 0.9998 [0.9962, 1.0061] |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_batch_parallel0` | 1.0000 [0.9956, 1.0058] | 1.0040 [0.9993, 1.0136] | 1.0072 [0.9959, 1.0142] | 1.0056 [0.9966, 1.0200] |
| `FLOAT_aligned_p2_null0_props0_all_w4_row_parallel0` | 0.9992 [0.9951, 1.0009] | 0.9989 [0.9947, 1.0028] | 1.0010 [0.9973, 1.0026] | 0.9995 [0.9939, 1.0015] |
| `FLOAT_aligned_p2_null0_props0_all_w4_batch_parallel0` | 0.9953 [0.9917, 0.9999] | 0.9993 [0.9965, 1.0018] | 1.0019 [0.9972, 1.0067] | 0.9974 [0.9949, 1.0021] |
| `FLOAT_aligned_p0_null1_props0_time_w1_row_parallel1` | 1.0000 [0.9940, 1.0049] | 0.9989 [0.9910, 1.0073] | 1.0040 [0.9917, 1.0078] | 0.9973 [0.9900, 1.0037] |
| `FLOAT_aligned_p0_null1_props0_time_w1_batch_parallel1` | 0.9923 [0.9848, 1.0064] | 1.0025 [0.9958, 1.0097] | 0.9987 [0.9872, 1.0069] | 0.9909 [0.9829, 0.9979] |
| `FLOAT_aligned_p0_null1_props0_app1_w4_row_parallel1` | 0.9942 [0.9853, 1.0004] | 0.9920 [0.9801, 1.0108] | 0.9149 [0.9055, 0.9190] | 0.9081 [0.8993, 0.9175] |
| `FLOAT_aligned_p0_null1_props0_app1_w4_batch_parallel1` | 0.9956 [0.9848, 0.9992] | 1.0050 [0.9954, 1.0151] | 0.9142 [0.9046, 0.9243] | 0.9029 [0.8930, 0.9106] |
| `FLOAT_nonaligned_p2_null0_props0_all_w4_row_parallel0` | 1.0077 [1.0003, 1.0207] | 0.9929 [0.9884, 1.0070] | 1.0038 [0.9858, 1.0116] | 1.0030 [0.9944, 1.0126] |
| `FLOAT_nonaligned_p2_null0_props0_all_w4_batch_parallel0` | 0.9951 [0.9842, 1.0127] | 0.9951 [0.9864, 1.0060] | 1.0002 [0.9900, 1.0090] | 0.9952 [0.9842, 1.0041] |
| `FLOAT_nonaligned_p0_null1_props0_time_w1_row_parallel1` | 0.9986 [0.9859, 1.0130] | 0.9973 [0.9906, 1.0008] | 0.9935 [0.9815, 1.0031] | 0.9916 [0.9801, 1.0011] |
| `FLOAT_nonaligned_p0_null1_props0_time_w1_batch_parallel1` | 0.9992 [0.9850, 1.0161] | 0.9993 [0.9906, 1.0070] | 0.9978 [0.9897, 1.0038] | 0.9998 [0.9858, 1.0175] |
| `FLOAT_nonaligned_p0_null1_props0_app1_w4_row_parallel1` | 0.9997 [0.9951, 1.0121] | 1.0004 [0.9883, 1.0048] | 0.9688 [0.9630, 0.9794] | 0.9760 [0.9657, 0.9865] |
| `FLOAT_nonaligned_p0_null1_props0_app1_w4_batch_parallel1` | 1.0044 [0.9981, 1.0110] | 1.0011 [0.9985, 1.0129] | 0.9769 [0.9629, 0.9859] | 0.9797 [0.9732, 0.9833] |
| `DOUBLE_aligned_p0_null1_props0_time_w1_row_parallel1` | 0.9988 [0.9893, 1.0035] | 1.0008 [0.9907, 1.0101] | 1.0023 [0.9904, 1.0108] | 0.9964 [0.9925, 1.0077] |
| `DOUBLE_aligned_p0_null1_props0_time_w1_batch_parallel1` | 1.0021 [0.9892, 1.0066] | 0.9940 [0.9895, 1.0045] | 0.9951 [0.9883, 1.0010] | 0.9989 [0.9890, 1.0055] |
| `DOUBLE_aligned_p0_null1_props0_app1_w4_row_parallel1` | 0.9989 [0.9942, 1.0042] | 0.9949 [0.9898, 1.0035] | 0.9279 [0.9220, 0.9411] | 0.9255 [0.9234, 0.9373] |
| `DOUBLE_aligned_p0_null1_props0_app1_w4_batch_parallel1` | 0.9997 [0.9926, 1.0091] | 0.9994 [0.9914, 1.0118] | 0.9218 [0.9122, 0.9295] | 0.9218 [0.9137, 0.9305] |
| `DOUBLE_nonaligned_p2_null0_props0_all_w4_row_parallel0` | 1.0011 [0.9924, 1.0079] | 0.9915 [0.9853, 1.0076] | 0.9955 [0.9865, 1.0018] | 0.9914 [0.9852, 1.0090] |
| `DOUBLE_nonaligned_p2_null0_props0_all_w4_batch_parallel0` | 0.9960 [0.9879, 1.0000] | 0.9925 [0.9837, 1.0023] | 0.9991 [0.9897, 1.0085] | 0.9934 [0.9870, 1.0004] |
| `DOUBLE_nonaligned_p0_null1_props0_time_w1_row_parallel1` | 1.0030 [0.9933, 1.0139] | 1.0036 [0.9911, 1.0133] | 0.9978 [0.9887, 1.0105] | 1.0049 [0.9999, 1.0106] |
| `DOUBLE_nonaligned_p0_null1_props0_time_w1_batch_parallel1` | 1.0035 [0.9812, 1.0247] | 1.0048 [0.9984, 1.0125] | 0.9922 [0.9770, 1.0050] | 1.0014 [0.9866, 1.0159] |
| `DOUBLE_nonaligned_p0_null1_props0_app1_w4_row_parallel1` | 0.9997 [0.9910, 1.0057] | 1.0044 [0.9960, 1.0124] | 0.9795 [0.9711, 0.9831] | 0.9768 [0.9662, 0.9850] |
| `DOUBLE_nonaligned_p0_null1_props0_app1_w4_batch_parallel1` | 0.9988 [0.9911, 1.0029] | 1.0007 [0.9955, 1.0066] | 0.9800 [0.9720, 0.9880] | 0.9765 [0.9689, 0.9846] |
| `FLOAT_aligned_p2_null1_props0_tag_w4_row_parallel1` | 0.9988 [0.9946, 1.0079] | 1.0032 [0.9910, 1.0101] | 1.0050 [0.9927, 1.0106] | 1.0023 [0.9906, 1.0080] |
| `FLOAT_aligned_p2_null1_props0_tag_w4_batch_parallel1` | 0.9823 [0.9708, 0.9915] | 0.9961 [0.9916, 1.0031] | 1.0021 [0.9905, 1.0102] | 0.9897 [0.9803, 0.9960] |
| `DOUBLE_nonaligned_p2_null1_props0_tag_w4_row_parallel0` | 1.0006 [0.9906, 1.0094] | 1.0004 [0.9898, 1.0074] | 1.0006 [0.9870, 1.0088] | 0.9988 [0.9882, 1.0099] |
| `DOUBLE_nonaligned_p2_null1_props0_tag_w4_batch_parallel0` | 0.9990 [0.9839, 1.0103] | 1.0009 [0.9862, 1.0101] | 0.9874 [0.9819, 1.0045] | 0.9961 [0.9822, 1.0056] |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_row_parallel0` | 1.0035 [0.9960, 1.0073] | 0.9992 [0.9912, 1.0043] | 0.9989 [0.9935, 1.0051] | 1.0030 [0.9997, 1.0066] |
| `FLOAT_nonaligned_p0_null1_props0_app0_w1_row_parallel0` | 1.0046 [0.9844, 1.0181] | 0.9941 [0.9850, 1.0082] | 0.9970 [0.9886, 1.0037] | 0.9998 [0.9939, 1.0046] |
| `FLOAT_nonaligned_p0_null1_props0_app0_w1_batch_parallel0` | 1.0015 [0.9952, 1.0089] | 0.9993 [0.9950, 1.0102] | 0.9974 [0.9783, 1.0065] | 0.9920 [0.9812, 1.0026] |

| Scenario | Baseline / fixed full p50 (ms) | Baseline / fixed full p95 (ms) | Baseline / fixed first accepted p50 (ms) | Baseline / fixed peak working set median (MiB) |
|---|---|---|---|---|
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` | 3.363 / 3.358 | 4.108 / 4.151 | 0.161 / 0.168 | 5.008 / 5.004 |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` | 2.818 / 2.827 | 3.492 / 3.503 | 0.169 / 0.166 | 5.008 / 5.004 |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_batch_parallel0` | 1.218 / 1.223 | 1.845 / 1.848 | 0.116 / 0.120 | 4.963 / 4.961 |
| `FLOAT_aligned_p2_null0_props0_all_w4_row_parallel0` | 3.538 / 3.537 | 4.191 / 4.205 | 0.185 / 0.181 | 5.012 / 5.012 |
| `FLOAT_aligned_p2_null0_props0_all_w4_batch_parallel0` | 3.002 / 2.998 | 3.693 / 3.675 | 0.183 / 0.185 | 5.012 / 5.012 |
| `FLOAT_aligned_p0_null1_props0_time_w1_row_parallel1` | 0.906 / 0.900 | 1.632 / 1.606 | 0.144 / 0.143 | 5.305 / 5.293 |
| `FLOAT_aligned_p0_null1_props0_time_w1_batch_parallel1` | 0.776 / 0.766 | 1.491 / 1.498 | 0.143 / 0.141 | 5.307 / 5.293 |
| `FLOAT_aligned_p0_null1_props0_app1_w4_row_parallel1` | 13.116 / 11.892 | 14.155 / 12.778 | 1.025 / 0.880 | 6.117 / 6.113 |
| `FLOAT_aligned_p0_null1_props0_app1_w4_batch_parallel1` | 12.786 / 11.444 | 13.967 / 12.862 | 1.024 / 0.887 | 6.119 / 6.107 |
| `FLOAT_nonaligned_p2_null0_props0_all_w4_row_parallel0` | 15.507 / 15.594 | 15.994 / 16.627 | 0.439 / 0.442 | 5.418 / 5.412 |
| `FLOAT_nonaligned_p2_null0_props0_all_w4_batch_parallel0` | 15.002 / 15.008 | 15.723 / 15.640 | 0.433 / 0.425 | 5.418 / 5.414 |
| `FLOAT_nonaligned_p0_null1_props0_time_w1_row_parallel1` | 2.689 / 2.669 | 3.449 / 3.384 | 0.174 / 0.169 | 5.273 / 5.262 |
| `FLOAT_nonaligned_p0_null1_props0_time_w1_batch_parallel1` | 2.542 / 2.555 | 3.312 / 3.226 | 0.169 / 0.173 | 5.283 / 5.262 |
| `FLOAT_nonaligned_p0_null1_props0_app1_w4_row_parallel1` | 16.360 / 15.927 | 17.243 / 17.136 | 0.446 / 0.438 | 5.508 / 5.484 |
| `FLOAT_nonaligned_p0_null1_props0_app1_w4_batch_parallel1` | 15.868 / 15.576 | 16.879 / 16.465 | 0.446 / 0.450 | 5.500 / 5.467 |
| `DOUBLE_aligned_p0_null1_props0_time_w1_row_parallel1` | 0.874 / 0.879 | 1.596 / 1.597 | 0.144 / 0.146 | 5.311 / 5.297 |
| `DOUBLE_aligned_p0_null1_props0_time_w1_batch_parallel1` | 0.742 / 0.738 | 1.446 / 1.470 | 0.140 / 0.142 | 5.316 / 5.301 |
| `DOUBLE_aligned_p0_null1_props0_app1_w4_row_parallel1` | 13.330 / 12.354 | 14.220 / 13.622 | 1.051 / 0.927 | 6.252 / 6.273 |
| `DOUBLE_aligned_p0_null1_props0_app1_w4_batch_parallel1` | 12.935 / 11.921 | 14.249 / 13.241 | 1.058 / 0.939 | 6.270 / 6.281 |
| `DOUBLE_nonaligned_p2_null0_props0_all_w4_row_parallel0` | 15.193 / 15.088 | 16.094 / 15.944 | 0.422 / 0.412 | 5.393 / 5.387 |
| `DOUBLE_nonaligned_p2_null0_props0_all_w4_batch_parallel0` | 14.657 / 14.582 | 15.596 / 15.164 | 0.418 / 0.409 | 5.391 / 5.387 |
| `DOUBLE_nonaligned_p0_null1_props0_time_w1_row_parallel1` | 2.615 / 2.625 | 3.310 / 3.382 | 0.171 / 0.173 | 5.266 / 5.254 |
| `DOUBLE_nonaligned_p0_null1_props0_time_w1_batch_parallel1` | 2.504 / 2.485 | 3.232 / 3.225 | 0.170 / 0.167 | 5.270 / 5.250 |
| `DOUBLE_nonaligned_p0_null1_props0_app1_w4_row_parallel1` | 15.957 / 15.509 | 17.215 / 16.566 | 0.450 / 0.434 | 5.414 / 5.391 |
| `DOUBLE_nonaligned_p0_null1_props0_app1_w4_batch_parallel1` | 15.444 / 15.130 | 16.322 / 16.287 | 0.437 / 0.430 | 5.418 / 5.395 |
| `FLOAT_aligned_p2_null1_props0_tag_w4_row_parallel1` | 6.601 / 6.605 | 7.325 / 7.453 | 1.014 / 1.002 | 6.055 / 6.070 |
| `FLOAT_aligned_p2_null1_props0_tag_w4_batch_parallel1` | 6.457 / 6.345 | 7.973 / 7.066 | 1.031 / 1.007 | 6.064 / 6.066 |
| `DOUBLE_nonaligned_p2_null1_props0_tag_w4_row_parallel0` | 8.074 / 8.101 | 8.864 / 8.731 | 0.434 / 0.426 | 5.066 / 5.062 |
| `DOUBLE_nonaligned_p2_null1_props0_tag_w4_batch_parallel0` | 7.878 / 7.793 | 8.786 / 8.694 | 0.420 / 0.430 | 5.066 / 5.068 |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_row_parallel0` | 1.472 / 1.466 | 2.051 / 2.085 | 0.117 / 0.118 | 4.965 / 4.965 |
| `FLOAT_nonaligned_p0_null1_props0_app0_w1_row_parallel0` | 5.206 / 5.146 | 6.090 / 5.975 | N/A (zero accepted rows) | 4.914 / 4.902 |
| `FLOAT_nonaligned_p0_null1_props0_app0_w1_batch_parallel0` | 4.906 / 4.858 | 5.478 / 5.556 | N/A (zero accepted rows) | 4.914 / 4.902 |
## 调用程序 × CPU 的独立控制

An independent 2×2 control compares mixed/reader-only callers and affinity mask 4/12, with parallel reads disabled. Each cell runs 192 alternating baseline/fixed process pairs, 3 complete queries/process, 2 warmups/variant. Both versions read the same fixed file for DOUBLE, and the same baseline file for FLOAT. Every sample is retained; the CI resamples 24 chronological blocks of 8 pairs.

| Case | Caller | CPU mask | Fixed / baseline block-median ratio [95% CI] |
|---|---|---:|---|
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` | `mixed` | 4 | 0.9979 [0.9944, 0.9990] |
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` | `mixed` | 12 | 0.9964 [0.9944, 0.9999] |
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` | `reader_only` | 4 | 1.0013 [0.9996, 1.0023] |
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` | `reader_only` | 12 | 0.9995 [0.9979, 1.0014] |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` | `mixed` | 4 | 0.9958 [0.9931, 0.9969] |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` | `mixed` | 12 | 0.9946 [0.9917, 0.9970] |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` | `reader_only` | 4 | 0.9993 [0.9978, 1.0003] |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` | `reader_only` | 12 | 1.0010 [0.9973, 1.0024] |
| `FLOAT_nonaligned_p2_null0_props0_all_w4_row_parallel0` | `mixed` | 4 | 0.9945 [0.9903, 0.9981] |
| `FLOAT_nonaligned_p2_null0_props0_all_w4_row_parallel0` | `mixed` | 12 | 0.9942 [0.9900, 0.9987] |
| `FLOAT_nonaligned_p2_null0_props0_all_w4_row_parallel0` | `reader_only` | 4 | 0.9993 [0.9947, 1.0014] |
| `FLOAT_nonaligned_p2_null0_props0_all_w4_row_parallel0` | `reader_only` | 12 | 1.0004 [0.9958, 1.0035] |

## PR #1024 的当前结论

The query timing backfill is measured and disclosed, including the original small mixed-caller slowdown and all controls. It is **not marked as an unconditional no-regression pass**. In the final 12-cell control, every reader-only block-median confidence interval includes 1, while the mixed-caller point estimates reverse direction (fixed slightly faster), including mask 12 used in the earlier confirmation. Thus the earlier slowdown is not stable across independent sessions/protocols. Caller/link layout and CPU placement are possible influences, not proven causes; this experiment changes from quartets to same-file reader pairs as well. Unchanged reader source and object-section matches alone cannot erase the earlier measured latency increase. The sub-percent, session-dependent signal remains unresolved; these observations do not justify a specific reader-source fix or a universal zero-regression claim. Production source and all previous failures remain unchanged.

Precision-2 writer products are byte-identical for these fixtures. Requested precision-0 inputs are integer-valued so both old/default-2 and fixed/0 files remain logically equivalent; Java inspects every value-page prefix and confirms actual precision 2 versus 0. The smaller revised files and their query effects are measured separately from same-file reader cost. This does not compare different rounded answers as if they were the same operation.

Native FIELD pushdown, sole/all-NULL projections, OFFSET/LIMIT timing, compressed-query performance, NaN/extreme-value performance, very large files/metadata and broad parallel scaling are unmeasured. Earlier correctness/coverage/write evidence and known Java extreme-precision failures remain intact in the prior report.

## 辅助程序内存检查与复现资料

The new helper passes five Linux ASan/UBSan scenarios with leak detection enabled against the previously validated PR02 library: nonempty-property read, non-aligned DOUBLE time/batch/parallel read, aligned FLOAT application filtering, fixture writing and zero-accepted-row read. This is helper validation, not a rerun of each PR's entire suite. No sanitizer suppression was added. Production source is unchanged, so the existing production coverage and write measurements are retained rather than relabeled as newly collected.

The archive includes driver/source/build scripts, all actual writer products for this PR (including the marked invalid control), Java raw-page/type/value audit, binary/library hashes, preflights, all raw timing arrays and discarded-order/initial/confirmation/control data. To reproduce, build static libraries from the pinned base/head with the stated MSVC Release options; configure `CMakeLists.txt` using its `PR01_SOURCE`, `PR01_BASE_INCLUDE`, `PR01_BASE_LIBRARY`, `PR01_FIXED_LIBRARY`, `PR02_BASE_SOURCE`, `PR02_FIXED_SOURCE`, `PR02_BASE_LIBRARY`, `PR02_FIXED_LIBRARY` cache parameters. Run `prepare_data.py`, then `benchmark.py`. The Java audit accepts `TSFILE_QUERY_JAVA_CLASSPATH_FILE` pointing to the classpath from the matching Java build. Reader-only and sanitizer scripts preserve their original local build locations; adapt those paths when replaying in another checkout.

**AI disclosure:** The implementation, tests and description in this pull request were written by an AI coding agent (OpenAI Codex), which also performed the reported local validation.

**AI 使用说明：** 本 PR 的代码修改、测试和正文由 AI 编程代理（OpenAI Codex）编写，文中报告的本地验证也由该 AI 代理执行。
