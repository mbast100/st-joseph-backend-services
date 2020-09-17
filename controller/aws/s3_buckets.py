import boto3
import logging
from botocore.exceptions import ClientError
from api_exception import ApiException


class S3Bucket():
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.response = {}
        self.message ={}

    def upload_file(self, file_name, bucket,object_name=None):
        if object_name is None:
            object_name = file_name
        try:
            self.response = self.s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

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