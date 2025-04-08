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

@api.route('/')
def status():
    return jsonify({'message': 'API is online.'}), 202

@api.route('/user', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user():
    if request.method == 'GET':

        data = request.get_json()

        cpf = data.get('cpf')

        return jsonify('')