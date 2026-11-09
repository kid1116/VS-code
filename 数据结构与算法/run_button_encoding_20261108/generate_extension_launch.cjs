const fs = require('node:fs');
const path = require('node:path');
const source = fs.readFileSync('C:/Users/12120/.vscode/extensions/danielpinto8zz6.c-cpp-compile-run-1.0.92/dist/extension.js','utf8');
const work = __dirname;
const config = JSON.parse(fs.readFileSync(path.join(work,'manifest.json'),'utf8'));
const cached = new Map();
const launches = [];
const shell = {cmd:'Command Prompt',powerShell:'PowerShell',gitBash:'Git Bash',wsl:'WSL Bash',others:'Others'};
let outputDirectory;
const configuration = {
    customRunPrefix:()=>config.prefix,
    runArgs:()=>'',
    winTerminal:()=>config.terminal
};
const mocks = {
    1398:{env:{shell:'C:\\Windows\\System32\\cmd.exe'}},
    9896:fs,
    6928:path,
    9334:{Configuration:configuration},
    3932:{ShellType:shell},
    8689:{Notification:{showErrorMessage:(s)=>{throw new Error(s)},showWarningMessage:()=>{}}},
    3882:{terminal:{}},
    1734:{},
    2862:{getOutputLocation:()=>outputDirectory},
    803:{default:false},
    7811:{ensureWorkspaceIsTrusted:async()=>true},
    5317:{exec:(command,options)=>{
        launches.push({command,cwd:options.cwd});
        return {on:()=>{}};
    }},
    205:{},
    2925:{},
    8499:{}
};
function load(id) {
    if (mocks[id]) return mocks[id];
    if (cached.has(id)) return cached.get(id);
    const marker = new RegExp(id+'\\(e(?:,t)?(?:,n)?\\)\\{').exec(source);
    if(!marker) throw new Error('Module not found: '+id);
    const bodyStart=marker.index+marker[0].length;
    const next=/},\d+\(e(?:,t)?(?:,n)?\)\{/.exec(source.slice(bodyStart));
    if(!next) throw new Error('Module end not found: '+id);
    const body=source.slice(bodyStart,bodyStart+next.index);
    const module={exports:{}};
    new Function('e','t','n',body)(module,module.exports,load);
    cached.set(id,module.exports);
    return module.exports;
}
(async()=>{
    const {Runner}=load(7532);
    const root='D:/VS code/58125117-吴天宇-第三次作业';
    for (const file of [
        {path:path.join(root,'平时作业/平时作业1.cpp'),directory:path.join(root,'平时作业'),executable:'平时作业1.exe'},
        {path:'D:/VS code/数据结构与算法/vscode_only_encoding_20261108/probe/console_probe.cpp',directory:'D:/VS code/数据结构与算法/vscode_only_encoding_20261108/probe',executable:'console_probe.exe'}
    ]) {
        outputDirectory=path.join(file.directory,'output');
        await new Runner(file,false).run(true);
    }
    if(launches.length!==2 || !launches.every(x=>x.command.startsWith('start cmd /c ')&&x.command.endsWith(' & echo. & pause"')))throw new Error('Unexpected extension command');
    fs.writeFileSync(path.join(work,'extension-launches.json'),JSON.stringify(launches,null,2),'utf8');
    console.log('Generated two launch commands using the installed extension\'s actual Runner and external-terminal modules.');
})().catch(e=>{console.error(e);process.exitCode=1});
