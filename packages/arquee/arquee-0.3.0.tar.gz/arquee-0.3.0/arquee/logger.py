from os import makedirs
import logging
from .config import logs_folder, logs_file


try:
    makedirs(logs_folder)
except Exception:
    pass

FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=logs_file, level=logging.INFO, format=FORMAT)
logger = logging.getLogger()
