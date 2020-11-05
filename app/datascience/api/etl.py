import requests
from datetime import timedelta

from app.spotify_api import get_auth_header


def get_albums(data):
    result = []
    for item in data:
        skip = False
        header = get_auth_header()
        songs_r = requests.get(f'https://api.spotify.com/v1/albums/{item["id"]}/tracks', headers=header)
        if songs_r.status_code == 200:
            if not songs_r.json()['items'][0]['preview_url']:
                continue
            else:
                songs = []
                counter = 1
                for song in songs_r.json()['items']:
                    sound_url = song['preview_url']
                    if not sound_url:
                        skip = True
                        break;
                    song_name = song['name']
                    spt_song_id = song['id']
                    order_number = counter
                    counter += 1
                    duration = str(timedelta(milliseconds=song['duration_ms']))[2:7]
                    songs.append({
                        'spt_song_id': spt_song_id,
                        'song_name': song_name,
                        'order_number': order_number,
                        'duration': duration,
                        'sound_url': sound_url
                        })

        if skip:
            continue
        spt_album_id = item['id']
        cover_image_url = item['images'][0]['url']
        album_name = item['name']
        artists = []
        for artist in item['artists']:
            r_artist = requests.get(artist['href'], headers=header)
            if r_artist.status_code == 200:
                artist_cover_img_url = r_artist.json()['images'][0]['url']
                spt_artist_id = artist['id']
                artist_name = artist['name']
            else:
                print(f'There was an error fetching {artist["name"]}\'s image.')
                continue
            artists.append({
                'spt_artist_id': spt_artist_id,
                'artist_name': artist_name,
                'cover_image_url': artist_cover_img_url
               })
        result.append({
           'spt_album_id': spt_album_id,
           'cover_image_url': cover_image_url,
           'album_name': album_name,
           'artists': artists,
           'songs': songs
           })
    return result

