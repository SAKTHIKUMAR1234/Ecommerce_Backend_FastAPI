from starlette.requests import Request
from starlette.responses import Response
from common import response
from http import HTTPStatus
from models import ActivityModel, RoleEnum, VendorModel, VendorStatus
from utils.jwt import JWT
from services.database import SessionLocal
from services.securityconfig import set_current_user

open_paths = [
  '/api/auth/login',
  '/api/auth/signup',
  '/docs',
  '/openapi.json'
]

vendor_user_open_paths = [
  '/api/vendor/request'
]

async def authmiddleware(req : Request ,  call_next):
  
  api_path = req.url.path
  if api_path not in open_paths:
    if 'Authorization' not in req.headers:
      return response.response_sender(data=None,message='Invalid Credentials',http=HTTPStatus.FORBIDDEN)
    token = req.headers['Authorization']
    data = JWT.verify_jwt_token(token=token)
    if data is None:
      return response.response_sender(data=None,message='Invalid Credentials',http=HTTPStatus.FORBIDDEN)
    session = SessionLocal()
    activity = session.query(ActivityModel).filter(ActivityModel.session_id == data['sub']).first()
    if activity.logout_at != None:
      session.close()
      return response.response_sender(data=None,message='Invalid Credentials',http=HTTPStatus.FORBIDDEN)
    set_current_user(activity)
    if not activity.user.isdev :
      if '/admin/' in api_path and activity.user.role != RoleEnum.admin:
        session.close()
        return response.response_sender(data=None,message='Invalid Credentials',http=HTTPStatus.FORBIDDEN)
      if '/vendor/' in api_path and api_path not in vendor_user_open_paths and (activity.user.role == RoleEnum.admin.value or session.query(VendorModel).filter(VendorModel.user == activity.user,VendorModel.status == VendorStatus.accepted.value).first() == None):
        session.close()
        return response.response_sender(data=None,message='Invalid Credentials',http=HTTPStatus.FORBIDDEN)
    session.close()
    res : Response = await call_next(req)
    return res
  else:
    return await call_next(req)