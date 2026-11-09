$ErrorActionPreference = 'Stop'
$manifest = Get-Content -Raw -LiteralPath (Join-Path $PSScriptRoot 'manifest.json') | ConvertFrom-Json
$targetRoot = [IO.Path]::GetFullPath('C:\Users\12120\Desktop\58125117-吴天宇-第三次作业')
foreach ($entry in $manifest) {
    $destination = [IO.Path]::GetFullPath($entry.destination)
    if (!$destination.StartsWith($targetRoot + '\', [StringComparison]::OrdinalIgnoreCase) -or
        [IO.Path]::GetExtension($destination) -ne '.cpp') { throw 'Unexpected target path.' }
    if ((Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.original_hash) {
        throw "Source changed after backup: $destination"
    }
}
foreach ($entry in $manifest) {
    Copy-Item -LiteralPath $entry.source -Destination $entry.destination -Force
    if ((Get-FileHash -LiteralPath $entry.source).Hash -ne (Get-FileHash -LiteralPath $entry.destination).Hash) {
        throw "Copy verification failed: $($entry.destination)"
    }
    Write-Output "Updated desktop source: $($entry.relative)"
}
