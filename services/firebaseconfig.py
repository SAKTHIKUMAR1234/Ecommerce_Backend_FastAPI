from firebase_admin import credentials
import firebase_admin.storage
from config.config import Config
import firebase_admin

def initialize_firbase():
  cred = credentials.Certificate(Config.FIREBASE_CREDENTIAL_PATH)
  firebase_admin.initialize_app(cred, {
    'storageBucket': 'ecommercefastapifilestorage.appspot.com'
  })
  
def get_storage_bucket():
  return firebase_admin.storage.bucket()  