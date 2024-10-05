import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    google_sheet_url = os.environ.get('GOOGLE_SHEETS_URL')
    static_text_sheet_gid = os.environ.get('GOOGLE_SHEET_STATIC_GID')
    game_text_sheet_gid = os.environ.get('GOOGLE_SHEET_GAME_GID')
    gridly_api_key = os.environ.get('GRIDLY_API_KEY')
    gridly_grid_id = os.environ.get('GRIDLY_GRID_ID')
    gridly_game_text_view_id = os.environ.get('GRIDLY_GAME_TEXT_VIEW_ID')
    gridly_static_texts_view_id = os.environ.get('GRIDLY_STATIC_TEXTS_VIEW_ID')
