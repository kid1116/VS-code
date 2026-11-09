$ErrorActionPreference = 'Stop'
$manifest = Get-Content -Raw -LiteralPath (Join-Path $PSScriptRoot 'manifest.json') | ConvertFrom-Json
if ((Get-FileHash -LiteralPath $manifest.destination -Algorithm SHA256).Hash.ToLowerInvariant() -ne $manifest.original_hash) {
    throw 'VS Code settings changed after preparation.'
}
Copy-Item -LiteralPath $manifest.stage -Destination $manifest.destination -Force
if ((Get-FileHash -LiteralPath $manifest.stage).Hash -ne (Get-FileHash -LiteralPath $manifest.destination).Hash) {
    throw 'Settings verification failed.'
}
Write-Output 'Updated the C/C++ Compile Run extension startup configuration.'
