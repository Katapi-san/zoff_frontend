$ErrorActionPreference = "Stop"

$SOURCE_DIR = "$PSScriptRoot\apps\customer"
$TEMP_DIR = "$PSScriptRoot\temp_frontend_sync"

Write-Host "Preparing files in $TEMP_DIR..."
if (Test-Path $TEMP_DIR) { Remove-Item -Recurse -Force $TEMP_DIR }
New-Item -ItemType Directory -Force -Path $TEMP_DIR | Out-Null

# 1. Copy Standalone
Write-Host "Copying Standalone Artifacts..."
robocopy "$SOURCE_DIR\.next\standalone" "$TEMP_DIR" /E /NFL /NDL /NJH /NJS
if ($LASTEXITCODE -gt 7) { Write-Error "Robocopy failed (Standalone) with exit code $LASTEXITCODE" }

# 2. Copy Static
New-Item -ItemType Directory -Force -Path "$TEMP_DIR\.next\static" | Out-Null
robocopy "$SOURCE_DIR\.next\static" "$TEMP_DIR\.next\static" /E /NFL /NDL /NJH /NJS
if ($LASTEXITCODE -gt 7) { Write-Error "Robocopy failed (Static) with exit code $LASTEXITCODE" }

# 3. Copy Public
New-Item -ItemType Directory -Force -Path "$TEMP_DIR\public" | Out-Null
robocopy "$SOURCE_DIR\public" "$TEMP_DIR\public" /E /NFL /NDL /NJH /NJS
if ($LASTEXITCODE -gt 7) { Write-Error "Robocopy failed (Public) with exit code $LASTEXITCODE" }

# 4. Fix package.json
Write-Host "Patching package.json..."
$pkgJsonPath = "$TEMP_DIR\package.json"
if (Test-Path $pkgJsonPath) {
    $pkgJson = Get-Content $pkgJsonPath -Raw | ConvertFrom-Json
    $pkgJson.scripts.start = "node server.js"
    $pkgJson | ConvertTo-Json -Depth 10 | Set-Content $pkgJsonPath
    Write-Host "Updated package.json start script."
} else {
    Write-Warning "package.json not found!"
}

Write-Host "Files prepared."
