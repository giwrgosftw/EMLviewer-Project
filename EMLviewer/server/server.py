# Our Back_end environment - Data processing + Application logic
# Everything starts from here, server.py is the core of the app's back-end

import os
import logging
import webbrowser
from threading import Timer
from werkzeug.utils import secure_filename

from flask import Flask, render_template, request, session, jsonify
from flask_cors import CORS

import eml_converter
import database_manager
import pony_database

logging.basicConfig(level=logging.INFO)  # Create our log file for tracking
LOGGER = logging.getLogger('WELCOME')  # It should be instantiated through the module-level function
# logging.getLogger('flask_cors').level = logging.DEBUG

UPLOAD_FOLDER = '/tmp'  # Our local folder for uploading
ALLOWED_EXTENSIONS = set(['eml'])  # The set of allowed file extensions (only .eml files)

# Create an Instance and points where the static bundle.js and index.html are
APP = Flask(__name__, static_folder='../static/dist', template_folder='../static')
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # holds the loaded configuration value
CORS(APP)  # enable CORS on the APP


# Check the file type/extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Mapping the URL to index.html
@APP.route('/')
def index():
    return render_template('index.html')


# Mapping the URL to the function 'upload_file'
# Call a function in one route end-point for easier unit and integration
@APP.route('/uploads', methods=['POST'])
def upload():
    return upload_file()


"""
def upload_file() => 
1) Inserts the .eml file to our local directory
2) Converts it to .txt (+ extract its attachments)
3) Saves the .eml file into the database
"""


def upload_file():
    target = os.path.join(UPLOAD_FOLDER)

    # Create the folder/directory if does not exist
    if not os.path.isdir(target):
        os.mkdir(target)

    # An INFO message, this will pop up on the console, in the beginning
    LOGGER.info("Welcome - The log for the upload has started")

    # Holds the uploaded .eml file ||| 'file' in server.py = 'file' Main.jsx
    file_ = request.files['file']

    # Check if the file type is valid and then upload/save the file
    if file_ and allowed_file(file_.filename):
        filename = secure_filename(file_.filename)  # Prevent the unwanted special characters
        destination = "/".join([target, filename])
        file_.save(destination)
        session['uploadFilePath'] = destination

        # When you press the submit/open button to upload the file
        filename_txt = eml_converter.metamorphosis(destination)
        pony_database.add_eml(filename, destination)  # Insert the .eml file to the database

        # The following 6 methods are used to create sqlite3 database
        # So, do not forget to disable the pony_database.add_eml() line from above
        # database_manager.main()  # Create the database table (if not already exists)
        # database_manager.insert_blob(filename, destination)  # Insert the .eml file to the database

        # The following 4 methods work for PONY database NOW too, you do not have to disable it
        # Do not forget to keep the 2 above [database_manager()] methods disable
        # database_manager.read_blob_data(filename)  # Retrieve/Extract the .eml file from the database
        # database_manager.read_all_blob_data()  # Retrieve/Extract all the .eml file from the database
        # database_manager.delete_record(filename)  # Delete the .eml file from the database
        # database_manager.delete_all_records()  # Delete all the .eml files from the database

        """
        # In case that the eml_converter.metamorphosis(destination) doe not work
        # This will convert the .eml to .txt (without its attachments)
        f_name = filename.split(".")[0]
        as_txt = file_.read()
        as_txt = as_txt.decode('utf-8')

        split_lines = as_txt.splitlines()
        txt_destination = "/".join([target, f_name + ".txt"])
        f = open(txt_destination, "w")
        for line in split_lines:
             f.write(line + "\n")
        f.close()
        """

        # This is for the switch buttons, it handles the filename of the .txt file
        with open(filename_txt, 'r') as file_txt:
            response = file_txt.read()
        return jsonify({"response": response, "filename": filename})


# Mapping the URL to the function 'load_file' which sends the content of the .txt file to the client
@APP.route('/load')
def load_file():
    target = os.path.join(UPLOAD_FOLDER)
    # Create the folder/directory if does not exist
    if not os.path.isdir(target):
        os.mkdir(target)
    filename = request.args.get("filename")
    txt_destination = "/".join([target, filename + ".txt"])
    # response = f.read()
    with open(txt_destination, "r") as file_txt:
        response = file_txt.read()
    return jsonify({"response": response})


# Open the browser automatically to the specific local port
def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')


# Execute the whole code
if __name__ == '__main__':
    # Keeps the client-side sessions secure by generating random key (output 24 bytes)
    APP.secret_key = os.urandom(24)
    Timer(1, open_browser).start()  # Open the browser automatically in 1sec
    APP.run()  # Run the local server
