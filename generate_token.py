import requests
import json 




def generate_token(device_number):
    url = 'https://c11jfu1uhzw5xo.credentials.iot.us-east-1.amazonaws.com/role-aliases/S3-IOT-access-role-alias/credentials'
    cert = ('deviceCert_{}.crt'.format(device_number), 'deviceCert_{}.key'.format(device_number))
    headers = {'x-amzn-iot-thingname': 'Tulip-thing-{}'.format(device_number)}

    try:
        print("Fetching the secure access token from IoT Core Credentials Provider...")
        # Make the request
        response = requests.get(url, cert=cert, headers=headers)
            
        # Check the response status code
        if response.status_code == 200:
                # Request successful, print the response content
                # print("Response:", response.text)
                response_data=json.loads(response.text)
                access_credentials = response_data.get('credentials', {})
                print("Successfully obtained secure token from IoT Credentials Provider!")
                return access_credentials
        else:
                # Request failed, print the status code and reason
                print("Request failed with status code:", response.status_code)
                print("Reason:", response.reason)
                return None


    except requests.exceptions.RequestException as e:
        # Request encountered an exception, print the error
        print("Error:", e)
