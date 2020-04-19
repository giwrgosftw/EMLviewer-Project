# Our Back_end environment - Data processing + Application logic

import os
import logging
# import flask_cors  # Cross-origin resources for all domains sharing/returning

from flask import Flask, render_template, request, session, jsonify, send_from_directory
from werkzeug.utils import secure_filename
# from flask_cors import CORS, cross_origin


# Create our log file for tracking
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('WELCOME')

UPLOAD_FOLDER = './'  # Our local folder for uploading
LOAD_FOLDER = '/tmp'  # Our local folder for loading the new version of the uploaded file type .txt
ALLOWED_EXTENSIONS = set(['eml'])  # The set of allowed file extensions (only .eml files)

APP = Flask(__name__, static_folder='../static/dist', template_folder='../static')
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
APP.config['LOAD_FOLDER'] = LOAD_FOLDER


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

    LOGGER.info("Welcome to upload`")
    file_ = request.files['file']
    # Check if the file type is valid and that uploads the file
    if file_ and allowed_file(file_.filename):
        filename = secure_filename(file_.filename)
        destination = "/".join([target, filename])
        file_.save(destination)
        session['uploadFilePath'] = destination
        response = "Good job"
        os.system('python eml_converter.py')
        os.remove("./" + filename)
    return jsonify({"response": response})


# Mapping the URL to the function 'send_file' which sends the content of a file to the client
@APP.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(APP.config['LOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    APP.secret_key = os.urandom(24)
    APP.run()

# flask_cors.CORS(APP, expose_headers='Authorization')
