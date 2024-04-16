from fastapi import APIRouter
from schemas.signup import Signup
from schemas.login import Login
from common.exceptions import CustomeException
from services.database import SessionLocal
from models import UsersModel,CartModel,ActivityModel
from common import response
from http import HTTPStatus
from utils.hashing import gethashpwd,checkpwd
from utils.uuid_generator import get_random_id
from utils.jwt import JWT
from fastapi import Request
import datetime


authroute = APIRouter(prefix='/auth')

@authroute.post('/signup')
def usersignup(signup : Signup):
  try:
    session = SessionLocal()
    session.begin()
    exist_user =  session.query(UsersModel).filter(UsersModel.email == signup.email).first()
    if exist_user is not None:
      session.rollback()
      session.close()
      return response.response_sender(data=None,message='Data Already Exists',http=HTTPStatus.CONFLICT)
    user = UsersModel()
    user.email = signup.email
    user.first_name = signup.first_name
    user.last_name  = signup.last_name
    user.password = gethashpwd(signup.password)
    user_cart = CartModel()
    session.add(user)
    session.commit()
    user_cart.user = user
    session.add(user_cart)
    session.commit()
    session.close()
    return response.response_sender(data=None,message='CREATED',http=HTTPStatus.CREATED)
    
  except Exception as e:
    session.rollback()
    session.close()
    raise CustomeException("OOP'S SOMETHNIG WENT WRONG")
  
  
@authroute.post('/login')
def user_login(login:Login):
  try:
    session = SessionLocal()
    session.begin()
    user = session.query(UsersModel).filter(UsersModel.email == login.email).first()
    if user is None:
      response_body = {'email':login.email}
      session.close()
      return response.response_sender(data=response_body,message='NOT FOUND',http=HTTPStatus.NOT_FOUND)
    
    if checkpwd(pwd=login.password,hpwd=user.password):
      activity = ActivityModel()
      activity.session_id = get_random_id()
      activity.user = user
      session.add(activity)
      response_body = {
        'auth_token' : JWT.get_jwt(subject=activity.session_id),
        'refresh_token' : JWT.get_jwt_refresh(subject=activity.session_id)
      }
      session.commit()
      session.close()
      return response.response_sender(data = response_body, message='OK', http=HTTPStatus.OK)
    else:
      session.close()
      return response.response_sender(data=None,message='INVALID PASSWORD',http=HTTPStatus.FORBIDDEN)
  except Exception as e:
    print(e)
    session.rollback()
    session.close()
    raise CustomeException("OOP'S SOMETHNIG WENT WRONG")
  
  
@authroute.get('/refresh')
def refresh_token(request:Request):
  try:
    data = JWT.verify_jwt_token(request.headers['Authorization'])
    additional_payload = {
      'extended' : True
    }
    response_body = {
        'auth_token' : JWT.get_jwt(subject=data['sub'],payload=additional_payload),
        'refresh_token' : JWT.get_jwt_refresh(subject=data['sub'],payload=additional_payload)
    }
    return response.response_sender(data = response_body, message='OK', http=HTTPStatus.OK)
  except Exception as e:
    raise CustomeException("OOP'S SOMETHNIG WENT WRONG")
  
@authroute.get('/logout')
def logout(request : Request):
  
  try:
    session = SessionLocal()
    session.begin()
    data = JWT.verify_jwt_token(request.headers['Authorization'])
    activity = session.query(ActivityModel).filter(ActivityModel.session_id == data['sub']).first()
    activity.logout_at = datetime.datetime.now()
    session.add(activity)
    session.commit()
    session.close()
    return response.response_sender(data = None, message='OK', http=HTTPStatus.OK)
  except Exception as e:
    session.rollback()
    session.close()
    raise CustomeException("OOP'S SOMETHNIG WENT WRONG")