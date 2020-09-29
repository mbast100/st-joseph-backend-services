from app import app
from flask import request, jsonify, make_response
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

        elif args.get("month"):
            db.get_items_by_month(args.get("month"))
            if len(db.items) == 0:
                return jsonify({"message":"no items found for month: '{}'".format(args.get("month"))}), 404
            return jsonify(db.items),200

        else:
            db.get_all_items()
            response = make_response(jsonify(db.items), 200)
            response.headers["Content-Range"] = len(db.items)
            response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
            return response

    elif request.method == "POST":
        data = request.get_json()
        if db.service_exists(data["name"]):
            return jsonify({"message":"duplicate service name"}), 400

        try:
            if args.get("type") == "seasonal":
                db.create_seasonal_service(data)
            if args.get("type") == "regular":
                db.create_regular_service(data)

            if db.status_code == 200:
                return jsonify({"message": "Service created"}), 201
        except Exception as e:
            raise ApiException(e.__dict__.get("message"), status_code=400)

    elif request.method == 'PUT':
        data = request.get_json()
        if db.service_exists(args.get("name")):
            try:
                db.update_service(args.get("name"), data)
                return jsonify({"message":"updated {}".format(args.get("name"))}), 200
            except Exception as e:
                raise ApiException(e.__dict__.get("message"), status_code=400)
        return jsonify({"message":"no service found with the following name: {}".format(args.get("name"))}), 404

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
