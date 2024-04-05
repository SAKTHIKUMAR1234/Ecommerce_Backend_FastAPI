import jwt
from datetime import datetime,timedelta,UTC
from config.config import Config

class JWT:
  def get_jwt(subject,payload = None):
    jwt_claims = {
      'exp' : datetime.now(UTC) + timedelta(seconds=float(Config.JWT_TOKEN_TIME)),
      'sub' : subject,
      'iat' : datetime.now(UTC)
    }
    if payload is None : 
      payload = jwt_claims
    payload.update(jwt_claims)
    return jwt.encode(payload,Config.JWT_SECRET,algorithm=Config.JWT_ALGO)
  
  
  def get_jwt_refresh(subject,payload = None):
    jwt_claims = {
      'exp' : datetime.now(UTC) + timedelta(seconds=float(Config.JWT_REFRESH_TIME)),
      'sub' : subject,
      'iat' : datetime.now(UTC)
    }
    if payload is None : 
      payload = jwt_claims 
    payload.update(jwt_claims)
    return jwt.encode(payload,Config.JWT_SECRET,algorithm=Config.JWT_ALGO)
  
  def verify_jwt_token(token):
    try:
      payload = jwt.decode(token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGO],verify=True)
      return payload  
    except jwt.ExpiredSignatureError as e:
      return None
    except jwt.InvalidTokenError as e:
      return None
    except Exception as e:
      return None