from os.path import exists
from os import makedirs
from shutil import rmtree
from pyspark.sql import SparkSession
from .logger import logger
from .server.server_db import ServerDB


server_db = ServerDB()
server_db.create_row()


def arquee_error(message: str):
    logger.error(message)
    print("ERROR, EXITED")
    server_db.failed_row()
    exit(1)


def create_folder(folder_name: str):
    try:
        if exists(folder_name):
            rmtree(folder_name)
            makedirs(folder_name)
        else:
            makedirs(folder_name)

    except Exception as e:
        print("e")
        arquee_error(e)


def get_tables(tables_file: str) -> list[str]:
    try:
        with open(tables_file, "r") as file:
            tables = file.readlines()
            return [table.strip() for table in tables]
    except FileNotFoundError:
        arquee_error(f"File {tables_file} not found")


def create_spark_session() -> SparkSession:
    spark: SparkSession = (
        SparkSession.builder.appName("ETL")
        .master("local[*]")
        .config("spark.executor.memory", "4g")
        .config("spark.sql.parquet.int96RebaseModeInWrite", "CORRECTED")
        .getOrCreate()
    )
    return spark
