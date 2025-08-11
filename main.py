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
        # Let yt-dlp choose best available formats (no -f best to avoid warning)
        result = subprocess.run(
            ["yt-dlp", "--dump-json", "--no-warnings", "--geo-bypass", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            return jsonify({"success": False, "error": result.stderr.strip()})

        # Only use the last JSON line in case there are multiple
        last_line = result.stdout.strip().split("\n")[-1]
        info = json.loads(last_line)

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
                       
