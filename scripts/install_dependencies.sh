#!/bin/bash
sudo yum update -y
sudo yum install -y python3 python3-pip
pip3 install --upgrade pip
pip3 install -r /home/ec2-user/flask-app/requirements.txt
