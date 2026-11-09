from pathlib import Path
import json,copy,shutil,hashlib

work=Path(__file__).resolve().parent
root=Path(r'D:\VS code')
project=root/'58125117-吴天宇-第三次作业'
user=Path(r'C:\Users\12120\AppData\Roaming\Code\User')
stage=work/'prepared';stage.mkdir(exist_ok=True)
backup=work/'backup';backup.mkdir(exist_ok=True)
manifest=[]

tasks=json.loads((root/'.vscode/tasks.json').read_text(encoding='utf-8-sig'))
alias='C/C++: 中文路径编译运行'
run=next(t for t in tasks['tasks'] if t['label']=='run cpp in terminal')
if not any(t.get('label')==alias for t in tasks['tasks']):
    entry=copy.deepcopy(run);entry['label']=alias;tasks['tasks'].append(entry)

settings={
    'files.encoding':'utf8',
    'code-runner.runInTerminal':True,
    'code-runner.saveFileBeforeRun':True,
    'code-runner.ignoreSelection':True,
    'code-runner.executorMap':{
        language:'powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\\Users\\12120\\AppData\\Roaming\\Code\\User\\cpp-unicode.ps1" -Source $fullFileName -Run'
        for language in ['c','cpp']
    }
}
launch=json.loads((root/'.vscode/launch.json').read_text(encoding='utf-8-sig'))
intellisense=json.loads((root/'.vscode/c_cpp_properties.json').read_text(encoding='utf-8-sig'))
compiler=Path(r'C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\bin\Hostx64\x64\cl.exe')
assert compiler.exists()
for config in intellisense['configurations']:config['compilerPath']=str(compiler)

def stage_file(label,destination,value):
    path=stage/(label+'.json')
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    old=None
    if destination.exists():
        raw=destination.read_bytes();old=hashlib.sha256(raw).hexdigest()
        (backup/(label+'.json')).write_bytes(raw)
    manifest.append({'stage':str(path),'destination':str(destination),'original_hash':old})

stage_file('parent-tasks',root/'.vscode/tasks.json',tasks)
for name,value in [('tasks',tasks),('launch',launch),('settings',settings),('c_cpp_properties',intellisense)]:
    stage_file('homework-'+name,project/'.vscode'/(name+'.json'),value)

# Verify that the existing F6 binding resolves to a real, executable task.
bindings=json.loads((user/'keybindings.json').read_text(encoding='utf-8-sig'))
f6=next(b for b in bindings if b['key']=='f6' and b['command']=='workbench.action.tasks.runTask')
assert f6['args']==alias
assert any(t.get('label')==alias and t.get('command')=='powershell.exe' for t in tasks['tasks'])
for t in tasks['tasks']:
    assert t['type']=='process' and t['command'] and Path(t['args'][t['args'].index('-File')+1]).is_file()
for config in launch['configurations']:
    assert any(t['label']==config['preLaunchTask'] for t in tasks['tasks'])

snapshot={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in project.rglob('*') if p.is_file()}
(work/'source_snapshot.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2),encoding='utf-8')
(work/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared 5 configuration files. F6 task name and debug build task verified.')
