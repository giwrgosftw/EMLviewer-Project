# EMLviewer-Project BETA
A web application which shows the content of an e-mail (.eml) as a text file (.txt)

# How to run it
1. Ensure you have npm, python, pip and flask installed on your machine.
2. Using your (IDE's) terminal, go to EMLviewer/static directory and run "npm install" (ignore if any warnings).
3. Using your (IDE's) terminal, go to EMLviewer/static directory and run "npm run watch".
4. Using your (IDE's) terminal, go to EMLviewer/server directory and run "pip install flask"
5. Using your (IDE's) terminal, go to EMLviewer/server directory and run "python server.py" to start the server.

# Notes
My virtualenv (venv) folder is not uploaded, so please check the requirements.txt file in the EMLviewer folder to see the installed packages. Then, on your production server, create the virtual environment (run "pip install virtualenv" in your project's directory) and run "pip install -r requirements.txt".
