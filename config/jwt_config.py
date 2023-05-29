import jwt as pyjwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from config.env import secret

class AuthHandler():

    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = secret

    def encode_token(self, uuid):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=180),
            'iat': datetime.utcnow(),
            'sub': uuid
        }
        return pyjwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        try:
            payload = pyjwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except pyjwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except pyjwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)