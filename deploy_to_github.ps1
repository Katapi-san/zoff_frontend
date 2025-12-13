
# Script to Deploy Frontend Build Artifacts to GitHub Repo
# The repo "zoff_Frontend_v2" is used as an artifact store for Azure.

$REPO_URL = "https://github.com/Katapi-san/zoff_Frontend_v2.git"
$SOURCE_DIR = "$PSScriptRoot\apps\customer"
$TEMP_DIR = "$PSScriptRoot\temp_kudu_deploy"

# 1. Clone Repo
Write-Host "1. Cloning repository..."
if (Test-Path $TEMP_DIR) { Remove-Item -Force -Recurse $TEMP_DIR }
git clone $REPO_URL $TEMP_DIR

if (-not (Test-Path "$TEMP_DIR\.git")) {
    Write-Error "Failed to clone repository."
    exit 1
}

# 2. Clean Repo (Keep .git and .github)
Write-Host "2. Cleaning repository..."
Start-Process -FilePath "git" -ArgumentList "rm -rf ." -WorkingDirectory $TEMP_DIR -NoNewWindow -Wait
Start-Process -FilePath "git" -ArgumentList "clean -fdx" -WorkingDirectory $TEMP_DIR -NoNewWindow -Wait

# 3. Copy Artifacts
Write-Host "3. Copying Standalone Artifacts..."
# Copy .next/standalone content to root
robocopy "$SOURCE_DIR\.next\standalone" "$TEMP_DIR" /E /NFL /NDL /NJH /NJS
# Copy .next/static to .next/static
New-Item -ItemType Directory -Path "$TEMP_DIR\.next\static" -Force | Out-Null
robocopy "$SOURCE_DIR\.next\static" "$TEMP_DIR\.next\static" /E /NFL /NDL /NJH /NJS
# Copy public to public
New-Item -ItemType Directory -Path "$TEMP_DIR\public" -Force | Out-Null
robocopy "$SOURCE_DIR\public" "$TEMP_DIR\public" /E /NFL /NDL /NJH /NJS

# 3b. Verify .github integrity
Write-Host "Restoring .github folder to ensure workflow persists..."
Start-Process -FilePath "git" -ArgumentList "checkout HEAD -- .github" -WorkingDirectory $TEMP_DIR -NoNewWindow -Wait

# 3c. FIX START SCRIPT FOR STANDALONE
$pkgJsonPath = "$TEMP_DIR\package.json"
$pkgJson = Get-Content $pkgJsonPath -Raw | ConvertFrom-Json
$pkgJson.scripts.start = "node server.js"
$pkgJson | ConvertTo-Json -Depth 10 | Set-Content $pkgJsonPath
Write-Host "Updated package.json start script to 'node server.js'"

# 4. Commit and Push
Write-Host "4. Pushing to GitHub..."
Set-Location $TEMP_DIR
git add .
git commit -m "Deploy Standalone Artifact (Mixed Content Fix)"
git push origin main
Write-Host "Done! Artifacts pushed to GitHub."
