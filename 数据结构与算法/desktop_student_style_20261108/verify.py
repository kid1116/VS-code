from pathlib import Path
import subprocess,json,re,hashlib

work=Path(__file__).resolve().parent
helper=Path(r'C:\Users\12120\AppData\Roaming\Code\User\cpp-unicode.ps1')
manifest=json.loads((work/'manifest.json').read_text(encoding='utf-8'))
logs=work/'logs';logs.mkdir(exist_ok=True)
results=[]

for entry in manifest:
    source=Path(entry['destination'])
    assert source.read_bytes()==Path(entry['source']).read_bytes()
    text=source.read_text(encoding='utf-8-sig')
    assert '题干' in text
    assert not re.search(r'_WIN32|windows\.h|SetConsole|CP_UTF8|\bassert\s*\(|\bthrow\b|\btemplate\s*<',text)
    r=subprocess.run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(helper),'-Source',str(source)],capture_output=True,timeout=90)
    (logs/(source.stem+'-build.log')).write_bytes(r.stdout+r.stderr)
    assert r.returncode==0,(source,(r.stdout+r.stderr).decode('utf-8',errors='replace'))
    exe=source.parent/'output'/(source.stem+'.exe')
    r=subprocess.run([str(exe)],input=b'0\n' if source.stem=='实践作业1' else b'',capture_output=True,timeout=20)
    assert r.returncode==0,(source,r.returncode,r.stderr)
    output=r.stdout.decode('utf-8')
    assert '\ufffd' not in output
    if source.stem=='平时作业1':
        assert re.findall(r'元素个数：(\d+)',output)==['0','1','4','5']
        assert '合并结果：栈底 [ 1 2 3 4 5 ] 栈顶' in output
    elif source.stem=='平时作业3-2':
        assert '奇数位置：队首 [ 1 3 5 ] 队尾' in output
        assert '偶数位置：队首 [ 2 4 6 ] 队尾' in output
    elif source.stem in ['平时作业2-1','平时作业3-1','平时作业3-3']:
        expected=4 if source.stem=='平时作业3-1' else 16
        assert re.findall(r'步数：(\d+)',output)==[str(expected),'0']
        assert '没有找到通路' in output
    else:
        assert '已起飞：5，平均等待：1.40' in output
        assert '已降落：11，平均等待：0.18，落地平均剩余燃油：2.00' in output
        assert '燃油为0时成功降落：6，失事：0' in output
        tests=['1\n0 2 5 3\n','1\n3 3 0 0 0\n','2\n0 3 1 1 1\n0 3 0 0 0\n']
        for data in tests:
            check=subprocess.run([str(exe)],input=data.encode(),capture_output=True,timeout=20)
            assert check.returncode==0
        assert '失事：1' in check.stdout.decode('utf-8')
    (logs/(source.stem+'-output.txt')).write_text(output,encoding='utf-8')
    print('DESKTOP BUILD/RUN OK:',source.name,flush=True)
    results.append(str(source))

for path,digest in json.loads((work/'protected_files.json').read_text(encoding='utf-8')).items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,('Other file changed',path)
(work/'result.json').write_text(json.dumps({'status':'passed','files':results},ensure_ascii=False,indent=2),encoding='utf-8')
print('All 6 desktop C++ files verified. Existing documents and pictures are unchanged.',flush=True)
