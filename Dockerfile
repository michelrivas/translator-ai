
# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.12-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Set the working directory in the Docker image to '/app'
WORKDIR /app

# Copy the 'src' directory from our local system to '/app/src/' in the Docker image
COPY src/ /app/src/

# Copy the requirements.txt file to '/app/' in the Docker image
COPY requirements.txt /app/

# Ensure pip is up-to-date
RUN pip install --upgrade pip

# Install the dependencies
RUN pip install -r /app/requirements.txt

# Run the web service on container startup.
CMD cd src && alembic upgrade head && cd .. && uvicorn src.main:app --host 0.0.0.0 --port $PORT
