from abc import ABC, abstractmethod


class FileMethods(ABC):

    @abstractmethod
    def add_vacancy(self):
        pass

    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    def delete_info(self):
        pass
