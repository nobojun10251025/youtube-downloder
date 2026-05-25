from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Player</title>
</head>
<body>
    <h1>YouTube再生サイト</h1>

    <form method="POST">
        <input type="text" name="url" placeholder="YouTube URL">
        <button type="submit">再生</button>
    </form>

    {% if video_id %}
        <h2>再生中</h2>
        <iframe width="560" height="315"
        src="https://www.youtube.com/embed/{{ video_id }}"
        frameborder="0"
        allowfullscreen></iframe>
    {% endif %}

</body>
</html>
"""

def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1]
    return None

@app.route("/", methods=["GET", "POST"])
def home():
    video_id = None

    if request.method == "POST":
        url = request.form["url"]
        video_id = get_video_id(url)

    return render_template_string(HTML, video_id=video_id)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
