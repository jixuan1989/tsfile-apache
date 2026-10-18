# PR #1024: algebraic rounding candidate rejected by query screening

Production head `75592b89d1523a96090e8bca1dcb4cd2180162e5` is unchanged and clean. **The query-performance gate remains uncleared.** This is a failed private candidate, not a source revision or a new no-regression claim.

## Candidate and why its arithmetic is equivalent

The previous PMU pattern suggested checking instruction locality, without proving causality. Instead of adjusting binary padding/order, one maintainable source candidate simplifies the fractional branch of `java_round<Int>`:

```cpp
// Previous fractional branch:
const uint64_t remainder = significand & ((uint64_t{1} << shift) - 1);
const uint64_t threshold = (uint64_t{1} << (shift - 1)) + negative;
rounded = (significand >> shift) + (remainder >= threshold);

// Candidate fractional branch:
rounded = (((significand - static_cast<uint64_t>(negative)) >>
            (shift - 1)) +
           1) >>
          1;
```

Write `significand = q * 2^k + r`, where `k=shift`, `0<=r<2^k`. Keeping the half-unit bit, adding one and dropping it gives `q + [r >= 2^(k-1)]` for positive values. For a negative magnitude, subtracting one first gives `q + [r > 2^(k-1)]`: `r=0` still yields `q`, and exact halves no longer increment the magnitude. Restoring the negative sign therefore preserves Java's ties toward positive infinity. Here `2^52 <= significand < 2^53` and `1<=k<=53`, so subtraction cannot underflow, the shift is0..52, and the addition cannot overflow uint64_t. Existing exponent, NaN, saturation and integral-value branches are untouched. No decoder, precision parser, wire marker, API or class layout changes.

Only `cpp/src/encoding/ts2diff_encoder.h` differs in an archived source copy. Repository Maven Spotless apply/check passes using clang-format17.0.6. The initial glob-like Spotless filter was invalid (it expects a regex), and the next attempt lacked the formatter on PATH; both logs are retained. The corrected regex/PATH run succeeds. These setup failures did not rerun or replace query samples.

## Correctness and footprint screens

The native candidate matches the earlier independently generated Java oracle on **1088975 inputs for both int32-saturated and int64 results**. The stored oracle SHA-256 is `3ca19b4154b5a794bf5d19f03c23a98afe9575893419f058cadbfa9a8fee4f98`; the original generator is included for regeneration. The oracle covers random IEEE bits, every exponent, half-neighbors, integer limits, NaNs and infinities. The older floor approximation still differs on251 vectors.

Fresh Java-generated value pages then pass **122 Java→C++ and122 C++→Java cases**,260 values/case, with **122 exact byte matches**. This includes FLOAT/DOUBLE, precision/default/malformed/Unicode property inputs and rounding boundaries. The Java library classpath reuses the already validated local Java artifacts; it is not a new full Java build. These are raw-page checks, not a new full-file or compressed-codec interoperability matrix.

Same-path, same-option unchanged and candidate Release builds were used. The matched unchanged control's `.text` bytes exactly reproduce the original PR image. Its `.rdata` differs in two bytes; zeroing only the PE debug-directory timestamp makes that section identical. This is verified from the PE directory, not assumed from file size. Candidate `.text` virtual size changes from651603 to651539 bytes (**−64**); `.rdata` stays133750 bytes. `read_fixture` stays at RVA67488; aligned batch decode and DOUBLE batch decode move by−64 to525584 and349360 respectively. This limited static audit does not establish cache behavior or a causal performance fix.

## Fixed query screen

Exactly **3 retained scenarios ×144 matched rounds ×6 children ×3 full checked queries =2592 measured children /7776 queries**. An additional864 warmup children/2592 queries and18 smoke children/54 queries are excluded. Two identical payload copies per version provide same-binary negative controls. The original upstream baseline, unchanged current-head rebuild and candidate rotate over the same six neutral paths every six-round block; each label uses each path four times and each execution position equally. All three cases use byte-identical baseline/fixed writer products, with copied SHA checks. Existing fixture Java audits remain applicable; candidate-generated full files were not substituted.

Affinity12 before initial resume, one physical core's two SMT siblings, pool2, parallel=false, warm filesystem cache. No WPR or invasive sampler. Interactive-host background, frequency and power remain uncontrolled. Every native result is fully consumed and checked; an independent offline verifier also checks rows, NULL counts and checksums. Full latency includes open/header/footer, metadata lookup, query setup, decoded value materialization/validation, result destruction and close. Timing is not verifier-free library CPU time.

Each round combines the two copies' full-query sums.24 chronological six-round block medians are bootstrapped20000 times using a fixed seed. Below: block-median change versus the indicated control [95% block-bootstrap interval]; positive is slower. These are correlated exploratory screening intervals, not equivalence or universal non-inferiority guarantees.

| Scenario | Current / upstream | Candidate / upstream | Candidate / current |
|---|---:|---:|---:|
| dense row / 4 FIELDs | +0.946% [+0.671%, +1.109%] | +1.005% [+0.777%, +1.244%] | +0.098% [-0.145%, +0.302%] |
| dense batch / 4 FIELDs | +1.130% [+1.056%, +1.342%] | +0.956% [+0.818%, +1.285%] | -0.086% [-0.500%, +0.261%] |
| sparse batch / app50 / 1 FIELD | +0.330% [-0.298%, +1.034%] | +0.419% [-0.480%, +0.948%] | -0.159% [-0.610%, +0.619%] |

Both dense candidate/upstream intervals remain above zero. All candidate/current intervals include zero: neither a reliable improvement nor equivalence is established. Sparse/app50 intervals include zero; the old sparse residual remains in the historical record rather than being erased. The existing trigger also considers paired median>1.03 and descriptive p95>1.10; those values, every raw round, and all original anomalies are retained.

Same-binary copy2/copy1 negative controls:

| Scenario | Baseline | Current | Candidate |
|---|---:|---:|---:|
| dense row / 4 FIELDs | +0.058% [-0.258%, +0.557%] | -0.097% [-0.360%, +0.236%] | +0.034% [-0.626%, +0.339%] |
| dense batch / 4 FIELDs | -0.070% [-0.256%, +0.189%] | +0.099% [-0.280%, +0.419%] | +0.091% [-0.281%, +0.502%] |
| sparse batch / app50 / 1 FIELD | -0.165% [-0.392%, +0.984%] | +0.454% [-0.632%, +0.734%] | +0.204% [-0.733%, +0.608%] |

All nine negative-control intervals include zero. Complete open/metadata/setup/first-decoded/first-accepted/full-query arrays, per-query p50/p95, decoded/accepted/projected-cell throughput and whole-process peak working-set statistics remain in `query-results.json`. Scope is the three selected scenarios only; controlled cold-cache/P99/native FIELD pushdown/all-NULL/compressed/general parallel scaling and the previous full-matrix gaps remain unmeasured. `app50` filters after complete native materialization and validation; that cost is included and it is not a native pushdown claim.

## Decision and next step

**Rejected under the predeclared stopping rule.** A64-byte reduction and successful arithmetic/wire checks did not remove the dense query signal. No further timing extension, outlier trimming, source-expression alternatives, linker-order/padding changes or production push. This does not prove code footprint irrelevant; it rejects this particular proposed remedy. The earlier PMU pattern remains a hypothesis, not a demonstrated cause.

The failed private candidate was not taken through full unit/sanitizer suites, new changed-line/module/branch coverage, full-file/compressed bidirectional compatibility, writer benchmarks or the complete32-case query acceptance matrix. Those are **unmeasured for the candidate**. Earlier production-head correctness, coverage, full interoperability and write measurements retain their original scope because production source did not change. No old passing percentage is transferred to this candidate.

Next work should resolve the attribution gap between whole-thread PMU totals and unchanged query code, including supported event-based instruction-cache sampling/calibration, before proposing another source/layout intervention. The administrator capture already completed; this report does not ask for it again. No new issue approval is implied.

## Recheck the public evidence

Extract the ZIP and run `python verify_public.py`. It checks all2592 native outputs/7776 queries, path/position balance, paired/block medians and the file manifest. Full raw query arrays, code/section hashes, one-file candidate diff, original Java oracle generator,122 page fixtures and build/format logs are included. Source paths are normalized; reproduction/build scripts are supplied for audit and need local project paths before rebuilding. No system ETL or absolute runtime addresses are included.

## 中文说明

本轮只验证一个有数学依据的候选：把舍入的“余数掩码与阈值比较”改为保留半位后的商运算。对负数先减1，可使精确半值的绝对值不进位，恢复符号后仍向正无穷舍入；有效值域保证无无符号下溢、移位越界或加法溢出。NaN、饱和、整数值、编码格式等分支均不变，仅在私有源码副本修改一个头文件。

1088975个Java舍入样本的int32/int64结果全部一致。另新生成122组Java编码页，双方互读均成功，122组字节全部一致，每组260值；Java库沿用此前验证产物，不冒充完整重建。仓库Spotless最终通过；前两次过滤正则/PATH配置失败日志保留。编译后的代码缩小64字节；匹配控制.text与原PR程序完全相同，.rdata的两字节差异经验证仅在PE调试时间戳内。

固定3场景×144轮×6进程×3查询，共2592个测量进程、7776次完整核验查询；预热2592次和smoke54次另计。基线/当前/候选各两个副本轮换相同六路径，路径与位置均衡；输入为此前两版writer字节相同的文件。保留所有异常样本和同二进制负对照，亲和性12为单物理核SMT线程，缓存预热，功耗和后台负载未控制。app50参考包含完整原生物化及校验成本。

上表为区块中位数及95%区间。候选相对上游：稠密行查询约+1.005%，批查询约+0.956%，两项区间仍完全大于0；候选/当前的三项区间均包含0，不能认定改善或完全等效。稀疏场景本轮未区分出方向，但历史残留不删除。九个同二进制负对照区间均包含0。按预定停止规则放弃，不推送源码，不继续换表达式或跑到通过，也不把体积变化当缓存因果证明。

该私有失败候选没有继续执行全量单测/sanitizer、完整文件/压缩兼容、修改行/模块/分支覆盖率、写入基准或全32场景验收；这些明确为未测，不能借用旧覆盖率冒充通过。原PR源码未变，旧正确性、兼容性、覆盖率及写入证据沿用原范围，查询门槛仍未通过。下一步先弥合硬件计数与具体查询热点之间的归因缺口，再提出有依据的新修改；已完成的管理员采集不重复要求运行，第4条issue仍需独立批准。

**AI disclosure:** The implementation, tests and description in this pull request were written by an AI coding agent (OpenAI Codex), which also performed the reported local validation.

**AI 使用说明：** 本 PR 的代码修改、测试和正文由 AI 编程代理（OpenAI Codex）编写，文中报告的本地验证也由该 AI 代理执行。
