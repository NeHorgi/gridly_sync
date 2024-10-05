from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List, Type, Dict

from constants.constants import Constants
from utils.database import Base
from utils.localization_data import LocalizationData


class DatabaseTable:

    def __init__(self, db_table: Type[Base]):
        self.db_table = db_table
        self.__engine = create_engine(f'sqlite:///{Constants.db_name}')
        Base.metadata.create_all(self.__engine)
        self.__sessionmaker = sessionmaker(bind=self.__engine)

    @property
    def session(self):
        return self.__sessionmaker()

    def insert_data_in_db(self, data: List[LocalizationData]):
        """
        Insert data from Google Sheet to the table in database.

        :param data: List of LocalizationData objs as a data from table from Google Sheet.
        """
        session = self.session
        for row in data:
            session.add(self.db_table(record_id=row.record_id,
                                      character=row.character,
                                      russian=row.russian,
                                      english=row.english,
                                      character_limit=row.character_limit,
                                      version=row.version,
                                      narrative_comment=row.narrative_comment))
        session.commit()
        print(
            f"Data with record_id's {[row.record_id for row in data]} was successfully added in table {self.db_table.__tablename__} of database.")

    def update_record_in_db(self, record_id: str, **updated_values: Dict[str, str]):
        """
        Update data in table in database with current record id.

        This method queries the database for a record that matches the provided `record_id`.
        If the record is found, it updates the fields specified in `updated_values` and commits
        changes to the database. If the record is not found, no changes are made and a message is logged.

        If an error occurs during the update process, all changes are rolled back to maintain
        database consistency, and an exception message is logged.

        :param record_id: Record id in table in database.
        :param updated_values: Updated data.
        """
        session = self.session
        try:
            record = session.query(self.db_table).filter_by(record_id=record_id).first()
            if record:
                for key, value in updated_values.items():
                    if hasattr(record, key):
                        setattr(record, key, value)
                session.commit()
                print(
                    f"Record with record_id={record_id} successfully updated in table {self.db_table.__tablename__} of database.")
            else:
                print(
                    f"Record with record_id={record_id} was not founded in table {self.db_table.__tablename__} of database.")
        except Exception as e:
            print(
                f"Error while updating record with record_id={record_id} in table {self.db_table.__tablename__} of database.: {e}")
            session.rollback()

    def get_data_from_table(self) -> List[LocalizationData]:
        """
        Get all data from table from database as a list with LocalizationData objs.

        :return: List of LocalizationData objs as a data from table from database.
        """
        session = self.session
        data_from_db = []
        for record in session.query(self.db_table).all():
            data_from_db.append(LocalizationData(
                record_id=record.record_id,
                character=record.character,
                russian=record.russian,
                english=record.english,
                character_limit=record.character_limit,
                version=record.version,
                narrative_comment=record.narrative_comment
            ))
        if not data_from_db:
            print(f"Data from table is empty, seems like table was not filled.")
        return data_from_db

    def get_record_by_id(self, record_id: str) -> LocalizationData:
        """
        Get a record from table by given record id.

        :param record_id: Record id of the record from table.
        :return: LocalizationData obj as a data from table given by current record id.
        """
        session = self.session
        try:
            record = session.query(self.db_table).filter_by(record_id=record_id).first()
            return LocalizationData(
                record_id=record.record_id,
                character=record.character,
                russian=record.russian,
                english=record.english,
                character_limit=record.character_limit,
                version=record.version,
                narrative_comment=record.narrative_comment
            )
        except Exception as e:
            print(
                f"Error while finding record with record_id={record_id} in table {self.db_table.__tablename__} of database.: {e}")

    def create_changes_in_database(self):
        """
        Method changes some data in tables in database for tests to have different data between Google Sheet tables
        and tables in database.
        """
        for row in self.get_data_from_table()[::2]:
            row.russian = 'Изменено для теста'
            row.english = 'Changed for test'
            self.update_record_in_db(row.record_id, russian=row.russian, english=row.english)
