#!/bin/bash
# Validate that the Flask app is running
curl -f http://localhost:5000 || exit 1
