import subprocess
import sys
from os.path import exists, normpath, join
from os import sep


def start_server():
    print(sys.executable)
    cmd = [
        sys.executable,
        "-m",
        "waitress",
        "serve",
        "arquee.server.web_server:app",
    ]

    with open("server.log", "wb"):
        subprocess.Popen(cmd)

    print("Servidor iniciado en segundo plano en el puerto 8000.")


def create_files():
    origin_example = 'ORIGIN_DB={"host": "host", "port":1433 , "user": "user", "pwd": "password", "db_name": "some_db"}\n'
    destiny_example = 'DESTINY_DB={"host": "host", "port":1433 , "user": "user", "pwd": "password", "db_name": "some_db"}\n'

    if not exists(".env"):
        with open(".env", "a") as file:
            file.write(origin_example)
            file.write(destiny_example)
            print("File .env created successfully")

    if not exists("tables.txt"):
        with open("tables.txt", "a") as file:
            file.write(
                "Here you can specify the tables for create the datalake, delete this line :)"
            )
            print("File tables.txt created successfully")


if __name__ == "__main__":
    create_files()
