import base64

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from encryption import encrypt, decrypt, encrypt_block_single, decrypt_block_single

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
    full_operation: bool


@app.post("/encrypt")
async def root(body: RequestBody):
    try:
        if body.full_operation:
            value = encrypt(body.key, body.text)
        else:
            value = encrypt_block_single(body.key, body.text)
    except Exception as e:
        return {"value": f"Inputs were defined incorrectly"}
    return {"value": value.hex()}


@app.post("/decrypt")
async def root(body: RequestBody):
    try:
        if body.full_operation:
            value = decrypt(body.key, bytes.fromhex(body.text))
        else:
            value = decrypt_block_single(body.key, bytes.fromhex(body.text))
    except Exception as e:
        return {"value": f"Inputs were defined incorrectly"}
    return {"value": value}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    # Run this in terminal: uvicorn main:app --reload
