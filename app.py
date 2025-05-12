from flask import Flask, jsonify, render_template, request
import json
import requests

app = Flask(__name__)

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tracks')
def get_tracks():
    return jsonify(load_data('data/tracks.json'))

@app.route('/albums')
def get_albums():
    return jsonify(load_data('data/albums.json'))

@app.route('/albums/<int:album_id>')
def get_album_tracks(album_id):
    all_tracks = load_data('data/tracks.json')
    album_tracks = [t for t in all_tracks if t['album_id'] == album_id]
    return jsonify(album_tracks)

@app.route('/album')
def album_page():
    album_id = request.args.get('id')
    return render_template('album.html', album_id=album_id)

@app.route('/deezer/search')
def deezer_search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Missing query"}), 400

    url = f'https://api.deezer.com/search?q={query}'
    res = requests.get(url)
    return jsonify(res.json())


if __name__ == '__main__':
    app.run(debug=True)
