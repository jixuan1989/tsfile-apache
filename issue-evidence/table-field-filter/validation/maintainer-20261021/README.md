# PR #1026 maintainer follow-up evidence

[Bilingual report](validation-report.md) · [Machine-readable summary](validation-summary.json)

Frozen source: `6f4a971eefffcc81cf62a75b6ad8bc91460b0fa6`. This evidence branch contains no production revision.
Query acceptance remains **NOT cleared**; full combined sanitizer acceptance is **NOT cleared**.

查询性能与完整 sanitizer 验收均**未通过**。本分支仅发布验证产物，没有生产代码修改。

Download `parts-manifest.json` and all three `validation-evidence.zip.part*` files into one folder. Reassemble and verify without modifying any part:

下载 `parts-manifest.json` 和全部三个 `validation-evidence.zip.part*` 到同一目录，然后运行：

```python
from pathlib import Path
import hashlib, json, zipfile
m = json.loads(Path("parts-manifest.json").read_text())
chunks = []
for p in m["parts"]:
    b = Path(p["name"]).read_bytes()
    assert len(b) == p["bytes"]
    assert hashlib.sha256(b).hexdigest() == p["sha256"]
    chunks.append(b)
b = b"".join(chunks)
assert len(b) == m["bytes"]
assert hashlib.sha256(b).hexdigest() == m["sha256"]
Path(m["archive"]).write_bytes(b)
with zipfile.ZipFile(m["archive"]) as z:
    assert z.testzip() is None
print(m["sha256"])
```

ZIP SHA256: `eafb4b26d9440f0c08cbd00b5516b5a46cb4d05e254b5bfdf24d7a933358d67e`. All test sources, protocols, raw samples, failed broader sanitizer logs and measured-scope limitations are retained in the archive. Native coverage report hashes are recorded; large build directories and fixtures are not embedded.

**AI disclosure:** The local validation, reproduction helpers and documentation were prepared by OpenAI Codex. The two reviewed production commits were authored by maintainer ColinLee/ColinLeeo.

**AI 使用说明：** 本地验证、复现辅助代码和说明由 OpenAI Codex 完成；被验证的两次生产提交由维护者 ColinLee/ColinLeeo 编写。
