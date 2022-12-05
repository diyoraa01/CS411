from flask import Flask, render_template, request, jsonify
from DB.music import get_music, get_musics_by_user
from DB.comment import add_comment, update_comment, delete_comment
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import flask_login
import config

# create the database
client = MongoClient('localhost', 27017)
db = client.flask_db
todos = db.todos

# connect with Mongodb compass







# start flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


#begin code used for login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/users', methods=['POST', 'GET'])
def data():
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        firstName = body['firstName']
        lastName = body['lastName']
        emailId = body['emailId'] 
        # db.users.insert_one({
        db['users'].insert_one({
            "firstName": firstName,
            "lastName": lastName,
            "emailId":emailId
        })
        return jsonify({
            'status': 'Data is posted to MongoDB!',
            'firstName': firstName,
            'lastName': lastName,
            'emailId':emailId
        })
    
    # GET all data from database
    if request.method == 'GET':
        allData = db['users'].find()
        dataJson = []
        for data in allData:
            id = data['_id']
            firstName = data['firstName']
            lastName = data['lastName']
            emailId = data['emailId']
            dataDict = {
                'id': str(id),
                'firstName': firstName,
                'lastName': lastName,
                'emailId': emailId
            }
            dataJson.append(dataDict)
        print(dataJson)
        return jsonify(dataJson)


@app.route('/users/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):

    # GET a specific data by id
    if request.method == 'GET':
        data = db['users'].find_one({'_id': ObjectId(id)})
        id = data['_id']
        firstName = data['firstName']
        lastName = data['lastName']
        emailId = data['emailId']
        dataDict = {
            'id': str(id),
            'firstName': firstName,
            'lastName': lastName,
            'emailId':emailId
        }
        print(dataDict)
        return jsonify(dataDict)
        
    # DELETE a data
    
    
    # UPDATE a data by id
    
    if request.method == 'PUT':
        body = request.json
        firstName = body['firstName']
        lastName = body['lastName']
        emailId = body['emailId']

        db['users'].update_one(
            {'_id': ObjectId(id)},
            {
                "$set": {
                    "firstName":firstName,
                    "lastName":lastName,
                    "emailId": emailId
                }
            }
        )

        print('\n # Update successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is updated!'})



@app.route('/comment', methods=["POST"])
#@jwt_required
def api_post_comment():
    """
    Posts a comment about a specific music. Validates the user is logged in by
    ensuring a valid JWT is provided
    """
    #claims = get_jwt_claims()
    #user = User.from_claims(claims)
    post_data = request.get_json()
    try:
        music_id = expect(post_data.get('music_id'), str, 'music_id')
        comment = expect(post_data.get('comment'), str, 'comment')
        add_comment(music_id, user, comment, datetime.now())
        updated_comments = get_music(music_id).get('comments')
        return jsonify({"comments": updated_comments}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/comment', methods=["PUT"])
#@jwt_required
def api_update_comment():
    """
    Updates a user comment. Validates the user is logged in by ensuring a
    valid JWT is provided
    """
#    claims = get_jwt_claims()
    user_email = "jane.doe@example.com"
    post_data = request.get_json()
    try:
        comment_id = expect(post_data.get('comment_id'), str, 'comment_id')
        updated_comment = expect(post_data.get(
            'updated_comment'), str, 'updated_comment')
        music_id = expect(post_data.get('music_id'), str, 'music_id')
        edit_result = update_comment(
            comment_id, user_email, updated_comment, datetime.now()
        )
        if edit_result.modified_count == 0:
            raise ValueError("no document updated")
        updated_comments = get_music(music_id).get('comments')
        return jsonify({"comments": updated_comments}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/comment', methods=["DELETE"])
#@jwt_required
def api_delete_comment():
    """
    Delete a comment. Requires a valid JWT
    """
#    claims = get_jwt_claims()
    user_email = "jane.doe@example.com"
    post_data = request.get_json()
    try:
        comment_id = expect(post_data.get('comment_id'), str, 'comment_id')
        music_id = expect(post_data.get('music_id'), str, 'music_id')
        delete_comment(comment_id, user_email)
        updated_comments = get_music(music_id).get('comments')
        return jsonify({'comments': updated_comments}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


def expect(input, expectedType, field):
    if isinstance(input, expectedType):
        return input
    raise AssertionError("Invalid input for type", field)






    
if __name__ == '__main__':
    app.debug = True
    app.run()
