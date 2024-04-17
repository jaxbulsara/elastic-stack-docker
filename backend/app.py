import hashlib
import logging

from .worker import calculate_hash
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.FileHandler("/logs/hash_requests.log")
formatter = logging.Formatter("[%(asctime)s] %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)

app = FastAPI()


class Item(BaseModel):
    message: str


@app.post("/hash")
async def hash_message(item: Item):
    if item.message:
        try:
            task = calculate_hash.delay(message)
            hash_hex = task.get()

            log.info("Hash: %s, Message: %s", hash_hex, item.message)

            return {"hash": hash_hex}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Empty message.")
