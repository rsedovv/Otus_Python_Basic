from fastapi import FastAPI

app = FastAPI()

@app.get("/ping/", status_code=200)
async def pong():
    return {"message": "pong"}