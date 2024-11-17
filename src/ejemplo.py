import requests


def conection():
    temp_url = f"https://api.hh.ru/employers/10636999"
    employer_data = requests.get(temp_url).json()
    print(employer_data)


x = conection()

