from app import app
from flask import request, jsonify, make_response
from api_exception import ApiException
from data.internal_configurations.internal_configurations import InternalConfigurations


@app.errorhandler(ApiException)
def handle_invalid_service(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/api/internal-configurations', methods=['GET', 'POST', 'PUT'])
def internal_configurations():
    query_params = request.args
    if request.method == "GET":
        internal_configs = InternalConfigurations()
        if query_params.get("feature"):
            return jsonify(internal_configs.find_by("feature", query_params.get("feature"))), 200
        else:
            return jsonify(internal_configs.all), 200

    elif request.method == "POST":
        internal_configs = InternalConfigurations(params=request.get_json())

        if internal_configs.save:
            return jsonify({"message": "Internal Configuration created."}), 200
        else:
            return jsonify({"message": "Internal Configuration not created."}), 400

    elif request.method == "PUT":
        if not query_params.get("feature"):
            return jsonify({"missing query `feature`."}), 400

        internal_configs = InternalConfigurations(
            feature=query_params.get("feature"))

        if internal_configs.exists:
            try:
                if internal_configs.update(request.get_json()):
                    return jsonify({"message": "Succssefuly upated."}), 200
                else:
                    return jsonify({"message": "Something went wrong while upating."}), 200
            except Exception as e:
                raise ApiException(e.message, 500)

        else:
            return jsonify({"message": "`{}`feature not found.".format(query_params.get("feature"))}), 404
