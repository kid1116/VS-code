from pathlib import Path
import subprocess,json,os,hashlib,re

work=Path(__file__).resolve().parent
commands=json.loads((work/'extension-launches.json').read_text(encoding='utf-8'))
manifest=json.loads((work/'manifest.json').read_text(encoding='utf-8'))
logs=work/'logs';logs.mkdir(exist_ok=True)
startup=subprocess.STARTUPINFO();startup.dwFlags=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=subprocess.SW_HIDE

def execute(entry,remove_prefix=False):
    command=entry['command']
    assert command.startswith('start cmd /c "') and command.endswith('"')
    body=command[len('start cmd /c "'):-1]
    if remove_prefix:
        assert manifest['prefix']+' ' in body
        body=body.replace(manifest['prefix']+' ','',1)
    # Start the CMD child exactly as the extension does, in a real console.
    # Force the previous non-UTF-8 code page before the extension payload runs.
    line='"'+os.environ['ComSpec']+'" /d /s /c "chcp.com 932 > nul & '+body+'"'
    r=subprocess.run(line,input=b'x\r\n',capture_output=True,cwd=entry['cwd'],
        creationflags=subprocess.CREATE_NEW_CONSOLE,startupinfo=startup,timeout=30)
    return r,line

control,_=execute(commands[1],True)
assert b'BEFORE=932 AFTER=932 INPUT=932' in control.stderr,(control.returncode,control.stdout,control.stderr)
print('OLD RUN-BUTTON ROUTE reproduced: CMD keeps code page 932.',flush=True)

stack=Path(commands[0]['cwd'])/'平时作业1.exe'
native=subprocess.run([str(stack)],capture_output=True,timeout=20)
for index,entry in enumerate(commands):
    r,line=execute(entry)
    (logs/f'run-button-{index}-raw-stdout.bin').write_bytes(r.stdout)
    (logs/f'run-button-{index}-raw-stderr.bin').write_bytes(r.stderr)
    assert r.returncode==0,(r.returncode,r.stdout,r.stderr)
    text=r.stdout.decode('utf-8')
    assert '原栈：栈底 [ ] 栈顶' in text,(text,r.stderr)
    assert '\ufffd' not in text
    assert 'Press any key to continue' in text
    if index==0:assert r.stdout.startswith(native.stdout),(r.stdout,native.stdout)
    if index==1:assert b'BEFORE=65001 AFTER=65001 INPUT=65001' in r.stderr,r.stderr
    (logs/f'run-button-{index}.txt').write_text(text,encoding='utf-8')
    (logs/f'run-button-{index}-command.txt').write_text(line,encoding='utf-8')
    (logs/f'run-button-{index}-diagnostic.txt').write_bytes(r.stderr)
    print('RUN-BUTTON ROUTE OK:', 'actual homework executable' if index==0 else 'real console code page 65001 before student code',flush=True)

for name,digest in json.loads((work/'source_snapshot.json').read_text(encoding='utf-8')).items():
    p=Path(name);assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
    assert not re.search(r'_WIN32|windows\.h|SetConsole|CP_UTF8',p.read_text(encoding='utf-8-sig'))
print('Verified the installed extension\'s real launch commands, including its CMD pause. All 7 C++ sources unchanged.',flush=True)
