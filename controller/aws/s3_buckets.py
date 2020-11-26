import boto3
import logging
from botocore.exceptions import ClientError
from api_exception import ApiException


class S3Bucket():
    def __init__(self, filename='', bucket_name=""):
        self.s3_client = boto3.client('s3')
        self.s3_resource = boto3.resource('s3')
        self.response = {}
        self.prefix = ''
        self.bucket_name = bucket_name
        self.file_name = filename
        self.message = ""
        self.image_url_seaonsal = "https://st-joseph-seasonal.s3.amazonaws.com/{}/{}"
        self.image_url = "https://st-joseph-media.s3.amazonaws.com/{}/{}"
        self.response_message = {
            "success": "uploaded {} to {}"
        }

    def set_prefix(self,prefix):
        self.prefix = prefix

    @property
    def bucket(self):
        return self.s3_resource.Bucket(self.bucket_name)

    def upload_file(self, bucket, filename, file, path=''):
        try:
            key = filename
            if path:
                key = path+"/"+filename
            self.response = self.s3_resource.Bucket(
                bucket).put_object(Key=key, Body=file)
        except Exception as e:
            raise ApiException(
                "something went wrong while uploading to s3 bucket", 400)

    def delete_file(self, bucket, key):
        try:
            self.response = self.s3_client.delete_object(
                Bucket=bucket, Key=key)
        except Exception as e:
            raise ApiException(
                "something went wrong while deleting o s3 bucket", 400)

    def list_files(self, bucket):
        try:
            contents = []
            self.response = self.s3_client.list_objects(Bucket=bucket)
            for item in self.s3_client.list_objects(Bucket=bucket)['Contents']:
                contents.append(item)
            return contents
        except Exception as e:
            print(e)
            print(e.__dict__)
            self.message == e.__dict__.get("message")
            self.response = e.__dict__.get("response")
            if self.status_code == 404:
                raise ApiException("bucket not found", 400)

    def list_files_by_prefix(self, prefix):
        self.set_prefix(prefix)
        self.response = self.s3_client.list_objects(
            Bucket=self.bucket_name, Prefix="{}/".format(prefix))

    def object_url(self, key, location="us-east-1"):
        return "https://{}.s3.amazonaws.com/{}".format(self.bucket_name, key)


    @property
    def contents(self):
        try:
            contents = self.response["Contents"]
            if contents[0]["Key"]:
                for item in contents:
                    try:
                        item["url"] = self.object_url(item["Key"])
                    except KeyError:
                        raise ApiException("S3 bucket missing key.")
            return contents
        except KeyError:
            self.message = "No contents found in s3 bucket response."
            return ''

    @property
    def status_code(self):
        return self.response["ResponseMetadata"]["HTTPStatusCode"]

    @property
    def error(self):
        try:
            return self.response["Error"]
        except KeyError:
            return self.message
