#!/bin/bash
sudo yum update -y
sudo yum install -y python3 python3-pip
pip3 install --upgrade pip
pip3 install --ignore-installed -r /home/ec2-user/Stock_Proj_1st_OCT/requirements.txt
