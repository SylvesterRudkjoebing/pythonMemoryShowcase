# Project Overview

This repository demonstrates my ability to integrate **Data Science** with **Full-Stack Development** using Python and React.

The core of this project is a **FastAPI-based RESTful API** that simulates human autobiographical memory. It leverages several key components:

1. **Associations** – Implemented with a **breadth-first search (BFS)** algorithm to identify the shortest connection paths between friends.
2. **Episodic Memory** – Stored in an "Events" database table, providing event descriptions to simulate memory recall.
3. **Semantic Memory** – Powered by a local Large Language Model (LLM), Llama-3.2-1B, through the Hugging Face "transformers" library for contextual understanding.

The result is a dynamic and interactive representation of how autobiographical memory functions.

<img width="613" alt="Skærmbillede 2024-11-28 kl  18 01 12" src="https://github.com/user-attachments/assets/32192cd4-86f5-4b26-a2f7-8d8de213ff03">

## Key Features

### 1. **LLM Integration**  
   This project integrates Meta's Llama-3.2-1B, a local language model. Performance depends on your system’s hardware (RAM/CPU), as no hardware accelerations are used to ensure broad compatibility.

### 2. **BFS Algorithm**  
   The BFS algorithm, responsible for identifying the shortest path between friends, is encapsulated in `bfsObject.py`.

### 3. **Back-End**  
   Built using **FastAPI**, the back-end handles data operations via **SQLAlchemy ORM** and processes HTTP requests, ensuring smooth communication with the front-end.

### 4. **Front-End**  
   The front-end is developed using **React** and styled with **Tailwind CSS**. A graph visually represents the connection paths between friends.

### 5. **Testing**  
   Unit tests for this project are planned to ensure robust functionality, but are yet to be written.

## Access to Llama-3.2-1B

If you would like access to the Llama-3.2-1B model, feel free to reach out. The model files are approximately 5GB in total.

## How to Run

This project can be run either locally or using Docker. If the Llama-3.2-1B model is not available, the program will automatically generate placeholder messages.

### Option 1: Running Locally

1) Put the **Llama-3.2-1B** folder in the same directory as the project’s root folder.
   
2) Open a terminal and run:
   ```bash
   uvicorn appAPI:app --reload
   
3) Open a terminal, navigate to the **memoryReactFrontEnd** folder, and run:
   ```bash
   npm run build
   npm start
  
### Option 2: Running with Docker

This project includes a Dockerized setup for easier deployment. Here's how you can run it using Docker:

1) **Ensure Docker is installed** on your system.

2) Clone the repository and navigate to the project folder.

3) Put the **Llama-3.2-1B** folder in the same directory as the project’s root folder.
   
4) **Build and run the Docker images** (both backend and frontend) by running the following command in your terminal:
   ```bash
   docker-compose up --build

5) **Access the application:**
   - The FastAPI backend will be running on [http://localhost:8000](http://localhost:8000)
   - The React frontend will be accessible at [http://localhost:3000](http://localhost:3000)
