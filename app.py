import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from demo import colorize_picture

input_folder = '../RAW/Input'

app = Flask(__name__)
app.config['input_folder'] = input_folder

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
    
@app.route('/')
def home_page():
    return render_template("home.html")

@app.route('/colorization', methods=["POST"])
def color_page():
    if request.method == 'POST':
        f = request.files['image']
        if f.filename == '':
            return redirect(url_for('home_page'))
        else:
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['input_folder'],filename))

        colorize_picture(filename)
    return render_template('colorization.html')

@app.route('/about')
def about_page():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug= True)