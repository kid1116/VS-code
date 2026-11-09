from pathlib import Path
import subprocess,json,hashlib,re,os

work=Path(__file__).resolve().parent
project=Path(r'D:\VS code\58125117-吴天宇-第三次作业')
helper=Path(r'C:\Users\12120\AppData\Roaming\Code\User\cpp-unicode.ps1')
results=[]
for source in sorted(project.rglob('*.cpp')):
    r=subprocess.run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(helper),'-Source',str(source)],capture_output=True,timeout=90)
    (work/(source.stem+'-build.log')).write_bytes(r.stdout+r.stderr)
    assert r.returncode==0,(source,(r.stdout+r.stderr).decode('utf-8',errors='replace'))
    exe=source.parent/'output'/(source.stem+'.exe')
    assert exe.exists()
    r=subprocess.run([str(exe)],input=b'0\n' if source.stem=='实践作业1' else b'',capture_output=True,timeout=20)
    assert r.returncode==0,(source,r.returncode)
    text=r.stdout.decode('utf-8')
    if source.stem=='实践作业1':
        assert '已起飞：5，平均等待：1.40' in text and '已降落：11' in text
    if source.stem=='平时作业3-1':assert '步数：4' in text
    if source.stem in ['平时作业2-1','平时作业3-3']:assert '步数：16' in text
    if source.stem=='平时作业2-2':assert '可能：5种' in text and '可能：14种' in text
    (work/(source.stem+'-run.log')).write_text(text,encoding='utf-8')
    results.append(str(source));print('BUILD AND RUN OK:',source.name,flush=True)

snapshot=json.loads((work/'source_snapshot.json').read_text(encoding='utf-8'))
for path,digest in snapshot.items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,('Existing file changed',path)
manifest=json.loads((work/'manifest.json').read_text(encoding='utf-8'))
for entry in manifest:
    assert Path(entry['stage']).read_bytes()==Path(entry['destination']).read_bytes()
    value=json.loads(Path(entry['destination']).read_text(encoding='utf-8'))
    if entry['destination'].endswith('tasks.json'):
        assert all(t.get('command') or t.get('dependsOn') for t in value['tasks'])
(work/'verification.json').write_text(json.dumps({'tested_sources':results,'status':'passed'},ensure_ascii=False,indent=2),encoding='utf-8')
print('Verified: 7 source files compile and run in their original Chinese paths. Existing homework files unchanged.',flush=True)
