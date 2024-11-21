from unittest.mock import MagicMock, patch

from src.user_interaction import UserInteraction


@patch("builtins.input", side_effect=["Python"])
def test_search_vacancies(mock_input):
    ui = UserInteraction()
    ui.api.load_vacancies = MagicMock()
    ui.saver.add_vacancy = MagicMock()

    ui.search_vacancies()
    ui.api.load_vacancies.assert_called_once_with("Python")
    ui.saver.add_vacancy.assert_called_once()


@patch("builtins.input", side_effect=["https://hh.ru/vacancy/123"])
def test_delete_vacancy(mock_input):
    ui = UserInteraction()
    ui.saver.delete_info = MagicMock()

    ui.delete_vacancy()
    ui.saver.delete_info.assert_called_once_with("https://hh.ru/vacancy/123")