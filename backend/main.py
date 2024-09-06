from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.file_routes import router as file_router
from routes.llm_routes import router as chat_router
import uvicorn

app = FastAPI()

# Set up CORS
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes
app.include_router(file_router)
app.include_router(chat_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
