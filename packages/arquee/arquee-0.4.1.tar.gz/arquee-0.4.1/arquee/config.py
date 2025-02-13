from os.path import join
from dotenv import load_dotenv
from time import time


load_dotenv()

execution_id = round(time())
base_folder = "arquee"
logs_folder = join(base_folder, "logs")
logs_file = join(logs_folder, f"{execution_id}.log")

