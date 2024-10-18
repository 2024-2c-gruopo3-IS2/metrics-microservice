from fastapi import FastAPI
from app.controllers import controller

app = FastAPI()

app.include_router(controller.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)