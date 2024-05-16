import subprocess
import json
import requests
import boto3

def generate_device(count_of_devices):
    for i in range(1, count_of_devices + 1):
            try:
                command = ["openssl", "genrsa", "-out",  "deviceCert_{}.key".format(i), "2048"]
                subprocess.run(command, check=True)
                print("RSA private key generated successfully for device")
# dfds

                req_command = ["openssl", "req", "-new", "-key",  "deviceCert_{}.key".format(i), "-out","deviceCert_{}.csr".format(i)]
                input_values = "US\n\n\nTulip\nTulip-dev\nTulip-thing-{}\n\n\n\n".format(i)
                subprocess.run(req_command, input=input_values.encode(), check=True)
                print("Certificate Signing Request (CSR) generated successfully for device")

                crt_command = ["openssl", "x509", "-req", "-in","deviceCert_{}.csr".format(i), "-CA", "deviceRootCA.pem", "-CAkey",  "deviceRootCA.key" , "-CAcreateserial", "-out", "deviceCert_{}.crt".format(i), "-days", "365", "-sha256"]
                subprocess.run(crt_command, check=True)
                print("Certificate (CRT) generated successfully for device")

                with open("deviceCert_{}.crt".format(i), "rb") as device_cert_file:
                    with open("deviceRootCA.pem", "rb") as ca_cert_file:
                        with open("deviceCertAndCACert_{}.crt".format(i), "wb") as output_file:
                            output_file.write(device_cert_file.read())
                            output_file.write(ca_cert_file.read())
                print("Certificate concatenated successfully for device")

                mosquitto_command_specific = [
                "mosquitto_pub",
                    "-h", "a163sgg7lpdtqv-ats.iot.us-east-1.amazonaws.com",
                    "--cafile", "awsRootCA.pem",
                    "--cert", "deviceCertAndCACert_{}.crt".format(i),  
                    "--key", "deviceCert_{}.key".format(i),
                    "-p", "8883",
                    "-q", "1",
                    "-t", "Tulip/Topic",
                    "-i", "Tulip-Thing-{}".format(i),
                    "--tls-version", "tlsv1.2",
                    "-m", "Hello",
                    "-d"
                ]
                subprocess.run(mosquitto_command_specific, check=True)
                print("Things generated successfully for devices")
                
                

            except subprocess.CalledProcessError as e:
                print("Error:", e)
            
            list_command = ["aws", "iot", "list-thing-principals", "--thing-name", "Tulip-thing-{}".format(i)]
            result = subprocess.run(list_command, capture_output=True,  check=True)

                # Parse JSON output
            data = json.loads(result.stdout)

                # Extract certificate ARN
            certificate_arn = data["principals"][0].split("/")[-1]

                # Attach policy to certificate
            attach_command = [
                        "aws", "iot", "attach-policy",
                        "--policy-name", "tulip-alias-policy",
                        "--target", "arn:aws:iot:us-east-1:705158173663:cert/{}".format(certificate_arn)
                    ]
            subprocess.run(attach_command, check=True)

            print("Policy attached successfully to certificate:", certificate_arn)



