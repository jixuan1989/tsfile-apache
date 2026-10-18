# TsFile PR #1018: query performance backfill

Baseline `12e39fe9d9dace63cc0ad39664aa0fbf5e29f52f`; tested PR head `5fb363774ed7b492252d2933707545edca5ca981`. No production code or new upstream source commit was made for this backfill. Existing correctness, bidirectional interoperability, coverage and write-performance results remain in the earlier reports, with their original limits. This follow-up adds query timings rather than treating untimed readback as performance evidence.

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
| `FLOAT_aligned_p2_null0_props0_all_w4_row_parallel0` | 0.9983 [0.9906, 1.0090] | 1.0025 [0.9956, 1.0068] | 1.0020 [0.9940, 1.0083] | 0.9990 [0.9918, 1.0065] |
| `FLOAT_aligned_p2_null0_props0_all_w4_batch_parallel0` | 1.0001 [0.9969, 1.0062] | 0.9972 [0.9928, 1.0024] | 0.9990 [0.9897, 1.0092] | 1.0014 [0.9948, 1.0057] |
| `FLOAT_aligned_p2_null0_props0_time_w1_row_parallel0` | 1.0095 [0.9924, 1.0171] | 1.0009 [0.9901, 1.0125] | 0.9994 [0.9858, 1.0065] | 1.0046 [0.9923, 1.0146] |
| `FLOAT_aligned_p2_null0_props0_time_w1_batch_parallel0` | 0.9916 [0.9846, 1.0015] | 1.0005 [0.9911, 1.0128] | 0.9983 [0.9916, 1.0091] | 0.9955 [0.9888, 1.0050] |
| `FLOAT_aligned_p2_null0_props0_tag_w4_row_parallel1` | 0.9959 [0.9814, 0.9987] | 1.0065 [0.9921, 1.0127] | 1.0058 [0.9973, 1.0173] | 0.9957 [0.9861, 1.0043] |
| `FLOAT_aligned_p2_null0_props0_tag_w4_batch_parallel1` | 0.9920 [0.9850, 0.9986] | 1.0034 [0.9984, 1.0168] | 1.0024 [0.9954, 1.0166] | 0.9940 [0.9853, 1.0119] |
| `FLOAT_aligned_p2_null1_props0_all_w4_row_parallel1` | 0.9954 [0.9781, 1.0080] | 1.0023 [0.9960, 1.0061] | 1.0007 [0.9882, 1.0075] | 0.9981 [0.9786, 1.0036] |
| `FLOAT_aligned_p2_null1_props0_all_w4_batch_parallel1` | 1.0057 [0.9947, 1.0246] | 0.9981 [0.9899, 1.0149] | 1.0026 [0.9855, 1.0099] | 1.0047 [0.9993, 1.0195] |
| `FLOAT_aligned_p2_null1_props0_app1_w4_row_parallel0` | 1.0021 [0.9935, 1.0042] | 1.0024 [0.9994, 1.0067] | 1.0017 [0.9991, 1.0043] | 0.9990 [0.9921, 1.0040] |
| `FLOAT_aligned_p2_null1_props0_app1_w4_batch_parallel0` | 1.0010 [0.9951, 1.0126] | 1.0041 [0.9941, 1.0099] | 1.0045 [0.9946, 1.0118] | 1.0019 [0.9975, 1.0112] |
| `FLOAT_nonaligned_p2_null1_props0_time_w4_row_parallel1` | 1.0020 [0.9921, 1.0066] | 1.0039 [0.9984, 1.0075] | 0.9971 [0.9913, 1.0036] | 1.0008 [0.9957, 1.0060] |
| `FLOAT_nonaligned_p2_null1_props0_time_w4_batch_parallel1` | 1.0080 [0.9974, 1.0133] | 0.9968 [0.9871, 1.0093] | 0.9901 [0.9828, 1.0025] | 0.9971 [0.9931, 1.0083] |
| `FLOAT_aligned_p2_null1_props1_all_w4_row_parallel0` | invalid old producer excluded | 0.9935 [0.9914, 1.0012] | N/A | N/A |
| `FLOAT_aligned_p2_null1_props1_all_w4_batch_parallel0` | invalid old producer excluded | 1.0007 [0.9939, 1.0058] | N/A | N/A |
| `FLOAT_aligned_p2_null1_props1_tag_w1_row_parallel1` | invalid old producer excluded | 0.9946 [0.9893, 1.0049] | N/A | N/A |
| `FLOAT_aligned_p2_null1_props1_tag_w1_batch_parallel1` | invalid old producer excluded | 0.9976 [0.9853, 1.0048] | N/A | N/A |

| Scenario | Baseline / fixed full p50 (ms) | Baseline / fixed full p95 (ms) | Baseline / fixed first accepted p50 (ms) | Baseline / fixed peak working set median (MiB) |
|---|---|---|---|---|
| `FLOAT_aligned_p2_null0_props0_all_w4_row_parallel0` | 3.280 / 3.283 | 4.194 / 4.195 | 0.182 / 0.188 | 5.436 / 5.430 |
| `FLOAT_aligned_p2_null0_props0_all_w4_batch_parallel0` | 2.695 / 2.703 | 3.528 / 3.550 | 0.175 / 0.175 | 5.430 / 5.441 |
| `FLOAT_aligned_p2_null0_props0_time_w1_row_parallel0` | 0.909 / 0.907 | 1.631 / 1.627 | 0.148 / 0.147 | 5.367 / 5.369 |
| `FLOAT_aligned_p2_null0_props0_time_w1_batch_parallel0` | 0.772 / 0.765 | 1.485 / 1.496 | 0.147 / 0.148 | 5.363 / 5.363 |
| `FLOAT_aligned_p2_null0_props0_tag_w4_row_parallel1` | 3.166 / 3.132 | 4.193 / 4.073 | 0.726 / 0.705 | 6.039 / 6.037 |
| `FLOAT_aligned_p2_null0_props0_tag_w4_batch_parallel1` | 2.812 / 2.841 | 3.739 / 3.683 | 0.708 / 0.697 | 6.041 / 6.041 |
| `FLOAT_aligned_p2_null1_props0_all_w4_row_parallel1` | 12.591 / 12.627 | 14.809 / 13.497 | 0.950 / 0.932 | 6.186 / 6.178 |
| `FLOAT_aligned_p2_null1_props0_all_w4_batch_parallel1` | 12.088 / 12.126 | 13.973 / 14.779 | 0.973 / 0.968 | 6.178 / 6.176 |
| `FLOAT_aligned_p2_null1_props0_app1_w4_row_parallel0` | 9.549 / 9.569 | 10.712 / 10.506 | 0.291 / 0.292 | 5.445 / 5.463 |
| `FLOAT_aligned_p2_null1_props0_app1_w4_batch_parallel0` | 9.004 / 9.061 | 9.947 / 10.012 | 0.291 / 0.290 | 5.449 / 5.439 |
| `FLOAT_nonaligned_p2_null1_props0_time_w4_row_parallel1` | 8.112 / 8.040 | 9.076 / 8.987 | 0.417 / 0.413 | 5.500 / 5.488 |
| `FLOAT_nonaligned_p2_null1_props0_time_w4_batch_parallel1` | 7.835 / 7.782 | 8.640 / 8.730 | 0.416 / 0.415 | 5.496 / 5.502 |
| `FLOAT_aligned_p2_null1_props1_all_w4_row_parallel0` | 9.620 / 9.542 | 10.433 / 10.415 | 0.290 / 0.292 | 5.443 / 5.445 |
| `FLOAT_aligned_p2_null1_props1_all_w4_batch_parallel0` | 9.006 / 9.020 | 9.940 / 9.818 | 0.287 / 0.284 | 5.449 / 5.449 |
| `FLOAT_aligned_p2_null1_props1_tag_w1_row_parallel1` | 0.791 / 0.793 | 1.532 / 1.523 | 0.134 / 0.135 | 5.355 / 5.354 |
| `FLOAT_aligned_p2_null1_props1_tag_w1_batch_parallel1` | 0.662 / 0.658 | 1.394 / 1.378 | 0.139 / 0.135 | 5.359 / 5.363 |

## PR #1018 的结论与边界

All 16 measured cases pass full result checks, and none triggers the recorded confirmation policy (paired-median 95% interval wholly above 1, median ratio above 1.03, or descriptive p95 ratio above 1.10). Valid empty-property baseline/fixed files are byte-identical. For nonempty properties the original producer output returns `E_PARTIAL_READ` (`code=6`) in both readers, so it cannot be timed as a valid original producer. The valid fixed nonempty-property file is timed with both reader versions, preserving its additional metadata work. This does not claim a valid before/after producer latency for previously malformed nonempty output.

The measured query gate is cleared for this corpus. It is not a guarantee of zero regression on every application/hardware/cache condition. Native FIELD pushdown, sole/all-NULL projections, OFFSET/LIMIT timing, compressed-query timing, special floating values, very large metadata sets and full parallel scaling are outside these measurements. Existing embedded-NUL string parsing limitations remain unchanged.

## 辅助程序内存检查与复现资料

The new helper passes five Linux ASan/UBSan scenarios with leak detection enabled against the previously validated PR02 library: nonempty-property read, non-aligned DOUBLE time/batch/parallel read, aligned FLOAT application filtering, fixture writing and zero-accepted-row read. This is helper validation, not a rerun of each PR's entire suite. No sanitizer suppression was added. Production source is unchanged, so the existing production coverage and write measurements are retained rather than relabeled as newly collected.

The archive includes driver/source/build scripts, all actual writer products for this PR (including the marked invalid control), Java raw-page/type/value audit, binary/library hashes, preflights, all raw timing arrays and discarded-order/initial/confirmation/control data. To reproduce, build static libraries from the pinned base/head with the stated MSVC Release options; configure `CMakeLists.txt` using its `PR01_SOURCE`, `PR01_BASE_INCLUDE`, `PR01_BASE_LIBRARY`, `PR01_FIXED_LIBRARY`, `PR02_BASE_SOURCE`, `PR02_FIXED_SOURCE`, `PR02_BASE_LIBRARY`, `PR02_FIXED_LIBRARY` cache parameters. Run `prepare_data.py`, then `benchmark.py`. The Java audit accepts `TSFILE_QUERY_JAVA_CLASSPATH_FILE` pointing to the classpath from the matching Java build. Reader-only and sanitizer scripts preserve their original local build locations; adapt those paths when replaying in another checkout.

**AI disclosure:** The implementation, tests and description in this pull request were written by an AI coding agent (OpenAI Codex), which also performed the reported local validation.

**AI 使用说明：** 本 PR 的代码修改、测试和正文由 AI 编程代理（OpenAI Codex）编写，文中报告的本地验证也由该 AI 代理执行。
