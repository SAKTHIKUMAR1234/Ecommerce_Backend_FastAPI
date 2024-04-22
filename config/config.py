from dotenv import load_dotenv
import os

load_dotenv()

class Config:
  
  PORT = int(os.getenv('PORT'))
  RELOAD = bool(os.getenv('RELOAD'))
  DATABASE_URL = str(os.getenv('MYSQL_DB_URL'))
  JWT_TOKEN_TIME = os.getenv('JWT_ACCESS_TOKEN_EXPIRES')
  JWT_REFRESH_TIME = os.getenv('JWT_REFRESH_TOKEN_EXPIRES')
  JWT_ALGO = os.getenv('JWT_ALGO')
  JWT_SECRET = os.getenv('APP_JWT_SECRET')
  FIREBASE_CREDENTIAL_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH')
  RAZOR_PAY_ID = os.getenv('RAZOR_PAY_ID')
  RAZOR_PAY_SECRET = os.getenv('RAZOR_PAY_SECRET')