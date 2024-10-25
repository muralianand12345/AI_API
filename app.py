import uvicorn
from config import Config

if __name__ == '__main__':
    uvicorn.run(Config.API.app_name, host=Config.API.host, port=Config.API.port)