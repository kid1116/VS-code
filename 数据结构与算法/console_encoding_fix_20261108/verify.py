from pathlib import Path
import subprocess,sys,json,re

work=Path(__file__).resolve().parent
project=Path(r'D:\VS code\58125117-吴天宇-第三次作业')
helper=Path(r'C:\Users\12120\AppData\Roaming\Code\User\cpp-unicode.ps1')
logs=work/'logs';logs.mkdir(exist_ok=True)

def compile_file(source):
    result=subprocess.run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(helper),'-Source',str(source)],capture_output=True,timeout=90)
    (logs/(source.stem+'-build.log')).write_bytes(result.stdout+result.stderr)
    assert result.returncode==0,(source,(result.stdout+result.stderr).decode('utf-8',errors='replace'))
    return source.parent/'output'/(source.stem+'.exe')

for source in sorted(project.rglob('*.cpp')):
    exe=compile_file(source)
    result=subprocess.run([str(exe)],input=b'0\n' if source.stem=='实践作业1' else b'',capture_output=True,timeout=20)
    assert result.returncode==0
    text=result.stdout.decode('utf-8')
    assert '\ufffd' not in text
    if source.stem=='平时作业1':assert '元素个数：0' in text and '原栈：栈底 [ ] 栈顶' in text
    if source.stem=='实践作业1':assert '已起飞：5' in text and '已降落：11' in text
    (logs/(source.stem+'-output.txt')).write_text(text,encoding='utf-8')
    print('UTF-8 BUILD/RUN OK:',source.name,flush=True)

# Allocate a real Windows console with a Japanese code page, reproducing the
# conditions in which UTF-8 bytes become the garbled characters in the screenshot.
# The console is hidden; these are test processes, not desktop automation.
probe=work/'probe';probe.mkdir(exist_ok=True)
(probe/'homework_new.cpp').write_bytes((project/'平时作业/平时作业1.cpp').read_bytes())
(probe/'homework_old.cpp').write_bytes((work/'backup/平时作业/平时作业1.cpp').read_bytes())
wrapper='''#include <windows.h>
#include <iostream>
#define main homework_main
#include "HOMEWORK"
#undef main
int main()
{
    if (!SetConsoleOutputCP(932) || !SetConsoleCP(932))
        return 90;
    int before = GetConsoleOutputCP();
    int code = homework_main();
    int after = GetConsoleOutputCP();
    std::cerr << "CONSOLE_CP_BEFORE=" << before << " AFTER=" << after << " INPUT=" << GetConsoleCP() << "\\n";
    if (code != 0 || after != CP_UTF8 || GetConsoleCP() != CP_UTF8)
        return 91;
    return 0;
}
'''
startup=subprocess.STARTUPINFO()
startup.dwFlags=subprocess.STARTF_USESHOWWINDOW
startup.wShowWindow=subprocess.SW_HIDE
for version,expected in [('old',91),('new',0)]:
    source=probe/(version+'_console.cpp')
    source.write_text(wrapper.replace('HOMEWORK','homework_'+version+'.cpp'),encoding='utf-8-sig')
    exe=compile_file(source)
    result=subprocess.run([str(exe)],capture_output=True,creationflags=subprocess.CREATE_NEW_CONSOLE,startupinfo=startup,timeout=20)
    assert result.returncode==expected,(version,result.returncode,result.stderr)
    assert '原栈：栈底 [ ] 栈顶' in result.stdout.decode('utf-8')
    status=result.stderr.decode().strip()
    (logs/(version+'-console.txt')).write_text(status,encoding='utf-8')
    print(version.upper(),'REAL CONSOLE:',status,flush=True)

# Verify the run helper's direct native launch path with the actual stack program.
# Child stdout must remain byte-for-byte identical, with no PowerShell recoding.
exe=project/'平时作业/output/平时作业1.exe'
quoted=str(exe).replace("'","''")
command="""$utf8=New-Object System.Text.UTF8Encoding($false)
[Console]::InputEncoding=$utf8
[Console]::OutputEncoding=$utf8
$OutputEncoding=$utf8
$program=Start-Process -FilePath 'EXE' -NoNewWindow -Wait -PassThru
exit $program.ExitCode
""".replace('EXE',quoted)
import base64
encoded=base64.b64encode(command.encode('utf-16-le')).decode('ascii')
result=subprocess.run(['powershell.exe','-NoProfile','-EncodedCommand',encoded],capture_output=True,timeout=20)
native=subprocess.run([str(exe)],capture_output=True,timeout=20)
assert result.returncode==0 and result.stdout==native.stdout,(result.returncode,result.stderr)
print('Direct console launch: UTF-8 output matches native bytes exactly.',flush=True)
manifest=json.loads((work/'manifest.json').read_text(encoding='utf-8'))
for entry in manifest:assert Path(entry['stage']).read_bytes()==Path(entry['destination']).read_bytes()
print('ALL ENCODING CHECKS PASSED.',flush=True)
