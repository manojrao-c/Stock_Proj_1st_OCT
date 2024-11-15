#!/bin/bash
# Navigate to app directory
cd /home/ec2-user/Stock_Proj_1st_OCT

# Activate virtual environment
source venv/bin/activate

# Start Flask app
nohup python3 app.py > app.log 2>&1 &
