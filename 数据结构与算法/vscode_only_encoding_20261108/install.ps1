$ErrorActionPreference = 'Stop'
$manifest = Get-Content -Raw -LiteralPath (Join-Path $PSScriptRoot 'manifest.json') | ConvertFrom-Json
foreach ($entry in $manifest) {
    if ($entry.original_hash) {
        if ((Get-FileHash -LiteralPath $entry.destination -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.original_hash) {
            throw "File changed after preparation: $($entry.destination)"
        }
    } elseif (Test-Path -LiteralPath $entry.destination) {
        throw "File already appeared: $($entry.destination)"
    }
}
foreach ($entry in $manifest) {
    Copy-Item -LiteralPath $entry.stage -Destination $entry.destination -Force
    if ((Get-FileHash -LiteralPath $entry.stage).Hash -ne (Get-FileHash -LiteralPath $entry.destination).Hash) {
        throw "Copy verification failed: $($entry.destination)"
    }
    Write-Output "Updated: $($entry.destination)"
}
