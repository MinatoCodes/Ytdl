import json
from pytube import YouTube

def handler(request, response):
    url = request.args.get("url")
    if not url:
        return response.status(400).json({
            "success": False,
            "error": "Missing 'url' query parameter"
        })

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension="mp4") \
                           .order_by("resolution").desc().first()

        if not stream:
            return response.status(404).json({
                "success": False,
                "error": "No suitable stream found"
            })

        data = {
            "success": True,
            "creator": "MinatoCodes",
            "platform": "youtube",
            "download_url": stream.url
        }
        return response.status(200).json(data)

    except Exception as e:
        return response.status(500).json({
            "success": False,
            "error": str(e)
        })
        
