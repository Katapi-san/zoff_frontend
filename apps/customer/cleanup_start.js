
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

console.log('[Startup] Starting cleanup of potential stale artifacts...');

// Files to remove to ensure fresh state
const filesToRemove = [
    'node_modules.tar.gz',
    'oryx-manifest.toml',
    'package-lock.json.bak'
];

filesToRemove.forEach(file => {
    const filePath = path.join(process.cwd(), file);
    if (fs.existsSync(filePath)) {
        try {
            fs.unlinkSync(filePath);
            console.log(`[Startup] Removed stale file: ${file}`);
        } catch (e) {
            console.warn(`[Startup] Failed to remove ${file}: ${e.message}`);
        }
    }
});

console.log('[Startup] Cleanup complete. Starting Next.js server...');

// Start the actual server
const server = spawn('node', ['server.js'], {
    stdio: 'inherit',
    env: process.env
});

server.on('close', (code) => {
    process.exit(code);
});
