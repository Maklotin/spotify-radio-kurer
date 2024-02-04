# Install required libraries:
# pip install spotipy pygame python-mpd2

import time
import subprocess
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pygame

# Spotify credentials (replace with your own values)
SPOTIPY_CLIENT_ID = 'your_client_id'
SPOTIPY_CLIENT_SECRET = 'your_client_secret'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

# Set your NRK Radio stream URL
NRK_RADIO_URL = 'http://lyd.nrk.no/nrk_radio_p1_hordaland_mp3_h'

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope='user-library-read user-read-playback-state user-modify-playback-state'))

# Initialize pygame for displaying information
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)
pygame.display.set_caption('Music Player')

# Font for displaying information
font = pygame.font.Font(None, 36)

# Function to get current Spotify track information
def get_spotify_track_info():
    track = sp.current_playback()
    if track is not None and 'item' in track:
        return track['item']['name'], track['item']['artists'][0]['name'], track['item']['album']['name'], track['item']['duration_ms']
    else:
        return None, None, None, None

# Function to display information on the screen
def display_info(title, artist, album, duration):
    screen.fill((0, 0, 0))  # Clear the screen
    if title is not None:
        text = font.render(f"{title} - {artist} - {album} - {duration}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
    pygame.display.flip()

# Main loop
while True:
    # Check the current mode (you can replace this with your switch logic)
    mode = 1  # For now, assume 1 means Spotify, 2 means radio

    if mode == 1:  # Spotify mode
        title, artist, album, duration = get_spotify_track_info()
        display_info(title, artist, album, duration)
    elif mode == 2:  # Radio mode
        # You may need to adjust this based on your specific radio streaming method
        subprocess.run(['mpc', 'clear'])
        subprocess.run(['mpc', 'add', NRK_RADIO_URL])
        subprocess.run(['mpc', 'play'])
        title = 'NRK Radio'
        artist = ''
        album = ''
        duration = ''  # Radio streams don't have a fixed duration
        display_info(title, artist, album, duration)

    # Handle events (e.g., quitting the program)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    time.sleep(1)  # Adjust the sleep duration based on your needs
