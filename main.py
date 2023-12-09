import base64

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from encryption import encrypt, decrypt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="null",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class RequestBody(BaseModel):
    key: str
    text: str


@app.post("/encrypt")
async def root(body: RequestBody):
    value = encrypt(body.key, body.text)
    json_data = jsonable_encoder(value, custom_encoder={
        bytes: lambda v: base64.b64encode(v).decode('utf-8')})
    return {"value": json_data}


@app.post("/decrypt")
async def root(body: RequestBody):
    value = base64.b64decode(body.text)
    return {"value": decrypt(body.key, value)}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)  # Dont run this
    # Run this in terminal: uvicorn main:app --reload
