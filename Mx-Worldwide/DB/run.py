from app import app
from app import get_database

db = get_database()

if __name__ == '__main__':
    app.run(debug=True)
    

