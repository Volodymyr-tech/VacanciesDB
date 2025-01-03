from unittest.mock import patch
from src.class_json_saver import JsonSaver
from src.class_vacancies import Vacancies


# Тест добавления вакансий
@patch("src.class_json_saver.JsonSaver._JsonSaver__open_file")
@patch("src.class_json_saver.JsonSaver._JsonSaver__write_to_file")
def test_add_vacancy(mock_write_to_file, mock_open_file):
    """Тест добавления вакансий в JSON файл"""

    # Создаем тестовые вакансии
    vacancy1 = Vacancies(
        name="Python Developer", url="https://hh.ru/vacancy/123", salary="100000", requirement="Python", employer_id="123"
    )
    vacancy2 = Vacancies(name="Java Developer", url="https://hh.ru/vacancy/456", salary="150000", requirement="Java",employer_id="223")

    # Имитируем, что в файле уже есть одна вакансия
    mock_open_file.return_value = {vacancy1}

    # Создаем объект JsonSaver
    saver = JsonSaver()

    # Добавляем вторую вакансию
    saver.add_vacancy(vacancy2)

    # Проверяем, что после добавления вакансий файл перезаписан с обеими вакансиями
    expected_vacancies = {vacancy1, vacancy2}
    mock_write_to_file.assert_called_once_with(expected_vacancies)


@patch("src.class_json_saver.JsonSaver._JsonSaver__open_file")
def test_get_all_vacancies(mock_open_file):
    """Тест получения всех вакансий"""

    # Создаем тестовые вакансии
    vacancy1 = Vacancies(
        name="Python Developer", url="https://hh.ru/vacancy/123", salary="100000", requirement="Python", employer_id="123"
    )
    vacancy2 = Vacancies(name="Java Developer", url="https://hh.ru/vacancy/456", salary="150000", requirement="Java", employer_id="124")

    # Имитация вакансий в файле
    mock_open_file.return_value = {vacancy1, vacancy2}

    # Создаем объект JsonSaver
    saver = JsonSaver()

    # Проверяем, что метод возвращает все вакансии
    all_vacancies = saver.get_all_vacancies()
    assert all_vacancies == {vacancy1, vacancy2}


@patch("src.class_json_saver.JsonSaver._JsonSaver__open_file")
def test_get_info(mock_open_file):
    """Тест фильтрации вакансий по ключевому слову"""

    # Создаем тестовые вакансии
    vacancy1 = Vacancies(
        name="Python Developer", url="https://hh.ru/vacancy/123", salary="100000", requirement="Python", employer_id="123"
    )
    vacancy2 = Vacancies(name="Java Developer", url="https://hh.ru/vacancy/456", salary="150000", requirement="Java", employer_id="1223")

    # Имитация вакансий в файле
    mock_open_file.return_value = {vacancy1, vacancy2}

    # Создаем объект JsonSaver
    saver = JsonSaver()

    # Имитируем ввод ключевого слова для поиска вакансий
    with patch("builtins.print") as mocked_print:
        saver.get_info("Python")
        mocked_print.assert_called_once_with(vacancy1)


@patch("src.class_json_saver.JsonSaver._JsonSaver__open_file")
def test_sort_vacancies_by_salary(mock_open_file):
    """Тест сортировки вакансий по зарплате"""

    # Создаем тестовые вакансии с разными зарплатами
    vacancy1 = Vacancies(
        name="Python Developer", url="https://hh.ru/vacancy/123", salary="100000", requirement="Python", employer_id="123"
    )
    vacancy2 = Vacancies(name="Java Developer", url="https://hh.ru/vacancy/456", salary="150000", requirement="Java", employer_id="1232")
    vacancy3 = Vacancies(name="Go Developer", url="https://hh.ru/vacancy/789", salary="200000", requirement="Go", employer_id="123")

    # Имитация вакансий в файле
    mock_open_file.return_value = {vacancy1, vacancy2, vacancy3}

    # Создаем объект JsonSaver
    saver = JsonSaver()

    # Имитируем сортировку вакансий
    with patch("builtins.print") as mocked_print:
        saver.sort_vacancies_by_salary(mock_open_file.return_value)

        # Проверяем, что вакансии напечатаны в правильном порядке (по убыванию зарплаты)
        mocked_print.assert_any_call(vacancy3)
        mocked_print.assert_any_call(vacancy2)
        mocked_print.assert_any_call(vacancy1)