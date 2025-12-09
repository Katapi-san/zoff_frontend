
# Frontend Sync Script
$ErrorActionPreference = "Stop"

$SOURCE_DIR = "apps/customer"
$REPO_URL = "https://github.com/Katapi-san/zoff_Frontend_v2.git"
$TEMP_DIR = "temp_frontend_sync"

Write-Host "1. Cloning remote repository..."
if (Test-Path $TEMP_DIR) { Remove-Item -Recurse -Force $TEMP_DIR }
git clone $REPO_URL $TEMP_DIR

Write-Host "2. Preparing files..."
# Clean existing files in temp repo (keep .git)
Set-Location $TEMP_DIR
git rm -rf .
git clean -fdx
Set-Location ..

# Copy new files from apps/customer
Write-Host "Copying from $SOURCE_DIR to $TEMP_DIR..."
# Use robocopy for robust copying, exclude node_modules and .next
robocopy $SOURCE_DIR $TEMP_DIR /E /XD node_modules .next .git /NFL /NDL /NJH /NJS
# Robocopy exit codes: 0-7 are success (0=no change, 1=copy success)
if ($LASTEXITCODE -gt 7) { 
    Write-Error "Robocopy failed with exit code $LASTEXITCODE" 
}
# Reset ErrorAction for robocopy weirdness
$ErrorActionPreference = "Stop"

Write-Host "3. Committing and Pushing..."
Set-Location $TEMP_DIR
git add .
git commit -m "Manual sync from local monorepo"
git push origin main
Set-Location ..

Write-Host "4. Cleanup..."
Remove-Item -Recurse -Force $TEMP_DIR

Write-Host "Done! Frontend successfully pushed."
