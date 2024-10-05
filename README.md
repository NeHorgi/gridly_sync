**Synchronization**

This script implements an algorithm to synchronize multiple tables, including Google Sheets,
database tables, and Gridly tables. It retrieves the latest information from a Google Sheet,
compares it with the data in the database, and if differences are found, treats them as updates.
These updates are then applied to both the database and the corresponding Gridly table.

The architecture of the table synchronizer assumes that Google Sheets is the primary source of truth for updates.
All changes are made in the Google Sheet, and those changes are synchronized with the other tables.

**Environment and Installation**

Before using the script, please ensure the following:

You have a copy of the Google Sheet saved to your Google Drive and you open a public access to it for everyone, who have a link.
You have registered with the Gridly service, created a test project, and set up two test tables (Grids)
by importing data from Google Sheets. You can find a copy of the Google Sheet
in the root directory of this repository as a backup.

Steps to follow before running the script:

Install the dependencies from requirements.txt:
```bash
pip install -r requirements.txt
```


Run the following script to create the database and make some initial changes for testing:
```bash
python database_creation.py
```
In the .env file, specify the following environment variables:

 - GOOGLE_SHEETS_URL – the link to your Google Sheet (Note: use the link up to the gid parameter, e.g. "https://docs.google.com/spreadsheets/d/{your_sheet_ID}/edit?")
 - GOOGLE_SHEET_GAME_GID – gid of the GAME TEXT table. 
 - GOOGLE_SHEET_STATIC_GID – gid of the STATIC TEXTS table. 
 - GRIDLY_API_KEY – your Gridly API key. 
 - GRIDLY_PROJECT_ID – the ID of your Gridly project. 
 - GRIDLY_GAME_TEXT_GRID_ID – the GRID ID of the GAME TEXT table in Gridly. 
 - GRIDLY_STATIC_TEXTS_GRID_ID – the GRID ID of the STATIC TEXTS table in Gridly. 
 - GRIDLY_GAME_TEXT_VIEW_ID – the VIEW ID of the GAME TEXT table in Gridly. 
 - GRIDLY_STATIC_TEXTS_VIEW_ID – the VIEW ID of the STATIC TEXTS table in Gridly. 

**Usage**

To use the script, update or add information to the Google Sheet, and then run the following command to synchronize the data:
```bash
python main.py
```
**Contacts**

Email: lesha.hodus@gmail.com
LinkedIn: Aleksei Khodus
