from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="RAG Chatbot API",
    description="Academicc and Programming RAG Chatbot",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message" : "RAG Chatbot API is running!",
        "status" : "healthy",
        "version" : "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status" : "healthy",
        "database" : "not_connected_yet",
        "vector_db" : "not_connected_yet"
    }
