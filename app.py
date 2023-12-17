import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from main import predict

UPLOAD_FOLDER = 'uploads/temp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
PATH_BEFORE = os.path.join(UPLOAD_FOLDER, "")
RESULT_PATH = "static/result.jpg"

image_name = None # nama file image before

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/result")
def output():
    predict(output_dir="static")
    file_path = os.path.join("static", image_name)
    result_path = os.path.join(RESULT_PATH)

    return render_template('output.html', file_path=file_path, result_path=result_path)

@app.route("/", methods=['GET', 'POST'])
def test():
    # hapus file image jika ada
    try:
        for i in os.listdir(UPLOAD_FOLDER): os.remove(os.path.join(UPLOAD_FOLDER, i))
        for i in os.listdir('static'): os.remove(os.path.join('static', i))
    except:
        pass

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            global image_name
            image_name = filename

            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)
            
            with open(image_path, "rb") as f:
                with open(os.path.join('static', image_name), "wb") as fs:
                    fs.write(f.read())

            return redirect(url_for("output"))
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)