from flask import Flask
from flask_cors import CORS
app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/api')
def hello_world():
    return 'Hello from flask.'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
