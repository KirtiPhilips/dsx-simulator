import boto3
import requests
from generate_token import generate_token
import os
from notification_iot import notification_to_iot

# Specify the bucket name and object key
bucket_name = 'iottestdevicedata'
object_key = 'deviceData'
path="./deviceData.json"

def s3_access(device_number):
    try:
        access_credentials=generate_token(device_number)
        if access_credentials is None:
                print("Failed to generate token")

        else:
                access_key_id = access_credentials.get('accessKeyId')
                secret_access_key = access_credentials.get('secretAccessKey')
                session_token = access_credentials.get('sessionToken')
                
                s3 = boto3.client('s3',aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key,aws_session_token=session_token)
                # s3 = boto3.client('s3')
                print("Enter 1: If you want to upload data into the s3 bucket")
                print("Enter 2: If you want to read data from the s3 bucket")
                n=int(input())
                if n==1:
                    # fetch data from the s3 bucket
                    try:
                        s3.upload_file(path, bucket_name, object_key)
                    except Exception as e:
                        print("Error uploading to S3:", e)
                    try:
                        notification_to_iot(device_number,bucket_name,object_key)
                        print("Upload successful!")
                    except Exception as e:
                        print("Error notifying to Iot:", e)
                elif n==2:
                        try:
                            response = s3.get_object(Bucket=bucket_name, Key=object_key)
                            data = response['Body'].read()
                            print("Data from S3:", data)
                        except Exception as e:
                            print("Error reading from S3:", e)

    except requests.exceptions.RequestException as e:
        # Request encountered an exception, print the error
        print("Error:", e)

            


       


