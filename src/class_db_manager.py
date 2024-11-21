import logging
import os
from typing import Any

import psycopg2
from dotenv import load_dotenv

from config import LOGS_DIR
from src.class_connection_to_db import DbConn

log_file_path = os.path.join(LOGS_DIR, "db_manager.log")

app_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(funcName)s %(message)s")
file_handler.setFormatter(file_formatter)
app_logger.addHandler(file_handler)
app_logger.setLevel(logging.DEBUG)


load_dotenv()


class DBManager:

    def save_data_to_database(
        self, data_employer: list[dict[str, Any]], data_vacancies: list[dict[str, Any]], database_name: str
    ):
        """Функция для сохранения вакансий и работадателей в базу данных."""
        conn = DbConn().connect_to_database(database_name)
        app_logger.info(f"Успешное  подключение к БД '{database_name}'")

        with conn.cursor() as cur:
            for employer in data_employer:
                cur.execute(
                    """
                    INSERT INTO employers (employer_id, employer_name, site_url, alternate_url, open_vacancies, address)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (employer_id) DO NOTHING;
                    """,
                    (
                        employer.get("id"),
                        employer.get("name"),
                        employer.get("site_url", "сайт не указан"),
                        employer.get("alternate_url"),
                        employer.get("open_vacancies"),
                        employer.get("area", {}).get("name"),
                    ),
                )

            for vacancy in data_vacancies:  # 'vacancy', не 'vacancies'
                salary_from = (
                    vacancy["salary"]["from"] if vacancy["salary"] and vacancy["salary"]["from"] is not None else 0
                )
                cur.execute(
                    """
                        INSERT INTO vacancies (vacancy_name, vacancy_url, salary, requirement, employer_id )
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                    (
                        vacancy["name"],
                        vacancy["alternate_url"],
                        salary_from,
                        vacancy["snippet"].get("requirement"),
                        vacancy["employer"]["id"],
                    ),
                )

        app_logger.info(f"Записываю данные в таблицы 'employers' и 'vacancies' в БД'{database_name}'")

        with conn.cursor() as cur:
            # Удлаение внещнего ключа, чтобы избежать конфликта между типами данных
            cur.execute(
                """
                ALTER TABLE vacancies
                DROP CONSTRAINT IF EXISTS vacancies_employer_id_fkey;
            """
            )
            app_logger.info(f"Удаляю Foreign Key в таблице'vacancies' в БД'{database_name}'")
            # меняем varchar на integer
            cur.execute(
                """
                 ALTER TABLE employers
                 ALTER COLUMN employer_id TYPE INTEGER USING employer_id::INTEGER,
                 ALTER COLUMN open_vacancies TYPE INTEGER USING open_vacancies::INTEGER;
             """
            )
            app_logger.info(f"Меняю тип данных в таблице 'employers' в БД'{database_name}'")

            # Преобразуем employer_id в INTEGER
            cur.execute(
                """
                            ALTER TABLE vacancies
                            ALTER COLUMN employer_id TYPE INTEGER USING employer_id::INTEGER;
                        """
            )
            app_logger.info(f"Меняю тип данных в таблице 'vacancies' в БД'{database_name}'")
            # Заново создаем внешний ключ
            cur.execute(
                """
                ALTER TABLE vacancies
                ADD CONSTRAINT vacancies_employer_id_fkey FOREIGN KEY (employer_id)
                REFERENCES employers (employer_id);
            """
            )
            app_logger.info(f"Заново создаем внешний ключ в таблице 'vacancies' в БД'{database_name}'")

        conn.commit()
        conn.close()
        app_logger.info(f" Контрольный комит и закрытие подключения к БД'{database_name}'")

    def get_companies(self, database_name):

        conn = DbConn().connect_to_database(database_name)
        app_logger.info(f"Успешное  подключение к БД '{database_name}'")

        with conn.cursor() as cur:
            # Выполнение SQL-запроса для получения всех работодателей
            cur.execute("SELECT employer_name, open_vacancies FROM employers;")
            # Извлечение всех строк
            results = cur.fetchall()
            return results  # список кортежей информации о компаниях

        conn.close()
        app_logger.info(f"закрытие подключения к БД'{database_name}'")

    def get_all_vacancies(self, database_name: str):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии,
        зарплаты и ссылки на вакансию.
        """
        conn = DbConn().connect_to_database(database_name)
        app_logger.info(f"Успешное  подключение к БД '{database_name}'")
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        SELECT 
                            e.employer_name AS company_name,
                            v.vacancy_name AS vacancy_name,
                            v.salary AS salary,
                            v.vacancy_url AS vacancy_url
                        FROM vacancies v
                        JOIN employers e ON v.employer_id = e.employer_id;
                    """
                )
                results = cur.fetchall()
                return results

        except psycopg2.Error as e:
            app_logger.error(f"Database error: {e}")
            return []
        finally:
            if conn:
                conn.close()
                app_logger.info(f"Закрытые подключения к БД '{database_name}'")

    def get_avg_salary(self, database_name: str):
        """
        Получает среднюю зарплату по всем вакансиям.
        """
        conn = DbConn().connect_to_database(database_name)
        app_logger.info(f"Успешное  подключение к БД '{database_name}'")
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT AVG(salary) AS average_salary
                    FROM vacancies
                    WHERE salary > 0;  -- Учитываем только вакансии с положительной зарплатой
                """
                )
                result = cur.fetchone()
                return result[0] if result else None  # Возвращаем среднюю зарплату или None, если данных нет

        except psycopg2.Error as e:
            app_logger.error(f"Database error: {e}")
            return None
        finally:
            if conn:
                conn.close()
                app_logger.info(f"Закрытые подключения к БД '{database_name}'")

    def get_vacancies_with_higher_salary(self, database_name: str):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        conn = DbConn().connect_to_database(database_name)
        app_logger.info(f"Успешное  подключение к БД '{database_name}'")
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT v.vacancy_name, e.employer_name, v.salary, v.vacancy_url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.employer_id
                    WHERE v.salary > (SELECT AVG(salary) FROM vacancies WHERE salary > 0);
                """
                )
                result = cur.fetchall()
                return result  # Возвращает список кортежей (vacancy_name, employer_name, salary, vacancy_url)

        except psycopg2.Error as e:
            app_logger.error(f"Database error: {e}")
            return None
        finally:
            if conn:
                conn.close()
                app_logger.info(f"Закрытые подключения к БД '{database_name}'")

    def get_vacancies_with_keyword(self, database_name: str, keyword: str):
        """
        Получает список всех вакансий, в названии которых содержатся переданные слова.

        :param database_name: Название базы данных.
        :param keyword: Ключевое слово для поиска в названии вакансий.
        :return: Список вакансий с ключевым словом.
        """
        conn = DbConn().connect_to_database(database_name)
        app_logger.info(f"Успешное  подключение к БД '{database_name}'")
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT v.vacancy_name, e.employer_name, v.salary, v.vacancy_url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.employer_id
                    WHERE v.vacancy_name ILIKE %s;
                """,
                    (f"%{keyword}%",),
                )
                result = cur.fetchall()
                return result  # Возвращает список кортежей (vacancy_name, employer_name, salary, vacancy_url)

        except psycopg2.Error as e:
            app_logger.error(f"Database error: {e}")
            return None
        finally:
            if conn:
                conn.close()
                app_logger.info(f"Закрытые подключения к БД '{database_name}'")
