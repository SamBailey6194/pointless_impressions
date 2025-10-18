// hash-js.js
import esbuild from 'esbuild';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import glob from 'glob';

// Define source and output folders
const srcDir = path.resolve(__dirname, '../js/build'); // only build-ready JS
const outDir = path.resolve(__dirname, '../../../../../static/js'); // hashed output

// Ensure output directory exists
if (!fs.existsSync(outDir)) {
  fs.mkdirSync(outDir, { recursive: true });
}

async function buildAndHash() {
  // Find all JS files in build folder
  const entryPoints = glob.sync(path.join(srcDir, '**/*.js'));

  for (const entry of entryPoints) {
    const fileName = path.basename(entry, '.js');

    // Bundle and minify each file
    const outFile = path.join(outDir, `${fileName}.js`);
    await esbuild.build({
      entryPoints: [entry],
      bundle: true,
      minify: true,
      outfile: outFile,
      sourcemap: false,
      write: true,
    });

    // Read file content and generate hash
    const content = fs.readFileSync(outFile);
    const hash = crypto.createHash('md5').update(content).digest('hex').slice(0, 8);
    const hashedFileName = `${fileName}.${hash}.js`;
    const hashedFilePath = path.join(outDir, hashedFileName);

    // Rename file to include hash
    fs.renameSync(outFile, hashedFilePath);
    console.log(`Built and hashed JS: ${hashedFileName}`);
  }
}

buildAndHash().catch((err) => {
  console.error(err);
  process.exit(1);
});