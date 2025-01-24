import os

from app_factory import AppFactory
from logger import LoggerFactory

app_factory = AppFactory()
data_service = app_factory.data_service

data_dir = os.getcwd() + "/data"

logger = LoggerFactory().get_logger("processing", "MindApply")

for i, fn in enumerate(os.listdir(data_dir), 1):
    logger.info(f"Step:{i}\nFilename:{fn}")
    try:
        data_service.extract_key_value(data_dir+"/"+fn)
    except Exception as e:
        logger.error(e)