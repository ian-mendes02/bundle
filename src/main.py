from fastapi import FastAPI, HTTPException
from src.api.schema import Payload, Response
from src.api.app import App

app = FastAPI()


@app.post("/")
def main(payload: Payload) -> Response:
    if not payload.containers:
        raise HTTPException(400, "No containers provided.")

    if not payload.containers:
        raise HTTPException(400, "Cart is empty.")

    instance = App(payload)
    instance.execute()
    return instance.get_response()
