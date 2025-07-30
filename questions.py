from s3 import create_bucket, list_buckets, delete_bucket, delete_all_objects
from ec2 import create_instance, list_instances, terminate_instance
from vpc import create_vpc, list_vpcs, create_subnet, list_subnets, create_security_group
from vpc import create_route, create_route_table,associate_route_table,get_igw_id_or_create_igw
from vpc import attach_igw_to_vpc,list_sgs,delete_vpc
from botocore.exceptions import ClientError

# Create a function that asks the user to create a bucket
# If the user says yes, ask the user to enter the bucket name
# If the user says no, print a message


def ask_create_bucket():
    response = input("Do you want to create a bucket? (yes/no): ").strip().lower()
    if response in ["yes", "y"]:
        bucket_name = input("Enter the bucket name you want to create: ").strip()
        create_bucket(bucket_name)
    else:
        print("You chose not to create a bucket")
    # Asks me if i want to list all buckets in a region
    response = (
        input("Do you want to list all buckets in the region? (yes/no): ")
        .strip()
        .lower()
    )
    if response in ["yes", "y"]:
        list_buckets()
    else:
        print("You chose not to list all buckets")
    # Asks me if i want to delete a bucket. If yes, it asks me for the bucket name
    # If it fails due to the bucket not being empty, it asks me if i want to delete all objects in the bucket
    response = input("Do you want to delete a bucket? (yes/no): ").strip().lower()
    if response in ["yes", "y"]:
        try:
            bucket_name = input("Enter the bucket name you want to delete: ").strip()
            delete_bucket(bucket_name)
        except ClientError as e:
            print(f"Error: {e}")
            if "BucketNotEmpty" in str(e):
                response = (
                    input("Do you want to delete all objects in the bucket? (yes/no): ")
                    .strip()
                    .lower()
                )
                if response in ["yes", "y"]:
                    delete_all_objects(bucket_name)
                    response = (
                        input("Do you want to delete the bucket now? (yes/no): ")
                        .strip()
                        .lower()
                    )
                    if response in ["yes", "y"]:
                        delete_bucket(bucket_name)
                else:
                    print("You chose not to delete all objects in the bucket")
    else:
        print("You chose not to delete a bucket")

def ask_create_instance():
    # Ask the user if they want to create an instance
    response = input("Do you want to create an instance? (yes/no): ").strip().lower()
    # If yes, ask the user to enter the instance name
    if response in ["yes", "y"]:
        instance_name = input("Enter the instance name you want to create: ").strip()
        list_subnets()
        subnet_id = input("Enter the subnet id: ").strip()
        list_sgs()
        sg_id = input("Enter the security group id: ").strip()
        user_data_file = input("Enter the user data file path: ").strip()
        create_instance(instance_name,subnet_id,sg_id,user_data_file)
    else:
        print("You chose not to create an instance")
    # Ask the user if they want to terminate an instance
    response = input("Do you want to terminate an instance? (yes/no): ").strip().lower()
    # If yes, ask the user to list all instances name and id
    if response in ["yes", "y"]:
        list_instances()
        instance_id = input("Enter the instance id you want to terminate: ").strip()
        terminate_instance(instance_id)
        
# Ask the user to Create a whole Infrastructure on AWS
def ask_to_create_VPC():
    response = input("Do you want to create a VPC? (yes/no): ").strip().lower()
    if response in ["yes", "y"]:
        vpc_cidr = input("Enter the VPC CIDR block you want to create: ").strip()
        vpc_id = create_vpc(vpc_cidr)
        # Ask the user repeatedly to create subnets until they say no
        subnet_cidr = input("Enter the Subnet CIDR block you want to create: ").strip()
        subnet_ids = []
        while True:
            subnet_id = create_subnet(vpc_id,subnet_cidr)
            subnet_ids.append(subnet_id)
            response = input("Do you want to create another subnet? (yes/no): ").strip().lower()
            if response in ["no", "n"]:
                break
            subnet_cidr = input("Enter the Subnet CIDR block you want to create: ").strip()
        group_name = input("Enter the Security Group name you want to create: ").strip()
        description = input("Enter the Security Group description: ").strip()
        create_security_group(group_name, description, vpc_id)
        route_table_id = create_route_table(vpc_id)
        igw_id = get_igw_id_or_create_igw()
        attach_igw_to_vpc(vpc_id,igw_id)
        create_route(route_table_id,"0.0.0.0/0",igw_id)
        associate_route_table(route_table_id, subnet_ids)
        print("Infrastructure created successfully")
    else:
        response = input("Do you want to delete a VPC? (yes/no): ").strip().lower()
        if response in ["yes", "y"]:
            list_vpcs()
            vpc_id = input("Enter the VPC id you want to delete: ").strip()
            delete_vpc(vpc_id)
        else:
            print("You chose not to create a VPC")

def ask_for_local_database_or_rds_instance():
    response = input("Do you want to create a local database or an RDS instance? (local/rds): ").strip().lower()
    if response == "local":
        print("You chose to create a local database. Please set it up manually.")
    elif response == "rds":
        print("You chose to create an RDS instance. Please follow the AWS documentation to set it up.")
    else:
        print("Invalid choice. Please choose 'local' or 'rds'.")