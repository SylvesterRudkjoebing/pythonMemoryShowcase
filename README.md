# Project Overview

This repository demonstrates my ability to integrate Data Science with Full-Stack Development using Python and React.

The core of this project is a FastAPI-based RESTful API that simulates human autobiographical memory. It leverages several key components:

1. **Associations** – Implemented with a **breadth-first search (BFS)** algorithm to identify the shortest connection paths between friends.
2. **Episodic Memory** – Stored in an "Events" database table, providing event descriptions to simulate memory recall.
3. **Semantic Memory** – Powered by a local Large Language Model (LLM), Llama-3.2-1B, through the Hugging Face "transformers" library for contextual understanding.

The result is a dynamic and interactive representation of how autobiographical memory functions.

<img width="644" alt="User interface showing connection paths" src="https://github.com/user-attachments/assets/7550028d-b116-4aaa-98ae-3b15d5334b44">

## Key Features

### 1. **LLM Integration**  
   This project integrates Meta's Llama-3.2-1B, a local language model. Performance depends on your system’s hardware (RAM/CPU), as no hardware accelerations are used to ensure broad compatibility.

### 2. **BFS Algorithm**  
   The BFS algorithm, responsible for identifying the shortest path between friends, is encapsulated in `bfsObject.py`.

### 3. **Back-End**  
   The back-end is built with **FastAPI**, which handles the data access layer and HTTP requests, enabling smooth communication with the front-end.

### 4. **Front-End**  
   The front-end is developed using **React** and styled with **Tailwind CSS**. A graph visually represents the connection paths between friends.

### 5. **Testing**  
   Unit tests for this project are planned to ensure robust functionality, but are yet to be written.

## Access to Llama-3.2-1B

If you would like access to the Llama-3.2-1B model, feel free to reach out. The model files are approximately 5GB in total.

## How to Run

1) Put the **Llama-3.2-1B** folder in the project folder.
2) Open a terminal and run: `uvicorn appAPI:app --reload`.
3) Open a terminal, navigate to the **memoryReactFrontEnd** folder, and run: 
   - `npm run build`
   - `npm start`
