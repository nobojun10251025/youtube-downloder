from flask import Flask, request, render_template_string
import yt_dlp

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>YouTubeアプリ</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body {
            font-family: Arial;
            background: #0f0f0f;
            color: white;
            text-align: center;
            margin: 0;
        }

        h1 {
            padding: 10px;
        }

        form {
            margin: 10px;
        }

        input {
            width: 80%;
            padding: 10px;
            border-radius: 10px;
            border: none;
            font-size: 16px;
        }

        button {
            padding: 10px 20px;
            border-radius: 10px;
            border: none;
            background: red;
            color: white;
            font-size: 16px;
            margin-top: 10px;
        }

        .video {
            margin: 15px;
            background: #1f1f1f;
            padding: 10px;
            border-radius: 10px;
        }

        img {
            width: 100%;
            border-radius: 10px;
        }

        iframe {
            width: 100%;
            height: 220px;
            border-radius: 10px;
        }
    </style>
</head>

<body>

<h1>YouTube Webアプリ</h1>

<form method="POST">
    <input type="text" name="input" placeholder="URL or 検索ワード">
    <br>
    <button type="submit">実行</button>
</form>

{% if video_id %}
    <h2>再生中</h2>
    <iframe src="https://www.youtube.com/embed/{{ video_id }}" allowfullscreen></iframe>
{% endif %}

{% if videos %}
    <h2>検索結果</h2>
    {% for v in videos %}
        <div class="video">
            <p>{{ v.title }}</p>
            <img src="{{ v.thumbnail }}">
            <br><br>
            <a href="/watch?v={{ v.id }}">
                <button>再生</button>
            </a>
        </div>
    {% endfor %}
{% endif %}

</body>
</html>
"""

PLAYER_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
    background: black;
    color: white;
    text-align: center;
}
iframe {
    width: 100%;
    height: 250px;
}
button {
    padding: 10px;
    margin-top: 20px;
}
</style>
</head>

<body>

<h2>動画再生</h2>

<iframe src="https://www.youtube.com/embed/{{ video_id }}" allowfullscreen></iframe>

<br>
<a href="/"><button>戻る</button></a>

</body>
</html>
"""

def get_video_id(text):
    if "youtube.com/watch?v=" in text:
        return text.split("v=")[1].split("&")[0]
    if "youtu.be/" in text:
        return text.split("youtu.be/")[1]
    return None

@app.route("/", methods=["GET", "POST"])
def home():
    videos = None
    video_id = None

    if request.method == "POST":
        text = request.form["input"]

        # URLなら再生
        video_id = get_video_id(text)

        if not video_id:
            # 検索
            ydl_opts = {'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(f"ytsearch5:{text}", download=False)

                videos = []
                for e in result["entries"]:
                    videos.append({
                        "title": e.get("title"),
                        "thumbnail": e.get("thumbnail"),
                        "id": e.get("id")
                    })

    return render_template_string(HTML, videos=videos, video_id=video_id)

@app.route("/watch")
def watch():
    vid = request.args.get("v")
    return render_template_string(PLAYER_HTML, video_id=vid)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
