param(
    [Parameter(Mandatory=$true)][string]$Program,
    [switch]$NoPause,
    [switch]$VerifyEncoding
)
$ErrorActionPreference = 'Stop'
$Program = (Resolve-Path -LiteralPath $Program).Path

# Configure the terminal here; student C/C++ files need no Windows-specific code.
chcp.com 65001 > $null
$utf8 = New-Object System.Text.UTF8Encoding($false)
[Console]::InputEncoding = $utf8
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8

try {
    $programProcess = Start-Process -FilePath $Program -WorkingDirectory (Split-Path -Parent $Program) -NoNewWindow -Wait -PassThru
    $programExitCode = $programProcess.ExitCode
} catch {
    Write-Host $_ -ForegroundColor Red
    $programExitCode = 1
}

if ($VerifyEncoding) {
    [Console]::Error.WriteLine('RUNNER_INPUT_CP=' + [Console]::InputEncoding.CodePage + '; OUTPUT_CP=' + [Console]::OutputEncoding.CodePage)
}
if (!$NoPause) {
    Write-Host ''
    Write-Host ('程序已结束，退出代码：' + $programExitCode)
    Read-Host '按回车关闭窗口' | Out-Null
}
exit $programExitCode
