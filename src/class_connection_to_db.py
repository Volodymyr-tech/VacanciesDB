from dotenv import load_dotenv
load_dotenv()
import os
import psycopg2
import logging
from config import LOGS_DIR

log_file_path = os.path.join(LOGS_DIR, "conn_db.log")

app_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
app_logger.addHandler(file_handler)
app_logger.setLevel(logging.DEBUG)





class DbConn:

    def __init__(self):
        self.__host = os.getenv("DB_HOST")
        self.__user = os.getenv("DB_USER")
        self.__password = os.getenv("DB_PASSWORD")
        self.__port = os.getenv('DB_PORT')


    def connect_to_database(self, database_name="postgres"):
        """Создает подключение к базе данных."""
        try:
            conn = psycopg2.connect(
                host=self.__host,
                dbname=database_name,
                user=self.__user,
                password=self.__password,
                port=self.__port
            )
            app_logger.info(f"Connector object for user {self.__user} is done")
            return conn
        except psycopg2.Error as e:
            app_logger.error(f"Error connecting to database: {e}")
            return None


#if __name__ == "__main__":
 #   db = DbConn()
  #  conn = db.connect_to_database('db_employers')
  #  if conn:
  #      print("Успешное подключение!")
  #  else:
   #     print("Ошибка подключения!")