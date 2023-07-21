import base64
import requests
import sys
import zipfile
import pytube
import os
from moviepy.editor import AudioFileClip
from flask import Flask, render_template, request, jsonify, send_file, Response
from flask_cors import CORS
import socket

# Get the IP address of the computer


def get_internal_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except socket.error:
        return None

# Change the IP address in the HTML files


def change_ip_address(ip_address):
    with open('templates/main.html', 'r') as file:
        filedata = file.read()

    filedata = filedata.replace('your_ip_address', ip_address)

    with open('templates/main.html', 'w') as file:
        file.write(filedata)

    with open('templates/playlist.html', 'r') as file:
        filedata = file.read()

    filedata = filedata.replace('your_ip_address', ip_address)

    with open('templates/playlist.html', 'w') as file:
        file.write(filedata)


ip_address = get_internal_ip()
change_ip_address(ip_address)


app = Flask(__name__)
CORS(app, origins="*")

playlists = {}
youtube_api_key = "<Your_api_key>"
spotify_client_id = "<Your_api_key>"
spotify_client_secret = "<Your_api_key>"


@app.route('/')
def home():
    return render_template('main.html')

# Gets spotify playlist link and returns a list of track names


@app.route('/playlist_link', methods=['POST'])
def playlist_data():
    global spotify_client_id
    global spotify_client_secret
    link = request.form['playlist-link']
    playlist_id = link.split("/")[-1]

    if playlist_id not in playlists:
        access_token = get_access_token(
            spotify_client_id, spotify_client_secret)
        track_names = get_tracks(link, access_token)
        if len(track_names) != 0:
            playlists[playlist_id] = track_names
    else:
        track_names = playlists[playlist_id]

    return render_template('playlist.html', tracks=track_names)


@app.route('/playlist_link', methods=['GET'])
def get_playlist_data():
    list = []
    for playlist_id in playlists:
        list.append(playlists[playlist_id])
    return jsonify(list)

# Gets youtube video link and downloads it as mp3


@app.route('/download_playlist', methods=['POST'])
def download_playlist():
    selected_tracks = request.form.getlist('tracks')
    global youtube_api_key

    file_names = []
    for track_name in selected_tracks:
        video_url = get_youtube_link(track_name, youtube_api_key)
        filename = download_ytvid_as_mp3(video_url)
        file_names.append(filename)

    zip_filename = 'music.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in file_names:
            zipf.write(file, arcname=os.path.basename(file))

    response = send_file(zip_filename, as_attachment=True)

    for file in file_names:
        os.remove(file)
    os.remove(zip_filename)

    return response

# Gets token to access spotify API


def get_access_token(client_id, client_secret):
    message = f"{client_id}:{client_secret}"
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    headers = {
        "Authorization": f"Basic {base64_message}"
    }

    payload = {
        "grant_type": "client_credentials"
    }

    response = requests.post(
        "https://accounts.spotify.com/api/token", headers=headers, data=payload)
    response.raise_for_status()

    data = response.json()
    return data["access_token"]


def get_tracks(url, access_token):
    if 'album' in url:
        album_id = url.split('album/')[1].split('/')[0]
        return get_album_tracks(album_id, access_token)
    elif 'track' in url:
        track_id = url.split('track/')[1].split('/')[0]
        return [get_track(track_id, access_token)]
    elif 'playlist' in url:
        playlist_id = url.split('playlist/')[1].split('/')[0]
        return get_playlist_tracks(playlist_id, access_token)
    else:
        return None

# Gets tracks from an album


def get_album_tracks(album_id, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(
        f"https://api.spotify.com/v1/albums/{album_id}/tracks", headers=headers)
    response.raise_for_status()

    data = response.json()

    track_names = []

    for item in data['tracks']['items']:
        track_names.append(item["name"] + ' - ' +
                           item["artists"][0]["name"])

    return track_names

# Gets trackname


def get_track(track_id, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(
        f"https://api.spotify.com/v1/tracks/{track_id}", headers=headers)
    response.raise_for_status()

    data = response.json()

    track_name = data["name"] + ' - ' + data["artists"][0]["name"]

    return track_name

# Gets tracks from a playlist


def get_playlist_tracks(playlist_id, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers)
    response.raise_for_status()

    data = response.json()

    track_names = []

    for item in data['tracks']['items']:
        track_names.append(item["track"]["name"] + ' - ' +
                           item["track"]["artists"][0]["name"])

    return track_names

# Downloads youtube video as mp3


def download_ytvid_as_mp3(video_url):
    yt = pytube.YouTube(video_url)
    stream = yt.streams.filter(only_audio=True).first()
    filename = stream.download()
    print(f"Downloaded: {filename}")

    base, ext = os.path.splitext(filename)
    new_file = base + '.mp3'

    # Convert mp4 audio to mp3
    audio = AudioFileClip(filename)
    audio.write_audiofile(new_file)

    # Delete the original file
    os.remove(filename)

    return new_file

# Gets youtube video link from track name


def get_youtube_link(track_name, api_key):
    base_search_url = 'https://www.googleapis.com/youtube/v3/search'

    # Parâmetros para a pesquisa
    search_params = {
        'part': 'snippet',
        'q': track_name,
        'key': api_key,
        'maxResults': 1,
        'type': 'video'
    }

    response = requests.get(base_search_url, params=search_params)
    response.raise_for_status()

    data = response.json()
    video_id = data['items'][0]['id']['videoId']

    return f'https://www.youtube.com/watch?v={video_id}'


if __name__ == '__main__':
    app.run(host=f"{ip_address}", port=5000, debug=True)
