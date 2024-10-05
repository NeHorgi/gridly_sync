import os

from configs.config import Config
from integration.database import DatabaseTable
from integration.google_sheet import GoogleSheet
from utils.database import StaticTextsRecordData, GameTextRecordData

FLAG_FILE = 'module_run.flag'


def main():

    if os.path.exists(FLAG_FILE):
        print("Database with tables already exists and not needed to be created again.")
        return

    with open(FLAG_FILE, 'w') as f:
        f.write('Database with tables was created.')

    config = Config()
    google_sheet = GoogleSheet(url=os.environ.get('GOOGLE_SHEETS_URL'))
    staic_texts_table, game_text_table = DatabaseTable(StaticTextsRecordData), DatabaseTable(GameTextRecordData)

    for table_gid in [config.static_text_sheet_gid, config.game_text_sheet_gid]:
        table_data = google_sheet.get_data_from_table(table_gid=table_gid)
        if table_gid == config.static_text_sheet_gid:
            staic_texts_table.insert_data_in_db(data=table_data)
        elif table_gid == config.game_text_sheet_gid:
            game_text_table.insert_data_in_db(data=table_data)

    print(f"Database was successfully created. Tables in it are fill.")
    print()

    staic_texts_table.create_changes_in_database()
    game_text_table.create_changes_in_database()

    print(f"Tables were successfully updated for tests.")


if __name__ == '__main__':
    main()
