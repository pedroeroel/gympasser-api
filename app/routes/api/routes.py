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
            'null',
            'https://gympasser-api.vercel.app/',
            'https://gympasser-admin.vercel.app',
            'https://gympasser-client.vercel.app'
            ],
    'supports_credentials': True,
    'Access-Control-Allow-Credentials': True
    }
}

CORS(api, resources=allowed_urls)

@api.route('/')
def status():
    return jsonify({'message': 'API is online.'}), 202

@api.route('/user', methods=['GET', 'POST'])
def user():

    userList = db.collection('users').stream()
    users = []

    for item in userList:
        users.append(item.to_dict())

    users.sort(key=lambda user: int(user['id']))
    
    if request.method == 'GET':

        return jsonify(users), 200


    data = request.get_json()
    
    if request.method == 'POST':

        newID = 1

        cpf = int(data.get('cpf'))
        newUser = data.get('user')

        for user in users:
            userCPF = user['cpf']
            if cpf == userCPF:
                return jsonify({'message':'ERROR: CPF already exists!'}), 409
            
        if users:
            newID = int(users[-1]['id']) + 1

        try:
            register = db.collection("users").document(f"{newID}")
            register.set({'cpf': cpf, 'id': newID, 'status':'inactive', 'user': newUser})
            return jsonify({'message': 'User created successfully!'}), 201
        except Exception as e:
            return jsonify({'message': f'ERROR! Could not save user: {str(e)}'}), 500

@api.route('/user/<int:cpf>', methods=['GET', 'PUT', 'DELETE'])
def userCPF(cpf):

    if request.method == 'GET':
        userList = db.collection('users').stream()
        users = []

        for item in userList:
            users.append(item.to_dict())
        
        userResult = None

        users.sort(key=lambda user: int(user['id']))

        for item in users:
            userCPF = item['cpf']
            if cpf == userCPF:
                userResult = item
                break

        if not cpf:
            return jsonify({'message':'ERROR: CPF not given.'})

        return jsonify({

            "user":f"{userResult['user']}",
            "cpf":f"{userResult['cpf']}",
            "status":f"{userResult['status']}",
            'id': userResult['id']
            
                        }), 200
    
    elif request.method == 'PUT':
        userList = db.collection('users').stream()
        users = []

        for item in userList:
            users.append(item.to_dict())
        
        userResult = None

        users.sort(key=lambda user: int(user['id']))

        for item in users:
            userCPF = item['cpf']
            if cpf == userCPF:
                userResult = item
                break
        
        data = request.get_json()
        newStatus = data.get('status')
        newUser = data.get('user')

        if not userResult:
            return jsonify({'message': f'ERROR: User with CPF {cpf} not found for update.'}), 404

        update_data = {}
        if newStatus is not None:
            update_data['status'] = newStatus

        if newUser is not None:
            update_data['user'] = newUser

        if not update_data:
            return jsonify({'message': 'ERROR: No data provided for update.'}), 400

        try:
            user_ref = db.collection('users').document(f'{userResult['id']}')
            user_ref.update(update_data)
            return jsonify({'message': f'User with CPF {cpf} updated successfully!'}), 200
        except Exception as e:
            return jsonify({'message': f'ERROR! Could not update user with CPF {cpf}: {str(e)}'}), 500

    elif request.method == 'DELETE':
        userList = db.collection('users').stream()
        users = []

        for item in userList:
            users.append(item.to_dict())
        
        userResult = None

        users.sort(key=lambda user: int(user['id']))

        for item in users:
            userCPF = item['cpf']
            if cpf == userCPF:
                userResult = item
                break

        if not userResult:
            return jsonify({'message': f'ERROR: User with CPF {cpf} not found for deletion.'}), 404
        try:
            user_ref = db.collection('users').document(f"{userResult['id']}")
            user_ref.delete()
            return jsonify({'message': f'User with CPF {cpf} deleted successfully!'}), 200
        except Exception as e:
            return jsonify({'message': f'ERROR! Could not delete user with CPF {cpf}: {str(e)}'}), 500