from unittest.mock import MagicMock

import pytest

from src.class_api import HH


def test_response_code(capsys):
    thing = HH()
    thing.load_vacancies = MagicMock(return_value=200)
    thing.load_vacancies("Python")


def test_error_response_code():
    thing = HH()
    thing.load_vacancies = MagicMock(side_effect=ConnectionError)
    with pytest.raises(ConnectionError):
        thing.load_vacancies("Python")


def test_getter():
    sub = HH()
    sub.load_vacancies("Python")
    vacancies_sub = sub.get_vacancies
    print(vacancies_sub)