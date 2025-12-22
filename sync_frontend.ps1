# Frontend Sync Script (Zip Deploy)
$ErrorActionPreference = "Stop"

$SOURCE_DIR = "$PSScriptRoot\apps\customer"
# Azure Deployment Credentials
$DEPLOY_USER = '$zoff-scope-frontend'
$DEPLOY_PASS = '2eTLRd9aco4QpLcH3rh3GhGR8DaMBtMSBRg3i4lzEtjQQ5X9Rd49XoXa6vN9'

# API URL for Zip Deploy (isAsync=true is recommended for stability)
# API URL for Zip Deploy (isAsync=true is recommended for stability)
$ZIP_DEPLOY_URL = "https://zoff-scope-frontend.scm.azurewebsites.net/api/zipdeploy?isAsync=true"

$TEMP_DIR = "$PSScriptRoot\temp_frontend_sync"
$ZIP_FILE = "$PSScriptRoot\frontend_deploy.zip"

Write-Host "1. Preparing files..."
if (Test-Path $TEMP_DIR) { Remove-Item -Recurse -Force $TEMP_DIR }
New-Item -ItemType Directory -Force -Path $TEMP_DIR | Out-Null

# Exclude node_modules primarily to force install on server, or if robocopy copy all then delete
# Reverting to INCLUDE node_modules to ensure they are present, using tar to zip reliably
robocopy "$SOURCE_DIR\.next\standalone" "$TEMP_DIR" /E /NFL /NDL /NJH /NJS
if ($LASTEXITCODE -gt 7) { Write-Error "Robocopy failed (Standalone) with exit code $LASTEXITCODE" }

# REMOVE WINDOWS NODE_MODULES
# ...

# 2. Copy Static Assets (Required for images/styles/fonts)
New-Item -ItemType Directory -Force -Path "$TEMP_DIR\.next\static" | Out-Null
robocopy "$SOURCE_DIR\.next\static" "$TEMP_DIR\.next\static" /E /NFL /NDL /NJH /NJS
if ($LASTEXITCODE -gt 7) { Write-Error "Robocopy failed (Static) with exit code $LASTEXITCODE" }

# 3. Copy Public Assets (Required for favicon, public images)
New-Item -ItemType Directory -Force -Path "$TEMP_DIR\public" | Out-Null
robocopy "$SOURCE_DIR\public" "$TEMP_DIR\public" /E /NFL /NDL /NJH /NJS
if ($LASTEXITCODE -gt 7) { Write-Error "Robocopy failed (Public) with exit code $LASTEXITCODE" }

# FIX START SCRIPT FOR STANDALONE
Write-Host "Patching package.json (Set start, Remove build)..."
$pkgJsonPath = "$TEMP_DIR\package.json"
if (Test-Path $pkgJsonPath) {
    $pkgJson = Get-Content $pkgJsonPath -Raw | ConvertFrom-Json
    $pkgJson.scripts.start = "node server.js"
    # Remove build script to prevent Oryx from trying to rebuild (which fails in standalone)
    if ($pkgJson.scripts.PSObject.Properties.Match("build").Count -gt 0) {
        $pkgJson.scripts.PSObject.Properties.Remove("build")
    }
    
    $pkgJson | ConvertTo-Json -Depth 10 | Set-Content $pkgJsonPath
    Write-Host "Updated package.json: set start='node server.js', removed build script"
}
else {
    Write-Warning "package.json not found in temp dir!"
}

Write-Host "2. Zipping artifacts..."
if (Test-Path $ZIP_FILE) { Remove-Item -Force $ZIP_FILE }

Write-Host "Zipping artifacts using tar (more reliable than Compress-Archive)..."
# Use tar to handle deep paths correctly
tar -a -c -f "$ZIP_FILE" -C "$TEMP_DIR" .

Write-Host "3. Uploading to Azure via Zip Deploy..."
Write-Host "Target URL: $ZIP_DEPLOY_URL"

# Create Basic Auth Header
$base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("${DEPLOY_USER}:${DEPLOY_PASS}")))

try {
    # Increase timeout to 10 minutes for large uploads
    Invoke-RestMethod -Uri $ZIP_DEPLOY_URL -Headers @{Authorization = ("Basic {0}" -f $base64AuthInfo) } -Method Post -InFile $ZIP_FILE -ContentType "application/zip" -TimeoutSec 1200
    Write-Host "Done! Deployment initiated successfully."
}
catch {
    Write-Error "Deployment failed: $_"
    try {
        if ($_.Exception.Response) {
            $stream = $_.Exception.Response.GetResponseStream()
            if ($stream) {
                $reader = New-Object System.IO.StreamReader($stream)
                $responseBody = $reader.ReadToEnd()
                Write-Host "Server Response: $responseBody"
            }
        }
    }
    catch {
        Write-Host "Could not read error response body."
    }
}

Write-Host "4. Cleanup..."
Remove-Item -Recurse -Force $TEMP_DIR
Remove-Item -Force $ZIP_FILE
Write-Host "Deployment script finished."
