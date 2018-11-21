from flask import Flask
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')

CORS(app)
api = Api(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
