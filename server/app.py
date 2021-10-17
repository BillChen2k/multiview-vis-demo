from flask import Flask
from flask_cors import CORS
import core
app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/api')
def hello_world():
    return 'This is the api.'

@app.route('/api/generate')
def generate():
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
