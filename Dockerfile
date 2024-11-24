# Use Python slim base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the webhook listener script
COPY webhook_listener.py /app/

# Expose the port Waitress will use
EXPOSE 5000

# Run the webhook listener with Waitress
CMD ["python", "/app/webhook_listener.py"]
