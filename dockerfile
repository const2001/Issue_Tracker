# Use an official Python runtime as the base image
FROM python:3.8

# Set the working directory within the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app/

# Make port 5000 available to the world outside this container
EXPOSE 8000

# Define environment variable for Flask
ENV FLASK_APP=app.py

# Run the command to start the Flask application
CMD ["flask", "run", "--host", "0.0.0.0"]
