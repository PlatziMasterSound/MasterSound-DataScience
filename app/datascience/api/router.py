from flask import request, Blueprint
from flask_restful import Api

from app.datascience.api.resources.album_resource import AlbumListResource

datascience_api_bp = Blueprint('datascience_api_bp', __name__)

api = Api(datascience_api_bp)

# Add resources here
api.add_resource(AlbumListResource, '/api/albums/new-releases', endpoint='album_list_resource')

