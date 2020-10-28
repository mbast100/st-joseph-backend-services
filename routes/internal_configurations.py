from app import app
from flask import request, jsonify, make_response
from api_exception import ApiException
from controller.aws.dynamodb import DynamoDb
import json

@app.errorhandler(ApiException)
def handle_invalid_service(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/api/internal-configurations', methods=['GET','POST', 'PUT'])
def internal_configurations():
    args = request.args
    db = DynamoDb("st_joseph_internal_configurations")
    if request.method == "GET":
        data = ""
        if args.get("feature"):
            if not db.internal_configuration_exists(feature=args.get("feature")):
                return jsonify({
                    "message": "`{}` feature not found".format(args.get("feature"))
                    }), 404
            else:
                db.get_internal_configurations(feature=args.get("feature"))  
                data = db.item
        else:
            db.get_internal_configurations()
            data = db.items
        
        return jsonify(data), 200
    
    elif request.method == "POST":
        pass

    elif request.method == "PUT":
        if not args.get("feature"):
            return jsonify({"missing query `feature`."}), 400

        elif db.internal_configuration_exists(args.get("feature")):
            try:
                db.update_internal_configuration(args.get("feature"), request.get_json())
                return jsonify({"message": "Succssefuly upated."}), 200

            except Exception as e:
                raise ApiException(e.message, 500)
        
        else:
            return jsonify({"message": "`{}`feature not found.".format(args.get("feature"))}), 404
        
    


