import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .log import handler
from .worker import calculate_hash

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(handler)

app = FastAPI()

log.debug("Set up web server.")


class Item(BaseModel):
    message: str


@app.post("/hash")
async def hash_message(item: Item):
    log.info("Request: /hash - %s", item)

    if item.message:
        try:
            task = calculate_hash.delay(item.message)
            hash_hex = task.get()

            log.info("Hashed message: '%s' -> '%s'", item.message, hash_hex)

            return {"hash": hash_hex}

        except Exception as e:
            log.exception(e)
            raise HTTPException(status_code=500, detail=str(e)) from e
    else:
        log.exception(e)
        raise HTTPException(status_code=400, detail="Empty message.")
