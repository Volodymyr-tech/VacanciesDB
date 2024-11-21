from src.class_api_employers import EmpHH
from src.class_connection_to_db import DbConn
from src.class_create_db import CreateDb
from src.class_db_manager import DBManager


class InteractionPostgre:

    def __init__(self, keyword):
        self.api = EmpHH()
        self.connection = DbConn()
        self.creator = CreateDb()
        self.db = DBManager()
        self.keyword = keyword

    def create_db(self):
        '''Подключаемся к указанной БД'''
        self.connection.connect_to_database()
        self.creator._create_database(self.keyword)
        self.creator._create_tables(self.keyword)

    def get_data_from_api(self):
        """Загружаем вакансии и работодателей"""
        employees = self.api.get_employees()
        employee_vacancies = self.api.load_employees_vacancies()
        return employees, employee_vacancies

    def _save_data(self):
        '''Сохраняем данные с Апи хедхантера в БД'''
        args = self.get_data_from_api()
        self.db.save_data_to_database(*args, self.keyword)

    def get_companies(self):
        '''Получаем список компаний и количество вакансий'''
        res = self.db.get_companies(self.keyword)
        for company in res:
            print(f"{company[0]}, колличество вакансий: {company[1]}  ")

    def get_all_vacancies(self):
        '''Получаем список всех вакансий'''
        res = self.db.get_all_vacancies(self.keyword)
        for vacancy in res:
            print(
                f"Работодатель: {vacancy[0]}, открытая вакансия: {vacancy[1]} с зарплатой {vacancy[2]}, ссылка: {vacancy[3]} "
            )

    def get_avg_salary(self):
        '''Получаем среднюю ЗП по вакансиям в БД'''
        res = self.db.get_avg_salary(self.keyword)
        print(res)

    def get_higher_salary_vac(self):
        '''Получаем ЗП выше среднего по вакансиям в БД'''
        res = self.db.get_vacancies_with_higher_salary(self.keyword)
        for vacancy in res:
            print(f"Вакансия: {vacancy[0]}, в компании {vacancy[1]} с зарплатой {vacancy[2]}, ссылка: {vacancy[3]} ")

    def get_vacancies_by_keyword(self):
        '''Получаем вакансии по ключевому слову в БД'''
        user_keyword = input("Введи строку для поиска ")
        res = self.db.get_vacancies_with_keyword(self.keyword, user_keyword)
        for vacancy in res:
            print(f"Вакансия: {vacancy[0]}, в компании {vacancy[1]} с зарплатой {vacancy[2]}, ссылка: {vacancy[3]} ")
