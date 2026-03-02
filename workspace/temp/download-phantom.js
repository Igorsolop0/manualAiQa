const fs = require('fs');
const https = require('https');
const path = require('path');
const { execSync } = require('child_process');

const PHANTOM_CRX_URL = 'https://crx-backup.phantom.dev/latest.crx';
const TMP_DIR = '/Users/ihorsolopii/.openclaw/workspace/temp/phantom-extension';

async function downloadPhantom() {
  console.log('Downloading Phantom extension...');
  
  if (!fs.existsSync(TMP_DIR)) {
    fs.mkdirSync(TMP_DIR, { recursive: true });
  }
  
  const crxPath = path.join(TMP_DIR, 'phantom.crx');
  
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(crxPath);
    https.get(PHANTOM_CRX_URL, (response) => {
      if (response.statusCode !== 200) {
        reject(new Error(`Failed to download: ${response.statusCode}`));
        return;
      }
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        console.log(`Downloaded to ${crxPath}`);
        resolve(crxPath);
      });
    }).on('error', (err) => {
      fs.unlink(crxPath, () => {});
      reject(err);
    });
  });
}

async function extractCrx(crxPath) {
  console.log('Extracting CRX...');
  const extractDir = path.join(TMP_DIR, 'extracted');
  if (!fs.existsSync(extractDir)) {
    fs.mkdirSync(extractDir, { recursive: true });
  }
  
  // Use unzip command (CRX is basically a ZIP)
  try {
    execSync(`unzip -q -o "${crxPath}" -d "${extractDir}"`);
    console.log(`Extracted to ${extractDir}`);
    
    // Check for manifest
    const manifestPath = path.join(extractDir, 'manifest.json');
    if (fs.existsSync(manifestPath)) {
      console.log('Manifest found:', JSON.parse(fs.readFileSync(manifestPath, 'utf8')).name);
      return extractDir;
    } else {
      throw new Error('No manifest.json found');
    }
  } catch (error) {
    console.error('Failed to extract:', error.message);
    throw error;
  }
}

async function main() {
  try {
    const crxPath = await downloadPhantom();
    const extensionPath = await extractCrx(crxPath);
    console.log(`✅ Phantom extension ready at: ${extensionPath}`);
    
    // Write path to file for playwright
    const pathFile = '/Users/ihorsolopii/.openclaw/workspace/temp/phantom-path.txt';
    fs.writeFileSync(pathFile, extensionPath);
    console.log(`Path saved to ${pathFile}`);
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

main();