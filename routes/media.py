from app import app
from flask import jsonify, request
from controller.aws.s3_buckets import S3Bucket


@app.route('/api/media', methods=["GET", "POST", "DELETE"])
def media():
    args = request.args
    bucket_name = args.get("bucket")    
    if not bucket_name:
        return jsonify({"message": "missing query param 'bucket'"}), 400
    
    s3 = S3Bucket(bucket_name=bucket_name)
    if request.method == "GET":
        if args.get("prefix"):
            s3.list_files_by_prefix(args.get("prefix"))
        else:
            s3.list_files(args.get("bucket"))
        return jsonify(s3.contents), 200
    
    elif request.method == "POST":
        try:
            file_to_upload = request.files["image"]
            if args.get("type") == "seasonal":
                s3.upload_file("st-joseph-seasonal",file_to_upload.filename, file_to_upload, path=args.get("month"))
                return jsonify({
                    "message":s3.response_message.get("success").format(file_to_upload.filename,"st-joseph-seasonal"),
                    "image":s3.image_url_seaonsal.format(args.get("month"),file_to_upload.filename)
                    }), 200
            else:
                s3.upload_file("st-joseph-media",file_to_upload.filename, file_to_upload,path=args.get("type"))
                return jsonify({
                    "message":s3.response_message.get("success").format(file_to_upload.filename,"st-joseph-media"),
                    "image":s3.image_url.format(args.get("type"), file_to_upload.filename)
                    }), 200
        except Exception as e:
            print(e)
            return jsonify({"error":e.__dict__.get("message")}), 500

    elif request.method == "DELETE":
        try:
            s3.delete_file(args.get("bucket"),args.get("filename"))
            return jsonify({"message":"Deleted {}".format(args.get("filename"))}), 200
        except Exception as e:
            return jsonify({"error":e.__dict__.get("message")}), 500