from pathlib import Path
import hashlib, json, urllib.request
root=Path(__file__).resolve().parent
m=json.loads((root/'parts.json').read_text())
pieces=[]
for p in m['parts']:
    path=root/p['name']
    if not path.exists():
        with urllib.request.urlopen(m['raw_base']+'/'+p['name'],timeout=60) as r: data=r.read()
        assert len(data)==p['bytes'] and hashlib.sha256(data).hexdigest()==p['sha256']
        path.write_bytes(data)
    data=path.read_bytes()
    assert len(data)==p['bytes'] and hashlib.sha256(data).hexdigest()==p['sha256']
    pieces.append(data)
data=b''.join(pieces)
assert len(data)==m['original_zip_bytes'] and hashlib.sha256(data).hexdigest()==m['original_zip_sha256']
out=root/'validation-evidence.zip'
if out.exists(): assert out.read_bytes()==data
else: out.write_bytes(data)
print('Original ZIP SHA-256 verified:',m['original_zip_sha256'])
