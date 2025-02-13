from sqlite3 import connect, OperationalError
from arquee.config import logs_folder, execution_id, logs_file
from os.path import join


class ServerDB:
    def __init__(self):
        self.db_path = join(logs_folder, "arquee.db")

        conn = connect(self.db_path)
        cursor = conn.cursor()
        query = """ 
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER,
            status TEXT DEFAULT 'RUNNING',
            timestamp DATETIME DEFAULT (datetime('now','localtime')),
            file_location TEXT)
        """

        cursor.execute(query)
        conn.commit()
        conn.close()

    def execute_query(self, query: str):
        conn = connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()

    def create_row(self):
        query = f"INSERT INTO history (id ,file_location) VALUES ({execution_id}, '{logs_file}')"
        self.execute_query(query)

    def failed_row(self):
        query = f"UPDATE history SET status = 'FAILED' WHERE id = {execution_id}"
        self.execute_query(query)

    def done_row(self):
        query = f"UPDATE history SET status = 'DONE' WHERE id = {execution_id} AND status != 'FAILED'"
        self.execute_query(query)
