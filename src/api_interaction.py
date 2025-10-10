import requests
from requests.models import Response


class HeadHunterEmployers:
    """Класс для подключения к API со справочником работодателей платформы hh.ru."""

    def __init__(self) -> None:
        """Метод для инициализации экземпляра класса."""

        self.__url = "https://api.hh.ru/employers"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"sort_by": "by_vacancies_open", "page": "0", "per_page": "10"}
        self.__employers: list = []

    def __connect(self) -> Response:
        """Метод для подключения к API."""

        response = requests.get(self.__url, headers=self.__headers, params=self.__params)
        response.raise_for_status()
        return response

    def get_employers(self) -> list:
        """Метод для получения списка работодателей."""

        result = self.__connect().json()["items"]
        data = []
        for item in result:
            employer = {
                "id": item["id"],
                "name": item["name"],
                "url": item["alternate_url"],
            }
            data.append(employer)
        self.__employers.extend(data)
        return self.__employers


class HeadHunterVacancies:
    """Класс для подключения к API со списком вакансий платформы hh.ru."""

    def __init__(self) -> None:
        """Метод для инициализации экземпляра класса."""

        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"page": "0", "per_page": "50", "only_with_salary": "True"}
        self.__vacancies: list = []

    def __connect(self, employer_id: int) -> Response:
        """Метод для подключения к API."""

        self.__params["employer_id"] = str(employer_id)
        response = requests.get(self.__url, headers=self.__headers, params=self.__params)
        response.raise_for_status()
        return response

    def get_vacancies(self, employer_id: int) -> list:
        """Метод для получения вакансий с hh.ru в формате JSON."""

        result = self.__connect(employer_id).json()["items"]
        data = []
        for item in result:
            if item["salary"]:
                salary_from = item["salary"]["from"] if item["salary"]["from"] else item["salary"]["to"]
                salary_to = item["salary"]["to"] if item["salary"]["to"] else item["salary"]["from"]
                currency = item["salary"]["currency"] if item["salary"]["currency"] else "RUR"
            else:
                salary_from = 0
                salary_to = 0
                currency = "RUR"

            vacancy = {
                "id": item["id"],
                "name": item["name"],
                "url": item["alternate_url"],
                "salary_from": salary_from,
                "salary_to": salary_to,
                "currency": currency,
                "employer_id": employer_id,
            }
            data.append(vacancy)
        self.__vacancies.extend(data)
        return self.__vacancies
