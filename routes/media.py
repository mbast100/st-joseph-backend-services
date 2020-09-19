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
    
    elif request.method == "POST":
        try:
            file_to_upload = request.files["image"]
            s3.upload_file(args.get("bucket"),file_to_upload.filename, file_to_upload)
            return jsonify({"message":"uploaded {} to {}".format(file_to_upload.filename, args.get("bucket"))}), 200
        except Exception as e:
            return jsonify({"error":e.__dict__.get("message")}), 500

    elif request.method == "DELETE":
        try:
            s3.delete_file(args.get("bucket"),args.get("filename"))
            return jsonify({"message":"Deleted {}".format(args.get("filename"))}), 200
        except Exception as e:
            return jsonify({"error":e.__dict__.get("message")}), 500