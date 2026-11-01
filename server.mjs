import { createServer } from "node:http";
import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
import { extname, resolve, relative, sep } from "node:path";

const root = resolve(".");
const port = Number(process.env.PORT || 3000);
const types = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".webmanifest": "application/manifest+json; charset=utf-8",
  ".mp3": "audio/mpeg",
  ".wav": "audio/wav",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
  ".woff2": "font/woff2",
  ".ico": "image/x-icon"
};
const topFiles = new Set(["/index.html", "/app.js", "/styles.css", "/manifest.webmanifest", "/favicon.ico", "/group-one.js", "/group-two.js", "/group-three.js", "/group-four.js", "/group-five.js", "/group-six.js", "/group-seven.js", "/group-eight.js", "/group-nine.js", "/group-ten.js", "/continuous-learning.js", "/pattern-learning.js", "/readalong-assist.js"]);
function safePath(requestUrl) {
  const pathname = decodeURIComponent(new URL(requestUrl, "http://local").pathname);
  if (pathname.includes("\0") || pathname.includes("\\")) return null;
  const p = pathname === "/" ? "/index.html" : pathname;
  if (!topFiles.has(p) && !p.startsWith("/assets/") && !p.startsWith("/data/")) return null;
  const full = resolve(root, "." + p);
  const rel = relative(root, full);
  if (!rel || rel.startsWith(".." + sep) || rel === "..") return null;
  return full;
}
createServer(async (req, res) => {
  if (req.url?.split("?")[0] === "/health") {
    res.writeHead(200, {"content-type": "text/plain; charset=utf-8", "cache-control": "no-store"});
    res.end("ok");
    return;
  }
  if (!["GET", "HEAD"].includes(req.method || "")) {
    res.writeHead(405, {allow: "GET, HEAD"}); res.end(); return;
  }
  let path;
  try { path = safePath(req.url || "/"); } catch { path = null; }
  if (!path) { res.writeHead(404); res.end("Not found"); return; }
  try {
    const info = await stat(path);
    if (!info.isFile()) { res.writeHead(404); res.end("Not found"); return; }
    const mime = types[extname(path).toLowerCase()] || "application/octet-stream";
    const headers = {
      "content-type": mime,
      "cache-control": mime.includes("text/html") ? "no-store" : "public, max-age=120",
      "accept-ranges": "bytes",
      "x-content-type-options": "nosniff"
    };
    const match = /^bytes=(\d*)-(\d*)$/.exec(req.headers.range || "");
    let start = 0, end = Math.max(0, info.size - 1), status = 200;
    if (match && info.size > 0) {
      start = match[1] ? Number(match[1]) : Math.max(0, info.size - Number(match[2]));
      end = match[1] ? (match[2] ? Number(match[2]) : info.size - 1) : info.size - 1;
      if (!Number.isFinite(start) || !Number.isFinite(end) || start < 0 || start >= info.size || end < start) {
        res.writeHead(416, {"content-range": "bytes */" + info.size}); res.end(); return;
      }
      end = Math.min(end, info.size - 1);
      status = 206;
      headers["content-range"] = "bytes " + start + "-" + end + "/" + info.size;
    }
    headers["content-length"] = status === 206 ? end - start + 1 : info.size;
    res.writeHead(status, headers);
    if (req.method === "HEAD" || info.size === 0) { res.end(); return; }
    createReadStream(path, status === 206 ? {start, end} : {}).on("error", () => res.destroy()).pipe(res);
  } catch {
    res.writeHead(404, {"content-type": "text/plain; charset=utf-8"});
    res.end("Not found");
  }
}).listen(port, "0.0.0.0", () => console.log("Learn English preview listening on " + port));
