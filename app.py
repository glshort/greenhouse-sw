#!/home/glshort/greenhouse/venv/bin/python

import os
import json
from flask import Flask, send_from_directory
from config import get_gpio_cfg

gpio_cfg = get_gpio_cfg()

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/get')
def get():
    return json.dumps({'L1': 100}, indent=4)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)

