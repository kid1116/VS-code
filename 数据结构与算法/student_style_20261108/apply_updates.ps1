$ErrorActionPreference = 'Stop'
$workRoot = $PSScriptRoot
$sourceRoot = Join-Path $workRoot 'modified'
$backupRoot = Join-Path $workRoot 'original'
$targetRoot = (Get-Item -LiteralPath 'D:\VS code\58125117-吴天宇-第三次作业').FullName
$relativePaths = Get-Content -Raw -LiteralPath (Join-Path $workRoot 'manifest.json') | ConvertFrom-Json
if ($relativePaths.Count -ne 7) { throw 'Expected exactly seven source files.' }

$untouched = @{}
Get-ChildItem -LiteralPath $targetRoot -Recurse -File | Where-Object Extension -ne '.cpp' | ForEach-Object {
    $untouched[$_.FullName] = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
}

# 先检查全部原文件，避免覆盖用户在备份之后另行编辑的代码。
foreach ($relative in $relativePaths) {
    $destination = [System.IO.Path]::GetFullPath((Join-Path $targetRoot $relative))
    if (!$destination.StartsWith($targetRoot + '\', [System.StringComparison]::OrdinalIgnoreCase) -or
        [System.IO.Path]::GetExtension($destination) -ne '.cpp') {
        throw 'Unexpected destination path.'
    }
    $original = Join-Path $backupRoot $relative
    $revised = Join-Path $sourceRoot $relative
    if (!(Test-Path -LiteralPath $revised)) { throw 'Revised source is missing.' }
    if ((Get-FileHash -LiteralPath $destination).Hash -ne (Get-FileHash -LiteralPath $original).Hash) {
        throw "File changed after backup: $relative"
    }
}

foreach ($relative in $relativePaths) {
    $destination = Join-Path $targetRoot $relative
    $revised = Join-Path $sourceRoot $relative
    Copy-Item -LiteralPath $revised -Destination $destination -Force
    if ((Get-FileHash -LiteralPath $destination).Hash -ne (Get-FileHash -LiteralPath $revised).Hash) {
        throw "Copy verification failed: $relative"
    }
    Write-Output "Updated: $relative"
}

foreach ($path in $untouched.Keys) {
    if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash -ne $untouched[$path]) {
        throw "Non-source file changed: $path"
    }
}
Write-Output 'All seven C++ files were updated and verified.'
