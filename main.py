from src.user_interaction import UserInteraction
from src.user_interaction_postgres import InteractionPostgre


# Основной цикл программы для взаимодействия с пользователем
def main():
    user = int(input("Для работы с PostgreSQL введите -'1',"
                     "Для работы с JSON введите -'2'  "))
    if user == 2:
        ui = UserInteraction()

        while True:
            print("\nВыберите действие:")
            print("1. Поиск вакансий")
            print("2. Показать топ N вакансий по зарплате")
            print("3. Найти вакансии по ключевому слову")
            print("4. Показать все вакансии")
            print("5. Удалить вакансию")
            print("0. Выйти")

            choice = input("Введите номер действия: ")

            if choice == "1":
                ui.search_vacancies()
            elif choice == "2":
                ui.show_top_n_vacancies()
            elif choice == "3":
                ui.show_vacancies_by_filter()
            elif choice == "4":
                ui.show_all_vacancies()
            elif choice == "5":
                ui.delete_vacancy()
            elif choice == "0":
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор, попробуйте снова.")
    elif user == 1:
        user_db = input("Введите название для создания базы данных: ")
        ui_postgre = InteractionPostgre(user_db)
        ui_postgre.create_db()
        ui_postgre.get_data_from_api()
        ui_postgre._save_data()

        while True:
            print("\nВыберите действие:")
            print("1. Посмотреть список всех компаний и количество вакансий")
            print("2. Получить список всех вакансий")
            print("3. Смотреть среднюю зарплату по вакансиям")
            print("4. Смотреть список вакансий с зарплатой выше средней")
            print("5. Поиск вакансии по ключевому слову")
            print("0. Выйти")

            choice = input("Введите номер действия: ")

            if choice == "1":
                ui_postgre.get_companies()
            elif choice == "2":
                ui_postgre.get_all_vacancies()
            elif choice == "3":
                ui_postgre.get_avg_salary()
            elif choice == "4":
                ui_postgre.get_higher_salary_vac()
            elif choice == "5":
                ui_postgre.get_vacancies_by_keyword()
            elif choice == "0":
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
