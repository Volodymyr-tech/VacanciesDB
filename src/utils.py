from src.class_vacancies import Vacancies


def sort_vacancies_by_salary(vacancies: list[Vacancies]) -> list[Vacancies]:
    """
    Функция для сортировки вакансий по зарплате
    """
    return sorted(vacancies, key=lambda x: x.average_salary(), reverse=True)
