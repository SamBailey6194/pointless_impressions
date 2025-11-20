import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const cssDir = path.resolve(__dirname, '../../../static/css');
const jsDir = path.resolve(__dirname, '../../../static/js');

function cleanDir(dir) {
  if (fs.existsSync(dir)) {
    fs.rmSync(dir, { recursive: true, force: true });
    fs.mkdirSync(dir, { recursive: true });
    console.log(`✓ Cleaned ${dir}`);
  }
}

cleanDir(cssDir);
cleanDir(jsDir);