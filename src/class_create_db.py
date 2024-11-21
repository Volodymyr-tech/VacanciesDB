import logging
import os
import time

from config import LOGS_DIR
from src.class_connection_to_db import DbConn

log_file_path = os.path.join(LOGS_DIR, "create_db.log")

app_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
app_logger.addHandler(file_handler)
app_logger.setLevel(logging.DEBUG)


class CreateDb:

    def _create_database(self, database_name: str):
        """Функция для создания базы данных."""
        conn = DbConn().connect_to_database()  # Подключаемся к стандартной базе
        app_logger.info("Подключено к стандартной базе данных 'postgres'.")
        if conn is None:
            app_logger.warning("Ошибка подключения к базе данных 'postgres'. Проверьте параметры подключения.")
            return

        conn.autocommit = True

        with conn.cursor() as cur:
            try:
                # Удаляем базу, если она уже существует
                cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
                # Создаём новую базу данных
                cur.execute(f"CREATE DATABASE {database_name}")
                app_logger.info(f"База данных '{database_name}' успешно создана.")
                print(f"База данных '{database_name}' успешно создана.")
            except Exception as e:
                app_logger.error(f"Ошибка при создании базы данных '{database_name}': {e}")
                print(f"Ошибка при создании базы данных '{database_name}': {e}")
                return
            finally:
                conn.close()
                app_logger.info(f"Подключение к '{database_name}' закрыто ")

        # Ожидаем некоторое время, чтобы база была готова
        time.sleep(5)

    def _create_tables(self, database_name: str):
        """Функция для создания таблиц в указанной базе данных."""
        time.sleep(5)

        conn = DbConn().connect_to_database(database_name)
        app_logger.info(f"Успешное  подключение к БД '{database_name}'")

        try:
            # Создание таблиц
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE employers (
                        employer_id varchar PRIMARY KEY,
                        employer_name varchar NOT NULL,
                        site_url varchar,
                        alternate_url varchar,
                        open_vacancies varchar,
                        address varchar
                    );
                """
                )
                cur.execute(
                    """
                    CREATE TABLE vacancies (
                        vacancy_name varchar,
                        vacancy_url VARCHAR,
                        salary INTEGER,
                        requirement VARCHAR,
                        employer_id varchar REFERENCES employers(employer_id)
                    );
                """
                )
            conn.commit()
            app_logger.info(f"Созданы таблицы в БД '{database_name}'")
            print("Таблицы успешно созданы.")
        except Exception as e:
            app_logger.error(f"Ошибка при создании таблиц: {e}")
            print(f"Ошибка при создании таблиц: {e}")
        finally:
            conn.close()
            app_logger.info(f"Подключение к '{database_name}' закрыто ")

