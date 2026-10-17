# PR #1024: sanitizer test lifetime correction

The Ubuntu Debug/Release ASan jobs on `1e8d230805d5823f1e0cd7a82af4e815510080e0` reported the same **424 bytes in 32 allocations** in `EncodingProps.ZeroOnlyPagesEscapeReservedPrecisionMarkers`. The functional assertions passed; LeakSanitizer failed the process at exit.

The test allocated a floating-point decoder through `DecoderFactory` and then used `DecoderFactory::free`, which only calls `common::mem_free`. It does not invoke the virtual destructor. The decoder's page bitmap vectors consequently lost their allocations. The fixture now constructs FLOAT and DOUBLE decoders on the stack and selects a non-owning base pointer. Both destructors run at scope exit, including on fatal assertion returns. The factory allocation/null check and matching raw free are removed from this test. No production file or wire behavior changes.

## Validation

- A local GCC 11 AddressSanitizer build of the original seven encoding tests reproduces the exact 424-byte / 32-allocation leak and exits 1. Its seven functional tests pass, illustrating why assertion-only runs missed the problem.
- The changed seven-test build exits 0 with `ASAN_OPTIONS=detect_leaks=1` and no ASan/LSan error.
- Full Linux Debug AddressSanitizer results: 1014 passed / 1 skipped / 10 disabled. All six optional codecs are enabled; ANTLR, tools and SIMD are disabled. The standalone reproduction instruments the test translation unit and inline codec code, while linking the previous non-ASan static library; the full run separately rebuilds the complete library and tests with ASan.
- Windows MSVC Release results: 993 passed / 3 skipped / 10 disabled. Existing disabled/skipped tests remain recorded in XML.
- clang-format 17.0.6, repository Spotless check and `git diff --check` pass.

SHA-256 verifies every production file changed in this PR and every library/benchmark/compatibility artifact from the previous validation is identical. The existing Java bidirectional, raw-byte compatibility, 97/97 changed executable-line coverage (44.78% corresponding branches) and retained 125/25-pair performance results therefore still apply to the same production implementation. No new performance run is claimed for this test-only correction. The prior report's Java invalid zero-page and table-schema limitations remain unchanged.

Raw logs, test sources before/after, XML, exact patch and build scripts are included in the supplementary archive. Public CI job links:

- https://github.com/apache/tsfile/actions/runs/39058914012/job/117472630774
- https://github.com/apache/tsfile/actions/runs/39058914012/job/117472630753

## 中文

两个 Ubuntu ASan 任务均由新测试遗漏 decoder 析构导致：`DecoderFactory::free` 只释放对象原始内存，不调用析构，因此页位图的 vector 分配泄漏了 424 字节，共 32 次。功能断言全部通过，但 LeakSanitizer 在进程退出时判定失败。测试现在在栈上构造两种 decoder，用基类指针选择当前类型；正常离开作用域及致命断言提前返回时均会析构。没有修改生产代码和文件格式。

本地保留了修改前相同泄漏及退出码 1 的证据；修改后的七项编码测试在启用泄漏检测时退出码为 0。Linux 全量重建为 Debug ASan，并启用六种可选压缩库；Windows Release 全量也重新执行。详细计数见上文及 XML。生产源码与此前测量的库、性能及兼容性程序均逐个核对 SHA-256 一致，因此沿用之前完全相同生产实现的兼容性、覆盖率和性能证据；未声称为测试生命周期修改重跑了性能。Java 无效全零页和表 schema 的已知限制仍保留。

**AI disclosure:** The correction, reproduction and reported validation were prepared/performed by OpenAI Codex.

**AI 使用说明：** 本修正、复现及报告的验证由 OpenAI Codex 编写或执行。
