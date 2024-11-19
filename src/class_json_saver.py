import json
import os.path

from config import DATA_DIR
from src.abstract_file_methods import FileMethods
from src.class_vacancies import Vacancies


class JsonSaver(FileMethods):
    """Класс для сохранения и обработки информации о вакансиях в JSON-файл."""

    filename: str

    def __init__(self, filename="vacancies.json"):
        self.__filename = os.path.join(DATA_DIR, filename)

    def add_vacancy(self, *args):
        """Добавляем одну или несколько вакансий, если их нет в файле"""

        existing_vacancies = self.__open_file()  # Получаем множество существующих вакансий

        new_vacancies = set()  # Получаем пустое множество

        for arg in args:  # Обрабатываем каждый переданный аргумент
            if isinstance(arg, list):
                new_vacancies.update(arg)  # Добавляем все элементы списка в пустое множество
            else:
                new_vacancies.add(arg)

        updated_vacancies = existing_vacancies.union(
            new_vacancies
        )  # Объединяем новые и существующие вакансии с помощью union

        self.__save_vacancy(updated_vacancies)  # преобразует вакансии в формат списка словарей.
        self.__write_to_file(updated_vacancies)  # Пишем данные в файл

    def __save_vacancy(self, vacancies):
        """Преобразуем вакансии в список словарей для сохранения в JSON"""
        data = [
            {
                "name": vac.name,
                "url": vac.url,
                "salary": vac.salary,
                "requirement": vac.requirement,
                "employer_id": vac.employer_id,
            }
            for vac in vacancies
        ]
        return data

    def __write_to_file(self, vacancies):
        """Сохраняем список вакансий в JSON файл"""
        data = self.__save_vacancy(vacancies)  # Вызываем метод для получения списка словарей вакансий
        with open(self.__filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def __open_file(self):
        """Открываем файл JSON и возвращаем множество вакансий"""

        if not os.path.exists(self.__filename):  # Если файл не существует, возвращаем пустое множество
            return set()

        if os.path.getsize(self.__filename) == 0:  # Если файл пустой, возвращаем пустое множество
            return set()

        with open(self.__filename, "r", encoding="utf-8") as file:
            vacancies_in_file = json.load(file)  # Получаем вакансии из JSON файла

        vacancies_set = {
            Vacancies(
                vac.get("name"),
                vac.get("url"),
                vac.get("salary"),
                vac.get("requirement"),
                vac.get("employer", {}).get("id"),
            )
            for vac in vacancies_in_file  # Преобразуем данные в множество объектов класса Vacancies
        }

        return vacancies_set

    def get_info(self, filter):
        """Вывод информации о вакансии по указанному ключевому слову полученому от юзера"""
        existing_vacancies = self.__open_file()  # Получаем множество существующих вакансий
        for vacancy in existing_vacancies:
            data = vacancy.requirement
            name = vacancy.name
            if filter in data or filter in name:
                print(vacancy)
        return "Больше вакансий нет (·_·) "  # Вакансии с ключевым словом по имени

    def get_all_vacancies(self):
        """Вывод информации о вакансии по указанному ключевому слову полученому от юзера"""
        existing_vacancies = self.__open_file()  # Загружаем данные из файла
        return existing_vacancies  # Возвращаем список объектов класса Vacancies

    def delete_info(self, filter):
        """Удаление вакансии из JSON файла"""
        existing_vacancies = self.__open_file()
        to_remove = None
        for vac in existing_vacancies:
            if filter == vac.url:
                to_remove = vac
        existing_vacancies.remove(to_remove)
        self.__save_vacancy(existing_vacancies)  # преобразует вакансии в формат списка словарей.
        self.__write_to_file(existing_vacancies)

    def sort_vacancies_by_salary(self, existing_vacancies):
        """Функция для сортировки вакансий по зарплате"""
        # existing_vacancies = self.__open_file()
        by_salary = sorted(existing_vacancies, key=lambda x: x.salary, reverse=True)
        for i in by_salary:
            print(i)
        else:
            None
