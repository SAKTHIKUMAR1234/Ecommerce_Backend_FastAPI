import razorpay
from config.config import Config
import uuid

client = razorpay.Client(auth=(Config.RAZOR_PAY_ID,Config.RAZOR_PAY_SECRET))

def get_random_id():
  return uuid.uuid4().hex