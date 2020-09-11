from app import app
from flask import request, jsonify
from api_exception import ApiException
from controller.aws.dynamodb import DynamoDb


@app.errorhandler(ApiException)
def handle_invalid_service(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/api/services', methods=['GET','POST', 'PUT', 'DELETE'])
def api_services():
    args = request.args
    db = DynamoDb("services")
    if request.method == 'GET':
        if args.get("type"):
            db.get_items_by_type(args.get("type"))
            if len(db.items) == 0:
                return jsonify({"message":"no items found for type: '{}'".format(args.get("type"))}), 404
            return jsonify(db.items), 200

    elif request.method == "POST":
        data = request.get_json()
        if args.get("type") == "seasonal":
            try:
                db.create_seasonal_service(data)
                if db.status_code == 200:
                    return jsonify({"message":"Service created"}), 201
            except Exception as e:
                raise ApiException(e.__dict__.get("message"), status_code=400)
        if args.get("type") == "regular":
            try:
                db.create_regular_service(data)
                print(db.response)
                if db.status_code == 200:
                    return jsonify({"message": "Service created"}), 201
            except Exception as e:
                raise ApiException(e.__dict__.get("message"), status_code=400)

    elif request.method == 'PUT':
        pass
    elif request.method == "DELETE":
        data = request.get_json()
        if not data:
            return jsonify({"message":"missing data"}), 400
        try:
            db.delete(data["name"])
            print(db.response)
            if db.status_code == 200:
                return jsonify({"message": "Service deleted"}), 200
        except Exception as e:
            raise ApiException(e.__dict__.get("message"), status_code=400)
