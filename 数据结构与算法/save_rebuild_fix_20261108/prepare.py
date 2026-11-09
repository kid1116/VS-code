from pathlib import Path
import json,re,hashlib

work=Path(__file__).resolve().parent
stage=work/'prepared';stage.mkdir(exist_ok=True)
backup=work/'backup';backup.mkdir(exist_ok=True)
user=Path(r'C:\Users\12120\AppData\Roaming\Code\User')
extension=Path(r'C:\Users\12120\.vscode\extensions\danielpinto8zz6.c-cpp-compile-run-1.0.92\dist\extension.js')
compiler=Path(r'C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\bin\Hostx64\x64\cl.exe')
assert compiler.is_file()
manifest=[]

def prepare(target,label,text,encoding='utf-8'):
    raw=target.read_bytes();(backup/label).write_bytes(raw)
    p=stage/label;p.write_text(text,encoding=encoding)
    manifest.append({'destination':str(target),'stage':str(p),'original_hash':hashlib.sha256(raw).hexdigest()})

text=extension.read_text(encoding='utf-8')
needle='const o=[...i.Configuration.additionalIncludePaths(),...i.Configuration.includePathsFromCppProperties()]'
assert text.count(needle)==1
branch=(work/'msvc_branch.js.txt').read_text(encoding='utf-8')
text=text.replace(needle,branch+needle,1)
prepare(extension,'extension.js',text)

helper=user/'cpp-unicode.ps1'
text=helper.read_text(encoding='utf-8-sig')
text=text.replace('    [switch]$Run\n','    [switch]$Run,\n    [string]$OutputDirectory,\n    [string]$CompilerArgumentsBase64,\n    [string]$LinkerArgumentsBase64\n',1)
old="$pdb = Join-Path $outputDir ($baseName + '.pdb')"
assert text.count(old)==1
text=text.replace(old,"$pdb = Join-Path $outputDir ($baseName + '.link.pdb')\n$compilerPdb = Join-Path $outputDir ($baseName + '.compile.pdb')",1)
text=text.replace("@('/nologo', '/utf-8', '/Zi', '/W4', \"/Fo$obj\", \"/Fd$pdb\")", "@('/nologo', '/utf-8', '/Zi', '/FS', '/W4', \"/Fo$obj\", \"/Fd$compilerPdb\")",1)
old="$outputDir = Join-Path $sourceDir 'output'"
assert text.count(old)==1
text=text.replace(old,"""if ([string]::IsNullOrWhiteSpace($OutputDirectory)) {
    $outputDir = Join-Path $sourceDir 'output'
} else {
    $outputDir = [IO.Path]::GetFullPath($OutputDirectory)
}""",1)
old='$compileArgs += @($Source, "/Fe$exe", \'/link\', "/PDB:$pdb", \'/INCREMENTAL:NO\')'
assert text.count(old)==1
new='''if ($CompilerArgumentsBase64) {
    $extraCompilerArgs = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($CompilerArgumentsBase64)) | ConvertFrom-Json
    $compileArgs += @($extraCompilerArgs)
}
$compileArgs += @($Source, "/Fe$exe", '/link', "/PDB:$pdb", '/INCREMENTAL:NO')
if ($LinkerArgumentsBase64) {
    $extraLinkerArgs = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($LinkerArgumentsBase64)) | ConvertFrom-Json
    $compileArgs += @($extraLinkerArgs)
}'''
text=text.replace(old,new,1)
prepare(helper,'cpp-unicode.ps1',text,'utf-8-sig')

settings=user/'settings.json'
text=settings.read_text(encoding='utf-8-sig')
values={
    'c-cpp-compile-run.cpp-compiler':str(compiler),
    'c-cpp-compile-run.c-compiler':str(compiler),
    'c-cpp-compile-run.cpp-flags':'/utf-8 /EHsc /std:c++17 /Zi /W4',
    'c-cpp-compile-run.c-flags':'/utf-8 /Zi /W4',
    'c-cpp-compile-run.skip-if-compiled':False
}
for key,value in values.items():
    pattern=r'("'+re.escape(key)+r'"\s*:\s*)("(?:\\.|[^"\\])*"|true|false)'
    replacement=json.dumps(value,ensure_ascii=False)
    if re.search(pattern,text):text=re.sub(pattern,lambda m:m[1]+replacement,text,count=1)
    else:
        at=text.index('{')+1
        text=text[:at]+'\n  '+json.dumps(key)+': '+replacement+',\n'+text[at:]
prepare(settings,'settings.json',text,'utf-8-sig')
snapshot={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(r'D:\VS code\58125117-吴天宇-第三次作业').rglob('*.cpp')}
(work/'source_snapshot.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2),encoding='utf-8')
(work/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(work/'effective-config.json').write_text(json.dumps(values,ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared extension compilation repair, MSVC configuration and build helper. Homework sources unchanged.')
