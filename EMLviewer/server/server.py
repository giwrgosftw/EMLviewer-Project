# Our Back_end environment - Data processing + Application logic

import os
import logging
# import flask_cors  # Cross-origin resources for all domains sharing/returning

from flask import Flask, render_template, request, session, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import eml_converter
import database

# from flask_cors import CORS, cross_origin


# Create our log file for tracking

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('WELCOME')

UPLOAD_FOLDER = '/tmp'  # Our local folder for uploading
ALLOWED_EXTENSIONS = set(['eml'])  # The set of allowed file extensions (only .eml files)

# Create an Instance and points where the static bundle.js and index.html are
APP = Flask(__name__, static_folder='../static/dist', template_folder='../static')
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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


# Inserts the file to our local directory
def upload_file():
    target = os.path.join(UPLOAD_FOLDER)
    # Create the folder/directory if does not exist
    if not os.path.isdir(target):
        os.mkdir(target)

    LOGGER.info("Welcome - The log for the upload has started")
    file_ = request.files['file']
    # Check if the file type is valid and that uploads the file
    if file_ and allowed_file(file_.filename):
        filename = secure_filename(file_.filename)  # secure the files/server
        destination = "/".join([target, filename])
        file_.save(destination)
        session['uploadFilePath'] = destination
        response = "Good job"
        # When pressing the "Upload" button
        eml_converter.metamorphosis(destination)
        database.main()
        database.insert_blob(filename, destination)
        # database.read_blob_data(filename)  # Outside the scope of the project
        # database.read_all_blob_data()  # Outside the scope of the project
        # database.delete_record(filename)  # Outside of scope of the project
        # database.delete_all_records()  # Outside of scope of the project
    return jsonify({"response": response})


# Mapping the URL to the function 'send_file' which sends the content of a file to the client
@APP.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(APP.config['UPLOAD_FOLDER'],
                               filename)


# Execute the whole code
if __name__ == '__main__':
    # Keeps the client-side sessions secure by generating random key (output 24 bytes)
    APP.secret_key = os.urandom(24)
    APP.run()  # run the local server

# flask_cors.CORS(APP, expose_headers='Authorization')
