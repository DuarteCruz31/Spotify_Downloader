# Spotify Playlist Downloader

This is a web-based Spotify Playlist Downloader. It provides an interface for downloading songs from a Spotify playlist link. It uses the Spotify API to get the playlist information and the Youtube Data API to search for the songs on Youtube. The Youtube Data API is used to get the video ID of the songs and the Youtube DL library is used to download the songs.

Please note that this application is for educational purposes only. I do not condone the use of this application for piracy.

## How to Use

1. Navigate to the web page.
2. Insert the Spotify playlist link into the provided input field.
3. Click 'Submit'. You will be redirected to a new page displaying all tracks on the playlist.
4. You can select the tracks you want to download or use the 'Select All' checkbox.
5. Click the 'Download' button to start the download process.

## Requirements

This application is built using Python 3, Flask, requests library, Pytube and Moviepy. 

- [Python 3](https://www.python.org/downloads/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Requests](https://docs.python-requests.org/en/latest/)
- [Pytube](https://python-pytube.readthedocs.io/en/latest/)
- [Moviepy](https://zulko.github.io/moviepy/)

You will also need a Spotify Developer account to use the Spotify API.

- [Spotify Developer](https://developer.spotify.com/dashboard/login)

You will also need a Google Developer account to use the Youtube Data API.

- [Google Developer](https://console.developers.google.com/)

## Setup
Enter virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

To install the dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Installation

To run this application, first clone the repository:

```bash
git clone https://github.com/yourusername/Spotify_Downloader.git
```

Change the directory to the project directory:

```bash
cd Spotify_Downloader
```

In the `spotifydownloader.py` file, replace the `spotify_client_id` and `spotify_client_secret` with your own Spotify API credentials. Replace the `youtube_api_key` with your own Youtube Data API key.

```python
client_id = 'your_client_id'
clinet_secret = 'your_client_secret'
youtube_api_key = 'your_api_key'
```

To run the application, run the following command:

```bash
python spotifydownloader.py
```

Access the application at `http://<Your_ip_Address>:5000/`
You might be able to see your access link in the terminal.