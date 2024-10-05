from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class StaticTextsRecordData(Base):
    __tablename__ = 'Static Texts'
    id = Column(Integer, primary_key=True)
    record_id = Column(String)
    character = Column(String)
    russian = Column(String)
    english = Column(String)
    character_limit = Column(String)
    version = Column(String)
    narrative_comment = Column(String)


class GameTextRecordData(Base):
    __tablename__ = 'Game Text'
    id = Column(Integer, primary_key=True)
    record_id = Column(String)
    character = Column(String)
    russian = Column(String)
    english = Column(String)
    character_limit = Column(String)
    version = Column(String)
    narrative_comment = Column(String)
