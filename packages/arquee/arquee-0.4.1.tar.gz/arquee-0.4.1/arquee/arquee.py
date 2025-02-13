from .db import DB
from os.path import join
from .config import base_folder
from .tools import create_folder, get_tables, create_spark_session
from .logger import logger
from py4j.protocol import Py4JJavaError
from .tools import server_db


class Arquee:
    def __init__(
        self,
        origin_db: str = "ORIGIN_DB",
        destiny_db: str = "DESTINY_DB",
        tables_file: str = "tables.txt",
    ):
        self.origin_db = DB(origin_db)
        self.destiny_db = DB(destiny_db)

        logger.info(f"{origin_db} connected successfully")
        logger.info(f"{destiny_db} connected successfully")

        self.datalake = join(base_folder, "data", "datalake")
        self.warehouse = join(base_folder, "data", "warehouse")

        create_folder(self.datalake)
        create_folder(self.warehouse)

        logger.info("Datalake folder created successfully")
        logger.info("Warehouse folder created successfully")

        self.tables = get_tables(tables_file)

        logger.info(f"{tables_file} processed successfully")

        self.spark = None  # Inicializamos en None para evitar problemas de referencia

    def create_datalake(self):
        self.spark = create_spark_session()  # Guardamos la sesión de Spark

        for table in self.tables:
            try:
                table_path = join(self.datalake, table)
                df = self.spark.read.jdbc(self.origin_db.url, table)
                df.write.parquet(table_path, mode="overwrite")
                logger.info(f"Table {table} loaded successfully on datalake")
            except Py4JJavaError as e:
                logger.error(
                    f"{table} does not exist in the database {self.origin_db.db_name}"
                )
                print(e)
                continue

    def close(self):
        if self.spark:
            self.spark.stop()
            logger.info("Spark session closed")
        server_db.done_row()
        logger.info("Arquee instance closed properly")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
