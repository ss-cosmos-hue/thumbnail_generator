from flask import Flask, request, send_file, flash, redirect
from werkzeug.utils import secure_filename
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'pkgs'))
from pkgs.generate import start

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'input')

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/generate', methods=['POST'])
def create_thumbnail():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)  
          
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_path = os.path.join(os.getcwd(), 'output', filename)
        file.save(input_path)
        start(input_path, output_path)
        send_file(output_path, mimetype='image/png')

if __name__ == '__main__':
    app.run()