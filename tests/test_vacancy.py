import pytest

from src.class_vacancies import Vacancies


def test_init():
    emp2 = Vacancies("java", "https://hh.ru/vacancy/108435856", "Зарплата от 10000 до 20000 USD", "работай больше", "1212")
    assert emp2.name == "java"
    assert emp2.url == "https://hh.ru/vacancy/108435856"
    assert emp2.salary == "Зарплата от 10000 до 20000 USD"
    assert emp2.requirement == "работай больше"
    assert emp2.employer_id == "1212"

    assert emp2._extract_numbers() == (10000, 20000)


def test_init_2():
    emp3 = Vacancies("python", "https://hh.ru/vacancy/108435856", "Зарплата от 0 до 20000 USD", "работай больше", "1212")
    assert emp3.name == "python"
    assert emp3.url == "https://hh.ru/vacancy/108435856"
    assert emp3.salary == "Зарплата от 0 до 20000 USD"
    assert emp3.requirement == "работай больше"

    assert emp3._extract_numbers() == (0, 20000)


def test_init_3():
    emp4 = Vacancies(
        "NODE", "https://hh.ru/vacancy/108435856", 'Зарплата от 0 до "Верхняя планка не указана" USD', "работай больше", "1212"
    )
    assert emp4.name == "NODE"
    assert emp4.url == "https://hh.ru/vacancy/108435856"
    assert emp4.salary == 'Зарплата от 0 до "Верхняя планка не указана" USD'
    assert emp4.requirement == "работай больше"

    assert emp4._extract_numbers() == (0, 0)


def test_average_salary():

    emp4 = Vacancies("NODE", "https://hh.ru/vacancy/108435856", "Зарплата от 100 до 100 USD", "работай больше", "1212")
    salary = emp4.average_salary()
    assert salary == 100


def test_ln():
    emp1 = Vacancies("NODE", "https://hh.ru/vacancy/108435856", "Зарплата от 100 до 100 USD", "работай больше", "1121212")
    emp2 = Vacancies("Python", "https://hh.ru/vacancy/1025", "Зарплата от 200 до 200 USD", "работай больше", "1223212")
    return emp1 <= emp2


def test_gt():
    emp1 = Vacancies("NODE", "https://hh.ru/vacancy/108435856", "Зарплата от 600 до 100 USD", "работай больше", "1223212")
    emp2 = Vacancies("Python", "https://hh.ru/vacancy/1025", "Зарплата от 200 до 200 USD", "работай больше", "1313")
    return emp1 > emp2


def test_ge():
    emp1 = Vacancies("NODE", "https://hh.ru/vacancy/108435856", "Зарплата от 600 до 100 USD", "работай больше", "1212")
    emp2 = Vacancies("Python", "https://hh.ru/vacancy/1025", "Зарплата от 200 до 500 USD", "работай больше","223123")
    return emp1.average_salary() >= emp2.average_salary()


@pytest.fixture
def sample_vacancy():
    return Vacancies(
        "Python Developer", "https://hh.ru/vacancy/123", "от 100 000 до 200 000 RUR", "Требования: опыт работы", "1212"
    )


def test_average_salary(sample_vacancy):
    assert sample_vacancy.average_salary() == 150000


def test_comparison(sample_vacancy):
    other_vacancy = Vacancies("Java Developer", "https://hh.ru/vacancy/124", "1510000 RUR", "Требования: опыт работы", "1221212")
    assert other_vacancy > sample_vacancy