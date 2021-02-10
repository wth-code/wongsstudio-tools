from flask import request, render_template, flash
from urllib.parse import urlparse, parse_qs


def get_thumb():
    if request.method == "POST":
        url = request.form["url"]
        if extract_video_id(url):
            id = extract_video_id(url)
            img = f"https://i.ytimg.com/vi/{id}/maxresdefault.jpg"
            flash(img)
            return render_template("yt_thumb.html")
        else:
            flash("Type a YouTube Video URL !")
            return render_template("yt_thumb.html")
    else:
        return render_template("yt_thumb.html")


def extract_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com'}:
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
    # fail
    return False
