from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class EncryptBody(BaseModel):
    key: str
    text: str


@app.post("/encrypt")
async def root(body: EncryptBody):
    pass


@app.get("/decrypt")
async def root():
    pass
