
from fastapi import FastAPI, File, UploadFile, HTTPException
import os
import uvicorn
from process import processor
app = FastAPI()

from fastapi import FastAPI, File, UploadFile, HTTPException, Header
from typing import Optional
import os
import uvicorn
from process import processor

app = FastAPI()

@app.post("/upload-image")
async def receive_image(
    file: UploadFile = File(...), 
   # authorization: Optional[str] = Header(None) # capture JWT
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # if not authorization or not authorization.startswith("Bearer "):
    #     raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    # token = authorization.split(" ")[1]

    image_data = await file.read()

    try:
        result = processor(image_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "Image processed",
        "filename": file.filename,
        "status": "success"
    }

if __name__ == "__main__":
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)