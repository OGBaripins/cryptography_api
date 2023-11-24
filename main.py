import uvicorn as uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from encrypt import encrypt, decrypt

app = FastAPI()


class RequestBody(BaseModel):
    key: str
    text: str


@app.post("/encrypt")
async def root(body: RequestBody):
    return {"value": encrypt(body.key, body.text)}


@app.post("/decrypt")
async def root(body: RequestBody):
    return {"value": decrypt(body.key, body.text)}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
