import os
import json
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv
import uvicorn
 
load_dotenv()

class BlogState(TypedDict):
    title: str
    outline: str
    content: str

try:
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
except ImportError:
    print("langchain_openai not installed. Please install it with: pip install langchain_openai")
    exit()
except Exception as e:
    print(f"Error initializing ChatOpenAI. Ensure OPENAI_API_KEY is set in .env: {e}")
    # Fallback to a placeholder if needed, though API calls will fail
    model = None 

def create_outline(state: BlogState) -> BlogState:
    print("--- Executing Node: create_outline ---")
    title = state['title']
    prompt = f"Generate a blog post outline for the topic: '{title}'.Only write 5 outline points, not detail)."
    
    if model:
        outline = model.invoke(prompt).content
        state['outline'] = outline
    else:
        state['outline'] = "Error: Model not initialized. Please check API key."
        
    return state

def create_blog(state: BlogState) -> BlogState:
    print("--- Executing Node: create_blog ---")
    title = state['title']
    outline = state['outline']
    
    prompt = f"Write a well-structured blog post based on the title '{title}' and this outline:\n\n{outline}\n\nEnsure the blog flows naturally and expands on each outline point. Only write 10 lines of content. Each Outline point has only 2 lines of content."
    
    if model:
        content = model.invoke(prompt).content
        state['content'] = content
    else:
        state['content'] = "Error: Model not initialized. Please check API key."
        
    return state

workflow = StateGraph(BlogState)

workflow.add_node('create_outline', create_outline)
workflow.add_node('create_blog', create_blog)

workflow.add_edge(START, 'create_outline')
workflow.add_edge('create_outline', 'create_blog')
workflow.add_edge('create_blog', END)

app_graph = workflow.compile()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class BlogRequest(BaseModel):
    title: str

async def stream_blog_generation(title: str):
    """
    Asynchronous generator to stream the graph's intermediate steps.
    """
    initial_state = {"title": title}
    
    # Use .astream_events to asynchronously stream events
    # We listen for the 'on_chain_end' event for each node
    try:
        async for event in app_graph.astream_events(initial_state, version="v1"):
            kind = event["event"]
            
            if kind == "on_chain_end":
                node_name = event["name"]
                output = event["data"]["output"]
                
                if node_name == "create_outline":
                    # First step is done: yield the outline
                    print("--- Streaming Outline ---")
                    yield json.dumps({"type": "outline", "data": output["outline"]}) + "\n"
                    
                elif node_name == "create_blog":
                    # Second step is done: yield the final content
                    print("--- Streaming Content ---")
                    yield json.dumps({"type": "content", "data": output["content"]}) + "\n"
                    
    except Exception as e:
        print(f"Error during streaming: {e}")
        yield json.dumps({"type": "error", "data": str(e)}) + "\n"

@app.post("/generate-blog-stream/")
async def generate_blog_stream(request: BlogRequest):
    """
    API endpoint to generate the blog post.
    It returns a StreamingResponse that sends JSON objects line by line.
    """
    return StreamingResponse(
        stream_blog_generation(request.title),
        media_type="application/x-ndjson" # ndjson (newline-delimited JSON)
    )

@app.get("/")
async def get_index():
    
    return FileResponse("index.html")

if __name__ == "__main__":
    """
    Runs the FastAPI server using uvicorn.
    """
    print("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)




