from pathlib import Path
import json,hashlib,re

work=Path(__file__).resolve().parent
project=Path(r'D:\VS code\58125117-吴天宇-第三次作业')
user=Path(r'C:\Users\12120\AppData\Roaming\Code\User')
stage=work/'prepared';stage.mkdir(exist_ok=True)
backup=work/'backup';backup.mkdir(exist_ok=True)
manifest=[]

def jsonc_load(text):
    # Skip comments and trailing commas while preserving quoted strings.
    out=[];i=0
    while i<len(text):
        if text[i]=='"':
            start=i;i+=1
            while i<len(text):
                if text[i]=='\\':i+=2;continue
                if text[i]=='"':i+=1;break
                i+=1
            out.append(text[start:i]);continue
        if text.startswith('//',i):
            i=text.find('\n',i)
            if i<0:break
            continue
        if text.startswith('/*',i):
            i=text.index('*/',i+2)+2;continue
        if text[i]==',':
            j=i+1
            while j<len(text) and text[j].isspace():j+=1
            if j<len(text) and text[j] in '}]':i+=1;continue
        out.append(text[i]);i+=1
    return json.loads(''.join(out))

def prepare(destination,relative,text):
    raw=destination.read_bytes() if destination.exists() else None
    if raw is not None:
        p=backup/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
    p=stage/relative;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(text,encoding='utf-8-sig')
    manifest.append({'stage':str(p),'destination':str(destination),'original_hash':hashlib.sha256(raw).hexdigest() if raw is not None else None})

snapshot={}
for source in sorted(project.rglob('*.cpp')):
    text=source.read_text(encoding='utf-8-sig');clean=text
    snapshot[str(source)]=hashlib.sha256(source.read_bytes()).hexdigest()
    clean=clean.replace('#ifdef _WIN32\n#include <windows.h>\n#endif\n','')
    clean=clean.replace('''#ifdef _WIN32
    // Windows控制台统一使用UTF-8，避免中文乱码
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif
''','')
    assert not re.search(r'_WIN32|windows\.h|SetConsole|CP_UTF8',clean),source
    if clean!=text:prepare(source,Path('sources')/source.relative_to(project),clean)

helper=user/'cpp-unicode.ps1'
text=helper.read_text(encoding='utf-8-sig')
start=text.index('    if ($Run) {')
end=text.index('} finally { Pop-Location }',start)
replacement='''    if ($Run) {
        $runner = Join-Path $PSScriptRoot 'cpp-console.ps1'
        if (!(Test-Path -LiteralPath $runner)) { throw "Console runner was not found: $runner" }
        $quotedRunner = $runner.Replace("'", "''")
        $quotedExe = $exe.Replace("'", "''")
        $consoleCommand = "& '$quotedRunner' -Program '$quotedExe'"
        $encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($consoleCommand))
        $consoleHost = Join-Path $env:WINDIR 'System32\\conhost.exe'
        Start-Process -FilePath $consoleHost -WorkingDirectory $sourceDir -ArgumentList @('powershell.exe', '-NoLogo', '-NoProfile', '-EncodedCommand', $encoded) | Out-Null
    }
'''
prepare(helper,Path('config/cpp-unicode.ps1'),text[:start]+replacement+text[end:])
prepare(user/'cpp-console.ps1',Path('config/cpp-console.ps1'),(work/'cpp-console.ps1').read_text(encoding='utf-8'))

# These are VS Code settings, not Windows regional or system-wide locale changes.
settings=user/'settings.json'
text=settings.read_text(encoding='utf-8-sig');old=jsonc_load(text)
init='chcp.com 65001 > $null; $utf8 = New-Object System.Text.UTF8Encoding($false); [Console]::InputEncoding = $utf8; [Console]::OutputEncoding = $utf8; $OutputEncoding = $utf8'
values={
    'files.encoding':'utf8',
    'terminal.integrated.profiles.windows':{
        'PowerShell UTF-8':{
            'path':r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe',
            'args':['-NoLogo','-NoExit','-Command',init]
        }
    },
    'terminal.integrated.defaultProfile.windows':'PowerShell UTF-8'
}
assert not (set(values)&set(old)), 'Existing terminal settings require a merge.'
opening=text.index('{')
insert=json.dumps(values,ensure_ascii=False,indent=2).strip()[1:-1].strip()
text=text[:opening+1]+'\n  '+insert+',\n'+text[opening+1:]
merged=jsonc_load(text)
assert all(merged[k]==v for k,v in old.items())
assert all(merged[k]==v for k,v in values.items())
prepare(settings,Path('config/settings.json'),text)

for label,folder in [('parent',Path(r'D:\VS code')),('homework',project)]:
    launch=folder/'.vscode/launch.json'
    value=json.loads(launch.read_text(encoding='utf-8-sig'))
    for config in value['configurations']:
        if config.get('type')=='cppvsdbg':config['console']='integratedTerminal'
    prepare(launch,Path('config')/(label+'-launch.json'),json.dumps(value,ensure_ascii=False,indent=2)+'\n')

(work/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(work/'source_snapshot.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2),encoding='utf-8')
(work/'profile_init.txt').write_text(init,encoding='utf-8')
print('Prepared',len(manifest),'updates; current student changes preserved; UTF-8 is configured outside C++ sources.')
