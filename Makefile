# Define the image name and Docker Hub username
IMAGE_NAME = email-generator-app
DOCKER_ID_USER = tzrrr

# Install dependencies
install:
	pip install -r requirements.txt

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run:
	docker run -p 5001:5001 $(IMAGE_NAME)

# Remove the Docker image
clean:
	docker rmi $(IMAGE_NAME)

# Show Docker images
image_show:
	docker images

# Show running Docker containers
container_show:
	docker ps

# Push the Docker image to Docker Hub
push:
	docker login -u $(DOCKER_ID_USER)
	docker tag $(IMAGE_NAME) $(DOCKER_ID_USER)/$(IMAGE_NAME)
	docker push $(DOCKER_ID_USER)/$(IMAGE_NAME):latest

# Log in to Docker Hub
login:
	docker login -u $(DOCKER_ID_USER)

# test the flask app
test:
	pytest test_app.py

format:	
	black *.py 

lint:
	ruff check *.py
