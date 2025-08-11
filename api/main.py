from flask import Flask, request, jsonify
from pytube import YouTube

app = Flask(__name__)

@app.route("/api/youtube")
def youtube_dl():
    url = request.args.get("url")
    if not url:
        return jsonify({
            "success": False,
            "error": "Missing 'url' query parameter"
        }), 400

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension="mp4") \
                           .order_by("resolution").desc().first()

        if not stream:
            return jsonify({
                "success": False,
                "error": "No suitable stream found"
            }), 404

        return jsonify({
            "success": True,
            "creator": "MinatoCodes",
            "platform": "youtube",
            "download_url": stream.url
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
            
