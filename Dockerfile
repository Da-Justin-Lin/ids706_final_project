# Step 1: Use a traditional Python image to build the app
FROM python:3.9-slim as builder

# Set the working directory in the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 2: Use a distroless Python image for the runtime
FROM gcr.io/distroless/python3

# Set the working directory
WORKDIR /app

# Copy the application and dependencies from the builder stage
COPY --from=builder /app /app

# Expose the Flask port
EXPOSE 5001

# Set the environment variable
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY

# Command to run the application
CMD ["app.py"]
