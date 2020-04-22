# EMLviewer-Project BETA
This web application is a .eml viewer where .eml file (the e-mail) is stored in SQLite DB and the frontend shows its content as a text file (.txt)

# How to run it
1. Ensure you have npm, python, pip, flask and SQLiteStudio installed on your machine
2. Using your (IDE's) terminal, go to EMLviewer/static directory and run "npm install" (ignore if any warnings)
3. Using your (IDE's) terminal, go to EMLviewer/static directory and run "npm run watch"
4. Using your (IDE's) terminal, go to EMLviewer/server directory and run "pip install flask"
5. Using your (IDE's) terminal, go to EMLviewer/server directory and run "python server.py" to start the server

# How it works
1. Press the "Upload" button, you will encounter a Browse Window
2. Navigate through your computer to select your .eml file
3. Press the "Display" button, a new tab with the text of the e-mail will pop up
4. The selected .eml file will be stored in a SQLite database called "database.db"

# Notes
My virtualenv (venv) folder is not uploaded, so please check the requirements.txt file in the EMLviewer folder to see the installed packages. Then, on your production server, create the virtual environment (check here: https://docs.python-guide.org/dev/virtualenvs/) and run "pip install -r requirements.txt".
