# TsFile #1020 本地验证报告

基线：`1180b13675e11a0230708af2cc70d037e0e12623`。修复提交：`5f4bc79a6db4d6cf79eb089a9dabe0e1fc4e12bb`。

输入值 `1.23456`，FLOAT/DOUBLE TS_2DIFF 的 `max_point_number=0` 原来写入后读回 `1.23`，现在与 Java 一致为 `1.0`；精度 `4` 从 `1.23` 修正为 `1.2346`。修复显式复制注册 schema 的属性，将其传至 chunk/page writer 与 encoder factory；保留旧接口重载和类布局。参数仅在初始化解析。极大精度下零乘无穷产生 NaN，增加 Java Math.round 对应的返回零处理。

## 正确性

同一组 49 项 writer 回归使用原版头文件/静态库时 33 项失败、16 项通过；修复后 49 项全部通过。48 项参数化案例覆盖 FLOAT/DOUBLE × 对齐/非对齐 × 复制/转移所有权 schema × Tablet/record × 精度 0/4/default，各 520 行、页上限 17、两次 chunk flush；另有表 value chunk 直接编码检查。另新增 5 项编码器测试，覆盖 35 个解析边界、其他 codec/type、跨页 reset、无穷缩放系数下的正/负零及整数饱和/舍入边界，共 54 项。

| 全量回归 | 通过 | 跳过 | 原有禁用 | 失败 |
|---|---:|---:|---:|---:|
| Windows x64 / MSVC 14.50 / Release / 静态库 | 959 | 3 | 10 | 0 |
| Linux GCC / Debug / 原子 gcov | 980 | 1 | 10 | 0 |

Linux 启用 SNAPPY、LZ4、LZOKAY、ZLIB、ZSTD、LZMA2；Windows 关闭可选压缩库。两者均启用线程和内存统计，关闭 ANTLR、SIMD 和 BUILD_TOOLS，本地批次不包含 CLI E2E。Linux 配置跨语言夹具后两项互通测试实际执行；仍跳过外部数据集索引测试。

## Java 兼容

- 最新基线 Java Maven `CompatibilityTest` 两项通过，JDK 24。
- 122 组 FLOAT/DOUBLE 编码页，每页 260 个值，跨 TS_2DIFF block；Java 写 C++ 读，C++ 写 Java 读，并逐字节比较编码页，122 组全部相同。
- 属性包括缺失键、无关键、0/2/4/9/1000、int-max、溢出、合法负数、符号、空白、内嵌 NUL、补充字符数字及 Java 接受的全部 BMP 数字字符“4”。输入包含正负有限值、正负零、极小值、NaN、无穷、FLOAT/DOUBLE 最大最小值。
- 完整 tree TsFile：FLOAT/DOUBLE × 对齐/非对齐 × 精度 0/2/4/default，共 16 组配置，Java/C++ 各写一份，32 个文件、64 次自身/交叉读取全部通过。
- 原生表模型互通：C++ 读取 135 个 Java 文件，Java 读取 117 个 C++ 文件；包括真实 UNCOMPRESSED/LZ4/ZSTD/LZMA2 数据压缩。仅 CSV 清单换行规范化，TsFile 二进制不改动。
- 表属性序列化仍由独立 #1017 / #1018 处理，本分支不包含那项修改；本项表精度回归直接核对编码页。当前证据对应已列的参数、类型和读写路径，不代表整个 C++ 库与 Java 所有功能完全等价。

## 覆盖率

采用全新 GCC `--coverage -fprofile-update=atomic` 构建，全量测试完成后收集 gcovr。初次普通计数构建出现 GCC 负分支计数错误，旧错误日志单独保留；最终原子计数报告未忽略解析错误、未裁剪负数、未排除异常或错误分支。

| 范围 | 行覆盖率 | 分支覆盖率 |
|---|---|---|
| 修改的生产可执行行 | 75/75 (100.00%) | 105/150 (70.00%) |
| `cpp/src/encoding/encoder_factory.h` 整个文件 | 108/126 (85.71%) | 118/187 (63.10%) |
| `cpp/src/encoding/encoding_props.h` 整个文件 | 38/38 (100.00%) | 60/62 (96.77%) |
| `cpp/src/encoding/ts2diff_encoder.h` 整个文件 | 367/438 (83.79%) | 272/472 (57.63%) |
| `cpp/src/writer/chunk_writer.cc` 整个文件 | 89/92 (96.74%) | 46/64 (71.88%) |
| `cpp/src/writer/page_writer.cc` 整个文件 | 79/91 (86.81%) | 40/68 (58.82%) |
| `cpp/src/writer/tsfile_writer.cc` 整个文件 | 992/1213 (81.78%) | 800/1493 (53.58%) |
| `cpp/src/writer/value_chunk_writer.cc` 整个文件 | 98/101 (97.03%) | 53/70 (75.71%) |
| `cpp/src/writer/value_page_writer.cc` 整个文件 | 80/88 (90.91%) | 45/70 (64.29%) |

新增/修改行按 `git diff --unified=0 1180b13675e11a0230708af2cc70d037e0e12623 -- cpp/src` 的新行集合，与 gcov 可执行行相交。构建复制头文件时先验证源码/副本字节及 SHA-256 相同，再按物理行及 source-block/branch 编号合并。统计包含完整旧模块，不能将其局部结果当作全库覆盖。未覆盖的分支主要涉及内存分配、异常及错误注入路径；完整明细见 coverage-summary.json。

## 性能

同机同 MSVC 14.50 Release 配置、静态库、线程/内存统计启用，时间和值列均 UNCOMPRESSED。两边编译同一份独立 benchmark_driver.cc，使用相同选项，分别链接原版和修复库。record 每组 500,000 行、Tablet 每组 5,000,000 行，每变体预热两次，25 轮交错先后顺序，均固定 CPU 掩码 4。配对比值 bootstrap 10,000 次。计时包含 writer open/register/write/close，Tablet 构造与读回不计入写入耗时；每轮读回全部行并核对值。工作集包括整个进程及读回。最终性能测量期间本任务没有构建或覆盖率收集负载。

| 工作负载 | 基线中位 ms | 修复中位 ms | 配对耗时比中位数 | 配对比 95% CI |
|---|---:|---:|---:|---|
| float_nonaligned_record_default | 177.184 | 177.393 | 1.0025 | [0.9851, 1.0185] |
| double_nonaligned_tablet_default | 50.321 | 50.504 | 0.9853 | [0.9777, 1.0004] |
| float_aligned_tablet_precision_2 | 66.786 | 67.859 | 1.0083 | [0.9975, 1.0183] |
| double_aligned_record_precision_2 | 251.245 | 251.629 | 0.9978 | [0.9784, 1.0101] |

| 工作负载 | 基线行/s | 修复行/s | 基线峰值工作集中位 bytes | 修复峰值工作集中位 bytes |
|---|---:|---:|---:|---:|
| float_nonaligned_record_default | 2,821,925 | 2,818,601 | 5,849,088 | 5,840,896 |
| double_nonaligned_tablet_default | 99,362,293 | 99,001,275 | 89,014,272 | 89,014,272 |
| float_aligned_tablet_precision_2 | 74,866,102 | 73,682,737 | 68,628,480 | 68,636,672 |
| double_aligned_record_precision_2 | 1,990,089 | 1,987,052 | 5,898,240 | 5,902,336 |

本次四组有效输出工作负载未观察到可分辨的性能退化。原版非默认精度 0/4 的输出错误，无法提供等价输出的性能基线，因此性能对照使用原来有效的 default/2，分别覆盖 FLOAT/DOUBLE、aligned/nonaligned、record/Tablet。

排查过程也保留在验证包中：早期驱动只有修复版包含额外 wire 验证代码，可能改变链接实现和代码布局，该数据不作为库性能结论。换为相同的独立驱动后，下界判断方案仍复现 FLOAT 对齐 Tablet 变慢。最终实现将 NaN 纳入原有上界分支，使用现有 FORCE_INLINE 宏保持小舍入函数内联，并避免精度 2 的重复设置；以上表格为最终代码的完整四组测量。此前探索结果、对照和补丁均另行命名保留。

## 格式与证据

clang-format 17.0.6 对 14 份改动逐一检查通过；仓库 Spotless apply/check 通过；补丁空白检查通过。验证包保留失败与通过的日志/XML、编解码原始页和清单、完整文件、覆盖率原始 JSON 和合并脚本、全部性能原始样本与脚本、构建命令、格式日志及提交补丁。

**AI disclosure:** The implementation, tests and description in this pull request were written by an AI coding agent (OpenAI Codex), which also performed the reported local validation.

**AI 使用说明：** 本 PR 的代码修改、测试和正文由 AI 编程代理（OpenAI Codex）编写，文中报告的本地验证也由该 AI 代理执行。
