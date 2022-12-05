#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import app, db
from flask import Flask, jsonify, request, abort
from datetime import datetime
from models.user import User
from models.music import Music




# create a new music info after a user search a music
@app.route('/create_music', methods=['POST'])
def create_music():
    if not request.json or not 'name' in request.json or not 'password' in request.json:
        print("Wrong format of request in create_music: ", request)
        abort(400)
    re = request.json
    #user = re['user']
    db['music'].insert_one({
        'musicname': re['musicname'],
        'author': re['author']
    })
    
    # user = User(name=request.json['name'], password=request.json['password']).save()
    return jsonify({'userinfo': User.objects.all()}), 201


# insert a music into user's music history
@app.route('/insert_music', methods=['POST'])
def create_music():
    if not request.json or not 'name' in request.json or not 'password' in request.json:
        print("Wrong format of request in create_music: ", request)
        abort(400)
    re = request.json
    user = re['user']
    db['music'].insert_one({
        'musicname': re['musicname'],
        'author': re['author']
    })
    # find user according to name
    db.users.find({'name': "$user"})
    
    # user = User(name=request.json['name'], password=request.json['password']).save()
    return jsonify({'userinfo': User.objects.all()}), 201




#  
@app.route('/get_music', methods=['GET'])
def get_user():
    name = request.json

    return jsonify({'musicinfo': User.objects(musicname=name).all()}), 201

