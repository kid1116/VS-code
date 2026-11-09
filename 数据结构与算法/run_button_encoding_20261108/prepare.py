from pathlib import Path
import json,hashlib

work=Path(__file__).resolve().parent
settings=Path(r'C:\Users\12120\AppData\Roaming\Code\User\settings.json')
original=settings.read_bytes();text=original.decode('utf-8-sig')
key='c-cpp-compile-run.custom-run-prefix'
assert '"'+key+'"' not in text
assert '"terminal.external.windowsExec"' not in text
prefix='chcp.com 65001 > nul &'
terminal=r'C:\Windows\System32\cmd.exe'
values={key:prefix,'terminal.external.windowsExec':terminal}
insert=''.join('  '+json.dumps(k)+': '+json.dumps(v,ensure_ascii=False)+',\n' for k,v in values.items())
index=text.index('{')+1
revised=text[:index]+'\n'+insert+text[index:]
(work/'settings.backup.json').write_bytes(original)
(work/'settings.prepared.json').write_text(revised,encoding='utf-8-sig')
project=Path(r'D:\VS code\58125117-吴天宇-第三次作业')
snapshot={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in project.rglob('*.cpp')}
(work/'source_snapshot.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2),encoding='utf-8')
(work/'manifest.json').write_text(json.dumps({'destination':str(settings),'stage':str(work/'settings.prepared.json'),'original_hash':hashlib.sha256(original).hexdigest(),'prefix':prefix,'terminal':terminal},ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared the Compile Run extension startup prefix. C++ files are unchanged.')
