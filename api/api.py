import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import sys

sys.path.append('D:\Codes\CloudComputingProject1\TestProject1\classifier')

from image_classification import *

UPLOAD_FOLDER = "D:/Codes/CloudComputingProject1/TestProject1/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config["Debug"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == "":
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_filename(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(path)
            result = evaluate_image(path)
            return result
            #return redirect(url_for('uploaded_file', filename = filename))
   return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


app.run()