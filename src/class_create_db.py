import time
from src.class_connection_to_db import DbConn


class CreateDb:

    def _create_database(self, database_name: str):
        """Функция для создания базы данных."""
        conn = DbConn().connect_to_database()  # Подключаемся к стандартной базе

        if conn is None:
            print("Ошибка подключения к базе данных 'postgres'. Проверьте параметры подключения.")
            return

        conn.autocommit = True

        with conn.cursor() as cur:
            try:
                # Удаляем базу, если она уже существует
                cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
                # Создаём новую базу данных
                cur.execute(f"CREATE DATABASE {database_name}")
                print(f"База данных '{database_name}' успешно создана.")
            except Exception as e:
                print(f"Ошибка при создании базы данных '{database_name}': {e}")
                return
            finally:
                conn.close()

        # Ожидаем некоторое время, чтобы база была готова
        time.sleep(10)

    def _create_tables(self, database_name: str):
        """Функция для создания таблиц в указанной базе данных."""
        time.sleep(10)

        conn = DbConn().connect_to_database(database_name)

        try:
            # Создание таблиц
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE employers (
                        employer_id varchar PRIMARY KEY,
                        employer_name varchar NOT NULL,
                        site_url varchar,
                        alternate_url varchar,
                        open_vacancies varchar,
                        address varchar
                    );
                """)
                cur.execute("""
                    CREATE TABLE vacancies (
                        vacancy_name varchar,
                        vacancy_url VARCHAR,
                        salary INTEGER,
                        requirement VARCHAR,
                        employer_id varchar REFERENCES employers(employer_id)
                    );
                """)
            conn.commit()
            print("Таблицы успешно созданы.")
        except Exception as e:
            print(f"Ошибка при создании таблиц: {e}")
        finally:
            conn.close()

if __name__ == "__main__":

    database_name = "db_employers"
    db_creator = CreateDb()
    db_creator._create_database(database_name)  # Вызываем метод для создания базы
    db_creator._create_tables(database_name)
