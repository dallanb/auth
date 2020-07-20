from .. import api
from .v1 import Login, Logout, Ping, Register, Status

api.add_resource(Login, '/login', methods=['POST'])
api.add_resource(Logout, '/logout', methods=['POST'])
api.add_resource(Ping, '/ping', methods=['GET'])
api.add_resource(Register, '/register', methods=['POST'])
api.add_resource(Status, '/status', methods=['GET'])
