const fs=require('node:fs');
const path=require('node:path');
const cp=require('node:child_process');
const crypto=require('node:crypto');
const work=__dirname;
const live=process.argv.includes('--live');
const fixtureOnly=process.argv.includes('--fixture-only');
const user='C:/Users/12120/AppData/Roaming/Code/User';
const extension=live?'C:/Users/12120/.vscode/extensions/danielpinto8zz6.c-cpp-compile-run-1.0.92/dist/extension.js':path.join(work,'prepared/extension.js');
const source=fs.readFileSync(extension,'utf8');
const config=JSON.parse(fs.readFileSync(path.join(work,'effective-config.json'),'utf8'));
const logdir=path.join(work,live?'live-logs':'logs');fs.mkdirSync(logdir,{recursive:true});
process.env.APPDATA='C:/Users/12120/AppData/Roaming';
let document,includes=[],outputLocation='output',spawnCount=0,taskCount=0;
const errors=[],infos=[],launches=[],cache=new Map();
const state={
    'cpp-compiler':config['c-cpp-compile-run.cpp-compiler'],
    'c-compiler':config['c-cpp-compile-run.c-compiler'],
    'cpp-flags':config['c-cpp-compile-run.cpp-flags'],
    'c-flags':config['c-cpp-compile-run.c-flags'],
    'cpp-linker-flags':'','c-linker-flags':'','save-before-compile':true,
    'skip-if-compiled':false,'run-args':'','custom-run-prefix':'chcp.com 65001 > nul &',
    'run-in-external-terminal':true,'mirror-output-location':false
};
const vscode={
    env:{shell:'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'},
    window:{get activeTextEditor(){return {document}},showErrorMessage:async()=>undefined},
    workspace:{
        workspaceFolders:[{uri:{fsPath:'D:/VS code'}}],
        getConfiguration:(section)=>({get:key=>{
            if(key==='terminal.external.windowsExec')return 'C:\\Windows\\System32\\cmd.exe';
            if(section==='c-cpp-compile-run'&&key==='output-location')return outputLocation;
            if(section==='c-cpp-compile-run'&&key==='additional-include-paths')return includes;
            return state[key];
        }})
    },
    tasks:{executeTask:()=>{taskCount++;throw new Error('Broken task API must not be called for MSVC.')}},
    ProcessExecution:class{constructor(){throw new Error('Unexpected process task.')}},
    ShellExecution:class{constructor(){throw new Error('Unexpected shell task.')}},
    Task:class{constructor(){throw new Error('Unexpected Task constructor.')}}
};
const fsExtra={...fs,mkdirpSync:p=>fs.mkdirSync(p,{recursive:true}),readJsonSync:p=>JSON.parse(fs.readFileSync(p,'utf8').replace(/^\uFEFF/,''))};
const childProcesses={...cp,
    spawn:(command,args,options)=>{
        spawnCount++;
        const actual=[...args];
        const fileIndex=actual.indexOf('-File')+1;
        if(!live&&fileIndex>0&&path.basename(actual[fileIndex])==='cpp-unicode.ps1')actual[fileIndex]=path.join(work,'prepared/cpp-unicode.ps1');
        const child=cp.spawn(command,actual,options);
        let output='';child.stdout?.on('data',d=>{output+=d.toString('utf8')});child.stderr?.on('data',d=>{output+=d.toString('utf8')});
        const count=spawnCount;child.on('close',()=>fs.writeFileSync(path.join(logdir,`compile-${count}.txt`),output,'utf8'));
        return child;
    },
    exec:(command,options)=>{launches.push({command,cwd:options.cwd});return {on:()=>{}}}
};
const mocks={
    1398:vscode,9896:fsExtra,6928:path,5317:childProcesses,
    8789:{isWindows:()=>true,isProcessRunning:async()=>false,commandExists:async p=>fs.existsSync(p)},
    8689:{Notification:{showErrorMessage:t=>errors.push(t),showInformationMessage:t=>infos.push(t),showWarningMessage:()=>{}}},
    7811:{ensureWorkspaceIsTrusted:async()=>true},803:{default:false},
    1734:{promptFlags:async t=>t},3882:{terminal:{}},2925:{outputChannel:{appendLine:()=>{}}},205:{}
};
function load(id){
    if(mocks[id])return mocks[id];if(cache.has(id))return cache.get(id);
    const marker=new RegExp(id+'\\(e(?:,t)?(?:,n)?\\)\\{').exec(source);
    if(!marker)throw new Error('Module missing: '+id);
    const start=marker.index+marker[0].length;
    const next=/},\d+\(e(?:,t)?(?:,n)?\)\{/.exec(source.slice(start));
    if(!next)throw new Error('Module ending missing: '+id);
    const module={exports:{}};
    const names=marker[0].slice(marker[0].indexOf('(')+1,marker[0].indexOf(')')).split(',');
    new Function(...names,'require',source.slice(start,start+next.index))(...names.map(name=>name==='e'?module:name==='t'?module.exports:load),require);
    cache.set(id,module.exports);return module.exports;
}
function assert(value,message){if(!value)throw new Error(message)}
async function click(file){
    document={fileName:file,languageId:'cpp',isUntitled:false,save:async()=>true};
    const before=spawnCount,runBefore=launches.length,errorBefore=errors.length;
    const {CompileRunManager}=load(6235);
    await new CompileRunManager().compileRun(false,false,true);
    return {builds:spawnCount-before,runs:launches.length-runBefore,errors:errors.slice(errorBefore),launch:launches.at(-1)};
}
function runExe(file,input=''){
    const result=cp.spawnSync(file,[],{input,encoding:'utf8',timeout:20000,windowsHide:true});
    assert(result.status===0,`${file} failed: ${result.stderr}`);return result.stdout;
}
(async()=>{
    const root='D:/VS code/58125117-吴天宇-第三次作业';
    const snapshot=JSON.parse(fs.readFileSync(path.join(work,'source_snapshot.json'),'utf8'));
    if(!fixtureOnly)for(const file of Object.keys(snapshot)){
        const result=await click(file);
        assert(result.builds===1&&result.runs===1&&result.errors.length===0,JSON.stringify(result));
        const exe=path.join(path.dirname(file),'output',path.basename(file,'.cpp')+'.exe');
        const output=runExe(exe,file.includes('实践作业1.cpp')?'0\n':'');
        assert(output.includes('原栈')||!file.endsWith('平时作业1.cpp'),'Chinese output corrupted.');
        console.log('REAL RUN-BUTTON COMPILE OK:',path.basename(file));
    }

    // Saving different text must compile a new binary instead of running a stale one.
    const fixture=path.join(work,"保存测试 ' 中文 路径");fs.mkdirSync(fixture,{recursive:true});
    const headers=path.join(fixture,'头文件 目录');fs.mkdirSync(headers,{recursive:true});
    fs.writeFileSync(path.join(headers,'score.h'),'const int score = 7;\n','utf8');
    includes=[headers];outputLocation='生成 目录';
    const file=path.join(fixture,'保存后运行.cpp');
    const contents=version=>'#include <iostream>\n#include "score.h"\nint main(){std::cout << "保存版本：'+version+'，头文件值：" << score << std::endl;return 0;}\n';
    const exe=path.join(fixture,outputLocation,'保存后运行.exe');
    for(const version of [1,2]){
        fs.writeFileSync(file,'\uFEFF'+contents(version),'utf8');
        const saved=fs.statSync(file).mtimeMs;
        const result=await click(file);
        assert(result.builds===1&&result.runs===1&&result.errors.length===0,JSON.stringify(result));
        assert(fs.statSync(exe).mtimeMs>=saved,'Executable was not rebuilt after save.');
        const output=runExe(exe);assert(output.includes('保存版本：'+version+'，头文件值：7'),output);
        console.log('SAVE THEN CLICK RUN OK: version '+version+' actually executed.');
    }
    const previous=crypto.createHash('sha256').update(fs.readFileSync(exe)).digest('hex');
    fs.writeFileSync(file,'int main(){ This_is_an_intentional_compile_error; }\n','utf8');
    const failure=await click(file);
    assert(failure.builds===1&&failure.runs===0&&failure.errors.some(s=>s.includes('Compilation failed')),JSON.stringify(failure));
    assert(crypto.createHash('sha256').update(fs.readFileSync(exe)).digest('hex')===previous,'Stale binary unexpectedly changed.');
    console.log('COMPILE ERROR CHECK OK: old executable was NOT run.');
    fs.writeFileSync(file,'\uFEFF'+contents(3),'utf8');
    const recovered=await click(file);
    assert(recovered.runs===1&&recovered.errors.length===0,JSON.stringify(recovered));
    assert(runExe(exe).includes('保存版本：3'),'Build did not recover.');
    console.log('RECOVERY CHECK OK: saved version 3 compiled and ran.');
    assert(taskCount===0,'Reserved process task API was still invoked.');
    for(const [name,digest]of Object.entries(snapshot)){
        const bytes=fs.readFileSync(name);
        assert(crypto.createHash('sha256').update(bytes).digest('hex')===digest,'Homework source changed: '+name);
        assert(!/_WIN32|windows\.h|SetConsole|CP_UTF8/.test(bytes.toString('utf8')),'Windows code added to homework.');
    }
    fs.writeFileSync(path.join(work,live?'live-result.json':'result.json'),JSON.stringify({status:'passed',spawnCount,taskCount,launches,expectedCompileErrors:errors},null,2),'utf8');
    console.log('ALL SAVE / RECOMPILE / RUN CHECKS PASSED. Homework sources unchanged.');
})().catch(e=>{console.error(e);process.exitCode=1});
