import os
from typing import Any
import psycopg2
from dotenv import load_dotenv
from src.class_connection_to_db import DbConn
from src.class_api_employers import EmpHH
from src.class_create_db import CreateDb

load_dotenv()

class DBManager:

    def save_data_to_database(self,
            data_employer: list[dict[str, Any]],
            data_vacancies: list[dict[str, Any]],
                              database_name:str
    ):
        """Функция для сохранения вакансий и работадателей в базу данных."""
        conn = DbConn().connect_to_database(database_name)

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

        conn = DbConn().connect_to_database(database_name)

        with conn.cursor() as cur:
            # Выполнение SQL-запроса для получения всех работодателей
            cur.execute("SELECT employer_name, open_vacancies FROM employers;")
            # Извлечение всех строк
            results = cur.fetchall()
            return results #список кортежей информации о компаниях

        conn.close()


    def get_all_vacancies(self, database_name: str):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии,
        зарплаты и ссылки на вакансию.
        """
        conn = DbConn().connect_to_database(database_name)

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
        conn = DbConn().connect_to_database(database_name)

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
        conn = DbConn().connect_to_database(database_name)

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
        conn = DbConn().connect_to_database(database_name)

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
    db = DBManager() # тул для управления бд
    hh = EmpHH() # to get info
    created_db = CreateDb()
    # Загружаем информацию о работодателях
    employees = hh.get_employees()

    # Загружаем вакансии по работодателям
    employee_vacancies = hh.load_employees_vacancies()


    db.save_data_to_database(employees, employee_vacancies, "Vova_krasavchik")

    print(db.get_companies("Vova_krasavchik"))
    print(db.get_all_vacancies("Vova_krasavchik"))
    print(db.get_avg_salary("Vova_krasavchik"))
    print(db.get_vacancies_with_higher_salary("Vova_krasavchik"))
    print(db.get_vacancies_with_keyword("Vova_krasavchik", "Python"))



