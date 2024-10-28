import os
import logging
from config import Config

def setup_logging():
    if not Config.Logging.enabled:
        return None
    
    os.makedirs(Config.Logging.log_folder, exist_ok=True)
    log_file_path = os.path.join(Config.Logging.log_folder, "app_log.log")
    
    logging.basicConfig(
        level=Config.Logging.log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info("Logging enabled")
    return logger

logger = setup_logging()