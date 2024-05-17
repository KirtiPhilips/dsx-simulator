import requests
import json 
def notification_to_iot(device_number,bucket_name,object_key):
    try:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        params = {
            'qos': '1',
        }

        cert = ('deviceCert_{}.crt'.format(device_number), 'deviceCert_{}.key'.format(device_number))

        data = '{"deviceId": "device-007","deviceSerialNumber": "DSN-001","timestamp": "2024-05-14T12:00:00Z","messageType": "notification","notificationType": "TherapyDataUploaded","data": {"bucketName": "{}","key": "{}" }      }'.format(bucket_name,object_key)

        response = requests.post(
            'https://a163sgg7lpdtqv-ats.iot.us-east-1.amazonaws.com:8443/topics/topic/topic1',
            params=params,
            headers=headers,
            data=data,
            cert=cert,
            verify='awsRootCA.pem',
        )

        # Check the response status code
        if response.status_code == 200:
                # Request successful, print the response content
                print("Response:", response.content)
        else:
                # Request failed, print the status code and reason
                print("Request failed with status code:", response.status_code)


    except requests.exceptions.RequestException as e:
        # Request encountered an exception, print the error
        print("Error:", e)

