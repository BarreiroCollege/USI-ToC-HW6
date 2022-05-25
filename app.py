import os

from flask import Flask, request, render_template

from store import FashionStore

app = Flask(__name__)
uploads_dir = os.path.join(app.instance_path, 'data')
app.config['MAX_CONTENT_PATH'] = 999999999
app.jinja_env.filters['to_json'] = lambda v: v.to_json()


@app.route("/", methods=('POST', 'GET'))
def index():
    if request.method == 'POST':
        uf = request.files['file']
        if uf.filename != '':
            uf.seek(0)
            store = FashionStore()
            store.parse_clothes(uf.read().decode('utf-8'))
            dresses = store.dress()
            return render_template('result.html', dresses=dresses)
    return render_template("index.html", **{"greeting": "Hello from Flask!"})
