from flask import Flask, request, abort, flash, redirect, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import sys
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), 'pkgs'))
from pkgs.sub import thumbnail_generator

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

        try:
            filename = secure_filename(file.filename)
            input_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(input_path)
            thumbnail_generator(text, input_path, "thumbnails/thumbnail.png")

            # clear input folder
            shutil.rmtree(UPLOAD_FOLDER)
            os.makedirs(UPLOAD_FOLDER)

            return jsonify({'status': 'success'}), 200
        except Exception as e:
            print(e)
            abort(500)


@app.route('/thumbnail', methods=['GET'])
def thumbnail():
    try:
        return send_from_directory("thumbnails", "thumbnail.png", as_attachment=True)
    except FileNotFoundError:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True, port=7777)
