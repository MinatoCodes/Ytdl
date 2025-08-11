import express from "express";
import { exec } from "child_process";
import util from "util";
import fs from "fs";
import path from "path";
import fetch from "node-fetch";

const app = express();
const execPromise = util.promisify(exec);

const YTDLP_PATH = path.join(process.cwd(), "yt-dlp");

// Download yt-dlp if not exists
async function ensureYtDlp() {
  if (!fs.existsSync(YTDLP_PATH)) {
    console.log("Downloading yt-dlp...");
    const res = await fetch("https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp");
    const fileStream = fs.createWriteStream(YTDLP_PATH, { mode: 0o755 });
    await new Promise((resolve, reject) => {
      res.body.pipe(fileStream);
      res.body.on("error", reject);
      fileStream.on("finish", resolve);
    });
    console.log("yt-dlp downloaded.");
  }
}

// Endpoint
app.get("/api/youtube", async (req, res) => {
  const url = req.query.url;
  if (!url) return res.json({ success: false, error: "No URL provided" });

  try {
    await ensureYtDlp();
    const { stdout } = await execPromise(`"${YTDLP_PATH}" -f best -g --no-warnings --no-check-certificate "${url}"`);
    const directUrl = stdout.trim();
    return res.json({
      success: true,
      creator: "MinatoCodes",
      platform: "youtube",
      download_url: directUrl
    });
  } catch (err) {
    return res.json({ success: false, error: err.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on ${PORT}`));
    
