from generate_device import generate_device
from s3_access import s3_access



def main():

    print("Enter 1: Device maker ( need to be done once ) - Generate devices and connect it to AWS Iot and attach policies to the thing generate in Iot Core  ")
    print("2: Simulator Work - Using device Certificate , create token from AWS credential provider and then access S3 (or any other aws services)")
    print("3: To exit")

    n=int(input())

    global count_of_devices
    
    # if you want to make devices, then press 1
    if(n==1):
        # Requirement: How many devices do you want to generate certificates for?
        print("For how many devices do you want to generate certificates?")
        count_of_devices = int(input())
        generate_device(count_of_devices)
        main()
        
    elif(n==2):
            print("Through which device do you want to access S3? (Enter the device number)")
            device_number=int(input())
            s3_access(device_number)
            main()
    elif(n==3):
        return

main()

            
