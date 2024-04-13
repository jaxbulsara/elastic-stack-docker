import hashlib
import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.FileHandler("/var/logs/hash_requests.log")
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
            hash_object = hashlib.sha256(item.message.encode())
            hash_hex = hash_object.hexdigest()

            log.info("Hash: %s, Message: %s", hash_hex, item.message)

            return {"hash": hash_hex}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Empty message.")
