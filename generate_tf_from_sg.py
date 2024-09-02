import boto3
import json

def fetch_security_groups():
    # Initialize boto3 client for EC2 in the source account
    ec2_client = boto3.client('ec2')

    # Fetch security groups
    response = ec2_client.describe_security_groups()
    return response['SecurityGroups']

def generate_terraform_config(sg_data):
    # Create a Terraform configuration file
    terraform_config = ""

    for sg in sg_data:
        sg_name = sg['GroupName']
        sg_description = sg.get('Description', 'No description provided')
        terraform_config += f'resource "aws_security_group" "{sg_name}" {{\n'
        terraform_config += f'  name        = "{sg_name}"\n'
        terraform_config += f'  description = "{sg_description}"\n'

        # Inbound Rules
        for permission in sg.get('IpPermissions', []):
            for ip_range in permission.get('IpRanges', []):
                terraform_config += '  ingress {\n'
                terraform_config += f'    from_port   = {permission.get("FromPort", 0)}\n'
                terraform_config += f'    to_port     = {permission.get("ToPort", 0)}\n'
                terraform_config += f'    protocol    = "{permission.get("IpProtocol", "tcp")}"\n'
                terraform_config += f'    cidr_blocks = ["{ip_range.get("CidrIp", "0.0.0.0/0")}"]\n'
                terraform_config += '  }\n'

        # Outbound Rules
        for permission in sg.get('IpPermissionsEgress', []):
            for ip_range in permission.get('IpRanges', []):
                terraform_config += '  egress {\n'
                terraform_config += f'    from_port   = {permission.get("FromPort", 0)}\n'
                terraform_config += f'    to_port     = {permission.get("ToPort", 0)}\n'
                terraform_config += f'    protocol    = "{permission.get("IpProtocol", "tcp")}"\n'
                terraform_config += f'    cidr_blocks = ["{ip_range.get("CidrIp", "0.0.0.0/0")}"]\n'
                terraform_config += '  }\n'

        terraform_config += '}\n\n'

    # Write to main.tf
    with open('main.tf', 'w') as f:
        f.write(terraform_config)

def main():
    sg_data = fetch_security_groups()
    generate_terraform_config(sg_data)
    print("Terraform configuration has been generated in 'main.tf'.")

if __name__ == '__main__':
    main()
