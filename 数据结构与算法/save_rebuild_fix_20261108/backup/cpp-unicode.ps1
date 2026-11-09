param(
    [Parameter(Mandatory=$true)][string]$Source,
    [switch]$Run
)
$ErrorActionPreference = 'Stop'
$Source = (Resolve-Path -LiteralPath $Source).Path
$sourceDir = Split-Path -LiteralPath $Source
$outputDir = Join-Path $sourceDir 'output'
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
$baseName = [IO.Path]::GetFileNameWithoutExtension($Source)
$exe = Join-Path $outputDir ($baseName + '.exe')
$obj = Join-Path $outputDir ($baseName + '.obj')
$pdb = Join-Path $outputDir ($baseName + '.pdb')
$devcmd = 'C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat'
if (!(Test-Path -LiteralPath $devcmd)) { throw "Visual Studio C++ build tools were not found: $devcmd" }
# Use the Unicode environment API to preserve non-ASCII paths from VsDevCmd.
$envLines = & $env:ComSpec /d /c "call `"$devcmd`" -no_logo -arch=x64 -host_arch=x64 >nul && set"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
foreach ($line in $envLines) {
    if ($line -match '^([^=]+)=(.*)$') { [Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process') }
}
chcp.com 65001 > $null
$compileArgs = @('/nologo', '/utf-8', '/Zi', '/W4', "/Fo$obj", "/Fd$pdb")
if ([IO.Path]::GetExtension($Source) -ne '.c') { $compileArgs += @('/EHsc', '/std:c++17') }
$compileArgs += @($Source, "/Fe$exe", '/link', "/PDB:$pdb", '/INCREMENTAL:NO')
Push-Location -LiteralPath $sourceDir
try {
    & cl.exe @compileArgs
    $buildExit = $LASTEXITCODE
    if ($buildExit -ne 0) { exit $buildExit }
    if ($Run) {
        $runner = Join-Path $PSScriptRoot 'cpp-console.ps1'
        if (!(Test-Path -LiteralPath $runner)) { throw "Console runner was not found: $runner" }
        $quotedRunner = $runner.Replace("'", "''")
        $quotedExe = $exe.Replace("'", "''")
        $consoleCommand = "& '$quotedRunner' -Program '$quotedExe'"
        $encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($consoleCommand))
        $consoleHost = Join-Path $env:WINDIR 'System32\conhost.exe'
        Start-Process -FilePath $consoleHost -WorkingDirectory $sourceDir -ArgumentList @('powershell.exe', '-NoLogo', '-NoProfile', '-EncodedCommand', $encoded) | Out-Null
    }
} finally { Pop-Location }
exit 0





