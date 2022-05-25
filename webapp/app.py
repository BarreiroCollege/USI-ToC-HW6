import os
from flask import Flask, request, url_for, redirect, render_template, flash
from store import FashionStore
# from werkzeug import secure_filename

app = Flask(__name__)
uploads_dir = os.path.join(app.instance_path, 'data')
app.config['MAX_CONTENT_PATH'] = 999999999

garments = []


@app.route("/", methods=('POST','GET'))
def index():
    if request.method == 'POST':
        uf = request.files['file']
        if uf.filename != '':
            # uf.save(os.path.join('data/',uf.filename)) # save the file in the data folder
            uf.seek(0)
            store = FashionStore()
            store.parse_clothes(uf.read().decode('utf-8'))
            st = store.dress()
            # with open(os.path.join('data/',uf.filename), 'r') as f:
            #     store.parse_clothes(f.read())
                # store.dress()
            garments.append({'garment': uf.filename, 'color': st})
            return redirect(url_for('result'))
    return render_template("index.html", **{"greeting": "Hello from Flask!"})

@app.route("/result")
def result():
    return render_template('result.html', garments = garments)
   # if request.method == 'POST':
        # f = request.files['file']
        # if not f:
        #    flash('File is required')
        # else:
            # f.save(f.filename)
            # return 'file uploaded successfully'
# def result():