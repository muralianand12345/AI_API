import uvicorn
from config import Config

if __name__ == '__main__':
    uvicorn.run(Config.API.module_path, host=Config.API.host, port=Config.API.port, reload=Config.API.reload)