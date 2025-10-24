import crypto from 'crypto';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const cssDir = path.resolve(__dirname, '../../../../static/css');
const cssFile = path.join(cssDir, 'styles.css');
const manifestPath = path.join(cssDir, 'manifest.json');

if (fs.existsSync(cssFile)) {
  const content = fs.readFileSync(cssFile, 'utf8');
  const hash = crypto.createHash('md5').update(content).digest('hex').substring(0, 8);
  const hashedName = `styles.${hash}.css`;
  const hashedPath = path.join(cssDir, hashedName);
  
  // Copy to hashed filename
  fs.copyFileSync(cssFile, hashedPath);
  
  // Delete unhashed file
  fs.unlinkSync(cssFile);
  
  // Create/update manifest
  const manifest = { 'styles.css': hashedName };
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
  
  console.log(`✓ CSS hashed: ${hashedName}`);
  console.log(`✓ Removed unhashed styles.css`);
} else {
  console.error('styles.css not found');
  process.exit(1);
}