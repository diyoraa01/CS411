from flask import Flask, request
from flask_cors import CORS
from flask import jsonify

app = Flask(__name__)
CORS(app)

@app.route('/api/hello')
def hello():
    return jsonify({'text': 'Hello World!'})

if __name__ == '__main__':
    app.run(debug=True,port="3052")