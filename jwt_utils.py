from extensions import jwt
from models.users_model import TokenBlocklist

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    from models.users_model import User
    identity = jwt_data["sub"]
    return User.query.get(identity)