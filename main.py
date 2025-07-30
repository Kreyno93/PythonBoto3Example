from questions import ask_create_instance, ask_create_bucket, ask_to_create_VPC

# main.py

def main():
    # Welcome Message with a Selection of 1 to X for the user to choose
    print("Welcome to the AWS CLI")
    print("What do you want to do?")
    print("(1) Manage VPCs?")
    print("(2) Manage EC2 Instances?")
    print("(3) Manage S3 Buckets?")
    print("(4) Exit")

    # Ask the user to select an option
    response = input("Enter the number of the option you want to choose: ").strip()
    # If the user selects 1, import the vpc module and call the ask_create_vpc function
    if response == "1":
        ask_to_create_VPC()
        main()
    # If the user selects 2, import the ec2 module and call the ask_create_instance function
    elif response == "2":
       ask_create_instance()
    # If the user selects 3, import the s3 module and call the ask_create_bucket function
    elif response == "3":
        ask_create_bucket()
    # If the user selects 5, print a goodbye message
    elif response == "4":
        print("Goodbye")
    # If the user selects anything else, print an error message
    else:
        print("Error: Invalid option selected. Please select a valid option")
        main()

if __name__ == "__main__":
    main()
