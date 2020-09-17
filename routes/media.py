from app import app
from flask import jsonify, request
from controller.aws.s3_buckets import S3Bucket


@app.route('/api/media', methods=["GET", "POST", "DELETE"])
def media():
    s3 = S3Bucket()
    args = request.args
    if request.method == "GET":
        if args.get("bucket"):
            return jsonify(s3.list_files(args.get("bucket"))), 200
        else:
            return jsonify({"message":"missing query param 'bucket'"}), 400