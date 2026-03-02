// =============================================================
// Simple bundler: concatenates compiled TS modules into one IIFE
// Run after tsc: node scripts/bundle.js
// =============================================================
const fs = require("fs");
const path = require("path");

const distDir = path.join(__dirname, "..", "dist");
const outDir = path.join(__dirname, "..", "out");

const files = ["types.js", "api.js", "renderers.js", "main.js"];

let bundle = "(function(){\n";
for (const f of files) {
  const fp = path.join(distDir, f);
  if (!fs.existsSync(fp)) {
    console.error(`Missing: ${fp}`);
    process.exit(1);
  }
  let code = fs.readFileSync(fp, "utf8");
  code = code.replace(/^export /gm, "");
  code = code.replace(/^import .+ from .+;?\s*$/gm, "");
  bundle += `// --- ${f} ---\n${code}\n`;
}
bundle += "})();\n";

if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, "app.js"), bundle, "utf8");
console.log(
  `Bundled → ${path.join(outDir, "app.js")} (${bundle.length} bytes)`,
);
