from dotenv import load_dotenv

load_dotenv()

import os
import psycopg2

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
            print("Connector object is done")
            print(type(conn))
            return conn
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            return None


#if __name__ == "__main__":
 #   db = DbConn()
  #  conn = db.connect_to_database('db_employers')
  #  if conn:
  #      print("Успешное подключение!")
  #  else:
   #     print("Ошибка подключения!")