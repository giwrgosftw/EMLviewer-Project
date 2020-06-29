# EMLviewer-Project
This web application is an EML-viewer where the .eml file (the e-mail) is stored in SQLite DB and the frontend shows its content as a text file. 
I used Python-Flask, React.js and PonyORM. It has been tested and works perfectly in python v2.7 (you can find python v2.7 here → https://1drv.ms/u/s!As6B4RGbfxQVgYw4A4mkjuYw_3b4wA?e=agQ6Xg) !

# How to run it
1. Ensure you have npm, python (at least v2.7), pip, requirements and SQLiteStudio installed on your machine
2. Using your (IDE's) terminal, go to EMLviewer/static directory and run "npm install" (ignore if any warnings)
3. Using your (IDE's) terminal, go to EMLviewer/static directory and run "npm run watch"
4. Using your (IDE's) terminal, go to EMLviewer/server directory and run "pip install -r requirements.txt"
5. Using your (IDE's) terminal, go to EMLviewer/server directory and run "python server.py" to start the server

# How it works
1. Press the "Choose file" button, you will encounter in the Browse Window
2. Navigate through your computer to select/open your .eml file
3. The text of the uploaded .eml file will pop up on the same page
4. If you upload more files, you can use the switch/multiple-choice selection button
5. The selected .eml file will be stored in a SQLite database called "database.sqlite"
6. You can manage "database.sqlite" by importing/exporting/deleting .eml files (these functions are outside the scope of the project)
7. The .txt file and the attached files of the e-mail are stored in the local folder path "/tmp/"

# Notes
My virtualenv (venv) folder is not uploaded. So, BEFORE install the "requirements.txt" from the EMLviewer/server folder, create a virtual environment using pyCharm on your production server (check here how: https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html)

# Video link
https://youtu.be/BYUfmsNCzwg
