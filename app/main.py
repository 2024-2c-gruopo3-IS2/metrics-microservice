from fastapi import FastAPI
from app.controllers import controller
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(controller.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)