# Project Overview

This repository showcases my ability to integrate Data Science with Full-Stack Development using Python and React.

The core of this project is a FastAPI-based RESTful API that simulates human autobiographical memory. It leverages several key components:

1. **Associations** – Implemented with a **breadth-first search (BFS)** algorithm to identify the shortest connection paths between friends.
2. **Episodic Memory** – Stored in an "Events" database table, providing event descriptions to simulate memory recall.
3. **Semantic Memory** – Powered by a local Large Language Model (LLM), Llama-3.2-1B, via the Hugging Face "transformers" library for contextual understanding.

The result is a dynamic and interactive representation of how autobiographical memory functions.

<img width="644" alt="Skærmbillede 2024-11-21 kl  15 10 06" src="https://github.com/user-attachments/assets/7550028d-b116-4aaa-98ae-3b15d5334b44">

## Key Features

### 1. **LLM Integration**  
   This project integrates Meta's Llama-3.2-1B, a local language model. Please note that performance is dependent on your system's hardware (RAM/CPU), as no hardware accelerations are used to ensure broad compatibility.

### 2. **BFS Algorithm**  
   The BFS algorithm, responsible for finding the shortest path between friends, is encapsulated in `bfsObject.py`.

### 3. **Back-End**  
   The back-end is built with **FastAPI**, providing the data access layer and handling HTTP requests for smooth communication with the front-end.

### 4. **Front-End**  
   The front-end is developed with **React** and styled using **Tailwind CSS**. A graph is used to visually represent the connection paths between friends.

### 5. **Testing**  
   Unit tests for this project are yet to be written, but they are planned for future development.

## Access to Llama-3.2-1B

If you would like access to the Llama-3.2-1B model, please feel free to reach out to me. The model files are approximately 5GB in total.
