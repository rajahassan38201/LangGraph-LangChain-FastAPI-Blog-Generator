# AI Blog Generator (FastAPI + LangGraph)

https://github.com/user-attachments/assets/dda8ee22-5804-4ee8-946e-2087a8593617



This is a full-stack web application that uses a multi-step AI agent to generate blog posts. The user provides a blog title, and the AI (powered by LangGraph) first generates a concise outline and then writes a full blog post based on that outline.

The application features a modern, responsive frontend built with Tailwind CSS and a powerful backend using FastAPI and LangGraph to manage the AI workflow.

# ✨ Features

## Two-Step AI Generation: Generates a 5-point outline first, then generates the full blog post based on that outline.

## Streaming Response: The frontend receives the outline and content as separate events, showing the results in two distinct steps.

## Modern UI: A clean, responsive single-page application built with Tailwind CSS, featuring an animated pink/blue gradient background.

## Copy to Clipboard: "Copy" buttons for both the outline and the final blog post for easy use.

## LangGraph Backend: Demonstrates a clear, multi-step AI workflow using LangGraph to chain AI calls and manage state.

# 🚀 Tech Stack

## Backend:

### FastAPI: For the high-performance asynchronous web server and API.

### LangGraph: To define and run the multi-step AI generation graph (outline -> content).

### Langchain (langchain-openai): To connect to the OpenAI LLM (gpt-4o-mini).

### Uvicorn: As the ASGI server to run the FastAPI application.

### python-dotenv: To manage environment variables (like your API key).

## Frontend:

### HTML5: For the application structure.

### Tailwind CSS (via CDN): For all styling, layout, and the animated gradient.

### JavaScript (Fetch API): To communicate with the backend, handle the streaming JSON response, and update the UI.

## 🔧 Setup and Installation

Follow these steps to get the project running on your local machine.

1. Clone the Repository

(If you have this in a git repository)

git clone https://your-repository-url/ai-blog-generator.git
cd ai-blog-generator


If not, just make sure main.py and index.html are in the same directory.

2. Backend Setup

Create a Virtual Environment (Recommended)

python -m venv venv


On macOS/Linux: source venv/bin/activate

On Windows: .\venv\Scripts\activate

Install Python Dependencies
You will need the following libraries:

pip install "fastapi[all]" uvicorn langgraph langchain-openai python-dotenv


Create a .env File
Create a file named .env in the same directory as main.py. Add your OpenAI API key to this file:

OPENAI_API_KEY=sk-your-secret-api-key-here


3. Frontend Setup

No setup is required! The index.html file uses the Tailwind CSS CDN, so it works immediately.

🏃‍♂️ How to Run the Application

Start the Backend Server
With your virtual environment activated, run the following command in your terminal:

python main.py


You should see a message indicating the server is running:

Starting FastAPI server at [http://127.0.0.1:8000](http://127.0.0.1:8000)
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on [http://127.0.0.1:8000](http://127.0.0.1:8000) (Press CTRL+C to quit)


Open the Application
Open your web browser and navigate to:
http://127.0.0.1:8000

Generate a Blog Post

Enter a topic in the input field (e.g., "The Benefits of Drinking Water").

Click the "Generate" button.

The application will show a loader, then display the generated outline.

It will then show a second loader and display the final blog post.

## 📁 File Structure

.
├── main.py     # The FastAPI backend server with LangGraph logic
├── index.html    # The main HTML/Tailwind/JS frontend
├── .env          # Stores your API key (you must create this)
└── README.md     # This file



This project is licensed under the MIT License.
