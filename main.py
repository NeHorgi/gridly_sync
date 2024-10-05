from typing import Dict, List
from configs.config import Config
from integration.database import DatabaseTable
from integration.google_sheet import GoogleSheet
from integration.gridly import GridlyTable
from utils.database import GameTextRecordData, StaticTextsRecordData
from utils.localization_data import LocalizationData


def get_updated_data(google_sheet_table_data: LocalizationData, database_table_data: LocalizationData) \
        -> Dict[str, str] | None:
    """
    Get difference between two LocalizationData objs as an updated data in Google Sheet table.

    Method gets two objs, looking for attrs of first one, compares it with attrs of second one.
    If it finds any changes, collect it to the dict, where key is an updated attr, and value is a new value.

    :param google_sheet_table_data: Data from row from Google Sheet table as a LocalizationData obj.
    :param database_table_data: Data from row from database as a LocalizationData obj.

    :return: Dict with updated data from Google Sheet table, if it exists,
    where key is an updated attr, and value is a new value.
    """
    differences = {}
    for attr in google_sheet_table_data.__dict__:
        if getattr(google_sheet_table_data, attr) != getattr(database_table_data, attr):
            differences[attr] = (getattr(google_sheet_table_data, attr))
    return differences


def synchronise_data(google_table: List[LocalizationData], database_table: DatabaseTable, gridly_table: GridlyTable):
    """
    Synchronise data in Google Sheet table, database table and Gridly table.

    Method gets table data from Google Sheet and compare it with data from database table.
    If it finds any difference, it considers that difference as an updating of data and this data should be updated
    in database and Gridly tables.
    If method finds any data, what is in Google Sheet table, but not in the database table, it considers that data
    as a new one, and this data should be added to the database and Gridly tables.

    :param google_table: List of LocalizationData objs as a row's data from table from Google Sheet.
    :param database_table: Database obj as table from database.
    :param gridly_table: GridlyTable obj as a table from Gridly.
    """
    data_to_add = []
    for google_table_row in google_table:
        try:
            database_row = database_table.get_record_by_id(google_table_row.record_id)
            if google_table_row != database_row:
                updated_data = get_updated_data(google_table_row, database_row)
                database_table.update_record_in_db(google_table_row.record_id, **updated_data)
                gridly_table.update_row(google_table_row)
        except AttributeError:
            data_to_add.append(google_table_row)
    if data_to_add:
        database_table.insert_data_in_db(data_to_add)
        for data in data_to_add:
            gridly_table.add_row(data)


def main():
    config = Config()

    google_sheet = GoogleSheet(config.google_sheet_url)
    game_text_table_data = google_sheet.get_data_from_table(table_gid=config.game_text_sheet_gid)
    static_texts_table_data = google_sheet.get_data_from_table(table_gid=config.static_text_sheet_gid)

    assert game_text_table_data, f"Google Sheet Game Text table wasn't collected, something went wrong."
    assert static_texts_table_data, f"Google Sheet Static Texts table wasn't collected, something went wrong."

    game_text_gridly_table = GridlyTable(config.gridly_game_text_view_id)
    static_texts_gridly_table = GridlyTable(config.gridly_static_texts_view_id)

    game_text_gridly_table_data = game_text_gridly_table.get_data_from_table()
    static_texts_gridly_table_data = static_texts_gridly_table.get_data_from_table()

    assert game_text_gridly_table_data, f"Gridly Game Text table wasn't collected, something went wrong."
    assert static_texts_gridly_table_data, f"Gridly Game Text table wasn't collected, something went wrong."

    game_text_database_table = DatabaseTable(GameTextRecordData)
    static_texts_database_table = DatabaseTable(StaticTextsRecordData)

    if game_text_table_data == game_text_database_table.get_data_from_table() \
            and static_texts_table_data == static_texts_database_table.get_data_from_table():
        print(f"No changes are needed to add to Gridly.")
        return

    synchronise_data(static_texts_table_data, static_texts_database_table, static_texts_gridly_table)
    synchronise_data(game_text_table_data, game_text_database_table, game_text_gridly_table)

    print(f"Tables were successfully synchronised.")


if __name__ == '__main__':
    main()
