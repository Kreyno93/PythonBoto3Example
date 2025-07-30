import boto3

# Create RDS Instance

def create_rds_instance(instance_name, db_instance_class, engine, master_username, master_user_password, allocated_storage):
    rds_client = boto3.client('rds')
    try:
        response = rds_client.create_db_instance(
            DBInstanceIdentifier=instance_name,
            DBInstanceClass=db_instance_class,
            Engine=engine,
            MasterUsername=master_username,
            MasterUserPassword=master_user_password,
            AllocatedStorage=allocated_storage
        )
        print("RDS instance created successfully")
    except Exception as e:
        print(f"Error creating RDS instance: {e}")