from flask import Flask, render_template, request, send_file
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR
import json
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            downloader = YoutubeCommentDownloader()
            try:
                # Fetch comments using the downloader
                comments_generator = downloader.get_comments_from_url(url, sort_by=SORT_BY_POPULAR)
                
                # Convert the generator to a list
                comments_list = list(comments_generator)
                
                # Convert the list to JSON
                comments_json = json.dumps(comments_list, indent=4)
                
                # Create an in-memory file
                return send_file(
                    io.BytesIO(comments_json.encode('utf-8')),
                    as_attachment=True,
                    download_name='comments.json',
                    mimetype='application/json'
                )
            except Exception as e:
                return f"An error occurred: {str(e)}"
    return '''
        <!doctype html>
        <title>YouTube Comment Downloader</title>
        <h1>Enter YouTube Video URL</h1>
        <form method=post>
          <input type=text name=url placeholder="https://www.youtube.com/watch?v=...">
          <input type=submit value=Submit>
        </form>
    '''

if __name__ == '__main__':
    app.run()
