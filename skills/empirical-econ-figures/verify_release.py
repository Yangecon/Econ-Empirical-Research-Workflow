"""Verify the downloaded repository against its published SHA-256 manifest."""
from pathlib import Path
import hashlib

root=Path(__file__).resolve().parent
manifest=root/'SHA256SUMS.txt'
checked=0
errors=[]
for line in manifest.read_text(encoding='utf-8').splitlines():
    expected,name=line.split('  ',1)
    path=root/name
    if not path.resolve().is_relative_to(root):
        errors.append(f'Path outside release: {name}')
    elif not path.is_file():
        errors.append(f'Missing: {name}')
    elif hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
        errors.append(f'Changed: {name}')
    checked+=1
if errors:
    raise SystemExit('\n'.join(errors))
print(f'RELEASE_INTEGRITY_OK files={checked}')
