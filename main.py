# main.py
import uvicorn
from api.routes import app

if __name__ == "__main__":
    print("Starting FastAPI server with uvicorn...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
