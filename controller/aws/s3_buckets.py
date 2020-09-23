import boto3
import logging
from botocore.exceptions import ClientError
from api_exception import ApiException


class S3Bucket():
    def __init__(self, filename = ''):
        self.s3_client = boto3.client('s3')
        self.s3_resource = boto3.resource('s3')
        self.response = {}
        self.file_name = filename
        self.message ={}
        self.image_url_seaonsal = "https://st-joseph-seasonal.s3.amazonaws.com/{}/{}"
        self.image_url = "https://st-joseph-media.s3.amazonaws.com/{}/{}"
        self.response_message ={
            "success" : "uploaded {} to {}"
        }

    def upload_file(self,bucket, filename, file, path=''):
        try:
            key = filename
            if path:
                key = path+"/"+filename
            self.response = self.s3_resource.Bucket(bucket).put_object(Key=key,Body=file)
        except Exception as e:
            raise ApiException("something went wrong while uploading to s3 bucket", 400)
    
    def delete_file(self, bucket, key):
        try:
            self.response = self.s3_client.delete_object(Bucket = bucket, Key =key)
        except Exception as e:
            raise ApiException("something went wrong while deleting o s3 bucket", 400)

    def list_files(self,bucket):
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
    
    @property
    def status_code(self):
        return self.response["ResponseMetadata"]["HTTPStatusCode"]

    @property
    def error(self):
        return self.response["Error"]