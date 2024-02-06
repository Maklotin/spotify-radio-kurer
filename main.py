# Install required libraries:
# pip install spotipy pygame python-mpd2

import time
import subprocess
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pygame
from dotenv import load_dotenv
import os
import requests
import io

load_dotenv()


NRK_RADIO_URL = 'https://radio.nrk.no/direkte/jazz'


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
                                               client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"),
                                               redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI"),
                                               scope='user-library-read user-read-playback-state user-modify-playback-state'))

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((2560, 1440), pygame.FULLSCREEN)
pygame.display.set_caption('Music Player')


font = pygame.font.Font(None, 36)

def get_spotify_track_info():
    track = sp.current_playback()
    if track is not None and 'item' in track:
        album_cover_url = track['item']['album']['images'][0]['url'] if track['item']['album']['images'] else None
        artist_id = track['item']['artists'][0]['id']
        artist_info = sp.artist(artist_id)
        artist_image_url = artist_info['images'][0]['url'] if artist_info['images'] else None
        progress_ms = track['progress_ms']
        return track['item']['name'], track['item']['artists'][0]['name'], track['item']['album']['name'], track['item']['duration_ms'], album_cover_url, progress_ms, artist_image_url
    else:
        return None, None, None, None, None, None, None

def display_info(title, artist, album, duration, album_cover_url, progress, artist_image_url):
    screen.fill((0, 0, 0))  # Clear the screen
    if title is not None:
        text = font.render(f"{title} - {artist} - {album} - {ms_to_min_sec(progress)} / {ms_to_min_sec(duration)}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        
        if album_cover_url is not None:
            response = requests.get(album_cover_url)
            image_file = io.BytesIO(response.content)
            album_image_surface = pygame.image.load(image_file)
            screen.blit(album_image_surface, (10, 50))  # Adjust the position based on your needs

        if artist_image_url is not None:
            response = requests.get(artist_image_url)
            image_file = io.BytesIO(response.content)
            artist_image_surface = pygame.image.load(image_file)
            screen.blit(artist_image_surface, (10, 300))  # Adjust the position based on your needs

    pygame.display.flip()

def ms_to_min_sec(ms):
    # Convert from milliseconds to seconds
    total_seconds = ms // 1000
    # Use divmod to get minutes and seconds
    minutes, seconds = divmod(total_seconds, 60)
    # Return as a string in the format 'minutes:seconds'
    return f"{minutes}:{seconds:02}"

# Main loop
while True:

    # 1 = Spotify, 2 = NRK Radio
    mode = 1

    if mode == 1:  # Spotify mode
        title, artist, album, duration, album_cover_url, progress, artist_image_url = get_spotify_track_info()
        display_info(title, artist, album, duration, album_cover_url, progress, artist_image_url)
    elif mode == 2:  # Radio mode
        # You may need to adjust this based on your specific radio streaming method
        subprocess.run(['mpc', 'clear'])
        subprocess.run(['mpc', 'add', NRK_RADIO_URL])
        subprocess.run(['mpc', 'play'])
        title = 'NRK Radio'
        artist = ''
        album = ''
        duration = ''  # Radio streams don't have a fixed duration
        album_cover_url = None  # Radio streams don't have an album cover
        display_info(title, artist, album, duration, album_cover_url)

    # Handle events (e.g., quitting the program)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    time.sleep(1)  # Adjust the sleep duration based on your needs