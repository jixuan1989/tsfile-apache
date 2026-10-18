# PR #1024: separate GCC/WSL query scope comparison

**This does not clear the original Windows query-performance gate or prove necessary cost.** The fixed three-case GCC/WSL protocol did not reproduce an upward direction, but a baseline same-binary batch control has a nonneutral interval. Compiler, OS/virtualization, LTO, filesystem and file-tail bytes change together; these data do not isolate a compiler cause or establish general speedup/equivalence.

## Scope and fixed method

Both C++ trees were freshly archived from pinned commits: baseline `1180b13675e11a0230708af2cc70d037e0e12623`, fixed `75592b89d1523a96090e8bca1dcb4cd2180162e5`. GCC11.4, Ubuntu22.04 under WSL2 kernel5.15.167.4, stock project Release `-O3 -flto -DNDEBUG`, static libraries, threads/memory statistics enabled, SIMD/ANTLR4 disabled, all six bundled compressors enabled. The unchanged query driver uses `-O3 -DNDEBUG -flto -std=c++14`. All query files are UNCOMPRESSED. Pinned source archives, driver, actual libraries/binaries, CMake caches/commands and tool versions are hashed and retained locally. No production source change or candidate was made.

The predeclared plan covers exactly the three residual Windows scenarios, 48 quartets each, two copies of each reader version, three fully consumed/checked queries per child: **576 measured processes /1,728 queries**. Four shared executable paths and execution positions are balanced12times per copy; case order is balanced16times per position. There were 1,152 excluded warmup processes /3,456 queries and 12 excluded cross-writer smoke processes /36 queries. Warmups are fixed before each image-path round; no optional extension or sample trimming. Child guest affinity CPUs2,3 is set and asserted before exec; parent CPU4. Reported guest topology groups2/3 on one guest core; actual host mapping/SMT contention is not independently controlled. Executables/data reside on WSL ext4; warm filesystem cache, no controlled cold-cache claim.

Every query validates all65,536 rows, projected values/NULLs, timestamps/order and checksum, including rejected application-filter rows. Timers include open/schema lookup/plan/result materialization/checking/destruction/close. `app50` is the correct application-side predicate `floor(v0/8)%100 <50` over fully materialized rows; its materialization cost is included. It is not native FIELD pushdown or comparison with an ignored/hanging predicate. Sparse input has NULLs in other columns, but the timed app50 projection is only non-NULL v0; it does not measure NULL-valued FIELD-filter performance.

For each round, compare summed full time of both fixed copies with both baseline copies. Primary statistic: median of12 chronological four-round block medians, bootstrapped10,000times (seed102420). Per-query p50/p95 use288 observations/version/case clustered in96 processes; p95 is descriptive, with no p95/P99 noninferiority inference. All initial/adverse observations and copy controls remain in results.json.

## Full-query results

| Case | Block-median fixed/baseline change | Bootstrap95% | Descriptive p95 ratio |
| --- | ---: | ---: | ---: |
| dense row /4 FIELDs | -0.5438% | -1.0344% to -0.0121% | 0.987829 |
| dense batch /4 FIELDs | -0.3062% | -0.6975% to +0.0477% | 0.995874 |
| sparse batch /app50 /1 FIELD | -0.7752% | -2.5451% to +0.0266% | 0.971948 |

The baseline dense-batch copy2/copy1 control is +0.2990%, interval [+0.0826%,+0.4332%]. Preserve it as a control limitation; do not classify the finite comparison as a clean equivalence/pass. The other five copy-control intervals include1. Multiple retrospective comparisons are descriptive; no multiplicity-adjusted universal claim is made.

| Case | Same binary copy2/copy1 | Block change | Bootstrap95% |
| --- | --- | ---: | ---: |
| dense row /4 FIELDs | baseline | +0.0180% | -0.5935% to +0.1817% |
| dense row /4 FIELDs | fixed | +0.0271% | -0.3570% to +0.3924% |
| dense batch /4 FIELDs | baseline | +0.2990% | +0.0826% to +0.4332% |
| dense batch /4 FIELDs | fixed | -0.0095% | -0.4706% to +0.4244% |
| sparse batch /app50 /1 FIELD | baseline | -0.0072% | -0.6503% to +1.0571% |
| sparse batch /app50 /1 FIELD | fixed | -0.1751% | -0.7957% to +0.6758% |

| Case | Reader | Full p50 ms | Full p95 ms | Decoded rows/s p50 | Accepted rows/s p50 | Peak process RSS bytes p50 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| dense row /4 FIELDs | baseline | 4.2275 | 4.5438 | 15502475 | 15502475 | 22697984 |
| dense row /4 FIELDs | fixed | 4.2157 | 4.4885 | 15545735 | 15545735 | 22700032 |
| dense batch /4 FIELDs | baseline | 3.4340 | 3.6413 | 19084569 | 19084569 | 22700032 |
| dense batch /4 FIELDs | fixed | 3.4241 | 3.6263 | 19139567 | 19139567 | 22700032 |
| sparse batch /app50 /1 FIELD | baseline | 1.2437 | 1.3756 | 52695439 | 26362193 | 22700032 |
| sparse batch /app50 /1 FIELD | fixed | 1.2290 | 1.3370 | 53323917 | 26676604 | 22700032 |

| Case | Reader | Open p50 us | Metadata p50 us | Plan p50 us | First accepted row p50 us |
| --- | --- | ---: | ---: | ---: | ---: |
| dense row /4 FIELDs | baseline | 7.104 | 6.894 | 8.401 | 96.531 |
| dense row /4 FIELDs | fixed | 6.976 | 6.753 | 8.356 | 97.025 |
| dense batch /4 FIELDs | baseline | 6.801 | 6.604 | 8.255 | 95.751 |
| dense batch /4 FIELDs | fixed | 6.840 | 6.615 | 8.275 | 95.949 |
| sparse batch /app50 /1 FIELD | baseline | 6.221 | 6.076 | 5.406 | 53.993 |
| sparse batch /app50 /1 FIELD | fixed | 6.153 | 5.997 | 5.392 | 53.130 |

Peak RSS is Linux `ru_maxrss*1024` for the whole process, not an isolated query allocation peak. Full open/metadata/plan/first-decoded/first-accepted/full arrays and p95 are retained in the evidence.

## Writer products and correctness cross-checks

Dense and sparse aligned DOUBLE precision2 files were generated independently with each Linux writer. Each baseline/fixed pair is byte-identical (169,559 and392,839bytes), so the same Linux file supplies an equivalent reader comparison for both writer products. C++ self/cross reads passed all12 smoke processes. The corresponding Windows file has the same length and identical bytes up to its final87bytes; exactly69bytes differ in that tail. These are byte observations, not a proven metadata/bloom-filter cause; no new cross-platform format issue is asserted.

After timing, four Linux C++ files were independently read in Java: all values/types/NULLs/timestamps,32value chunks,1,024value pages and page precision2 passed. Both native reader versions additionally consumed Windows→Linux and Linux→Windows products across all three cases:12 processes /36 extra checked queries. These are separate correctness checks; their returned native timer arrays are not substituted into the48-quartet comparison. **No new Java→C++ run** was performed. Earlier bidirectional Java and coverage/write evidence retains its original scope; this report adds one-way Java reads and native cross-platform reads only.

## Limits and next inference

This finite WSL/GCC observation bounds platform scope and does not fix, replace or clear the original MSVC signals. Different original-image code/data/link context, virtualization, filesystems, CPUs and tail bytes prevent a single-factor attribution. The stopped private read_buf probe remains stopped; no direct-call timings, layout/rounding variant, repeated administrator capture or new production push occurred. No new coverage, sanitizer suite or write-throughput result is claimed. Cold cache, bare-metal Linux, P99, compressed queries, general parallel scaling, native FIELD filtering and special floating-value latency remain unmeasured here. Correctness, write and query conclusions are kept separate.

## 中文译稿

**原Windows查询性能门槛仍未通过，必要代价未证明。** 本轮是独立的GCC/WSL范围比较，不是修复候选，也不替代原验收。精确提交号见上，使用GCC11.4/Ubuntu22.04/WSL2，标准Release `-O3 -flto -DNDEBUG`、静态库、线程和内存统计开启、SIMD/ANTLR4关闭，六种压缩库均编入，但查询数据UNCOMPRESSED。原查询驱动未改，生产源码未改；源归档、库、可执行文件、命令及实际构建选项均留存哈希。

事先固定三个场景、每场景48轮，每版两个副本、每进程三次完整核验查询，共576正式进程/1728查询；1152预热进程/3456查询、12次交叉writer预检进程/36查询单列。每副本在四路径及四位置各出现12次，三个场景在各顺序位置各16次；没有加轮数或剔除异常。子进程exec前设置并核对guest CPU2/3，父进程CPU4；guest拓扑不代表已独立控制宿主SMT映射/争用。使用WSL ext4及热文件系统缓存，没有受控冷缓存结论。

每次完整消费并核对65536行及所有投影值、NULL、时间、顺序和校验和。计时包括打开、元数据、计划、物化、检查与关闭。app50为应用层完整物化后按 `floor(v0/8)%100 <50` 筛选，包含物化成本，不是native FIELD下推。稀疏文件其他列有NULL，但该计时只投影非NULL的v0，不冒充NULL值过滤性能。主统计为12个连续四轮区块中位数，再进行10000次bootstrap（seed102420）；每版本/场景288个逐查询时间，聚集在96个进程中，p95仅作描述，不声称p95/P99非劣性。

三个场景区块变化分别约−0.5438%、−0.3062%、−0.7752%，区间及打开/元数据/首行/全查询吞吐/峰值RSS见上表。但dense-batch的baseline同二进制副本对照为+0.2990%，95%区间[+0.0826%,+0.4332%]，必须保留为限制，不能宣称干净的性能等价或通过。其余五个副本对照区间跨1。没有在此引入可接受退化阈值。

Linux两版writer各自产生文件，dense/sparse对应字节完全一致。Windows文件长度相同，前部字节相同，仅最后87字节内有69字节差异；没有断言其具体结构或新格式缺陷。计时完成后，4份Linux C++文件被Java逐值/类型/NULL/时间完整读取，每份32个value chunk、1024个value page、精度2均核对通过；Windows/Linux两版C++互读另做12进程/36次查询通过，这些时间不纳入正式统计。本轮没有新Java→C++运行，不把一向Java读取冒充双向验证；既有双向互通、覆盖率和写入证据保留原范围。

编译器、OS/虚拟化、LTO、文件系统、CPU及文件尾字节共同变化，不能单独归因于编译器或宣称整体加速。原Windows信号和全部相反/异常样本保留，查询门槛仍未通过。已停止的read_buf探针不重跑；没有直接调用计时、新布局/舍入候选、重复管理员采集、生产推送或新增覆盖率/写入吞吐/全sanitizer通过声明。受控冷缓存、裸机Linux、P99、压缩查询、并行扩展、native FIELD过滤及特殊浮点性能仍未测。
