import requests
import json

from typing import List, Dict
from configs.config import Config
from utils.localization_data import LocalizationData

config = Config()


class GridlyTable:
    """
    Class for work with Gridly table.
    """

    def __init__(self, view_id: str, table_name: str | None = None):
        self.view_id = view_id
        self.table_name = table_name
        self.url = f'https://api.gridly.com/v1/views/{self.view_id}/records/'
        self.__headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'ApiKey {config.gridly_api_key}'
        }

    @staticmethod
    def __prepare_data(data: LocalizationData) -> List[Dict[str, str | List[Dict[str, str]]]]:
        """
        Get prepared to add in the table in Gridly data.

        This method converts a `LocalizationData` object into the format required by Gridly's API.
        It maps the properties of `LocalizationData` to the corresponding column identifiers in the Gridly table.

        :param data: LocalizationData obj as a data what need to be prepared as a part of request.

        :return: List with dict with prepared data for inserting in request.
        """
        prepared_data = [{
            "id": data.record_id,
            "cells": [{
                "columnId": "column1",
                "value": data.character},
                {"columnId": "column2",
                 "value": data.russian},
                {"columnId": "column3",
                 "value": data.english},
                {"columnId": "column4",
                 "value": data.character_limit},
                {"columnId": "column5",
                 "value": data.version},
                {"columnId": "column6",
                 "value": data.narrative_comment}]
        }]
        return prepared_data

    def add_row(self, data: LocalizationData):
        """
        Add current prepared data as a new row to the table in Gridly.

        :param data: LocalizationData obj as data to be added in the table in Gridly.
        """
        data_to_add = self.__prepare_data(data)
        response = requests.post(self.url, headers=self.__headers, data=json.dumps(data_to_add))
        if response.status_code in range(200, 300):
            print(f"Data was successfully added to the table {self.table_name}.")
        else:
            print(f"Error while adding data to the table {self.table_name}: {response.status_code} - {response.text}")

    def update_row(self, data):
        """
        Update row with the same record_id by given prepared data.

        :param data: LocalizationData obj as data to be added in the table in Gridly.
        """
        data_to_update = self.__prepare_data(data)
        response = requests.patch(self.url, headers=self.__headers, data=json.dumps(data_to_update))
        if response.status_code in range(200, 300):
            print(f"Data was successfully updated in the table {self.table_name}.")
        else:
            print(f"Error while updating data in the table {self.table_name}: {response.status_code} - {response.text}")

    def get_data_from_table(self) -> List[LocalizationData]:
        """
        Get data from the Gridly table and converts it into a list of LocalizationData objs.

        This method makes a GET request to the Gridly API, retrieves the table data in JSON format,
        and converts each row into a LocalizationData obj, where each row's record_id
        and associated cells are mapped to the appropriate attributes in the LocalizationData obj.

        :return: List of LocalizationData objs as a data from Gridly table.
        """
        try:
            table_data = []
            for row in requests.get(self.url, headers=self.__headers).json():
                record_id = row['id']
                cells = []
                for cell in row['cells']:
                    cells.append(cell['value'])
                table_data.append(LocalizationData(record_id, *cells))
            return table_data
        except Exception as e:
            print(f"Error while getting table {self.table_name} from Gridly: {e}")
