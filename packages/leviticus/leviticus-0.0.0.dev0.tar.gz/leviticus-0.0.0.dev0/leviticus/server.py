"""Web server module for the Leviticus package."""

from fastapi import FastAPI
from . import main

app = FastAPI()

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": main.hello()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
