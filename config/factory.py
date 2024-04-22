from fastapi import FastAPI
from routers import authrouter, vendorrouter, productsrouter, userrouter
from common import exception_handlers
from common.exceptions import CustomeException, InvalidDataException
from middleware.Authmiddleware import authmiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from services.firebaseconfig import initialize_firbase
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "http://localhost",
    "http://localhost:3000"
]


class CreateApp: 
  app = None
  
  def __init__(self) -> None:
    if self.app is None:
      self.app = FastAPI()
      self.app.exception_handler(CustomeException)(exception_handlers.handle_500)
      self.app.exception_handler(InvalidDataException)(exception_handlers.handle_validation_error)
      self.app.include_router(authrouter.authroute,prefix='/api')
      self.app.include_router(vendorrouter.vendorrouter,prefix='/api')
      self.app.include_router(productsrouter.products_router,prefix='/api')
      self.app.include_router(userrouter.user_router,prefix='/api')
      self.app.add_middleware(BaseHTTPMiddleware,dispatch = authmiddleware)
      self.app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
      )
      initialize_firbase()
      
      
          
  def getapp(self):
    return self.app