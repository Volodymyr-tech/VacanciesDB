import os
from typing import Any

from mypy.metastore import connect_db
from psycopg2 import connect

from class_api import HH
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class DBManager:
    def __init__(self):
        self.__host = os.getenv("DB_HOST")
        self.__user = os.getenv("DB_USER")
        self.__password = os.getenv("DB_PASSWORD")
        self.__port = os.getenv('PORT')

    def _connect_to_database(self, database_name: str = "postgres"):
        """Создает подключение к базе данных."""
        try:
            conn = psycopg2.connect(
                dbname=database_name,
                host=self.__host,
                user=self.__user,
                password=self.__password,
                port=self.__port
            )
            return conn
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def _create_database(self, database_name: str):
        """Функция для создания базы данных и таблиц."""

        conn = self._connect_to_database("postgres")

        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")

        conn.close()

        conn = self._connect_to_database(database_name)

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

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE vacancies (
                    vacancy_name varchar,
                    vacancy_url VARCHAR,
                    salary INTEGER,
                    requirement VARCHAR,
                    employer_id varchar REFERENCES employers(employer_id)
                )
            """
            )

        print("Таблицы были созданы успешно")
        conn.commit()
        conn.close()


    def save_data_to_database(self,
            data_employer: list[dict[str, Any]],
            data_vacancies: list[dict[str, Any]],
                              database_name:str
    ):
        """Функция для сохранения вакансий и работадателей в базу данных."""
        conn = self._connect_to_database(database_name)

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
                        employer.get("area", {}).get("name")
                    ),
                )

            for vacancy in data_vacancies:  # 'vacancy', не 'vacancies'
                salary_from = (
                    vacancy["salary"]["from"]
                    if vacancy["salary"] and vacancy["salary"]["from"] is not None
                    else 0
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

        with conn.cursor() as cur:
            #Удлаение внещнего ключа, чтобы избежать конфликта между типами данных
            cur.execute("""
                ALTER TABLE vacancies
                DROP CONSTRAINT IF EXISTS vacancies_employer_id_fkey;
            """)
            #меняем varchar на integer
            cur.execute("""
                 ALTER TABLE employers
                 ALTER COLUMN employer_id TYPE INTEGER USING employer_id::INTEGER,
                 ALTER COLUMN open_vacancies TYPE INTEGER USING open_vacancies::INTEGER;
             """)

            # Преобразуем employer_id в INTEGER
            cur.execute("""
                            ALTER TABLE vacancies
                            ALTER COLUMN employer_id TYPE INTEGER USING employer_id::INTEGER;
                        """)
            #Заново создаем внешний ключ
            cur.execute("""
                ALTER TABLE vacancies
                ADD CONSTRAINT vacancies_employer_id_fkey FOREIGN KEY (employer_id)
                REFERENCES employers (employer_id);
            """)

        conn.commit()
        conn.close()


    def get_companies(self, database_name):

        conn = self._connect_to_database(database_name)

        with conn.cursor() as cur:
            # Выполнение SQL-запроса для получения всех работодателей
            cur.execute("SELECT employer_id, open_vacancies FROM employers;")
            # Извлечение всех строк
            results = cur.fetchall()
            return results #список кортежей информации о компаниях

        conn.close()


    def get_all_vacancies(self, database_name: str):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии,
        зарплаты и ссылки на вакансию.
        """
        conn = self._connect_to_database(database_name)

        try:
            with conn.cursor() as cur:
                cur.execute("""
                        SELECT 
                            e.employer_name AS company_name,
                            v.vacancy_name AS vacancy_name,
                            v.salary AS salary,
                            v.vacancy_url AS vacancy_url
                        FROM vacancies v
                        JOIN employers e ON v.employer_id = e.employer_id;
                    """)
                results = cur.fetchall()
                return results

        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def get_avg_salary(self, database_name: str):
        """
        Получает среднюю зарплату по всем вакансиям.
        """
        conn = self._connect_to_database(database_name)

        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT AVG(salary) AS average_salary
                    FROM vacancies
                    WHERE salary > 0;  -- Учитываем только вакансии с положительной зарплатой
                """)
                result = cur.fetchone()
                return result[0] if result else None  # Возвращаем среднюю зарплату или None, если данных нет

        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def get_vacancies_with_higher_salary(self, database_name: str):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        conn = self._connect_to_database(database_name)

        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT v.vacancy_name, e.employer_name, v.salary, v.vacancy_url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.employer_id
                    WHERE v.salary > (SELECT AVG(salary) FROM vacancies WHERE salary > 0);
                """)
                result = cur.fetchall()
                return result  # Возвращает список кортежей (vacancy_name, employer_name, salary, vacancy_url)

        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def get_vacancies_with_keyword(self, database_name: str, keyword: str):
        """
        Получает список всех вакансий, в названии которых содержатся переданные слова.

        :param database_name: Название базы данных.
        :param keyword: Ключевое слово для поиска в названии вакансий.
        :return: Список вакансий с ключевым словом.
        """
        conn = self._connect_to_database(database_name)

        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT v.vacancy_name, e.employer_name, v.salary, v.vacancy_url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.employer_id
                    WHERE v.vacancy_name ILIKE %s;
                """, (f"%{keyword}%",))
                result = cur.fetchall()
                return result  # Возвращает список кортежей (vacancy_name, employer_name, salary, vacancy_url)

        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn:
                conn.close()


if __name__ == "__main__":
    db = DBManager()
    hh = HH()
    db._connect_to_database()
    db._create_database("test")
    # Загружаем информацию о работодателях
    employees = hh.get_employees()

    # Загружаем вакансии по работодателям
    employee_vacancies = hh.load_employees_vacancies()

    db.save_data_to_database(employees, employee_vacancies, "test")

    print(db.get_companies("test"))
    print(db.get_all_vacancies("test"))
    print(db.get_avg_salary("test"))
    print(db.get_vacancies_with_higher_salary("test"))
    print(db.get_vacancies_with_keyword("test", "Python"))



