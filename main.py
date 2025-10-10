from src.db_manager import DBManager
from src.utils import create_database, create_tables, insert_employers, insert_vacancies


def main() -> None:
    """Функция для взаимодействия с пользователем."""

    # Приветствие
    print("Добро пожаловать в программу работы с вакансиями.\n"
          "Идет загрузка данных.............................\n")

    # Выгрузка данных из API и сохранение в БД PostgreSQL
    db_name = "hh_vacancies"
    create_database(db_name)
    create_tables(db_name)
    insert_employers(db_name)
    insert_vacancies(db_name)

    print("Загружены вакансии ТОП-10 компаний.")

    # Выбор параметров вывода данных
    menu_selection = ""
    while menu_selection != "6":
        print(
            "\nМеню:\n"
            "1. Показать список компаний\n"
            "2. Показать все вакансии\n"
            "3. Показать среднюю зарплату по всем вакансиям\n"
            "4. Показать все вакансии, у которых зарплата выше средней по всем вакансиям\n"
            "5. Найти вакансии по ключевым словам\n"
            "6. Завершить работу\n"
        )

        menu_selection = input("Введите номер одного из пунктов меню: ")

        while menu_selection not in ["1", "2", "3", "4", "5", "6"]:
            menu_selection = input("Номер пункта выбран неверно, введите цифру от 1 до 5: ")

        # Вывод результатов выбора пользователя
        db_manager = DBManager(db_name)

        if menu_selection == "1":
            all_companies = db_manager.get_companies_and_vacancies_count()
            print("\nТОП-10 компаний:")
            for item in all_companies:
                print(f"{item[0]}: {item[1]} вакансий ({item[2]})")

        elif menu_selection == "2":
            all_vacancies = db_manager.get_all_vacancies()
            print("\nСписок всех вакансий с диапазоном зарплат:")
            for item in all_vacancies:
                print(
                    f"\nВакансия: {item[0]}"
                    f"\nКомпания: {item[5]}"
                    f"\nЗарплата от {item[2]} до {item[3]} {item[4]}"
                    f"\nСсылка: {item[1]}"
                )

        elif menu_selection == "3":
            avg_salary = db_manager.get_avg_salary()
            print("\nСписок всех вакансий со средней зарплатой:")
            for item in avg_salary:
                print(
                    f"\nВакансия: {item[0]}"
                    f"\nКомпания: {item[4]}"
                    f"\nСредняя зарплата {item[2]} {item[3]}"
                    f"\nСсылка: {item[1]}"
                )

        elif menu_selection == "4":
            avg_salary_plus = db_manager.get_vacancies_with_higher_salary()
            print("\nСписок всех вакансий, у которых зарплата выше средней по всем вакансиям:")
            for item in avg_salary_plus:
                print(
                    f"\nВакансия: {item[0]}"
                    f"\nКомпания: {item[4]}"
                    f"\nСредняя зарплата {item[2]} {item[3]}"
                    f"\nСсылка: {item[1]}"
                )

        elif menu_selection == "5":
            words_input = input("Введите через запятую ключевые слова/части слов для поиска вакансий (без пробелов): ")
            print(words_input)
            words_list = words_input.split(",")
            keywords = []
            for word in words_list:
                keywords.append(f"%{word}%")
            print(keywords)
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keywords)
            if len(vacancies_with_keyword) > 0:
                print(f"\nРезультат поиска по ключевым словам {words_list}:")
                for item in vacancies_with_keyword:
                    print(
                        f"\nВакансия: {item[0]}"
                        f"\nКомпания: {item[5]}"
                        f"\nЗарплата от {item[2]} до {item[3]} {item[4]}"
                        f"\nСсылка: {item[1]}"
                    )
            else:
                print("\nПо введенным ключевым словам ничего не найдено.")

        elif menu_selection == "6":
            print("\nРабота программы завершена. До свидания!")


if __name__ == "__main__":
    main()
