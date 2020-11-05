import os

import requests
from flask import request, jsonify
from flask_restful import Resource

from app.spotify_api import get_auth_header
from app.common.error_handling import AppErrorBaseClass
from app.datascience.api.etl import get_albums


class AlbumListResource(Resource):
    def post(self):
        result = []
        header = get_auth_header()
        r = requests.get('https://api.spotify.com/v1/browse/new-releases', headers=header)
        if r.status_code == 401:
            header = get_auth_header()
            r = requests.get('https://api.spotify.com/v1/browse/new-releases', headers=header)
        if r.status_code == 200:
            try:
                data = r.json()['albums']['items']
                result = get_albums(data)
                while r.json()['albums']['next']:
                    header = get_auth_header()
                    r = requests.get(r.json()['albums']['next'], headers=header)
                    data = r.json()['albums']['items']
                    result.extend(get_albums(data))
                back_response = requests.post('https://mastersound-backend.azurewebsites.net/api/albums/new-releases', json=result)
                if back_response.status_code == 201:
                    return {'msg': 'Success.'}, 201
                else:
                    raise AppErrorBaseClass('There was an error sending the json to the backend API.')
            except Exception as e:
                print(e)
                raise AppErrorBaseClass(f'There was an error fetching the albums. Error: {e}')
        else:
            return jsonify({'msg': f'Could not get the albums. Try again. Code: {r.status_code}'})

