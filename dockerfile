# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app


COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 5000

CMD ["python", "app.py"]
