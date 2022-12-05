from app import app, db
from flask import Flask, jsonify, request, abort
from datetime import datetime
from models.user import User
from models.music import Music


def add_comment(music_id,name , email, comment, date):
    
    comment_doc = { 'music_id' : music_id, 'name' : name, 'email' : email,'text' : comment, 'date' : date}
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