from flask import Flask, Blueprint, request, jsonify
from firebase_admin import firestore, credentials
import firebase_admin
from flask_cors import CORS
import os
import json

api = Blueprint('api', __name__)

serviceAccountKeyContent = os.environ.get('serviceAccountKey')
serviceAccountKeyPath = 'app/routes/api/key/serviceAccountKey.json'

if serviceAccountKeyContent:
    cred = credentials.Certificate(json.loads(serviceAccountKeyContent))
elif serviceAccountKeyPath:
    cred = credentials.Certificate(serviceAccountKeyPath)
else:
    print('Error: serviceAccountKey not found.')

    cred = None


if cred:
    firebase_admin.initialize_app(cred)

else:
    print("Firebase Admin SDK couldn't initialized.")

db = firestore.client()

allowed_urls = {
    r"/*": {
    'origins':[
            'https://127.0.0.1:5000',
            'null'
            ],
    'supports_credentials': True,
    'Access-Control-Allow-Credentials': True
    }
}

CORS(api, resources=allowed_urls)

@api.route('/')
def status():
    return jsonify({'message': 'API is online.'}), 202

@api.route('/user/<int:cpf>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user(cpf):
    if request.method == 'GET':

        if not cpf:
            return jsonify({'message':'ERROR: CPF not given.'})
        
        userList = db.collection('users').stream()

        users = []

        for item in userList:
            users.append(item.to_dict())

        userResult = None

        for user in users:
            userCPF = user['cpf']
            if cpf == userCPF:
                userResult = user
                break

        return jsonify({

            "user":f"{userResult['user']}",
            "cpf":f"{userResult['cpf']}",
            "status":f"{userResult['status']}"
            
                        }), 200