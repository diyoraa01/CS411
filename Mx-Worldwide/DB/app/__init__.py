from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS
import flask_login

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

#client = MongoClient('localhost', 27017, username='username', password='password')
client = MongoClient('localhost', 27017)

#begin code used for login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


def get_database():
    return client['Mx_world']



if __name__ == "__main__":   
  
   # Get the database
   db = get_database()



