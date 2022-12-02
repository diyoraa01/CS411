import bson

from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:

        db = g._database = PyMongo(current_app).db
       
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


"""
Ticket: Create/Update Comments

For this ticket, you will need to implement the following two methods:

- add_comment
- update_comment

You can find these methods below this docstring. Make sure to read the comments
to better understand the task.
"""


def add_comment(movie_id,name , email, comment, date):
    """
    Inserts a comment into the comments collection, with the following fields:

    - "name"
    - "email"
    - "movie_id"
    - "text"
    - "date"

    Name and email must be retrieved from the "user" object.
    """
    
    comment_doc = { 'movie_id' : movie_id, 'name' : name, 'email' : email,'text' : comment, 'date' : date}
    return db.comments.insert_one(comment_doc)


def update_comment(comment_id, user_email, text, date):
    """
    Updates the comment in the comment collection. Queries for the comment
    based by both comment _id field as well as the email field to doubly ensure
    the user has permission to edit this comment.
    """
    # TODO: Create/Update Comments
    # Use the user_email and comment_id to select the proper comment, then
    # update the "text" and "date" of the selected comment.
    response = db.comments.update_one(
        { "comment_id": comment_id },
        { "$set": { "text ": text, "date" : date } }
    )

    return response


def delete_comment(comment_id, user_email):
    """
    Given a user's email and a comment ID, deletes a comment from the comments
    collection
    """

    response = db.comments.delete_one( { "_id": ObjectId(comment_id) } )
    return response