import requests

from typing import List
from bs4 import BeautifulSoup
from utils.localization_data import LocalizationData


class GoogleSheet:

    def __init__(self, url):
        self.url = url

    def get_data_from_table(self, table_gid: str) -> List[LocalizationData]:
        """
        Get data from current table from Google Sheet as a list with LocalizationData objs.

        :param table_gid: id of list from Google Sheet with current table.
        :return: list of LocalizationData objs, every LocalizationData obj contains data from row from table.
        """
        try:
            html = requests.get(self.url + f'gid={table_gid}#gid={table_gid}').text
            soup = BeautifulSoup(html, features="html.parser")
            table = soup.find_all('table')[0]
            rows = [[td.text for td in row.find_all("td")] for row in table.find_all('tr')]
            filtered_rows = [row for row in rows if row]
            filtered_not_empty_rows = [row for row in filtered_rows if any(item != '' for item in row)]
            table_data = []
            for row in filtered_not_empty_rows[1:]:
                record_id = row[0]
                if not record_id:
                    raise RuntimeError(f"Record ID column is necessary, please, add it and try again.")
                localization_data = [record_id]
                for data in row[1:]:
                    localization_data.append(data)
                table_data.append(LocalizationData(*localization_data[:7]))
            return table_data
        except Exception as e:
            print(f"Error while getting data from table from Google Sheet: {e}")
