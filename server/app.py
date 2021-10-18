from flask import Flask
from flask_cors import CORS
import core
import pandas as pd
import numpy as np
app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/api')
def hello_world():
    return 'This is the api.'

@app.route('/api/generate')
def generate_graph(csv_path, mv_count, k1, k2):
    # todo: returns graph
    pass

@app.route('/api/test')
def test_api():
    v = np.array([1,2,3])
    return str(v[2])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
