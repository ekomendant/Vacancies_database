import psycopg2

from config import config
from src.api_interaction import HeadHunterEmployers, HeadHunterVacancies


def create_database(db_name: str) -> None:
    """Функция для создания БД в PostgreSQL."""

    params = config()

    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(
        f"""SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{db_name}'
                AND pid <> pg_backend_pid();"""
    )

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    cur.close()
    conn.close()


def create_tables(db_name: str) -> None:
    """Функция для создания таблиц в БД PostgreSQL."""

    params = config()
    conn = psycopg2.connect(dbname=db_name, **params)
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""SELECT pg_terminate_backend(pg_stat_activity.pid)
                            FROM pg_stat_activity
                            WHERE pg_stat_activity.datname = '{db_name}'
                            AND pid <> pg_backend_pid();"""
                )
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS employers ("
                    "employer_id int PRIMARY KEY, "
                    "employer_name varchar(255) NOT NULL, "
                    "employer_url varchar(255))"
                )
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS vacancies ("
                    "vacancy_id int PRIMARY KEY,"
                    "vacancy_name varchar(255) NOT NULL,"
                    "vacancy_url varchar(255),"
                    "salary_from real,"
                    "salary_to real,"
                    "currency varchar(10),"
                    "employer_id int NOT NULL, "
                    "CONSTRAINT fk_employer_id FOREIGN KEY (employer_id) REFERENCES employers(employer_id))"
                )
    finally:
        conn.close()


def insert_employers(db_name: str) -> None:
    """Функция для добавления списка работодателей в таблицу."""

    employers = HeadHunterEmployers().get_employers()
    params = config()
    conn = psycopg2.connect(dbname=db_name, **params)
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""SELECT pg_terminate_backend(pg_stat_activity.pid)
                            FROM pg_stat_activity
                            WHERE pg_stat_activity.datname = '{db_name}'
                            AND pid <> pg_backend_pid();"""
                )
                cur.execute("TRUNCATE TABLE employers CASCADE")
                for employer in employers:
                    cur.execute(
                        "INSERT INTO employers VALUES (%s, %s, %s)",
                        (employer["id"], employer["name"], employer["url"]),
                    )
    finally:
        conn.close()


def insert_vacancies(db_name: str) -> None:
    """Функция для добавления списка работодателей в таблицу."""

    employers = HeadHunterEmployers().get_employers()
    params = config()
    conn = psycopg2.connect(dbname=db_name, **params)
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""SELECT pg_terminate_backend(pg_stat_activity.pid)
                            FROM pg_stat_activity
                            WHERE pg_stat_activity.datname = '{db_name}'
                            AND pid <> pg_backend_pid();"""
                )
                cur.execute("TRUNCATE TABLE vacancies")
                for employer in employers:
                    vacancies = HeadHunterVacancies().get_vacancies(employer["id"])
                    for vacancy in vacancies:
                        cur.execute(
                            "INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (
                                vacancy["id"],
                                vacancy["name"],
                                vacancy["url"],
                                vacancy["salary_from"],
                                vacancy["salary_to"],
                                vacancy["currency"],
                                vacancy["employer_id"],
                            ),
                        )
    finally:
        conn.close()
