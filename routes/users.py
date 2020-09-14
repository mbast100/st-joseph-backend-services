from app import app
from flask import jsonify, request, make_response
from controller.aws.get_users import *
from controller.aws.post_users import *
from controller.aws.put_users import *
from controller.aws.delete_users import *
from api_exception import ApiException

"""
Users API
- GET: returns all users in the DB
    - if successful, status code: 200 (OK)
    - if no users are found, returns and empty payload, status code: 404 (NOT FOUND)
- POST: creates and adds user to the DB, generates user ID
    - if successful, status code: 201 (CREATED)
    - if information in payload is missing, status code: 406 (NOT ACCEPTABLE)
    - if email already exists in DB, status code: 406 (NOT ACCEPTABLE)
    - if schema error, return 400 (BAD REQUEST)
- PUT: modifies a user in the DB given a user ID
    - if successful, status code: 200 (OK)
    - if user not found, status code: 404 (NOT FOUND)
    - if information in payload is missing, status code: 406 (NOT ACCEPTABLE)
    - if email already exists in DB, status code: 406 (NOT ACCEPTABLE)
    - if schema error, return 400 (BAD REQUEST)
- DELETE: deletes a user from the DB given a user ID
    - if successful, status code: 200 (OK)
    - if user not found, status code: 404 (NOT FOUND)
"""


@app.route('/api/users', methods=['POST', 'GET'])
def users_api():
    if request.method == 'GET':
        users = get_all_users()
        response = make_response(jsonify(users), 200)
        response.headers["Content-Range"] = len(users)
        response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
        return response

    if request.method == 'POST':
        data = request.get_json()
        try:
            response = post_users(data)
            if response['status_code'] == 201:
                return jsonify({
                    'message': response['message']
                }), response['status_code']
            elif response['status_code'] == 400:
                return jsonify({'message': response['message']}), 400
            elif response['status_code'] == 406:
                return jsonify({'message': response['message']}), 406
        except ApiException as e:
            return jsonify({'message': str(e)}), 406


@app.route('/api/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_id_api(user_id):
    if request.method == 'GET':
        response = get_user_by_id(user_id)
        if response['status_code'] == 200:
            return jsonify(response['message']), response['status_code']
        else:
            return jsonify({'message': response['message']}), 400

    if request.method == 'PUT':
        data = request.get_json()
        try:
            response = put_users(data, user_id)
            if response['status_code'] == 200:
                return jsonify({
                    'message': response['message']
                }), response['status_code']
            elif response['status_code'] == 404:
                return jsonify({'message': response['message']}), 404
            elif response['status_code'] == 400:
                return jsonify({'message': response['message']}), 400
            elif response['status_code'] == 406:
                return jsonify({'message': response['message']}), 406
        except ApiException as e:
            return jsonify({'message': str(e)}), 406

    if request.method == 'DELETE':
        try:
            response = delete_users(user_id)
            if response['status_code'] == 200:
                return jsonify({
                    'message': response['message']
                }), response['status_code']
            elif response['status_code'] == 404:
                return jsonify({'message': response['message']}), 404
        except ApiException as e:
            return jsonify({'message': str(e)}), 404


@app.route('/api/test/users', methods=['GET'])
def test_users():
    return jsonify({'message': 'User API is up and running.'}), 200
