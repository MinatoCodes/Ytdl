import sys
import json
from pytube import YouTube

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Missing URL"}))
        return
    
    url = sys.argv[1]
    
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
        if not stream:
            print(json.dumps({"error": "No suitable stream found"}))
            return
        
        result = {
            "success"="true",
            "creator"="MinatoCodes",
            "title": yt.title,
            "length": yt.length,
            "views": yt.views,
            "download_url": stream.url
        }
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
  
