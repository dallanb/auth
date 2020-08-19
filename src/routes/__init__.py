from .. import api
from .v1 import PingAPI

# Ping
api.add_resource(PingAPI, '/ping', methods=['GET'])
