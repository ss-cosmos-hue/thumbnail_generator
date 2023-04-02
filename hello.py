from flask import Flask, request, send_file, abort, flash, redirect
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import io
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'pkgs'))
from pkgs.generate import start

app = Flask(__name__)
app.secret_key = "super secret key"
CORS(app)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'input')


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        file = request.files['img']
        text = request.form['imgText']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)
        start(input_path, text)
        try:
            return send_file("thumbnails/thumbnail.png", mimetype='image/png', as_attachment=True)
        except FileNotFoundError:
            abort(404)


if __name__ == '__main__':
    app.run(debug=True)
