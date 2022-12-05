from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

#client = MongoClient('localhost', 27017, username='username', password='password')
client = MongoClient('localhost', 27017)


def get_database():
    return client['Mx_world']


if __name__ == "__main__":   
  
   # Get the database
   db = get_database()



