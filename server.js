import express from "express";
import { exec } from "child_process";
import util from "util";

const app = express();
const execPromise = util.promisify(exec);

app.get("/api/youtube", async (req, res) => {
    const videoUrl = req.query.url;
    if (!videoUrl) {
        return res.status(400).json({ success: false, error: "No URL provided" });
    }

    try {
        // yt-dlp command to get best format direct URL
        const { stdout } = await execPromise(
            `yt-dlp -f best -g "${videoUrl}"`
        );

        const downloadUrl = stdout.trim();

        return res.json({
            success: true,
            creator: "MinatoCodes",
            platform: "youtube",
            download_url: downloadUrl
        });
    } catch (error) {
        return res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
            
