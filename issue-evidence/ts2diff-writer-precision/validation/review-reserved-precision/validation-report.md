# TsFile PR #1024 审阅修订验证

当前修复提交 `1e8d230805d5823f1e0cd7a82af4e815510080e0`，基线 `1180b13675e11a0230708af2cc70d037e0e12623`。修订前 PR 提交 `5f4bc79a6db4d6cf79eb089a9dabe0e1fc4e12bb`。

两个合法精度值 `2147483646`、`2147483647` 同时也是格式开头的位图标记。全零输入乘无穷并按 Java 规则舍入为零后，所有 scaled flag 都置位，`has_overflow()` 为假；若直接写精度，解码器会把后续整数块当成位图头，C++ 因读到零数量而返回 `E_DECODE_ERR`。现在 FLOAT/DOUBLE 的 `flush()` 遇到这两个精度时，也进入现有位图包装，依次写 scaled-value 标记、数量、全部置位的 scaled 位图、实际精度和整数块。位图之后的精度作为值读取，不再递归当成标记。两边现有 decoder 都支持这个布局，无需修改；只在封页时增加判断，空页仍不输出。

record 的 schema 检查辅助函数改为通过 const 引用借用调用方的 `shared_ptr<DeviceID>`，避免逐条复制所有权及增减引用计数。函数只查找、不保留引用；调用方在整个调用期间拥有对象，临时参数也存活到完整表达式结束。只改私有辅助函数参数，公共 API、对象布局和错误返回保持原样。

新增测试覆盖两种类型、`1000`、`2147483645` 及两个保留值、1/8/129/260 个值、正负零、reset/重复页和全部 writer 路径。兼容性限制：当前 Java 自己也会为两个保留精度产生无法读回的全零页，已复现 16 个原始页及 8 个完整文件；因此修复采用可解码的现有包装，不复制这些无效字节。新增 64 个 C++ 页均能被 Java 读取，48 个有效 Java 页能被 C++ 读取；其中 36 个原始字节相同，12 个单值页只在原有、未使用的零 delta 块最小值字段不同（Java 为 `MAX_VALUE`，C++ 为 `0`），比较时仅规范化该未使用字段。剩余 16 个 Java 页在 Java 自身和 C++ 中都无法读取。新增 8 个全零 C++ 文件自身/Java 读取共 16 次通过；原始证据保留这些边界。

初版包装实现在 FLOAT record 出现可重复变慢（合并全部 125 轮，中位比 1.0172，95% CI [1.0062, 1.0244]）。位图辅助函数及仅强制内联的实验未消除全部 record 信号，均未采用；生成代码、源码快照及所有测量保留。最终版本还修正了上述舍入近似问题，下方四组结果对应最终源码。


新增回归在修订前 33 项失败（32 个 writer 变体及 1 个跨页/边界编码器测试）；修订后全部 88 项专项测试通过。原版基线的既有 49 项 writer 回归仍有 33 项失败，验证属性接线问题。

Windows MSVC 14.50 Release：993 通过、3 跳过、10 原有禁用；Linux GCC 11.4 Debug 原子 gcov：1014 通过、1 跳过、10 原有禁用，无失败。Linux 启用 SNAPPY/LZ4/LZOKAY/ZLIB/ZSTD/LZMA2，原生 GenerateFixtures/ValidateFixtures 均实际执行，覆盖 C++ 读 135 个 Java 文件、Java 读 117 个 C++ 文件；Windows 可选压缩关闭。本地关闭 CLI 工具和 ANTLR/SIMD，线程/内存统计启用。

原有 122 组 × 260 个值的编码页已重跑双向解码和逐字节比较，122 组一致；精度 0/2/4/default、FLOAT/DOUBLE、对齐/非对齐的完整文件重新生成，共 32 个文件、64 次自身/交叉读取通过。新增边界矩阵及 Java 无效输入的实际失败均保留，不将无效 Java 页误计为通过。

舍入的额外 Java 对照包含 1,088,975 个确定性随机/边界输入，同时校验 32 位饱和和 64 位结果，全部一致；旧 floor 近似的 64 位结果有 251 处差异。另生成包含半值相邻数和大奇数的 122 组 × 260 个值的 wire 矩阵，双向读取及原始字节全部一致。舍入实现直接操作 IEEE 有效数，避免 x+0.5 的二次舍入，NaN 返回零，范围外饱和，负数恰好半值向正无穷方向舍入。

## 当前覆盖率

全量 Linux 测试前清理仅构建目录中的旧 gcda，使用 `-O0 -g --coverage -fprofile-update=atomic`；gcovr 未忽略解析错误、未排除分支。逐字节相同的源码/构建复制头文件按物理行及分支标识合并。对最新基线的修改生产可执行行 **97/97 (100.00%)**，相同行分支 **180/402 (44.78%)**，不是全库覆盖率。

| 受影响模块整个文件 | 行 | 分支 |
|---|---|---|
| `cpp/src/encoding/encoder_factory.h` | 108/126 (85.71%) | 118/187 (63.10%) |
| `cpp/src/encoding/encoding_props.h` | 38/38 (100.00%) | 60/62 (96.77%) |
| `cpp/src/encoding/ts2diff_encoder.h` | 383/452 (84.73%) | 336/688 (48.84%) |
| `cpp/src/writer/chunk_writer.cc` | 89/92 (96.74%) | 46/64 (71.88%) |
| `cpp/src/writer/page_writer.cc` | 79/91 (86.81%) | 40/68 (58.82%) |
| `cpp/src/writer/tsfile_writer.cc` | 992/1213 (81.78%) | 800/1493 (53.58%) |
| `cpp/src/writer/value_chunk_writer.cc` | 98/101 (97.03%) | 53/70 (75.71%) |
| `cpp/src/writer/value_page_writer.cc` | 80/88 (90.91%) | 45/70 (64.29%) |

## 当前性能

使用原有同一独立 benchmark_driver.cc、同机 MSVC 14.50 Release、相同编译/链接选项、时间/值均 UNCOMPRESSED、固定 CPU 掩码 4；record 500,000 行，Tablet 5,000,000 行。两边各预热 2 次，每组先 25 轮交错运行，FLOAT record 另做预先固定 100 轮确认，合并保留全部 125 轮；配对中位数 bootstrap 10,000 次。计时包含 open/register/write/close，排除 Tablet 构建与读回；每轮仍完整读回核对全部行。峰值工作集包含整个进程/读回。测量期间无本任务构建/覆盖率负载；最终测量后记录源码、库和驱动 SHA，并在后续全量验证后复核；测量期间没有修改源码或重建二进制。

| 工作负载 | 基线秒 | 修复秒 | 配对中位比 | 95% CI | 基线/修复 行每秒 | 基线/修复 峰值工作集 bytes |
|---|---:|---:|---:|---|---|---|
| float_nonaligned_record_default | 0.171447 | 0.171778 | 1.0000 | [0.9941, 1.0049] | 2,916,353 / 2,910,734 | 5,844,992 / 5,828,608 |
| double_nonaligned_tablet_default | 0.050030 | 0.049999 | 0.9812 | [0.9662, 0.9901] | 99,940,236 / 100,002,000 | 89,018,368 / 89,018,368 |
| float_aligned_tablet_precision_2 | 0.066084 | 0.064618 | 0.9822 | [0.9756, 0.9868] | 75,661,852 / 77,378,180 | 68,628,480 / 68,636,672 |
| double_aligned_record_precision_2 | 0.247340 | 0.247682 | 0.9999 | [0.9910, 1.0044] | 2,021,509 / 2,018,718 | 5,898,240 / 5,898,240 |

四组等价输出工作负载未观察到可分辨退化；原版非默认精度输出错误，因此只以有效 default/2 为性能基线。这里不声称其他场景绝无退化。原有探索过程和首次验证证据继续保留在 [原始不可变证据](https://raw.githubusercontent.com/jixuan1989/tsfile-apache/b772f16255c3e45a9c6599235621126d4fa399e2/issue-evidence/ts2diff-writer-precision/validation/validation-evidence.zip) 中；当前修订数据以本报告及同目录补充包为准。

clang-format 17.0.6、仓库 Spotless 15 个改动文件检查及 git diff --check 均通过。已按用户授权在原审阅线程回复复现、判断和进度；未主动合并上游 PR。AI 说明继续置于 PR 正文末尾。

**AI disclosure:** The implementation, tests and description in this pull request were written by an AI coding agent (OpenAI Codex), which also performed the reported local validation.

**AI 使用说明：** 本 PR 的代码修改、测试和正文由 AI 编程代理（OpenAI Codex）编写，文中报告的本地验证也由该 AI 代理执行。
