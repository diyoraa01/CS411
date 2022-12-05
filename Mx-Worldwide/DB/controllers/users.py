#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import app, db
from flask import Flask, jsonify, request, abort
from datetime import datetime
from models.user import User
from models.music import Music




# create a new user after login with OAuth
@app.route('/create_user', methods=['POST'])
def create_user():
    if not request.json or not 'name' in request.json or not 'password' in request.json:
        print("Wrong format of request in create_user: ", request)
        abort(400)
    re = request.json
    db['users'].insert_one({
        'name': re['name'],
        'gender': re['gender'],
        'language': re['language'],
        'music_history': {}
    })
    
    # user = User(name=request.json['name'], password=request.json['password']).save()
    return jsonify({'userinfo': User.objects.all()}), 201


# get the user information by (user name or user id)?
@app.route('/get_user', methods=['GET'])
def get_user():
    name = request.json


    return jsonify({'userinfo': User.objects(name=name).all()}), 201



'''

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




@app.route('/todo/api/v1/user', methods=['GET'])
def get_user():
    devices = Device1.objects().all()
    print (devices) 
    
    user = User.objects(name="test2").first()
    print (user)
    
    #user.update(device=device)
    #user.update(devices=devices)
    #print device.devicename
    
    #user.update(emdevices=devices)

    return jsonify({'userinfo': User.objects.all()}), 201

@app.route('/todo/api/v1/user', methods=['POST'])
def create_user():
    if not request.json or not 'name' in request.json or not 'password' in request.json:
        print(request)
        abort(400)
    
    user = User(name=request.json['name'], password=request.json['password']).save()
    return jsonify({'userinfo': User.objects.all()}), 201

'''