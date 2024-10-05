from dataclasses import dataclass


@dataclass
class LocalizationData:
    record_id: str
    character: str
    russian: str
    english: str
    character_limit: str
    version: str
    narrative_comment: str
