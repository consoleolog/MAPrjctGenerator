import os

from ioc_container import IocContainer
from logger import LoggerFactory
from service.data_service import DataService

container = IocContainer()
container.compose()
data_service = container.get(DataService)

data_dir = os.getcwd() + "/data"

logger = LoggerFactory().get_logger("processing", "MindApply")

for i, fn in enumerate(os.listdir(data_dir), 1):
    logger.info(f"Step:{i}\nFilename:{fn}")
    try:
        data_service.extract_key_value(data_dir+"/"+fn)
    except Exception as e:
        logger.error(e)