
# Azure App Service Zip Deploy Script for Backend
# Created by Antigravity

# --- CONFIGURATION (PLEASE UPDATE THESE) ---
$DEPLOY_USER = "`$zoff-scope-backend"  # Default App Credentials User (Application Scope)
$DEPLOY_PASS = "AqiyFiSPTfCoBTYAMph7hu9qoY2Qox83P3pWDy3neLminTcrTrrRNxo5qddL" # <--- PLEASE ENTER PASSWORD HERE

# API URL for Zip Deploy (isAsync=true is recommended for stability)
$ZIP_DEPLOY_URL = "https://zoff-scope-backend.scm.azurewebsites.net/api/zipdeploy?isAsync=true"

$SOURCE_DIR = "$PSScriptRoot\backend"
$TEMP_DIR = "$PSScriptRoot\temp_backend_deploy"
$ZIP_FILE = "$PSScriptRoot\backend_deploy.zip"

# -------------------------------------------

Write-Host "1. Preparing files..."
if (Test-Path $TEMP_DIR) { Remove-Item -Force -Recurse $TEMP_DIR }
New-Item -ItemType Directory -Path $TEMP_DIR | Out-Null

# Copy backend files (excluding venv, __pycache__, .git etc.)
Write-Host "Copying Backend Artifacts..."
# Use robocopy for robust exclusion
# Exclude: venv, __pycache__, .git, .vscode, logs, tmp
robocopy "$SOURCE_DIR" "$TEMP_DIR" /E /XD "venv" "__pycache__" ".git" ".vscode" "logs" "temp_*" /XF "*.pyc" "*.log" "*.DS_Store" /NFL /NDL /NJH /NJS

# Zip the artifacts using tar to ensure POSIX paths
Write-Host "2. Zipping artifacts using tar..."
if (Test-Path $ZIP_FILE) { Remove-Item -Force $ZIP_FILE }
# -a: auto-detect suffix (zip), -c: create, -f: file, -C: change directory
tar -a -c -f "$ZIP_FILE" -C "$TEMP_DIR" .

Write-Host "3. Uploading to Azure via Zip Deploy..."
Write-Host "Target URL: $ZIP_DEPLOY_URL"

# Create Authorization Header (Basic Auth)
$authPair = "$($DEPLOY_USER):$($DEPLOY_PASS)"
$authBytes = [System.Text.Encoding]::ASCII.GetBytes($authPair)
$base64Auth = [System.Convert]::ToBase64String($authBytes)
$headers = @{
    "Authorization" = "Basic $base64Auth"
}

# Upload Zip
try {
    # Using curl for upload to handle large files better or stick to Invoke-RestMethod
    # We will use Invoke-RestMethod for consistency, but with timeout
    Invoke-RestMethod -Uri $ZIP_DEPLOY_URL -Method Post -InFile $ZIP_FILE -ContentType "application/zip" -Headers $headers -TimeoutSec 600
    Write-Host "`nDone! Deployment initiated successfully."
}
catch {
    Write-Error "Deployment failed: $_"
    exit 1
}

Write-Host "4. Cleanup..."
# Remove-Item -Force -Recurse $TEMP_DIR
# Remove-Item -Force $ZIP_FILE

Write-Host "Deployment script finished."
