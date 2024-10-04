
# Creating FastAPI endpoints and Docker containers to spin these on Cloud

This GitHub repository contains a containerized application that utilizes FastAPI, a modern web framework for building APIs, to serve a machine learning model for inference. The application is packaged as a Docker container, making it easy to deploy and run in any environment. The machine learning model is trained to perform a specific task, such as image classification or text sentiment analysis, and is loaded into the FastAPI application for real-time inference. The repository also includes example data and model binary for demonstration purposes. The containerized application provides a scalable and efficient solution for deploying machine learning models in production environments with FastAPI, allowing for seamless integration into existing workflows or applications. Additionally, a PostgreSQl Database is used to store all the data in a dedicated container.

## Spin the Application

```
docker compose build

docker compose up -d (Detached mode: Run containers in the background)
```

## Spin the Application using Makefile
```
make build_c

make up_c
```