from abc import ABC, abstractmethod


class Parser(ABC):

    @abstractmethod
    def load_vacancies(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass
