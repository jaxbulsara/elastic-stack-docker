import datetime
import hashlib

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Model for the incoming payload where message is a string.
class Item(BaseModel):
    message: str


# Function to log requests.
def log_request(message: str, hash_value: str):
    timestamp = datetime.datetime.now().replace(microsecond=0).isoformat()
    log_message = f"[{timestamp}] Hash: {hash_value}, Message: {message}\n"
    with open("/var/logs/hash_requests.log", "a") as log_file:
        log_file.write(log_message)


@app.post("/hash")
async def hash_message(item: Item):
    if item.message:
        try:
            # Create a SHA256 hash of the message.
            hash_object = hashlib.sha256(item.message.encode())
            hash_hex = hash_object.hexdigest()

            # Log the request and response details.
            log_request(item.message, hash_hex)

            return {"message": item.message, "hash": hash_hex}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Empty message.")
