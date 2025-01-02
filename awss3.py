import boto3
import os
# import io
import pickle
# import pandas as pd
from dotenv import load_dotenv

from parameters import *

load_dotenv()


class AwsS3:

    @staticmethod
    def check_s3_availability():

        if os.environ.get('AWS_ACCESS_KEY_ID') is None:
            
            return False
        
        else:
            
            return True


    @classmethod
    def __get_credentials(cls):

        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY_ID')
        aws_session_token = os.environ.get('AWS_SESSION_TOKEN')

        if (aws_access_key_id is None) or (aws_secret_access_key is None):

            local_env = load_dotenv()

            if local_env is True:

                aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
                aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY_ID']
                aws_session_token = os.environ['AWS_SESSION_TOKEN']
            
            else:

                raise Exception('AWS credentials not found in environment variables (neither for ECS and local .env file).')

        return {
            'aws_access_key_id': aws_access_key_id,
            'aws_secret_access_key': aws_secret_access_key,
            'aws_session_token': aws_session_token
        }


    @classmethod
    def __session_setup(cls):

        creds = cls.__get_credentials()
        
        return boto3.Session(
            aws_access_key_id=creds.get('aws_access_key_id'),
            aws_secret_access_key=creds.get('aws_secret_access_key'),
            aws_session_token=creds.get('aws_session_token')
        )


    @classmethod
    def __s3_resource(cls):

        # Aqui: para ambiente localhost
        # session = cls.__session_setup()

        # s3 = session.resource('s3')

        # Aqui: para ambiente EKS
        s3 = boto3.resource('s3')

        return s3


    @classmethod
    def save_on_s3(cls, obj, bucket, file_name):

        s3 = cls.__s3_resource()

        pickle_buffer = pickle.dumps(obj)

        s3.Object(bucket, file_name).put(Body=pickle_buffer)


    @classmethod
    def load_from_s3(cls, bucket, file_name):

        s3 = cls.__s3_resource()

        obj = s3.Bucket(bucket).Object(file_name).get()["Body"].read()

        return pickle.loads(obj)


    @classmethod
    def delete_on_s3(cls, bucket, file_name):

        s3 = cls.__s3_resource()

        s3.Object(bucket, file_name).delete()
