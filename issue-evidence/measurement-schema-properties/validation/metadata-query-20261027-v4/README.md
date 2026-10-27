README: fixed PR01 metadata query diagnostics

Read validation-report.md and analysis-summary.json first. All420 comparison rows are in comparisons.tsv. report-metrics-v4.json inside the ZIP contains every phase/P50/P95/throughput/whole-process peak with sample counts. Every formal/warmup raw stdout/stderr, process command, original qualification failure, source/protocol/review history, immutable input hash manifests and final integrity are inside the ZIP. Actual final independent reviews are separate final-integration.json and final-different-model.json files next to this README; protocol READY is not an acceptance or historical PR pass.

Concatenate the 28 parts in numeric name order to evidence.zip. SHA256 `ebbe7b44ef49d4126e30130f755e31dccb94ef3a80f16647ea6bd9a28934b699`, bytes `14610760`. Use Python: 

```python
from pathlib import Path
import hashlib, zipfile
p=Path(".")
b=b"".join(f.read_bytes() for f in sorted(p.glob("evidence.zip.part*")))
assert len(b)==14610760 and hashlib.sha256(b).hexdigest()=="ebbe7b44ef49d4126e30130f755e31dccb94ef3a80f16647ea6bd9a28934b699"
(p/"evidence.zip").write_bytes(b)
with zipfile.ZipFile(p/"evidence.zip") as z:
    assert z.testzip() is None
```

Full native/JDK/JAR/classpath binaries and TsFile payloads are preserved locally and hash-bound, omitted from this public ZIP; source, setup commands, all4199 input hashes and raw validation records are included. This is not a hermetic runnable archive. Whole-process memory includes warmup/oracle; no fresh write throughput, full suite/coverage/sanitizer, Java performance or global query acceptance. Old16 results remain independent. All source/query/writer gates remain false for this supplemental diagnostic scope.

中文：先读报告/摘要，420项比较见TSV，全部分项计时/分位数/吞吐/进程整体峰值及样本量见ZIP内metrics；正式与固定首query预热、所有命令/stdout/stderr/原失败/完整hash与审阅历史均保留。最终两个实际独立审阅JSON单独随本目录发布，不把READY追认为性能验收或历史门槛。按数字顺序拼接各part并按上列SHA/字节数验核。原生/JDK/JAR/类路径二进制及TsFile有效载荷仅本地保留且哈希绑定，公开ZIP含源码、构建复现命令、4199输入hash及完整原始验证记录，非自包含可运行档案。整体峰值包括预热/oracle；未新测写吞吐/全套/覆盖/sanitizer/Java计时，不解除全局查询门槛，历史16独立，补充诊断的源码/查询/写入门槛保持false。

**AI disclosure:** The implementation, tests and description in this pull request were written by an AI coding agent (OpenAI Codex), which also performed the reported local validation.

**AI 使用说明：** 本 PR 的代码修改、测试和正文由 AI 编程代理（OpenAI Codex）编写，文中报告的本地验证也由该 AI 代理执行。
