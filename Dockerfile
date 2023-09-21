# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python application code to the container
COPY test-service.py /app/test-service.py

# Install Flask and any other dependencies
RUN pip install Flask netifaces

# Expose the port the application will run on
EXPOSE 8080

# Define the command to run the application
CMD ["python", "test-service.py"]
