const express = require("express");
const { execFile } = require("child_process");
const path = require("path");

const app = express();
const PORT = 3000;

app.get("/api/youtube", (req, res) => {
    const videoUrl = req.query.url;
    if (!videoUrl) return res.status(400).json({ error: "Missing 'url' query parameter" });

    const pythonScript = path.join(__dirname, "yt_fetch.py");

    execFile("python3", [pythonScript, videoUrl], (error, stdout) => {
        if (error) {
            return res.status(500).json({ error: error.message });
        }
        try {
            const data = JSON.parse(stdout);
            res.json(data);
        } catch (e) {
            res.status(500).json({ error: "Invalid response from Python script" });
        }
    });
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
  
