from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route("/api/youtube")
def youtube_dl():
    url = request.args.get("url")
    if not url:
        return jsonify({"success": False, "error": "No URL provided"}), 400

    try:
        # Run yt-dlp to get video info (best quality direct URL)
        result = subprocess.run(
            ["yt-dlp", "-f", "best", "--dump-json", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            return jsonify({"success": False, "error": result.stderr.strip()})

        info = json.loads(result.stdout)
        return jsonify({
            "success": True,
            "creator": "MinatoCodes",
            "platform": "youtube",
            "download_url": info.get("url")
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
        
