# Individual Project 3 - Auto-Scaling Flask App with AWS and Docker

[![CI](https://github.com/TzRRR/individual3/actions/workflows/cicd.yml/badge.svg)](https://github.com/TzRRR/individual3/actions/workflows/cicd.yml)

## **Project Overview**

This project demonstrates how to build a scalable, web-hosted application using **Flask**, containerized with **Docker**, and deployed on **AWS** with auto-scaling capabilities. It also integrates an embedded **LLM (Large Language Model)** API via OpenAI, enabling users to generate emails dynamically.

---

## **Features**

- **Flask Application**: A web app to generate professional emails based on user input (purpose, tone, and details).
- **Embedded LLM**: Integrated OpenAI's GPT-3.5-turbo model for email generation.
- **Dockerized Deployment**: The app is containerized using Docker for portability and scalability.
- **Auto-Scaling on AWS**: Hosted on AWS with auto-scaling to handle variable traffic.
- **Public Accessibility**: The app is publicly accessible.

---

## **Steps to Build and Deploy**

### **1. Flask App Development**

- Integrated OpenAI's GPT-3.5-turbo model for generating emails dynamically.
- Utilized HTML templates to render the input form and display the generated email.

### **2. Dockerization**

- Wrote a `Dockerfile` to containerize the Flask app.
- Configured dependencies using a `requirements.txt` file.
- Docker Image on DockerHub: https://hub.docker.com/r/tzrrr/email-generator-app
- Docker Pull Command
  ```bash
  docker pull tzrrr/email-generator-app
  ```

### **3. Secrets Management**

- OpenAI API key is securely managed using GitHub Actions secrets.
- The API key is passed to the container at runtime to prevent exposing sensitive information.

### **4. AWS Deployment**

- Deployed the Docker container to AWS using Elastic Container Service (ECS).
- Published the app through AWS App Runner.
- Ensured the app is publicly accessible with a secure endpoint.

---

## **Usage**

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Build and run the Docker container locally:

   ```bash
   docker build -t email-generator-app .
   docker run -p 5001:5001 -e OPENAI_API_KEY=<your-api-key> email-generator-app
   ```

3. Access the app locally at http://localhost:5001 or through the server at https://qbemnkmu4s.us-east-1.awsapprunner.com/
