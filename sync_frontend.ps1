
# Frontend Sync Script (Standalone Artifact Deployment)
$ErrorActionPreference = "Stop"

$SOURCE_DIR = "$PSScriptRoot\apps\customer"
# Azure Deployment Credentials (Fill these in!)
# NOTE: Use single quotes '' to handle special characters like $ safely
$DEPLOY_USER = 'REPLACE_WITH_VARIABLE_git_username'
$DEPLOY_PASS = 'REPLACE_WITH_VARIABLE_password'

# Construct URL with credentials
$REPO_URL = "https://${DEPLOY_USER}:${DEPLOY_PASS}@zoff-scope-frontend.scm.azurewebsites.net:443/zoff-scope-frontend.git"
$TEMP_DIR = "$PSScriptRoot\temp_frontend_sync"

Write-Host "1. Cloning remote repository..."
if (Test-Path $TEMP_DIR) { Remove-Item -Recurse -Force $TEMP_DIR }
git clone $REPO_URL $TEMP_DIR

Write-Host "2. Preparing files (Standalone Artifact)..."
# Clean existing files (REMOVE EVERYTHING except .git to replace with artifact)
Set-Location $TEMP_DIR
git rm -rf .
git clean -fdx
Set-Location ..

Write-Host "Copying Standalone Artifacts..."
# 1. Copy Standalone (Base Server)
# This includes server.js, package.json, compiled server files, and node_modules
robocopy "$SOURCE_DIR\.next\standalone" "$TEMP_DIR" /E /NFL /NDL /NJH /NJS
if ($LASTEXITCODE -gt 7) { Write-Error "Robocopy failed (Standalone) with exit code $LASTEXITCODE" }

# 2. Copy Static Assets (Required for images/styles/fonts)
# Must be placed in .next/static inside the deployment root
New-Item -ItemType Directory -Force -Path "$TEMP_DIR\.next\static" | Out-Null
robocopy "$SOURCE_DIR\.next\static" "$TEMP_DIR\.next\static" /E /NFL /NDL /NJH /NJS
if ($LASTEXITCODE -gt 7) { Write-Error "Robocopy failed (Static) with exit code $LASTEXITCODE" }

# 3. Copy Public Assets (Required for favicon, public images)
New-Item -ItemType Directory -Force -Path "$TEMP_DIR\public" | Out-Null
robocopy "$SOURCE_DIR\public" "$TEMP_DIR\public" /E /NFL /NDL /NJH /NJS
if ($LASTEXITCODE -gt 7) { Write-Error "Robocopy failed (Public) with exit code $LASTEXITCODE" }

# Reset ErrorAction
$ErrorActionPreference = "Stop"

Write-Host "3. Committing and Pushing Artifacts..."
Set-Location $TEMP_DIR
git add .
git commit -m "Deploy Standalone Artifact (Local Build)"
git push origin main
Set-Location ..

Write-Host "4. Cleanup..."
Remove-Item -Recurse -Force $TEMP_DIR

Write-Host "Done! Standalone artifact successfully pushed."
