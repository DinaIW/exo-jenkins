# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y gcc python3-dev

# Copy the requirements file into the container
COPY build/movie-service/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY build/movie-service/app ./app

# Copy the main application file into the container
COPY main.py .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the command to start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
