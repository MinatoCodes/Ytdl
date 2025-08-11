import json
from pytube import YouTube

def handler(event, context):
    # Get query parameters
    params = event.get("queryStringParameters") or {}
    url = params.get("url")

    if not url:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "success": False,
                "error": "Missing 'url' query parameter"
            })
        }

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension="mp4") \
                           .order_by("resolution").desc().first()

        if not stream:
            return {
                "statusCode": 404,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "success": False,
                    "error": "No suitable stream found"
                })
            }

        result = {
            "success": True,
            "creator": "MinatoCodes",
            "platform": "youtube",
            "download_url": stream.url
        }

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "success": False,
                "error": str(e)
            })
            }
        
