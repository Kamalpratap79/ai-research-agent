from fastapi import FastAPI
from dotenv import load_dotenv
from backend.endpoints.research import router

load_dotenv()

app = FastAPI(title="AI Research Agent Backend")
app.include_router(router)
