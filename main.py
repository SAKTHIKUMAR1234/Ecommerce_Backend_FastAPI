import uvicorn
from config.config import Config

if __name__ == '__main__':
  uvicorn.run('app.app:app',port=Config.PORT,reload=Config.RELOAD)