# Flask REST API with Docker, GitHub Actions, and EC2 Deployment

This project demonstrates building and deploying a containerized Flask REST API using **Docker**, **GitHub Actions** for CI/CD, and deploying to an **AWS EC2** instance.

---

## 📌 Project Overview

**Goal:** Build a lightweight REST API with Flask, containerize it with Docker, automate the build and deployment pipeline using GitHub Actions, and deploy to an EC2 instance.

---

## 🛠️ Tech Stack
- **Flask**: Python web framework
- **Docker**: Containerization
- **GitHub Actions**: CI/CD pipeline
- **AWS EC2**: Hosting environment

---

## 📁 Folder Structure
```
.
├── app.py
├── Dockerfile
├── requirements.txt
├── deploy.sh
└── .github
    └── workflows
        └── deploy.yml
```

---

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/flask-docker-cicd.git
cd flask-docker-cicd
```

### 2. Build Docker Image Locally (Optional Test)
```bash
docker build -t flask-api .
docker run -d -p 5000:5000 flask-api
```
Then visit `http://localhost:5000`.

### 3. Push to GitHub and Configure Secrets
Add these GitHub secrets:
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`
- `EC2_HOST`
- `EC2_USER`
- `EC2_SSH_KEY`

### 4. GitHub Actions CI/CD Pipeline
The pipeline will:
- Build and push the Docker image to Docker Hub
- SSH into the EC2 instance
- Pull and restart the container

---

## 📦 Dockerfile
```Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

---

## 🐍 Flask App (`app.py`)
```python
from flask import Flask, jsonify, request

app = Flask(__name__)
data_store = []

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Flask REST API!"})

@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(data_store)

@app.route("/items", methods=["POST"])
def add_item():
    item = request.json
    data_store.append(item)
    return jsonify({"status": "Item added", "item": item}), 201

@app.route("/items/<int:index>", methods=["DELETE"])
def delete_item(index):
    try:
        removed = data_store.pop(index)
        return jsonify({"status": "Item removed", "item": removed})
    except IndexError:
        return jsonify({"error": "Item not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

## ⚙️ GitHub Actions Workflow (`deploy.yml`)
```yaml
name: CI/CD Pipeline
on:
  push:
    branches:
      - main
jobs:
  build-deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Login to DockerHub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        push: true
        tags: ${{ secrets.DOCKER_USERNAME }}/flask-api:latest

    - name: Deploy to EC2
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.EC2_HOST }}
        username: ${{ secrets.EC2_USER }}
        key: ${{ secrets.EC2_SSH_KEY }}
        script: |
          docker pull ${{ secrets.DOCKER_USERNAME }}/flask-api:latest
          docker stop flask-api || true
          docker rm flask-api || true
          docker run -d --name flask-api -p 80:5000 ${{ secrets.DOCKER_USERNAME }}/flask-api:latest
```

---

## 🖥️ EC2 Deployment Script (`deploy.sh`)
```bash
#!/bin/bash

docker pull your_dockerhub_username/flask-api:latest
docker stop flask-api || true
docker rm flask-api || true
docker run -d --name flask-api -p 80:5000 your_dockerhub_username/flask-api:latest
```

---

## 📌 To Do
- [ ] Add unit tests & linting to CI
- [ ] Add HTTPS support
- [ ] Add persistent storage

---

## 👨‍💻 Author
**Pradeep Mahadevaiah**  
AWS & DevOps Enthusiast | GitHub: [PradeepMahadevaiah](https://github.com/PradeepMahadevaiah)

---

## 📜 License
MIT License
