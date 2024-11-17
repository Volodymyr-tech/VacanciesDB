import re
from typing import Any


class Vacancies:
    """Класс для работы с вакансиями получеными с хедхантера"""

    name: str
    url: str
    salary: Any
    requirement: str
    employer_id: str

    __slots__ = ("name", "url", "salary", "requirement", "employer_id")

    def __init__(self, name, url, salary, requirement, employer_id):

        self.name = name
        self.url = url
        self.salary = salary
        self.requirement = requirement
        self.employer_id = employer_id

    @classmethod
    def get_list_vacancies(cls, vacancies: list):
        """Класс-метод для создания списка объектов класса Vacancy"""

        vacancies_list = [
            cls(
                name=vac.get("name", "Нет названия"),
                url=vac.get("alternate_url", "Нет URL"),
                salary=(
                    f"Зарплата от "
                    f'{vac["salary"].get("from") if vac["salary"].get("from") is not None else "не указано"} до '
                    f'{vac["salary"].get("to") if vac["salary"].get("to") is not None else "Верхний предел не указан"} '
                    f'{vac["salary"].get("currency", "Валюта не указана")}'
                    if vac["salary"] is not None
                    else "Зарплата не указана"
                ),
                requirement=vac.get("snippet", {}).get("requirement", "нет описания"),
                employer_id=vac["employer"]["id"]
            )
            for vac in vacancies
        ]

        return vacancies_list  # Преобразовывем список словарей в список объектов класса Вакансия

    #def __validation(self):
     #    pass

    def __str__(self):
        return f"{self.name} средняя зарплата:{self.average_salary()},ссылка: {self.url}"

    def __eq__(self, other):
        if isinstance(other, Vacancies):
            return self.url == other.url  # Сравниваем объекты только по URL
        return False

    def __hash__(self):
        return hash(self.url)

    def _extract_numbers(self):
        """Извлекает все числа из строки зарплаты."""
        if isinstance(self.salary, (int, float)):  # Если salary уже число
            return self.salary, self.salary

        if isinstance(self.salary, str):  # Если salary строка, обрабатываем как строку
            pattern = r"(\d[\d\s]*)"  # Паттерн для поиска чисел в строке
            numbers = re.findall(pattern, self.salary)  # Находим все числовые части в строке
            numbers = [int(num.replace(" ", "")) for num in numbers]  # Убираем пробелы и преобразуем в int

            if not numbers:  # Если чисел нет, возвращаем (0, 0)
                return 0, 0

            if len(numbers) == 1:  # Если найдено одно число, возвращаем его и 0
                return numbers[0], 0

            return numbers[0], numbers[-1]

        return 0, 0  # Если формат зарплаты непонятный

    def average_salary(self):
        "Метод для подсчета средней зарплаты вакансии"
        min_salary, max_salary = self._extract_numbers()

        if min_salary == 0 and max_salary == 0:  # Если оба числа равны 0, возвращаем 0
            return 0

        if min_salary == 0:  # Если одно из чисел равно 0, возвращаем ненулевое значение
            return max_salary
        if max_salary == 0:
            return min_salary
        result = (min_salary + max_salary) / 2
        return result

    def __le__(self, other):
        if not isinstance(other, Vacancies):
            raise TypeError("Операнд справа должен иметь тип Vacancy")
        else:
            return self.average_salary() <= other.average_salary()

    def __gt__(self, other):
        if not isinstance(other, Vacancies):
            raise TypeError("Операнд справа должен иметь тип Vacancy")
        else:
            return self.average_salary() > other.average_salary()

    def __ge__(self, other):
        if not isinstance(other, Vacancies):
            raise TypeError("Операнд справа должен иметь тип Vacancy")
        else:
            return self.average_salary() >= other.average_salary()
