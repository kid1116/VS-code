from pathlib import Path
import hashlib,json

work=Path(__file__).resolve().parent
project=Path(r'D:\VS code\58125117-吴天宇-第三次作业')
helper=Path(r'C:\Users\12120\AppData\Roaming\Code\User\cpp-unicode.ps1')
stage=work/'prepared';stage.mkdir(exist_ok=True)
backup=work/'backup';backup.mkdir(exist_ok=True)
manifest=[]

def prepare(destination,relative,content):
    original=destination.read_bytes()
    saved=backup/relative;saved.parent.mkdir(parents=True,exist_ok=True)
    saved.write_bytes(original)
    revised=stage/relative;revised.parent.mkdir(parents=True,exist_ok=True)
    revised.write_text(content,encoding='utf-8-sig')
    manifest.append({'stage':str(revised),'destination':str(destination),'original_hash':hashlib.sha256(original).hexdigest()})

for source in sorted(project.rglob('*.cpp')):
    s=source.read_text(encoding='utf-8-sig')
    assert 'SetConsoleOutputCP' not in s,source
    i=s.index('#include')
    s=s[:i]+'#ifdef _WIN32\n#include <windows.h>\n#endif\n'+s[i:]
    old='int main()\n{'
    assert s.count(old)==1,source
    s=s.replace(old,old+'''
#ifdef _WIN32
    // Windows控制台统一使用UTF-8，避免中文乱码
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif
''',1)
    prepare(source,source.relative_to(project),s)

s=helper.read_text(encoding='utf-8-sig')
old="""chcp.com 65001 > `$null
try {
    & '$quotedExe'
    `$programExitCode = `$LASTEXITCODE"""
assert s.count(old)==1
new="""chcp.com 65001 > `$null
`$utf8 = New-Object System.Text.UTF8Encoding(`$false)
[Console]::InputEncoding = `$utf8
[Console]::OutputEncoding = `$utf8
`$OutputEncoding = `$utf8
try {
    # Inherit the console directly so PowerShell does not decode and re-encode stdout.
    `$program = Start-Process -FilePath '$quotedExe' -NoNewWindow -Wait -PassThru
    `$programExitCode = `$program.ExitCode"""
s=s.replace(old,new,1)
prepare(helper,Path('cpp-unicode.ps1'),s)
(work/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared UTF-8 initialization for 7 programs and corrected the run helper.')
