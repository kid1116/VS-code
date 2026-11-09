from pathlib import Path
import subprocess,base64,json,re,hashlib

work=Path(__file__).resolve().parent
project=Path(r'D:\VS code\58125117-吴天宇-第三次作业')
user=Path(r'C:\Users\12120\AppData\Roaming\Code\User')
helper=user/'cpp-unicode.ps1'
logs=work/'logs';logs.mkdir(exist_ok=True)

def compile_file(source):
    r=subprocess.run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(helper),'-Source',str(source)],capture_output=True,timeout=90)
    (logs/(source.stem+'-build.log')).write_bytes(r.stdout+r.stderr)
    assert r.returncode==0,(source,(r.stdout+r.stderr).decode('utf-8',errors='replace'))
    return source.parent/'output'/(source.stem+'.exe')

sources=sorted(project.rglob('*.cpp'))
assert len(sources)==7
for source in sources:
    text=source.read_text(encoding='utf-8-sig')
    assert not re.search(r'_WIN32|windows\.h|SetConsole|CP_UTF8',text),source
    exe=compile_file(source)
    r=subprocess.run([str(exe)],input=b'0\n' if source.stem=='实践作业1' else b'',capture_output=True,timeout=20)
    assert r.returncode==0
    output=r.stdout.decode('utf-8')
    assert '\ufffd' not in output
    if source.stem=='平时作业1':assert '原栈：栈底 [ ] 栈顶' in output
    if source.stem=='实践作业1':assert '已起飞：5' in output and '已降落：11' in output
    (logs/(source.stem+'-output.txt')).write_text(output,encoding='utf-8')
    print('STANDARD C++ BUILD/RUN OK:',source.name,flush=True)

probe=work/'probe';probe.mkdir(exist_ok=True)
(probe/'student.cpp').write_bytes((project/'平时作业/平时作业1.cpp').read_bytes())
wrapper='''#include <windows.h>
#include <iostream>
#define main student_main
#include "student.cpp"
#undef main
int main()
{
    int before = GetConsoleOutputCP();
    int result = student_main();
    int after = GetConsoleOutputCP();
    std::cerr << "BEFORE=" << before << " AFTER=" << after << " INPUT=" << GetConsoleCP() << "\\n";
    return result == 0 && before == 65001 && after == 65001 && GetConsoleCP() == 65001 ? 0 : 91;
}
'''
source=probe/'console_probe.cpp';source.write_text(wrapper,encoding='utf-8-sig')
exe=compile_file(source)
startup=subprocess.STARTUPINFO();startup.dwFlags=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=subprocess.SW_HIDE
def run_console(command):
    encoded=base64.b64encode(command.encode('utf-16-le')).decode('ascii')
    return subprocess.run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-EncodedCommand',encoded],
        capture_output=True,creationflags=subprocess.CREATE_NEW_CONSOLE,startupinfo=startup,timeout=30)
quoted=str(exe).replace("'","''")

# Negative control: the unchanged student program does not configure the console.
r=run_console("chcp.com 932 > $null; & '"+quoted+"'; exit $LASTEXITCODE")
assert r.returncode==91,(r.returncode,r.stderr)
assert b'BEFORE=932 AFTER=932 INPUT=932' in r.stderr
print('CONTROL: standard student code leaves code page 932 unchanged.',flush=True)

# Run through the exact helper used by VS Code F6, beginning with the wrong code page.
runner=str(user/'cpp-console.ps1').replace("'","''")
r=run_console("chcp.com 932 > $null; & '"+runner+"' -Program '"+quoted+"' -NoPause -VerifyEncoding")
assert r.returncode==0,(r.returncode,r.stderr)
assert b'BEFORE=65001 AFTER=65001 INPUT=65001' in r.stderr
assert b'RUNNER_INPUT_CP=65001; OUTPUT_CP=65001' in r.stderr
assert '原栈：栈底 [ ] 栈顶' in r.stdout.decode('utf-8')
(logs/'f6-real-console.txt').write_text(r.stderr.decode('utf-8'),encoding='utf-8')
print('F6 REAL CONSOLE: UTF-8 is set by VS Code runner before student main executes.',flush=True)

# Verify the new VS Code integrated-terminal profile initialization as well.
init=(work/'profile_init.txt').read_text(encoding='utf-8')
r=run_console("chcp.com 932 > $null; "+init+"; & '"+quoted+"'; exit $LASTEXITCODE")
assert r.returncode==0 and b'BEFORE=65001 AFTER=65001 INPUT=65001' in r.stderr,(r.returncode,r.stderr)
assert '原栈：栈底 [ ] 栈顶' in r.stdout.decode('utf-8')
(logs/'profile-real-console.txt').write_text(r.stderr.decode('utf-8'),encoding='utf-8')
print('INTEGRATED TERMINAL: UTF-8 profile passes with source files unchanged.',flush=True)

for entry in json.loads((work/'manifest.json').read_text(encoding='utf-8')):
    assert Path(entry['stage']).read_bytes()==Path(entry['destination']).read_bytes()
snapshot=json.loads((work/'source_snapshot.json').read_text(encoding='utf-8'))
# The stack source was already cleaned by the user; preserve it byte-for-byte.
stack=str(project/'平时作业/平时作业1.cpp')
assert hashlib.sha256(Path(stack).read_bytes()).hexdigest()==snapshot[stack]
print('ALL CHECKS PASSED. No Windows-specific encoding code remains in the 7 homework files.',flush=True)
