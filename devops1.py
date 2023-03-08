#!/usr/bin/env python3
import sys
import boto3
import subprocess
import time
import webbrowser
import uuid

ec2 = boto3.resource('ec2')

ew_instances = ec2.create_instances(
    ImageId='ami-006dcf34c09e50022',
    MinCount=1,
    MaxCount=1,
    UserData=f"""#!/bin/bash
                yum update -y
                
                yum install httpd -y
                systemctl enable httpd
                systemctl start httpd
                echo '<html>Instance meta-data' |  sudo tee  /var/www/html/index.html 
                echo '<br> instance-id = ' >> /var/www/html/index.html
                curl http://169.254.169.254/latest/meta-data/instance-id >> /var/www/html/index.html
                echo '<br> ami-id = ' >> /var/www/html/index.html
                curl http://169.254.169.254/latest/meta-data/ami-id >> /var/www/html/index.html
                echo '<br>instance-type = ' >> /var/www/html/index.html
                curl http://169.254.169.254/latest/meta-data/instance-type >> /var/www/html/index.html
                echo '<br><img src=https://86fa6be0-9cc4-11ed-a8fc-0242ac120002.s3.amazonaws.com/Seagull-near-Alcatraz.JPG width="500" height="600"></html>' >> /var/www/html/index.html
                """,
    TagSpecifications=[{
        'ResourceType': "instance",
        'Tags': [
            {
                'Key': 'Name',
                'Value': 'Devops1'

            },
        ]}],
    SecurityGroupIds=[
        'sg-0bdb387f73bea9cdd',
    ],
    KeyName='newkeypair',
    InstanceType='t2.nano')

print(f"created instance with name {ew_instances[0].tags} and instance_id= {ew_instances[0].instance_id} and image_id = {ew_instances[0].image_id} ,instance_type = {ew_instances[0].instance_type}")

ew_instances[0].start()
ew_instances[0].wait_until_running()

print("Instance Running.")

IP = ew_instances[0].public_ip_address

webbrowser.open_new_tab(f'{IP}')

