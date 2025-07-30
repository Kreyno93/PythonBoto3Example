import boto3

# Create VPC client
vpc = boto3.client('ec2')

# Create a new VPC function
def create_vpc(vpc_cidr):
    response = vpc.create_vpc(
        CidrBlock=vpc_cidr
    )

    vpc_id = response['Vpc']['VpcId']
    print(f'VPC created with id: {vpc_id}')
    return vpc_id

# Function to list all VPCs
def list_vpcs():
    ec2 = boto3.client('ec2')
    response = ec2.describe_vpcs()

    vpcs = response['Vpcs']
    for vpc in vpcs:
        vpc_id = vpc['VpcId']
        cidr_block = vpc['CidrBlock']
        print(f'VPC ID: {vpc_id}, CIDR Block: {cidr_block}')


# Creates a subnet in a VPC
def create_subnet(vpc_id, cidr_block):
    response = vpc.create_subnet(
        VpcId=vpc_id,
        CidrBlock=cidr_block
    )

    subnet_id = response['Subnet']['SubnetId']
    print(f'Subnet created with id: {subnet_id}')
    return subnet_id

# Function to list all subnets with their ids, cidr blocks, and availability zones
def list_subnets():
    response = vpc.describe_subnets()
    for subnet in response['Subnets']:
        print(f'Subnet id: {subnet["SubnetId"]}, CIDR Block: {subnet["CidrBlock"]}, Availability Zone: {subnet["AvailabilityZone"]}')

# Function to Create a Security Group
def create_security_group(group_name, description, vpc_id):
    ec2 = boto3.client('ec2')

    # Create the security group
    response = ec2.create_security_group(
        GroupName=group_name,
        Description=description,
        VpcId=vpc_id
    )

    security_group_id = response['GroupId']
    print(f'Security Group Created {security_group_id} in vpc {vpc_id}.')

    # Add inbound rules for SSH (port 22) and HTTP (port 80)
    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }
        ]
    )

    print('Ingress Successfully Set for SSH and HTTP.')
    return security_group_id

# Function to list all security groups with their ids, names, and descriptions
def list_sgs():
    response = vpc.describe_security_groups()
    for sg in response['SecurityGroups']:
        print(f'Security Group id: {sg["GroupId"]}, Name: {sg["GroupName"]}, Description: {sg["Description"]}')

# Function to create a route table
def create_route_table(vpc_id):
    response = vpc.create_route_table(
        VpcId=vpc_id,
        TagSpecifications=[
            {
                'ResourceType': 'route-table',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'MyRouteTable'
                    },
                ]
            },
        ]
    )

    route_table_id = response['RouteTable']['RouteTableId']
    print(f'Route Table created with id: {route_table_id}')
    return route_table_id

def attach_igw_to_vpc(vpc_id, igw_id):
    response = vpc.attach_internet_gateway(
        VpcId=vpc_id,
        InternetGatewayId=igw_id
    )
    print(f'Internet Gateway {igw_id} attached to VPC {vpc_id}')

# Function to get the Internet Gateway ID, if there is no IGW, it will create one
def get_igw_id_or_create_igw():
    response = vpc.describe_internet_gateways()
    if len(response['InternetGateways']) == 0:
        response = vpc.create_internet_gateway()
        igw_id = response['InternetGateway']['InternetGatewayId']
        print(f'Internet Gateway created with id: {igw_id}')
        return igw_id
    else:
        igw_id = response['InternetGateways'][0]['InternetGatewayId']
        return igw_id


# Function to add routes to a route table
def create_route(route_table_id, destination_cidr_block, gateway_id):
    response = vpc.create_route(
        RouteTableId=route_table_id,
        DestinationCidrBlock=destination_cidr_block,
        GatewayId=gateway_id,
    )
    print(f'Route added to Route Table {route_table_id}')

# Function to associate subnets with a route table. It will associate all subnets with the route table
def associate_route_table(route_table_id, subnet_ids):
    for subnet_id in subnet_ids:
        response = vpc.associate_route_table(
            RouteTableId=route_table_id,
            SubnetId=subnet_id
        )
        print(f'Subnet {subnet_id} associated with Route Table {route_table_id}')

# Function to delete a specific VPC, with all its subnets, security groups, and route tables
def delete_vpc(vpc_id):
    ec2 = boto3.client('ec2')

    # Disassociate and delete route tables
    response = ec2.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    for route_table in response['RouteTables']:
        route_table_id = route_table['RouteTableId']
        # Disassociate non-main route tables
        for association in route_table.get('Associations', []):
            if not association['Main']:
                association_id = association['RouteTableAssociationId']
                ec2.disassociate_route_table(AssociationId=association_id)
        # Skip deletion of the main route table, it will be deleted with the VPC
        if not any(assoc['Main'] for assoc in route_table['Associations']):
            ec2.delete_route_table(RouteTableId=route_table_id)

    # Delete subnets
    response = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    for subnet in response['Subnets']:
        subnet_id = subnet['SubnetId']
        ec2.delete_subnet(SubnetId=subnet_id)

    # Delete security groups
    response = ec2.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    for sg in response['SecurityGroups']:
        sg_id = sg['GroupId']
        # Skip default security group as it cannot be deleted
        if sg['GroupName'] != 'default':
            ec2.delete_security_group(GroupId=sg_id)

    # Detach and delete internet gateways
    response = ec2.describe_internet_gateways(Filters=[{'Name': 'attachment.vpc-id', 'Values': [vpc_id]}])
    for igw in response['InternetGateways']:
        igw_id = igw['InternetGatewayId']
        ec2.detach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
        ec2.delete_internet_gateway(InternetGatewayId=igw_id)

    # Delete the VPC
    ec2.delete_vpc(VpcId=vpc_id)
    print(f'VPC {vpc_id} deleted successfully')


    


