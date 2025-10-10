from typing import Any

import psycopg2

from config import config


class DBManager:
    """Класс для подключения к БД PostgreSQL и получения данных."""

    def __init__(self, db_name: str) -> None:
        """Метод для инициализации экземпляра класса."""

        self.__db_name = db_name

    def __execute_query(self, query: str) -> Any:
        """Метод для подключения БД PostgreSQL."""

        params = config()
        with psycopg2.connect(dbname=self.__db_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()

        conn.close()
        return result

    def get_companies_and_vacancies_count(self) -> Any:
        """Метод для получения списка всех компаний и количество вакансий у каждой компании."""

        query = (
            "SELECT employers.employer_name, COUNT(vacancies.vacancy_id), employers.employer_url "
            "FROM vacancies "
            "INNER JOIN employers USING(employer_id) "
            "GROUP BY employers.employer_name, employers.employer_url;"
        )
        return self.__execute_query(query)

    def get_all_vacancies(self) -> Any:
        """Метод для получения списка всех вакансий."""

        query = (
            "SELECT vacancy_name, vacancy_url, salary_from, salary_to, currency, employers.employer_name "
            "FROM vacancies "
            "INNER JOIN employers USING(employer_id)"
        )
        return self.__execute_query(query)

    def get_avg_salary(self) -> Any:
        """Метод для получения средней зарплаты по вакансиям."""

        query = (
            "SELECT vacancy_name, vacancy_url, (salary_from + salary_to) / 2 as avg_salary, currency, "
            "employers.employer_name "
            "FROM vacancies "
            "INNER JOIN employers USING(employer_id)"
        )
        return self.__execute_query(query)

    def get_vacancies_with_higher_salary(self) -> Any:
        """Метод для получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям."""

        query = (
            "SELECT vacancy_name, vacancy_url, (salary_from + salary_to) / 2 as avg_salary, currency, "
            "employers.employer_name "
            "FROM vacancies "
            "INNER JOIN employers USING(employer_id) "
            "WHERE (salary_from + salary_to) / 2 > (SELECT AVG((salary_from + salary_to) / 2) FROM vacancies)"
        )
        return self.__execute_query(query)

    def get_vacancies_with_keyword(self, words: list) -> Any:
        """Метод для получения списка всех вакансий, в названии которых содержатся переданные в метод слова."""

        query = (
            "SELECT vacancy_name, vacancy_url, salary_from, salary_to, currency, employers.employer_name "
            "FROM vacancies "
            "INNER JOIN employers USING(employer_id) "
            f"WHERE vacancy_name ILIKE ANY(ARRAY{words})"
        )
        return self.__execute_query(query)
