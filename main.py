from src.user_interaction import UserInteraction


# Основной цикл программы для взаимодействия с пользователем
def main():
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


if __name__ == "__main__":
    main()
