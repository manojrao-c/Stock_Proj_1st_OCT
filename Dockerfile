# Use a lightweight base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies in one step to leverage Docker cache
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run the application
CMD ["python", "app.py"]
