from flask import Flask, request, jsonify
import syncedlyrics
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)



def get_song_info(video_id):
    url = f"https://www.youtube.com/oembed?format=json&url=https%3A%2F%2Fmusic.youtube.com%2Fwatch%3Fv%3D{video_id}"
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
        title = data.get("title", "Unknown Title")
        uploader = data.get("author_name", "Unknown Uploader")
        # Remove "- Topic" if it exists
        if uploader.endswith(" - Topic"):
            uploader = uploader.replace(" - Topic", "")
        #print(f"Title: {title}")
        #print(f"Uploader: {uploader}")
        return title , uploader
    else:
        return (f"Failed to fetch data. Status code: {response.status_code}")


# Example usage


def getlyrics(Title, Artist):
    lrc = syncedlyrics.search(f"{Title} {Artist}")
    return lrc

def parse_lyrics(lrc):
    lyrics_dict = {}
    if lrc:
        for line in lrc.split('\n'):
            if line.strip():
                try:
                    timestamp, lyric = line.split(']', 1)
                    timestamp = timestamp[1:]  # Remove the opening bracket
                    lyrics_dict[timestamp] = lyric.strip()
                except ValueError:
                    continue  # Skip lines that don't match the expected format
    return lyrics_dict

@app.route('/lyrics', methods=['GET'])
def get_lyrics():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({"Responce":400,
                        "error": "Missing video_id parameter"}), 400

    try:
        title, artist = get_song_info(video_id)
        lrc = getlyrics(title, artist)
        lyrics_dict = parse_lyrics(lrc)

        if not lyrics_dict:
            return jsonify({"Responce": 404,
                            "error": "lyrics not found"}), 404

        response = {
            "Responce": 200,
            "lyrics": lyrics_dict
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 8000)
