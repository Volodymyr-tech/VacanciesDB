import requests

class HhEmployees:
    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 1}
        self.__vacancies = []
        self.__employers = [
            10288002,
            10636999,
            1122462,
            9498112,
            2855463,
            64174,
            4949,
            1664868,
            2324020,
            4596113,
            9938436,
            906557,
            2705050,
            4934,
            3530,
            4767781
        ]

    def __api_conection(self):
        """Метод для проверки подключения API"""
        response = requests.get(self.__url)
        if response.status_code == 200:
            return "Подключение стабильно, ищу вакансии в интернете"
        else:
            raise ConnectionError(f"Ошибка {response.status_code}")

    def load_vacancies(self, keyword):
        """Метод получения Json ответа от API HH"""
        print(self.__api_conection())
        self.__params["text"] = keyword
        while self.__params.get("page") != 20:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            vacancies = response.json()["items"]
            self.__vacancies.extend(vacancies)
            self.__params["page"] += 1

    def get_employees(self, employer_id):
        """Загрузка информации о работодателе"""
        response = requests.get(f'https://api.hh.ru/employers/{employer_id}')
        print(response.status_code)
        if response.status_code == 200:
            try:
                employers = response.json()
                self.__employers.append(employers)
            except ValueError:
                print("Ошибка: Невозможно декодировать JSON.")
        else:
            print(f"Ошибка: Запрос не удался. Код ответа: {response.status_code}")


    def load_vacancies_by_company(self):
        """Метод для загрузки вакансий."""

        vacancy_info = []
        for employer_id in self.__employers:
            params_copy = self.__params.copy()
            params_copy["employer_id"] = employer_id

            vacancy_url = f"{self.__url}"
            response = requests.get(
                vacancy_url, headers=self.__headers, params=params_copy
            )
            vacancies = response.json()["items"]
            vacancy_info.extend(vacancies)
        return vacancy_info


    @property
    def print_employers(self):
        """Геттер который возвращает список словарей с информацией о работодателях"""
        return self.__employers


if __name__ == '__main__':
    emp = HhEmployees()
    print(emp.load_vacancies_by_company())
