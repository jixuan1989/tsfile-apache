A C++ measurement schema with non-empty properties returned `E_OK` after writing only the property count. Its key/value payload was missing, so reading the schema (or table metadata containing it) failed. For the issue reproducer, this changes the incomplete 22-byte output to the same 47 bytes produced by Java.

Enter the property loop after the count is written successfully. Add eight regressions for Java wire bytes, embedded NUL bytes on write, empty/multiple/UTF-8/long properties, page boundaries, consecutive schemas, table schemas and truncated input. Seven regressions fail against the original implementation; all eight pass with this fix.

### Why the condition must be `RET_SUCC`

Both macros evaluate their argument once and assign its return code to the local `ret`. Ignoring the branch-prediction hints, their conditions are:

```cpp
#define RET_FAIL(expr) (common::E_OK != (ret = (expr)))
#define RET_SUCC(expr) (common::E_OK == (ret = (expr)))
```

The body guarded by the property-count write contains the normal work of serializing each property key and value. It must run when that write succeeds.

| Property-count write | Original `RET_FAIL` condition | Corrected `RET_SUCC` condition |
| --- | --- | --- |
| Succeeds | Skips every key/value and returns `E_OK` with an incomplete payload | Writes every key/value |
| Fails | Enters the property loop; later successful writes can overwrite the original error in `ret` | Skips the loop and returns the count-write error |

The corrected outer control flow is equivalent to:

```cpp
ret = common::SerializationUtil::write_ui32(props_.size(), out);
if (ret == common::E_OK) {
    // Serialize each property key and value.
}
return ret;
```

The existing inner `RET_FAIL` guards still handle key/value failures: they save the error in `ret`, and `IS_FAIL(ret)` breaks the loop. The earlier header-field `RET_FAIL` checks also remain appropriate because their empty failure branches stop the `else if` chain. Their bodies serve a different purpose from this property-writing loop.

An empty map still writes a zero count and executes zero loop iterations. For the reported non-empty input, the count is one; the original serializer omits the 25-byte key/value payload, producing 22 bytes instead of Java's 47. This one-condition change emits the missing payload while preserving the format and error-return convention.

Fixes #1017.

Validation:

- MSVC Release: 912 passed; Linux GCC with all compression libraries enabled: 930 passed in the full batch. Each full batch skips three tests requiring external fixture configuration and has ten existing disabled tests. The subsequent Linux batch passes all eight new regressions and both configured interoperability tests.
- 360 schema cases pass Java → C++ → Java with exact bytes. Full table files with properties and all values pass in both directions. Native interoperability validates 123 Java-written and 117 C++-written files, including actual compressed data.
- GCC/gcovr line coverage: changed line and serializer **100%**, `MeasurementSchema` **96.88%**, complete `schema.h` **96.14%**. Corresponding branch coverage: serializer **55.56%**, class **59.26%**, header **64.75%**. Byte-identical source/build header paths are merged; error branches are not excluded. Allocation/write failures were not fault-injected; their propagation above is established by control-flow inspection.
- 25 warmed, alternating performance pairs: paired median fixed/original latency ratios are **0.9993** for empty-property serialization and **0.9915** for normal table writing, with comparable peak working sets. Non-empty cases use a separate valid-output reference because the original output is incomplete. No regression observed in the measured valid workloads.
- clang-format 17.0.6 / Spotless checks for both changed files and `git diff --check` pass.

[Detailed validation report](https://github.com/jixuan1989/tsfile-apache/blob/029495b1e09d37adcddb736a2a2f3b44d477e1a8/issue-evidence/measurement-schema-properties/validation/validation-report.md) · [Raw evidence and validation scripts](https://raw.githubusercontent.com/jixuan1989/tsfile-apache/029495b1e09d37adcddb736a2a2f3b44d477e1a8/issue-evidence/measurement-schema-properties/validation/validation-evidence.zip)

A separate existing `read_str` limitation truncates embedded NUL bytes in both original and fixed builds. The serializer's NUL-containing output is verified against Java. Encoder precision wiring and string reading remain separate follow-up work.

### Query performance backfill (2026-10-18)

Added 16 native table-query scenarios over aligned/non-aligned chunks, row/batch APIs, 1/4 projected fields, time/TAG filters, sparse NULLs and parallel settings; application FIELD references include full native materialization cost. Two devices × 32,768 rows × four fields, 32 position-balanced process repetitions and three full checked queries/process. Open/initialization, cached schema lookup, setup, first decoded/accepted row, full-result latency/throughput, per-query p50/p95 and whole-process peak working set are retained. Query samples are clustered by process; no cold-cache, P99 or universal no-regression claim.

No scenario triggers the confirmation policy in the measured corpus. Valid empty-property products are byte-identical. The original nonempty-property product is malformed and is retained as an untimed expected failure; both readers instead time the valid revised nonempty-property file. This does not present invalid output as a fast baseline. Existing write/coverage/bidirectional compatibility results retain their original scope.

One initial ordering attempt was stopped after its self-check found unequal execution positions; those samples are preserved and excluded from conclusions. The corrected order gives each variant every position equally. Every native returned cell/NULL/timestamp and Python row/checksum expectation is checked. Java independently audits all valid C++ products and actual value-page codecs/counts/precision; five new helper sanitizer scenarios pass with Linux leak detection.

[Query backfill report](https://github.com/jixuan1989/tsfile-apache/blob/c15ad57d4aec83e969f37d665eb187c81bab6b77/issue-evidence/measurement-schema-properties/validation/query-performance-backfill/validation-report.md) · [Sources, actual products, raw timing arrays and controls](https://raw.githubusercontent.com/jixuan1989/tsfile-apache/c15ad57d4aec83e969f37d665eb187c81bab6b77/issue-evidence/measurement-schema-properties/validation/query-performance-backfill/validation-evidence.zip)

### 查询性能补测（2026-10-18）

新增 16 个原生表查询场景，覆盖对齐/非对齐 chunk、行/批接口、1/4 个投影字段、时间/TAG 过滤、稀疏 NULL 和并行配置；应用层 FIELD 参考包含完整原生读取与物化成本。每文件 2 个设备 × 32,768 行 × 4 个字段，32 轮执行位置均衡的独立进程，每进程完整消费并核对 3 次查询。保留打开/初始化、缓存 schema 查询、查询构建、首个解码/接受行、完整延迟/吞吐、逐查询 p50/p95 和进程峰值工作集。统计按进程聚类，不声称冷缓存、P99 或所有场景均无退化。

本次 16 个场景均未触发复查条件；有效的空属性前后产物字节一致。旧版本非空属性文件本身损坏，作为预期失败保留且不计时；改用修复后的有效非空属性文件分别计时两个 reader，没有把无效输出当作快速基线。原有写入、覆盖率与双向兼容证据保留原先范围。

最初一次执行顺序存在位置不均衡，已中止并保留数据，不用于结论；修正后各版本在所有执行位置出现次数相等。原生程序逐单元格核验值/NULL/时间戳，Python 独立核验行数与校验和；Java 独立核验全部有效 C++ 产物及实际页编码/数量/精度。新增辅助程序的 5 个 Linux sanitizer 场景通过，开启泄漏检测。

[查询补测报告](https://github.com/jixuan1989/tsfile-apache/blob/c15ad57d4aec83e969f37d665eb187c81bab6b77/issue-evidence/measurement-schema-properties/validation/query-performance-backfill/validation-report.md) · [源码、实际文件、原始计时与控制实验](https://raw.githubusercontent.com/jixuan1989/tsfile-apache/c15ad57d4aec83e969f37d665eb187c81bab6b77/issue-evidence/measurement-schema-properties/validation/query-performance-backfill/validation-evidence.zip)

**AI disclosure:** The implementation, tests and description in this pull request were written by an AI coding agent (OpenAI Codex), which also performed the reported local validation.

**AI 使用说明：** 本 PR 的代码修改、测试和正文由 AI 编程代理（OpenAI Codex）编写，文中报告的本地验证也由该 AI 代理执行。