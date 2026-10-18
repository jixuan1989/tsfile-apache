# TsFile PR #1024: matched-protocol caller control

Baseline `1180b13675e11a0230708af2cc70d037e0e12623`; PR head `75592b89d1523a96090e8bca1dcb4cd2180162e5`. All four measured original executable hashes, the Java-audited input file, and both production source checkouts match the retained backfill. No production or upstream source commit is made. The two diagnostic stages alone do not clear the query gate; the corrected full-matrix disposition is reported below. Earlier repeated slowdowns and opposite-direction runs remain intact.

**Latest controlled-confirmation disposition: query gate uncleared.** Remaining end-to-end block medians are `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0`: +1.06%; `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0`: +1.27%; `DOUBLE_aligned_p2_null1_props0_app50_w1_batch_parallel0`: +0.45%. Image identity/loading context is a measured contributor, but correcting it does not fully explain or eliminate these repeated mixed-caller signals. No source fix is inferred or production padding changed.

## Question and fixed protocol

Earlier mixed-caller timing showed small dense DOUBLE slowdowns, while earlier reader-only controls changed both caller and CPU/protocol. This experiment compares the two original caller forms under the **same** launch, file, pinning, timing and query protocol. The mixed executable contains its writer path; the reader-only executable reuses one compiled reader object across the two libraries. Removing writer contents and fixing caller compilation change together, so this is not a pure layout intervention or proof of a source-level cause.

The plan is saved before measurement with a stopping rule of **192 complete process quartets in each of four cells**: row/batch × mixed/reader-only. Every child is created suspended, pinned to mask 12, checked, then resumed. Pool size 2, parallel read disabled, same fixed-produced precision-2 file in all children. The baseline/fixed precision-2 products are byte-identical. Mask 12 is two SMT siblings of one physical core. Filesystem cache is warmed; host background load/power/clock state are uncontrolled. Two warmups per label/cell precede measurement.

Each quartet contains two runs of each version, three complete queries per child. For each round/caller, the primary fixed/baseline ratio uses the **sum of six fixed queries / sum of six baseline queries**, keeping all repeats. The direct caller interaction is that round's mixed ratio / reader-only ratio. Its 95% bootstrap interval resamples 24 chronological blocks of eight complete, position-balanced rounds (20,000 draws; median within each block). Caller cells rotate/reverse across rounds, and all label/cell execution positions are asserted equal before sampling. This paired interaction is the primary test of caller dependence; it is not inferred by comparing separate significance labels.

All 3,072 measured child processes consume and validate 9,216 queries, each with 65,536 rows and four projected fields. Every value, NULL state, timestamp and row order is checked by the unchanged native driver; Python independently checks row counts/checksum. No result truncation/early exit is timed as a speedup. Each quartet's second/first same-version run supplies two internal same-binary controls. All samples are retained; no adaptive stopping, outlier removal or acceptance-margin change occurs.

## Primary caller interaction

Ratios are fixed/baseline within each caller. The interaction is mixed ratio / reader-only ratio; brackets are block-bootstrap 95% intervals. A positive interaction narrows the scope to caller/link context without identifying which constituent change is causal. A non-significant interaction does not prove equality.

| Mode | Mixed caller | Reader-only caller | Paired caller interaction |
|---|---|---|---|
| row | 1.00472 [1.00358, 1.00801] | 1.00566 [1.00486, 1.00703] | 1.00033 [0.99393, 1.00274] |
| batch | 1.00687 [1.00550, 1.00920] | 1.00890 [1.00767, 1.01004] | 0.99756 [0.99501, 1.00105] |

## Internal negative controls and lifetime cycles

Same-binary controls compare the two repeat labels of the identical binary reading the same file; their intervals are not source-regression tests. Main-thread cycle ratios cover initialization, printing and exit in addition to the queries; they are not query-only CPU costs or retired instruction counts. No short-process OS CPU-time ratio is collected after the preceding experiment exposed zero-accounting granularity.

| Mode | Caller | Baseline repeat 2 / 1 | Fixed repeat 2 / 1 | Main-thread lifetime fixed / baseline cycles |
|---|---|---|---|---|
| row | mixed | 1.00089 [0.99797, 1.00203] | 1.00139 [0.99782, 1.00312] | 1.00545 [1.00283, 1.00791] |
| row | reader_only | 0.99899 [0.99722, 1.00137] | 1.00141 [0.99715, 1.00241] | 1.00247 [1.00188, 1.00446] |
| batch | mixed | 1.00000 [0.99781, 1.00551] | 1.00091 [1.00013, 1.00222] | 1.00337 [1.00182, 1.00599] |
| batch | reader_only | 1.00176 [0.99760, 1.00436] | 0.99944 [0.99809, 1.00230] | 1.00577 [1.00305, 1.00684] |

## Descriptive full-query latency

Each version/cell has 1,152 individual queries clustered within 384 child processes and 192 matched rounds. These p50/p95 values are descriptive distributions, not independent-tail non-inferiority guarantees. Raw open, cached schema lookup, plan, first decoded/accepted row, full-result times and process peak-memory measurements are retained; this report analyzes full latency and caller interaction rather than claiming a new complete metric matrix.

| Mode | Caller | Baseline / fixed full p50 (ms) | Baseline / fixed full p95 (ms) |
|---|---|---|---|
| row | mixed | 3.3517 / 3.3759 | 4.2364 / 4.2559 |
| row | reader_only | 3.3528 / 3.3755 | 4.2200 / 4.2503 |
| batch | mixed | 2.8156 / 2.8404 | 3.6968 / 3.7259 |
| batch | reader_only | 2.8206 / 2.8452 | 3.6874 / 3.7138 |


## Follow-up: exact-byte image-identity crossover

This second-stage hypothesis was selected **after** the caller interaction was measured. The reader-only caller also shows upward ratios in the matched protocol, and both primary caller-interaction intervals include one; the first-stage results therefore do not support attributing the signal solely to the mixed executable. This is a new, separately fixed diagnostic plan, not a predeclared confirmatory test of the first stage.

The second stage uses the same original reader-only bytes and launch/query protocol, comparing original executable paths to four neutral file copies. Baseline/fixed content assignments rotate among the four neutral paths every eight-round block. Every neutral path carries each version for twelve blocks; label/cell execution positions are balanced. Each copied image is SHA-256 checked before its block; no instruction, static data byte, PE header or relative address is patched. Copies are warmed once per label/mode after each block replacement, before any timed child. Original paths have two initial warmups per label/mode. Additional warmups/copy preparation are outside each driver query timer.

There are four cells (row/batch × original/neutral) × 192 quartets, another 3,072 measured processes and 9,216 complete queries. Per-round neutral ratio / original ratio is the primary image-identity interaction, with 24 chronological blocks of eight and 20,000 bootstrap draws. Within-version repeat labels refer to distinct neutral copies in that condition; they are not same-path controls. Path, file backing allocation, loader/cache history and possible ASLR placement change together, so this cannot isolate a filename-only or code-layout cause. Loaded image bases, physical mapping, cache misses and hardware instruction counters were not measured.

| Mode | Original path fixed / baseline | Neutral crossover fixed / baseline | Paired image-identity interaction |
|---|---|---|---|
| row | 1.00752 [1.00639, 1.00897] | 0.99973 [0.99866, 1.00139] | 0.99287 [0.99047, 0.99443] |
| batch | 1.00784 [1.00636, 1.00929] | 1.00098 [0.99905, 1.00237] | 0.99391 [0.99200, 0.99490] |

| Mode | Condition | Baseline repeat 2 / 1 | Fixed repeat 2 / 1 |
|---|---|---|---|
| row | original_path | 0.99593 [0.99438, 1.00002] | 0.99953 [0.99724, 1.00227] |
| row | neutral_crossover | 1.00033 [0.99884, 1.00259] | 0.99981 [0.99811, 1.00272] |
| batch | original_path | 1.00024 [0.99885, 1.00349] | 0.99847 [0.99590, 0.99937] |
| batch | neutral_crossover | 1.00053 [0.99927, 1.00291] | 0.99988 [0.99660, 1.00167] |

All previous positive and opposite-direction observations remain intact. These two stages measure 6,144 child processes and 18,432 fully checked queries in total, plus separately described warmups. Neither an interaction interval containing one nor a changed point estimate establishes complete equivalence or authorizes clearing the strict query gate.

## Original linked locations

After the first-stage timings finish, map-only sidecars reuse the exact measured object files and pinned static libraries. Original `.text`/`.pdata` equality is checked, and `.rdata` differences must be only PE debug-directory timestamps. The following table records exact symbol locations and offsets modulo 64. These are layout observations, not cache-miss/branch hardware-counter measurements or proof that aligning a function would fix performance. The original binaries are not overwritten or retimed as sidecars.

| Symbol | Caller | Baseline RVA (mod 64) | Fixed RVA (mod 64) |
|---|---|---|---|
| `?mem_free@common` | mixed | `0x15640` (0) | `0x15640` (0) |
| `?mem_free@common` | reader_only | `0x199c0` (0) | `0x199c0` (0) |
| `?next@TableResultSet@storage` | mixed | `0x75d50` (16) | `0x761f0` (48) |
| `?next@TableResultSet@storage` | reader_only | `0x4f4d0` (16) | `0x4f4d0` (16) |
| `?read_batch_double@DoubleTS2DIFFDecoder@storage` | mixed | `0x55050` (16) | `0x554f0` (48) |
| `?read_batch_double@DoubleTS2DIFFDecoder@storage` | reader_only | `0x31590` (16) | `0x31590` (16) |
| `?read_double@DoubleTS2DIFFDecoder@storage` | mixed | `0x57db0` (48) | `0x58250` (16) |
| `?read_double@DoubleTS2DIFFDecoder@storage` | reader_only | `0x342f0` (48) | `0x342f0` (48) |
| `?read_fixture` | mixed | `0x107a0` (32) | `0x107a0` (32) |
| `?read_fixture` | reader_only | `0xe3e0` (32) | `0xe3e0` (32) |

## Scope and disposition

The tables report every primary comparison, internal negative control and original code-location check. They narrow or constrain caller dependence; they do not establish intrinsic reader-source overhead or demonstrate a production fix. Earlier same-binary launch controls, contradictory sessions, raw-object and normalized linked-instruction comparisons remain published. Strict no-regression status is not relaxed, and untested workloads are not silently cleared.

The first two stages are uncompressed, warm-cache, dense aligned DOUBLE full-scan diagnostics in a single SMT-core configuration. The later corrected matrix below separately remeasures the original FLOAT/non-aligned/NULL/filter/projection corpus. None of these stages retests writer throughput, compressed queries, cold cache, P99 or physical-core scaling. Earlier correctness/Java interoperability/coverage/write evidence keeps its original scope. No production coverage or sanitizer rerun is claimed for unchanged C++ artifacts. The Python launcher smoke checks both callers; the full run additionally validates every child result and all affinity operations.

The archive contains pre-sample plans, complete order/raw arrays, scripts, linker maps, code-location/integrity reports, pinned backfill metadata and actual input products. Build static libraries and original benchmark objects at the pinned base/head using the previous evidence; run `matched_callers.py --smoke`, then `matched_callers.py` once. Configure/build `CMakeLists.txt` in Release outside a timing run and run `compare_layout.py`. Paths are preserved for reproducibility and need adaptation on another machine. Measurement scripts refuse to overwrite existing runs; `--analyze-only` recomputes statistics without launching children. Generate the report only after all three stages below finish.

After the first-stage results, `image_identity.py` records its separate plan and creates/rotates four private image copies, then measures the second stage. `counterbalanced_matrix.py` subsequently records its own corrected full-corpus plan and runs the initial and any required independent confirmations. Finally run `prepare_report.py`. The evidence contains each plan, assignments, every raw child result and internal controls; executable copies need not be distributed because each is an exact hash-checked copy of an original measured binary.

## Corrected full query corpus: counterbalanced identities

The exact-byte crossover demonstrates that image identity/loading context changes the ratio while static code/data/RVAs stay fixed. The concrete repair is in the **benchmark comparison protocol**, not production source: use private neutral executable/data paths and balance which version occupies each path. This corrects a demonstrated comparison confound without a numeric acceptance margin or production padding change. It does not identify whether path, backing pages, ASLR or another loader/cache mechanism supplies the effect.

The full original 32-case PR02 corpus is remeasured with the original mixed binaries and actual Java-audited baseline/fixed writer products. For every case, 64 position-balanced quartets are grouped in eight blocks; each block copies exact images/products to neutral paths and performs two warmups per label before timings. Each image path carries each reader version equally, and each data path carries each writer product equally. Joint path interactions are not fully factorial. Affinity 12 is applied before initial-thread resume, with the original pool, parallel flag, three complete checked queries/process and warm-cache conditions. Existing application FIELD references still consume/validate all native rows before applying their 0/1/50% reference filter; they do not imply native pushdown.

The **unchanged trigger rule** is: a paired-median 95% interval wholly above 1, paired median above 1.03, or descriptive p95 ratio above 1.10 triggers one independent 192-quartet confirmation. No additional adaptive re-runs are allowed. Intervals now resample entire eight-round identity blocks (eight initial blocks or 24 confirmation blocks), because samples sharing an identity assignment are dependent. Per-variant p50/p95 use 192 initial or 576 confirmation queries clustered by process/block; P99 and formal tail non-inferiority remain unmeasured. Earlier failures and all initial flags are retained.

| Scenario | Reader on baseline product | Reader on fixed product | Writer products, fixed reader | End-to-end | Initial signals |
|---|---|---|---|---|---|
| `FLOAT_aligned_p2_null0_props0_all_w4_row_parallel0` | 0.97256 [0.97184, 0.98279] | 0.97371 [0.96977, 0.97607] | 0.99945 [0.99650, 1.00303] | 0.97155 [0.96793, 0.97782] | none |
| `FLOAT_aligned_p2_null0_props0_all_w4_batch_parallel0` | 0.96789 [0.96342, 0.97020] | 0.97437 [0.96207, 0.98022] | 1.00337 [1.00037, 1.00804] | 0.97028 [0.96131, 0.97969] | writer_products_fixed_reader |
| `FLOAT_aligned_p0_null1_props0_time_w1_row_parallel1` | 0.99261 [0.97922, 0.99855] | 0.99576 [0.98764, 1.00232] | 1.00302 [0.99189, 1.01068] | 0.99250 [0.98613, 0.99902] | none |
| `FLOAT_aligned_p0_null1_props0_time_w1_batch_parallel1` | 0.98868 [0.97248, 0.99315] | 0.98766 [0.97881, 0.99032] | 0.99318 [0.98961, 1.00334] | 0.97787 [0.97325, 0.98221] | none |
| `FLOAT_aligned_p0_null1_props0_app1_w4_row_parallel1` | 0.98898 [0.97300, 1.00739] | 1.00428 [0.99559, 1.01162] | 0.93943 [0.93049, 0.94858] | 0.93556 [0.92236, 0.93867] | none |
| `FLOAT_aligned_p0_null1_props0_app1_w4_batch_parallel1` | 0.99259 [0.97721, 1.00381] | 0.99834 [0.97848, 1.00557] | 0.93971 [0.93162, 0.95033] | 0.93421 [0.92609, 0.93869] | none |
| `FLOAT_nonaligned_p2_null0_props0_all_w4_row_parallel0` | 0.98211 [0.97519, 0.99217] | 0.98801 [0.97512, 0.99164] | 1.00297 [0.99222, 1.00408] | 0.98259 [0.97782, 0.98802] | none |
| `FLOAT_nonaligned_p2_null0_props0_all_w4_batch_parallel0` | 0.98843 [0.98216, 1.00133] | 0.98927 [0.98121, 0.99795] | 0.99530 [0.98771, 1.00555] | 0.98975 [0.98505, 0.99393] | none |
| `FLOAT_nonaligned_p0_null1_props0_time_w1_row_parallel1` | 0.98823 [0.98229, 1.00612] | 0.99113 [0.98822, 0.99988] | 1.00307 [0.99315, 1.00418] | 0.98740 [0.98113, 0.99572] | none |
| `FLOAT_nonaligned_p0_null1_props0_time_w1_batch_parallel1` | 0.98815 [0.97561, 1.00297] | 0.99276 [0.98884, 0.99641] | 1.00009 [0.99228, 1.00198] | 0.98896 [0.97776, 0.99950] | none |
| `FLOAT_nonaligned_p0_null1_props0_app1_w4_row_parallel1` | 0.98434 [0.97754, 0.99115] | 0.98868 [0.97446, 0.99740] | 0.97683 [0.96965, 0.98276] | 0.95827 [0.95219, 0.96775] | none |
| `FLOAT_nonaligned_p0_null1_props0_app1_w4_batch_parallel1` | 0.98330 [0.97594, 0.98937] | 0.98274 [0.97820, 0.99501] | 0.97429 [0.97086, 0.98069] | 0.96154 [0.95547, 0.96701] | none |
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` | 1.00873 [1.00213, 1.01393] | 1.00665 [1.00312, 1.00854] | 0.99927 [0.99560, 1.00087] | 1.00747 [1.00418, 1.01142] | reader_on_baseline_file, reader_on_fixed_file, end_to_end |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` | 1.00793 [1.00531, 1.01356] | 1.01084 [1.00864, 1.01517] | 0.99669 [0.99498, 0.99981] | 1.00850 [1.00273, 1.01212] | reader_on_baseline_file, reader_on_fixed_file, end_to_end |
| `DOUBLE_aligned_p0_null1_props0_time_w1_row_parallel1` | 0.99779 [0.98722, 1.00114] | 1.00626 [0.99557, 1.01196] | 1.00701 [1.00190, 1.01598] | 0.99927 [0.99611, 1.00259] | writer_products_fixed_reader |
| `DOUBLE_aligned_p0_null1_props0_time_w1_batch_parallel1` | 0.99984 [0.98996, 1.00620] | 0.99820 [0.99353, 0.99899] | 0.99986 [0.99417, 1.00963] | 0.99504 [0.98646, 1.00942] | none |
| `DOUBLE_aligned_p0_null1_props0_app1_w4_row_parallel1` | 1.00384 [0.98035, 1.01763] | 0.99870 [0.99433, 1.00761] | 0.95642 [0.93420, 0.96421] | 0.95759 [0.94193, 0.96932] | none |
| `DOUBLE_aligned_p0_null1_props0_app1_w4_batch_parallel1` | 0.99871 [0.99003, 1.01135] | 1.00761 [0.99979, 1.02122] | 0.95830 [0.95082, 0.97021] | 0.95536 [0.94882, 0.97572] | reader_on_fixed_file |
| `DOUBLE_nonaligned_p2_null0_props0_all_w4_row_parallel0` | 0.99859 [0.99299, 1.00672] | 0.99968 [0.98856, 1.00577] | 0.99960 [0.99730, 1.00401] | 0.99983 [0.99282, 1.00242] | none |
| `DOUBLE_nonaligned_p2_null0_props0_all_w4_batch_parallel0` | 0.99901 [0.98524, 1.00209] | 1.00061 [0.98962, 1.00526] | 1.00333 [0.99124, 1.01573] | 1.00401 [0.99166, 1.01089] | none |
| `DOUBLE_nonaligned_p0_null1_props0_time_w1_row_parallel1` | 0.99866 [0.99214, 1.00595] | 0.99635 [0.98277, 1.00617] | 0.99235 [0.98621, 1.00036] | 0.99609 [0.98415, 1.00248] | none |
| `DOUBLE_nonaligned_p0_null1_props0_time_w1_batch_parallel1` | 0.99088 [0.97885, 1.00117] | 0.99483 [0.98194, 1.00823] | 1.00621 [1.00253, 1.01635] | 0.99722 [0.99408, 1.01451] | writer_products_fixed_reader |
| `DOUBLE_nonaligned_p0_null1_props0_app1_w4_row_parallel1` | 0.99852 [0.98990, 1.00503] | 0.99991 [0.99358, 1.00219] | 0.97705 [0.96542, 0.98978] | 0.97560 [0.96973, 0.98137] | none |
| `DOUBLE_nonaligned_p0_null1_props0_app1_w4_batch_parallel1` | 0.99091 [0.98735, 0.99362] | 0.99521 [0.98668, 1.01383] | 0.98047 [0.97499, 0.98271] | 0.97502 [0.97181, 0.98582] | none |
| `FLOAT_aligned_p2_null1_props0_tag_w4_row_parallel1` | 0.99272 [0.98695, 1.00382] | 0.99376 [0.98405, 1.00609] | 1.00410 [0.99710, 1.02011] | 0.99468 [0.97909, 1.00575] | none |
| `FLOAT_aligned_p2_null1_props0_tag_w4_batch_parallel1` | 1.00247 [0.99275, 1.01083] | 0.99301 [0.98771, 1.00336] | 0.99451 [0.97760, 1.01059] | 1.00201 [0.98679, 1.00935] | none |
| `DOUBLE_nonaligned_p2_null1_props0_tag_w4_row_parallel0` | 1.00018 [0.99906, 1.00747] | 0.99900 [0.99249, 1.00992] | 1.00300 [0.98892, 1.01071] | 1.00027 [0.99508, 1.01101] | none |
| `DOUBLE_nonaligned_p2_null1_props0_tag_w4_batch_parallel0` | 1.00072 [0.99308, 1.00584] | 0.98819 [0.98194, 1.00484] | 0.99298 [0.98890, 1.00730] | 0.99387 [0.98732, 1.00379] | none |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_row_parallel0` | 0.99985 [0.99600, 1.00620] | 1.00370 [0.99515, 1.00701] | 0.99938 [0.99382, 1.00311] | 0.99755 [0.99321, 1.00380] | none |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_batch_parallel0` | 1.00459 [1.00077, 1.00922] | 1.00708 [0.98427, 1.01118] | 1.00361 [0.98854, 1.00842] | 1.00521 [0.99779, 1.01253] | reader_on_baseline_file |
| `FLOAT_nonaligned_p0_null1_props0_app0_w1_row_parallel0` | 0.98923 [0.98533, 0.99584] | 1.00013 [0.98724, 1.00174] | 0.99870 [0.98947, 1.00127] | 0.98855 [0.98464, 1.00265] | none |
| `FLOAT_nonaligned_p0_null1_props0_app0_w1_batch_parallel0` | 0.99497 [0.98161, 0.99914] | 0.99334 [0.98964, 1.01755] | 1.00594 [0.99946, 1.03570] | 0.99979 [0.99063, 1.01357] | none |

### Independent confirmations

| Scenario | Contrast | Block-median ratio [95% CI] | Descriptive p95 ratio |
|---|---|---|---|
| `FLOAT_aligned_p2_null0_props0_all_w4_batch_parallel0` | `reader_on_baseline_file` | 0.96608 [0.96374, 0.97194] | 0.96530 |
| `FLOAT_aligned_p2_null0_props0_all_w4_batch_parallel0` | `reader_on_fixed_file` | 0.96790 [0.96463, 0.97088] | 0.97829 |
| `FLOAT_aligned_p2_null0_props0_all_w4_batch_parallel0` | `writer_products_fixed_reader` | 0.99798 [0.99423, 1.00177] | 1.00149 |
| `FLOAT_aligned_p2_null0_props0_all_w4_batch_parallel0` | `end_to_end` | 0.96499 [0.96161, 0.96918] | 0.96674 |
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` | `reader_on_baseline_file` | 1.01040 [1.00781, 1.01185] | 1.01620 |
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` | `reader_on_fixed_file` | 1.01008 [1.00814, 1.01202] | 1.01207 |
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` | `writer_products_fixed_reader` | 0.99951 [0.99774, 1.00136] | 0.99278 |
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` | `end_to_end` | 1.01064 [1.00832, 1.01370] | 1.00886 |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` | `reader_on_baseline_file` | 1.01164 [1.00780, 1.01404] | 1.00975 |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` | `reader_on_fixed_file` | 1.01102 [1.00645, 1.01280] | 1.00139 |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` | `writer_products_fixed_reader` | 0.99956 [0.99665, 1.00243] | 0.99750 |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` | `end_to_end` | 1.01274 [1.00943, 1.01434] | 1.00724 |
| `DOUBLE_aligned_p0_null1_props0_time_w1_row_parallel1` | `reader_on_baseline_file` | 0.99888 [0.99447, 1.00198] | 0.99048 |
| `DOUBLE_aligned_p0_null1_props0_time_w1_row_parallel1` | `reader_on_fixed_file` | 1.00248 [0.99996, 1.00952] | 1.01511 |
| `DOUBLE_aligned_p0_null1_props0_time_w1_row_parallel1` | `writer_products_fixed_reader` | 0.99971 [0.99154, 1.00799] | 1.00934 |
| `DOUBLE_aligned_p0_null1_props0_time_w1_row_parallel1` | `end_to_end` | 1.00243 [0.99532, 1.00743] | 0.99973 |
| `DOUBLE_aligned_p0_null1_props0_app1_w4_batch_parallel1` | `reader_on_baseline_file` | 1.00144 [0.99659, 1.00598] | 1.03986 |
| `DOUBLE_aligned_p0_null1_props0_app1_w4_batch_parallel1` | `reader_on_fixed_file` | 1.00442 [0.99823, 1.00693] | 1.02102 |
| `DOUBLE_aligned_p0_null1_props0_app1_w4_batch_parallel1` | `writer_products_fixed_reader` | 0.95549 [0.95137, 0.96533] | 0.97670 |
| `DOUBLE_aligned_p0_null1_props0_app1_w4_batch_parallel1` | `end_to_end` | 0.95659 [0.95240, 0.96124] | 1.01563 |
| `DOUBLE_nonaligned_p0_null1_props0_time_w1_batch_parallel1` | `reader_on_baseline_file` | 0.99949 [0.99379, 1.00221] | 0.99969 |
| `DOUBLE_nonaligned_p0_null1_props0_time_w1_batch_parallel1` | `reader_on_fixed_file` | 0.99811 [0.99294, 1.00163] | 1.00554 |
| `DOUBLE_nonaligned_p0_null1_props0_time_w1_batch_parallel1` | `writer_products_fixed_reader` | 0.99801 [0.99555, 1.00635] | 1.00564 |
| `DOUBLE_nonaligned_p0_null1_props0_time_w1_batch_parallel1` | `end_to_end` | 0.99938 [0.99285, 1.00380] | 1.00533 |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_batch_parallel0` | `reader_on_baseline_file` | 0.99980 [0.99718, 1.00588] | 0.99850 |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_batch_parallel0` | `reader_on_fixed_file` | 1.00439 [0.99735, 1.00835] | 1.01848 |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_batch_parallel0` | `writer_products_fixed_reader` | 1.00222 [0.99646, 1.00879] | 1.01459 |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_batch_parallel0` | `end_to_end` | 1.00447 [1.00052, 1.01037] | 1.01307 |

### Full-result descriptive metrics

| Scenario | Baseline / fixed full p50 (ms) | Baseline / fixed full p95 (ms) |
|---|---|---|
| `FLOAT_aligned_p2_null0_props0_all_w4_row_parallel0` | 3.5455 / 3.4570 | 4.5075 / 4.3088 |
| `FLOAT_aligned_p2_null0_props0_all_w4_batch_parallel0` | 3.0257 / 2.9135 | 3.8915 / 3.9335 |
| `FLOAT_aligned_p0_null1_props0_time_w1_row_parallel1` | 0.9124 / 0.9034 | 1.7702 / 1.7605 |
| `FLOAT_aligned_p0_null1_props0_time_w1_batch_parallel1` | 0.7871 / 0.7595 | 1.6173 / 1.5833 |
| `FLOAT_aligned_p0_null1_props0_app1_w4_row_parallel1` | 13.2801 / 12.1648 | 14.2682 / 13.9798 |
| `FLOAT_aligned_p0_null1_props0_app1_w4_batch_parallel1` | 12.6378 / 11.7038 | 13.5859 / 13.2407 |
| `FLOAT_nonaligned_p2_null0_props0_all_w4_row_parallel0` | 15.5145 / 15.2483 | 16.3551 / 16.1612 |
| `FLOAT_nonaligned_p2_null0_props0_all_w4_batch_parallel0` | 14.8230 / 14.7099 | 15.7360 / 15.7075 |
| `FLOAT_nonaligned_p0_null1_props0_time_w1_row_parallel1` | 2.6799 / 2.6643 | 3.5292 / 3.4890 |
| `FLOAT_nonaligned_p0_null1_props0_time_w1_batch_parallel1` | 2.5585 / 2.5122 | 3.4466 / 3.3413 |
| `FLOAT_nonaligned_p0_null1_props0_app1_w4_row_parallel1` | 16.4375 / 15.8643 | 17.4818 / 16.9946 |
| `FLOAT_nonaligned_p0_null1_props0_app1_w4_batch_parallel1` | 15.9959 / 15.3727 | 16.8967 / 16.3056 |
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` | 3.3571 / 3.3748 | 4.2532 / 4.2875 |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` | 2.8268 / 2.8561 | 3.7300 / 3.7186 |
| `DOUBLE_aligned_p0_null1_props0_time_w1_row_parallel1` | 0.8896 / 0.8883 | 1.7423 / 1.7537 |
| `DOUBLE_aligned_p0_null1_props0_time_w1_batch_parallel1` | 0.7593 / 0.7583 | 1.5941 / 1.6192 |
| `DOUBLE_aligned_p0_null1_props0_app1_w4_row_parallel1` | 13.3555 / 12.5720 | 15.8556 / 14.4255 |
| `DOUBLE_aligned_p0_null1_props0_app1_w4_batch_parallel1` | 12.7661 / 12.3012 | 14.1153 / 14.6324 |
| `DOUBLE_nonaligned_p2_null0_props0_all_w4_row_parallel0` | 14.9075 / 14.9347 | 15.9483 / 15.8542 |
| `DOUBLE_nonaligned_p2_null0_props0_all_w4_batch_parallel0` | 14.3939 / 14.4279 | 15.4036 / 15.4637 |
| `DOUBLE_nonaligned_p0_null1_props0_time_w1_row_parallel1` | 2.6290 / 2.6166 | 3.4930 / 3.4399 |
| `DOUBLE_nonaligned_p0_null1_props0_time_w1_batch_parallel1` | 2.5067 / 2.5229 | 3.3548 / 3.4086 |
| `DOUBLE_nonaligned_p0_null1_props0_app1_w4_row_parallel1` | 16.0373 / 15.6579 | 17.1440 / 16.6062 |
| `DOUBLE_nonaligned_p0_null1_props0_app1_w4_batch_parallel1` | 15.6529 / 15.2169 | 16.5942 / 16.1048 |
| `FLOAT_aligned_p2_null1_props0_tag_w4_row_parallel1` | 6.7261 / 6.7022 | 7.8310 / 7.5929 |
| `FLOAT_aligned_p2_null1_props0_tag_w4_batch_parallel1` | 6.4606 / 6.3993 | 7.2847 / 7.8730 |
| `DOUBLE_nonaligned_p2_null1_props0_tag_w4_row_parallel0` | 8.0602 / 8.1063 | 8.9073 / 9.0038 |
| `DOUBLE_nonaligned_p2_null1_props0_tag_w4_batch_parallel0` | 7.8905 / 7.8572 | 8.7332 / 8.6511 |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_row_parallel0` | 1.4880 / 1.4861 | 2.3365 / 2.3220 |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_batch_parallel0` | 1.2324 / 1.2408 | 2.0876 / 2.1183 |
| `FLOAT_nonaligned_p0_null1_props0_app0_w1_row_parallel0` | 5.1671 / 5.1090 | 5.9835 / 5.9049 |
| `FLOAT_nonaligned_p0_null1_props0_app0_w1_batch_parallel0` | 4.9274 / 4.9499 | 5.7205 / 6.0849 |

### Open, first row, throughput and memory

Open includes native initialization; schema lookup may reuse metadata loaded by open. First accepted-row latency includes initialization/query setup and full row validation; app0 has no accepted first row. Throughput is computed from complete verified per-query latency (input and accepted rows separately). Peak working set is the whole native child process, not incremental query memory. These are descriptive baseline/fixed medians from end-to-end variants.

| Scenario | Open µs B/F | Cached schema µs B/F | First accepted µs B/F | Input rows/s B/F | Accepted rows/s B/F | Peak MiB B/F |
|---|---|---|---|---|---|---|
| `FLOAT_aligned_p2_null0_props0_all_w4_row_parallel0` | 54.25 / 52.15 | 7.25 / 7.45 | 182.65 / 181.05 | 18484279 / 18957753 | 18484279 / 18957753 | 5.48 / 5.48 |
| `FLOAT_aligned_p2_null0_props0_all_w4_batch_parallel0` | 51.50 / 53.10 | 6.30 / 7.40 | 180.50 / 180.95 | 21659781 / 22493913 | 21659781 / 22493913 | 5.48 / 5.48 |
| `FLOAT_aligned_p0_null1_props0_time_w1_row_parallel1` | 48.10 / 48.55 | 5.95 / 6.20 | 148.10 / 147.40 | 35918681 / 36276496 | 35918681 / 36276496 | 5.38 / 5.36 |
| `FLOAT_aligned_p0_null1_props0_time_w1_batch_parallel1` | 47.05 / 46.85 | 6.05 / 5.95 | 146.60 / 142.80 | 41638934 / 43154916 | 41638934 / 43154916 | 5.38 / 5.36 |
| `FLOAT_aligned_p0_null1_props0_app1_w4_row_parallel1` | 71.55 / 72.75 | 10.00 / 10.60 | 1038.55 / 923.40 | 4934903 / 5387347 | 49397 / 53926 | 6.20 / 6.17 |
| `FLOAT_aligned_p0_null1_props0_app1_w4_batch_parallel1` | 72.15 / 71.80 | 9.55 / 10.40 | 1045.40 / 928.60 | 5185713 / 5599549 | 51908 / 56050 | 6.18 / 6.18 |
| `FLOAT_nonaligned_p2_null0_props0_all_w4_row_parallel0` | 71.20 / 66.10 | 8.30 / 7.90 | 439.50 / 424.15 | 4224165 / 4297923 | 4224165 / 4297923 | 5.56 / 5.55 |
| `FLOAT_nonaligned_p2_null0_props0_all_w4_batch_parallel0` | 66.10 / 67.30 | 7.90 / 8.10 | 427.05 / 418.25 | 4421252 / 4455231 | 4421252 / 4455231 | 5.57 / 5.55 |
| `FLOAT_nonaligned_p0_null1_props0_time_w1_row_parallel1` | 50.05 / 50.30 | 6.50 / 6.55 | 171.95 / 170.20 | 12229791 / 12301401 | 12229791 / 12301401 | 5.35 / 5.33 |
| `FLOAT_nonaligned_p0_null1_props0_time_w1_batch_parallel1` | 49.85 / 48.80 | 6.50 / 6.35 | 175.15 / 171.25 | 12809852 / 13046196 | 12809852 / 13046196 | 5.35 / 5.33 |
| `FLOAT_nonaligned_p0_null1_props0_app1_w4_row_parallel1` | 69.00 / 66.75 | 8.20 / 8.40 | 447.75 / 438.05 | 3986981 / 4131036 | 39909 / 41351 | 5.57 / 5.52 |
| `FLOAT_nonaligned_p0_null1_props0_app1_w4_batch_parallel1` | 68.00 / 66.75 | 8.20 / 8.20 | 443.45 / 435.15 | 4097050 / 4263142 | 41011 / 42673 | 5.57 / 5.53 |
| `DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0` | 52.40 / 51.45 | 5.80 / 5.80 | 173.20 / 167.20 | 19521320 / 19419225 | 19521320 / 19419225 | 5.43 / 5.42 |
| `DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0` | 52.10 / 51.05 | 5.60 / 5.70 | 166.00 / 163.20 | 23183816 / 22946440 | 23183816 / 22946440 | 5.43 / 5.42 |
| `DOUBLE_aligned_p0_null1_props0_time_w1_row_parallel1` | 48.15 / 48.85 | 5.90 / 6.20 | 148.75 / 148.90 | 36843367 / 36895260 | 36843367 / 36895260 | 5.39 / 5.36 |
| `DOUBLE_aligned_p0_null1_props0_time_w1_batch_parallel1` | 48.20 / 48.10 | 5.70 / 6.30 | 148.10 / 147.80 | 43163488 / 43220422 | 43163488 / 43220422 | 5.39 / 5.36 |
| `DOUBLE_aligned_p0_null1_props0_app1_w4_row_parallel1` | 75.30 / 76.30 | 12.00 / 11.85 | 1042.50 / 962.55 | 4907042 / 5212855 | 49118 / 52179 | 6.36 / 6.34 |
| `DOUBLE_aligned_p0_null1_props0_app1_w4_batch_parallel1` | 72.35 / 71.25 | 11.95 / 11.40 | 1045.40 / 959.15 | 5133616 / 5327590 | 51386 / 53328 | 6.35 / 6.33 |
| `DOUBLE_nonaligned_p2_null0_props0_all_w4_row_parallel0` | 68.10 / 65.95 | 7.75 / 7.70 | 417.55 / 412.40 | 4396167 / 4388170 | 4396167 / 4388170 | 5.49 / 5.47 |
| `DOUBLE_nonaligned_p2_null0_props0_all_w4_batch_parallel0` | 66.20 / 65.45 | 7.60 / 7.85 | 410.35 / 409.25 | 4553025 / 4542295 | 4553025 / 4542295 | 5.49 / 5.47 |
| `DOUBLE_nonaligned_p0_null1_props0_time_w1_row_parallel1` | 49.25 / 48.80 | 6.40 / 6.20 | 170.25 / 171.95 | 12466347 / 12525415 | 12466347 / 12525415 | 5.35 / 5.31 |
| `DOUBLE_nonaligned_p0_null1_props0_time_w1_batch_parallel1` | 50.00 / 49.45 | 6.05 / 6.00 | 170.65 / 172.20 | 13074300 / 12990356 | 13074300 / 12990356 | 5.34 / 5.31 |
| `DOUBLE_nonaligned_p0_null1_props0_app1_w4_row_parallel1` | 69.05 / 67.25 | 7.85 / 8.30 | 440.25 / 431.35 | 4086474 / 4185478 | 40905 / 41896 | 5.49 / 5.45 |
| `DOUBLE_nonaligned_p0_null1_props0_app1_w4_batch_parallel1` | 66.15 / 67.45 | 7.95 / 8.10 | 441.10 / 438.85 | 4186828 / 4306805 | 41909 / 43110 | 5.49 / 5.45 |
| `FLOAT_aligned_p2_null1_props0_tag_w4_row_parallel1` | 67.55 / 66.90 | 10.35 / 10.05 | 1047.40 / 1023.85 | 4871769 / 4889177 | 4871769 / 4889177 | 6.14 / 6.15 |
| `FLOAT_aligned_p2_null1_props0_tag_w4_batch_parallel1` | 67.55 / 67.90 | 9.40 / 9.85 | 1033.45 / 1007.45 | 5071975 / 5120561 | 5071975 / 5120561 | 6.14 / 6.14 |
| `DOUBLE_nonaligned_p2_null1_props0_tag_w4_row_parallel0` | 62.05 / 61.95 | 7.40 / 7.50 | 430.05 / 432.00 | 4065383 / 4042290 | 4065383 / 4042290 | 5.49 / 5.46 |
| `DOUBLE_nonaligned_p2_null1_props0_tag_w4_batch_parallel0` | 63.80 / 61.10 | 7.55 / 7.60 | 432.85 / 427.30 | 4152869 / 4170416 | 4152869 / 4170416 | 5.49 / 5.46 |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_row_parallel0` | 47.85 / 48.40 | 6.00 / 5.80 | 121.10 / 122.25 | 44044492 / 44097837 | 22034343 / 22061030 | 5.38 / 5.37 |
| `DOUBLE_aligned_p2_null1_props0_app50_w1_batch_parallel0` | 48.35 / 49.20 | 5.60 / 5.95 | 122.70 / 122.75 | 53179704 / 52817537 | 26604458 / 26423275 | 5.38 / 5.36 |
| `FLOAT_nonaligned_p0_null1_props0_app0_w1_row_parallel0` | 60.40 / 53.55 | 7.35 / 7.30 | N/A (zero accepted) | 12683201 / 12827560 | 0 / 0 | 5.33 / 5.30 |
| `FLOAT_nonaligned_p0_null1_props0_app0_w1_batch_parallel0` | 54.00 / 61.05 | 6.80 / 7.55 | N/A (zero accepted) | 13300321 / 13240000 | 0 / 0 | 5.34 / 5.31 |

**Disposition:** The corrected comparison still has unresolved confirmation signals; the query gate remains uncleared. There were 7 initial cases selected for independent confirmation; remaining confirmation signals: `{"DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0": ["reader_on_baseline_file", "reader_on_fixed_file", "end_to_end"], "DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0": ["reader_on_baseline_file", "reader_on_fixed_file", "end_to_end"], "DOUBLE_aligned_p2_null1_props0_app50_w1_batch_parallel0": ["end_to_end"]}`. This is a measured-scope disposition, not a promise that every original fixed image identity has zero latency change. Its observed approximately 0.75–0.78% context effect stays explicitly published. No production source fix or new Java/coverage/write benchmark is inferred from the protocol repair. All 22 existing PR02 writer products retain their Java audit and exact copied SHA-256; open/metadata/first-row/full-result/memory arrays are retained for every child. The previous write/correctness/coverage reports retain their scope and known Java-side boundary failures.

Cold cache, P99, native FIELD pushdown, sole/all-NULL projections, large metadata sets, physical-core scaling and compressed-query performance remain outside this corpus. The initial/confirmation results and fixed protocol are in `counterbalanced-matrix-*.json`; run `counterbalanced_matrix.py` only in a fresh result directory. It refuses to overwrite an initial run. `--analyze-only` recomputes statistics without new timing samples.

## 中文说明

为减少旧实验中调用程序、CPU 与协议同时改变的混杂，本轮统一为恢复执行前绑核、相同亲和性 12、相同文件与查询计时。行/批 × 混合/独立 reader 共四组，每组固定 192 轮四标签、每个版本每轮两个进程、每进程三次完整查询。全部 3,072 个计时进程、9,216 次查询逐单元格核验完整结果；原二进制、输入文件哈希及源码目录状态均复核一致。两次预热与全部异常样本保留，未按结果延长采样或更改通过阈值。

主比较直接估计同一轮“混合程序前后比 / 独立 reader 前后比”，按 24 个连续时间块重采样，结果见上表。这样可以约束调用程序依赖性，但混合 writer 路径和统一编译对象等因素一起改变，仍不能单独确定链接布局因果关系。置信区间包含 1 也不能证明完全等价。每轮同一版本的两次运行作为内部负对照；主线程生命周期周期数包含启动/输出/退出，不是查询区间 CPU 或退休指令数。

链接地址映射在全部计时结束后生成，旁路程序的指令/异常信息与原计时程序相同，rdata 只允许 debug 构建时间戳不同；地址和模 64 偏移不等同于缓存计数器证据。旧的正向、反向结果与所有原始证据继续保留，**这两项诊断本身不清除门槛，完整矩阵结论另列**，不会通过修改 padding 或放宽标准得到通过结果。原 Java 兼容、覆盖率与写入性能证据沿用原范围；本轮没有生产代码修改或新的完整 sanitizer/覆盖率测试声明。

第一阶段两种调用程序的交互区间都包含 1，且独立 reader 也有延迟上升，因此未支持“只有混合程序受影响”的解释。得到该结果后，另行事先固定第二阶段计划：四个中性路径轮换放入两版原始 reader-only 二进制，每 8 轮更换分配，每个路径承载两版各 12 个区块；副本字节、静态地址均不修改，复制后核对 SHA-256 并单独预热。行/批 × 原路径/中性路径再测四组各 192 轮，同一轮的中性路径比 / 原路径比作为主交互。两阶段总计 6,144 个计时进程、18,432 次完整查询，另有明确列出的预热。

第二阶段同时改变文件路径、映像文件背景、加载/缓存历史和可能的 ASLR 位置；运行基址、物理映射及硬件缓存计数器未测，不能只归因于文件名。主结果与全部重复标签对照见上表，两阶段分开保留，不把第二阶段冒充第一阶段事先规定的确认实验；任何区间包含 1 也不等同于证明完全兼容或性能等价。

第三阶段修复的是已验证的**基准比较条件混杂**，没有修改 C++ 生产代码、padding 或数值容忍阈值：四个中性程序路径均等承载两版 reader，四个数据路径均等承载两版真实 writer 产物。完整 32 场景各测 64 轮（八个身份区块），每区块复制核验后每标签两次预热，再完整消费核对三次查询；身份与标签位置均衡，未估计全部路径高阶交互。整组置信区间按身份区块重采样，避免把共享路径分配的样本冒充独立观测。

沿用原有规则：配对中位数区间完全大于 1、中位数超过 1.03 或描述性 p95 比超过 1.10 时，独立复查该场景一次、192 轮；之后不再反复重跑求通过。本轮初测 7 个场景触发复查；剩余信号为 `{"DOUBLE_aligned_p2_null0_props0_all_w4_row_parallel0": ["reader_on_baseline_file", "reader_on_fixed_file", "end_to_end"], "DOUBLE_aligned_p2_null0_props0_all_w4_batch_parallel0": ["reader_on_baseline_file", "reader_on_fixed_file", "end_to_end"], "DOUBLE_aligned_p2_null1_props0_app50_w1_batch_parallel0": ["end_to_end"]}`。**纠正后的比较仍有未解决的复查信号，查询门槛未通过**，只适用于报告中的可比条件和场景，并不声称原固定映像身份的约 0.75%–0.78% 差异已从所有环境消失。该原始效应和所有相反方向结果仍公开保留，不把修复比较方法冒充源码修复或 Java/覆盖率/写入性能重测。

全部 22 个原 PR02 writer 文件的 Java 审计与复制 SHA-256 可追溯；每个计时子进程仍保留打开、schema、构建查询、首行、完整延迟与峰值内存数组。初测每版本/产物有 64 个进程、192 次查询，复查为 192 个进程、576 次查询，不能把它们当作全部独立样本。未测项继续列出，所有初测触发和异常样本保留。两项诊断加完整矩阵总计 19712 个计时进程、59136 次完整查询，另有单列的预热。

**AI disclosure:** The implementation, tests and description in this pull request were written by an AI coding agent (OpenAI Codex), which also performed the reported local validation.

**AI 使用说明：** 本 PR 的代码修改、测试和正文由 AI 编程代理（OpenAI Codex）编写，文中报告的本地验证也由该 AI 代理执行。
