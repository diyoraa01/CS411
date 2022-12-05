# Get the database using the method we defined in pymongo_test_insert file
from __init__ import get_database
from controllers import users

db = get_database()
db_users = db["users"]

user1 = {
        'name': 'test1',
        'gender': 'male',
        'language': 'English',
        'music_history': {}
}

user2 = {
        'name': 'test2',
        'gender': 'female',
        'language': 'Japanese',
        'music_history': {}
}

db_users.insert_many([user1, user2])
