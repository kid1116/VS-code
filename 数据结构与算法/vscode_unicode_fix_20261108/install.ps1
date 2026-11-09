$ErrorActionPreference = 'Stop'
$manifest = Get-Content -Raw -LiteralPath (Join-Path $PSScriptRoot 'manifest.json') | ConvertFrom-Json
foreach ($entry in $manifest) {
    if ($entry.original_hash) {
        $current = (Get-FileHash -LiteralPath $entry.destination -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($current -ne $entry.original_hash) { throw "Configuration changed: $($entry.destination)" }
    } elseif (Test-Path -LiteralPath $entry.destination) {
        throw "A new configuration appeared: $($entry.destination)"
    }
}
foreach ($entry in $manifest) {
    $directory = Split-Path -Parent $entry.destination
    New-Item -ItemType Directory -Path $directory -Force | Out-Null
    Copy-Item -LiteralPath $entry.stage -Destination $entry.destination -Force
    if ((Get-FileHash -LiteralPath $entry.stage).Hash -ne (Get-FileHash -LiteralPath $entry.destination).Hash) {
        throw 'Copy verification failed.'
    }
    Write-Output "Updated: $($entry.destination)"
}
