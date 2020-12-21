from app import app
from flask import request, jsonify, make_response
from api_exception import ApiException
import json
from data.services.services import Services
from utils.auth import validate_token
import os


@app.errorhandler(ApiException)
def handle_invalid_service(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.before_request
def before_request_func():
    if request.method in ["POST", "PUT", "DELETE"] and not app.testing:
        validate_token()


@app.route('/api/services', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_services():
    args = request.args
    query_param = args.to_dict()
    #db = DynamoDb("services")

    if request.method == 'GET':
        services = Services()
        if len(args.to_dict()) == 2:
            data = services.where(query_param)
            if len(data) == 0:
                return jsonify({"message": "No items found for {}.".format(str(query_param))}), 404
            else:
                return jsonify(data), 200

        elif len(args.to_dict()) == 1:
            key = list(query_param.keys())[0]
            data = services.find_by(key, query_param.get(key))
            if len(data) == 0:
                return jsonify({"message": "No items found for {}.".format(str(query_param))}), 404
            return jsonify(data), 200

        else:
            data = Services().all
            response = make_response(jsonify(data), 200)
            response.headers["Content-Range"] = len(data)
            response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
            return response

    elif request.method == "POST":
        data = request.get_json()
        services = Services(params=data, type=args.get("type"))

        if not services.ok or services.exists:
            resp = {}
            if services.error:
                resp["error"] = services.error
            resp["message"] = services.message
            return jsonify(resp), 400

        try:
            if services.save:
                return jsonify({"message": "Service created"}), 201
            else:
                return jsonify({"message": "Something went wrong when trying to create service"}), 500
        except Exception as e:
            raise ApiException(e.__dict__.get("message"), status_code=400)

    elif request.method == 'PUT':
        data = request.get_json()
        if not args.get("name"):
            return jsonify({"message": "Missing query param 'name'."}), 400

        services = Services()
        records = services.find_by("name", args.get("name"))
        if len(records) > 0:
            try:
                services.update(updates=data)
                return jsonify({"message": services.message}), 200
            except Exception as e:
                raise ApiException(e.__dict__.get("message"), status_code=400)
        else:
            return jsonify({"message": "no service found with the following name: {}".format(args.get("name"))}), 404

    elif request.method == "DELETE":
        data = request.get_json()
        if not data:
            return jsonify({"message": "missing data"}), 400

        services = Services(params=data)
        if args.get("type") and args.get("type") == "batch":
            try:
                services.delete_all(data)
            except Exception as e:
                raise ApiException(
                    "Something went wrong when trying t batch delete", 500)
        else:
            try:
                if services.delete:
                    return jsonify({"message": "Service deleted."}), 200

            except Exception as e:
                raise ApiException(e.__dict__.get("message"), status_code=400)
