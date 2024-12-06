# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the default Flask port
EXPOSE 5001

# Command to run the application
CMD ["python", "app.py"]

# Copy the .env file to the container
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY

