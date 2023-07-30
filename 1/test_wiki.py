import pytest
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from dataclasses import dataclass


TEST_VALUES = [10**7, 1.5 * 10**7, 5 * 10**7, 10**8, 5 * 10**8, 10**9, 1.5 * 10**9]


class TableData:
    def __init__(self, url, table_head, data_class):
        self.url = url
        self.table_head = table_head
        self.data_class = data_class
        self.table_data = self.load_table()

    def load_table(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        # Находим таблицу с нужным названием с помощью BeautifulSoup
        table = None
        for caption in soup.find_all("caption"):
            if self.table_head in caption.get_text().strip():
                table = caption.find_parent("table")
                break

        if table is not None:
            # Парсим таблицу с помощью Pandas
            data = pd.read_html(str(table))[0]
            columns = self.get_columns_by_content(data)
            data.columns = columns  # Синхронизируем столбцы с содержимым строк таблицы
            # Создаем список объектов даткласса
            table_data = []
            for row in data.itertuples(index=False):
                table_item = self.data_class(*row)
                table_data.append(table_item)
            return True, table_data, ""
        
        else:
            return False, [], f"Таблица с названием {self.table_head} не найдена"

    def get_columns_by_content(self, data):
        # Синхронизируем столбцы с содержимым строк таблицы
        columns = []
        for column_name in data.columns:
            for field in self.data_class.__dataclass_fields__:
                if field.lower() in column_name.lower():
                    columns.append(field)
                    break

        return columns

    def get_table_data(self):
        return self.table_data


# Датакласс таблицы "Programming languages used in most popular websites"
@dataclass
class PLofWebsitesTableItem:
    Website: str
    Popularity: str
    Front: str
    Back: str
    Database: str
    Notes: str


# Получить очищенное от ссылок значение Вебсайта
def find_website_value(website_data):
    match = re.search(r"[^\[\]]+", website_data)
    if match:
        return True, str(match.group(0)), ""
    
    return False, "", f"Значение Website в {website_data} не найдено"


# Получить очищенное от ссылок и преобразованное в число значение популярности вебсайта
def find_popularity_value(popularity_data):
    match = re.search(r"(?<!\(|\[)(\d[\d,.]*)", popularity_data)
    if match:
        return True, int(re.sub(r'[,.]', '', match.group(0))), ""
    
    return False, 0, f"Значение Popularity в {popularity_data} не найдено"
    

# Получить список языков Фронтенда
def find_frontend_value(frontend_data):
    if frontend_data:
        return True, frontend_data, ""

    return False, "", f"Значение Front-End в {frontend_data} не найдено"
    

# Получить очищенный от ссылок список языков Бэкенда
def find_backend_value(backend_data):
    match = re.sub(r'\[[^\]]*\]', '', backend_data)
    if match:
        return True, match, ""

    return False, "", f"Значение Back-End в {backend_data} не найдено"
    

@pytest.mark.parametrize(
        "popularity_threshold",  TEST_VALUES
)
def test_wiki(popularity_threshold):
    """
    Проверить, все ли вебсайты из статьи Википедии достаточно популярны по количеству пользователей ежемесячно.
    """

    url = "https://en.wikipedia.org/wiki/Programming_languages_used_in_most_popular_websites"
    table_head = "Programming languages used in most popular websites"

    table_data = TableData(url, table_head, PLofWebsitesTableItem)
    # Получаем данные таблицы в виде списка объектов датакласса PLofWebsitesTableItem
    res, data, error_str = table_data.get_table_data()
    assert res, error_str

    for row in data:
        res, website_value, error_str = find_website_value(row.Website)
        assert res, error_str

        res, popularity_value, error_str = find_popularity_value(row.Popularity)
        assert res, error_str

        res, frontend_value, error_str = find_frontend_value(row.Front)
        assert res, error_str

        res, backend_value, error_str = find_backend_value(row.Back)
        assert res, error_str

        assert popularity_value >= popularity_threshold, \
            f"{website_value} (Frontend: {frontend_value} | Backend: {backend_value}) has {popularity_value} unique visitors per month. (Expected not less than {popularity_threshold})"


# При необходимости раскомментировать
# if __name__ == "__main__":
#     pytest.main([__file__])
