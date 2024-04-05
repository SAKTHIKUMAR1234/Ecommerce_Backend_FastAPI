import bcrypt

def gethashpwd(pwd):
  
  return (bcrypt.hashpw(bytes(pwd,'utf-8'),bcrypt.gensalt(rounds=12))).decode('utf-8')


def checkpwd(pwd:str,hpwd:str):
  
  return bcrypt.checkpw(hashed_password=hpwd.encode('utf-8'),password=pwd.encode('utf-8'))