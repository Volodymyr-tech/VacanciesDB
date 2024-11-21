import time
import requests

class EmpHH():
    """
    Класс для работы с API HeadHunter
    """
    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 10}
        self.__vacancies = []
        self.__employers = (
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
            4767781,
        )

    def get_employees(self):
        """Загрузка информации о работодателе"""
        employers_info = []
        for employer in self.__employers:
            temp_url = f"https://api.hh.ru/employers/{employer}"
            try:
                response = requests.get(temp_url, self.__headers)
                response.raise_for_status()
                employer_data = response.json()
                filtered_data = {
                    "id": employer_data.get("id"),
                    "name": employer_data.get("name"),
                    "site_url": employer_data.get("site_url"),
                    "alternate_url": employer_data.get("alternate_url"),
                    "open_vacancies": employer_data.get("open_vacancies"),
                    "address": employer_data.get("area", {}).get("name"),
                }
                employers_info.append(filtered_data)

            except requests.exceptions.RequestException as e:
                print(f"Ошибка при получении данных о работодателе {employer}: {e}")
            time.sleep(0.5)
        return employers_info

    def load_employees_vacancies(self):
        """Метод для загрузки вакансий по работодателям"""
        vacancy_info = []
        for employer_id in self.__employers:
            try:
                response = requests.get(
                    f"https://api.hh.ru/vacancies/{employer_id}",
                    headers=self.__headers,
                    params={"employer_id": employer_id, **self.__params},
                )
                response.raise_for_status()
                vacancies = response.json().get("items", [])
                vacancy_info.extend(vacancies)
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при загрузке вакансий работодателя {employer_id}: {e}")
        return vacancy_info



if __name__ == "__main__":
    data = EmpHH()
    emp = data.get_employees()
    vac = data.load_employees_vacancies()
    for e in emp:
        print(e)


    for v in vac:
        print(v)