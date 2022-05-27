import json
import os
from pathlib import Path

from flask import Flask, request, render_template, jsonify

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
    return render_template("index.html")


@app.route("/wardrobe", methods=('GET',))
def wardrobe():
    wardrobe_json = Path().joinpath("data").joinpath("wardrobe.json").absolute()
    assert wardrobe_json.exists() and wardrobe_json.is_file()

    with open(wardrobe_json, "r") as f:
        data = json.loads(f.read())

    return jsonify(
        garments=data['garments'],
        colors=data['colors'],
    )
