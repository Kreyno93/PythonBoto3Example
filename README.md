# AWS Infrastructure Management Tool

A Python-based command-line interface for managing AWS infrastructure components including VPCs, EC2 instances, and S3 buckets using boto3.

## Overview

This project provides an interactive CLI tool that simplifies AWS resource management through a menu-driven interface. It allows users to create, manage, and delete AWS resources such as Virtual Private Clouds (VPCs), EC2 instances, and S3 buckets without needing to remember complex AWS CLI commands.

## Features

- **VPC Management**: Create VPCs, subnets, security groups, route tables, and internet gateways
- **EC2 Instance Management**: Launch, list, and terminate EC2 instances with custom configurations
- **S3 Bucket Management**: Create, list, and delete S3 buckets with object management
- **Interactive Menu System**: User-friendly command-line interface
- **WordPress Deployment**: Automated WordPress setup on EC2 instances using user data scripts
- **Infrastructure as Code**: Complete VPC infrastructure creation with networking components

## Prerequisites

Before using this tool, ensure you have the following:

### Software Requirements
- Python 3.6 or higher
- pip (Python package installer)

### AWS Requirements
- AWS Account with appropriate permissions
- AWS CLI configured with credentials
- IAM user with the following permissions:
  - EC2 full access (or specific EC2 permissions)
  - S3 full access (or specific S3 permissions)
  - VPC full access (or specific VPC permissions)

### Python Dependencies
- `boto3` - AWS SDK for Python
- `botocore` - Low-level interface to AWS services

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/PythonBoto3Example.git
cd PythonBoto3Example
```

### 2. Install Dependencies
```bash
pip install boto3 botocore
```

### 3. Configure AWS Credentials
Make sure your AWS credentials are configured. You can do this using:

```bash
aws configure
```

Or by setting environment variables:
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=your_preferred_region
```

## Usage

### Running the Application
```bash
python main.py
```

### Menu Options

The application presents a main menu with the following options:

1. **Manage VPCs**: Create complete VPC infrastructure including subnets, security groups, and routing
2. **Manage EC2 Instances**: Launch and terminate EC2 instances
3. **Manage S3 Buckets**: Create, list, and delete S3 buckets
4. **Exit**: Close the application

### Example Workflows

#### Creating a Complete VPC Infrastructure
1. Select option 1 (Manage VPCs)
2. Choose to create a VPC
3. Enter VPC CIDR block (e.g., `10.0.0.0/16`)
4. Create subnets with appropriate CIDR blocks
5. Configure security groups
6. Set up routing and internet gateway

#### Launching an EC2 Instance
1. Select option 2 (Manage EC2 Instances)
2. Choose to create an instance
3. Provide instance name
4. Select subnet and security group
5. Optionally specify user data script path

#### Managing S3 Buckets
1. Select option 3 (Manage S3 Buckets)
2. Create, list, or delete buckets as needed
3. Handle bucket cleanup including object deletion

## File Structure

```
PythonBoto3Example/
├── main.py              # Main application entry point
├── questions.py         # User interaction and menu logic
├── ec2.py              # EC2 instance management functions
├── s3.py               # S3 bucket management functions
├── vpc.py              # VPC and networking functions
├── rds.py              # RDS database functions
├── lookup-s3.py        # S3 lookup utilities
├── userdata.sh         # WordPress installation script
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Configuration

### Default Settings
- **Region**: The S3 functions default to `eu-north-1`
- **Instance Type**: EC2 instances use `t3.micro` by default
- **AMI**: Uses Amazon Linux 2 AMI (hardcoded, may need updates)
- **Key Pair**: References `WordpressDeham14` (update as needed)

### Customization
You can modify the following in the respective files:
- Change default regions in `s3.py`
- Update AMI IDs in `ec2.py`
- Modify instance types and key pair names
- Customize user data scripts

## WordPress Deployment

The included `userdata.sh` script automatically sets up a WordPress installation on EC2 instances with:
- Apache web server
- PHP 8.0
- MariaDB database
- WordPress latest version
- Proper file permissions and database configuration

## Error Handling

The application includes comprehensive error handling for:
- AWS service errors
- Invalid user inputs
- Resource conflicts (e.g., bucket name already exists)
- Network and connectivity issues

## Security Considerations

- Ensure your AWS credentials are properly secured
- Use IAM roles with minimal required permissions
- Regularly rotate access keys
- Review security group rules before creation
- Be cautious when deleting resources in production environments

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## Troubleshooting

### Common Issues

**AWS Credentials Not Found**
- Ensure AWS CLI is configured or environment variables are set
- Check that credentials have the necessary permissions

**Region Mismatch**
- Verify that resources are being created in the intended region
- Update region settings in the code if necessary

**Resource Limits**
- Check AWS service limits for your account
- Ensure you're not exceeding VPC, instance, or bucket limits

**AMI Not Found**
- Update the hardcoded AMI ID in `ec2.py` to a current Amazon Linux 2 AMI for your region

## License

MIT License

Copyright (c) 2024 PythonBoto3Example

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Support

For questions, issues, or contributions, please open an issue on the GitHub repository.

---

**Note**: This tool is designed for educational and development purposes. Always review and test thoroughly before using in production environments.
