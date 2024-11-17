from src.class_api import HH
from src.class_json_saver import JsonSaver
from src.class_vacancies import Vacancies
from src.utils import sort_vacancies_by_salary


class UserInteraction:
    def __init__(self):
        self.api = HH()  # Инициализируем класс для работы с API hh.ru
        self.saver = JsonSaver()  # Инициализируем класс для сохранения данных

    def search_vacancies(self):
        """Запрашиваем ключевое слово у пользователя и ищем вакансии"""
        keyword = input("Введите ключевое слово для поиска вакансий: ")
        self.api.load_vacancies(keyword)  # Поиск вакансий на hh.ru по ключевому слову
        vacancies = self.api.get_vacancies  # Получаем список вакансий
        vacancy_objects = Vacancies.get_list_vacancies(vacancies)  # Преобразуем в объекты класса Vacancies
        self.saver.add_vacancy(vacancy_objects)  # Сохраняем вакансии
        print(f"Найдено и сохранено {len(vacancy_objects)} вакансий.")

    def show_top_n_vacancies(self):
        """Получаем топ N вакансий по зарплате"""
        n = int(input("Введите количество вакансий для вывода (топ N по зарплате): "))
        all_vacancies = self.saver.get_all_vacancies()  # Получаем все вакансии как объекты Vacancies

        sorted_vacancies = sort_vacancies_by_salary(all_vacancies)  # Сортируем вакансии по зарплате
        top_n = sorted_vacancies[:n]  # Берем топ N вакансий
        for vacancy in top_n:
            print(vacancy)

    def show_vacancies_by_filter(self):
        """Показываем вакансии по ключевому слову"""
        keyword = input("Введите ключевое слово для фильтра вакансий: ")
        self.saver.get_info(keyword)

    def show_all_vacancies(self):
        """Показываем все вакансии"""
        res = self.saver.get_all_vacancies()
        for i in res:
            print(i)

    def delete_vacancy(self):
        """Удаляем вакансию по URL"""
        url = input("Введите URL вакансии, которую нужно удалить: ")
        self.saver.delete_info(url)
        print("Вакансия удалена.")
