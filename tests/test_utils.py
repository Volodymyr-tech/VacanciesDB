from src.class_vacancies import Vacancies
from src.utils import sort_vacancies_by_salary


def test_sort_vacancies_by_salary():
    vacancies = [
        Vacancies("Dev", "https://hh.ru/1", "50 000 RUR", "Описание", "1212"),
        Vacancies("Manager", "https://hh.ru/2", "70 000 RUR", "Описание", "121212"),
        Vacancies("Intern", "https://hh.ru/3", "30 000 RUR", "Описание", "121221244"),
    ]
    sorted_vacancies = sort_vacancies_by_salary(vacancies)
    assert sorted_vacancies[0].name == "Manager"
    assert sorted_vacancies[-1].name == "Intern"