from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from fastapi.responses import StreamingResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

sizes = {
    "youtube_shorts": (1080, 1920),
    "youtube_video": (1280, 720),
    "instagram_post": (1080, 1080),
}

@app.post("/resize")
async def resize_image(platform: str, file: UploadFile = File(...)):
    try:
        content = await file.read()
        print("📦 File size:", len(content))

        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Empty file")

        try:
            image = Image.open(BytesIO(content))
            image = image.convert("RGB")
        except UnidentifiedImageError:
            print("❌ Image format not supported")
            raise HTTPException(status_code=400, detail="Unsupported image format")

        if platform not in sizes:
            raise HTTPException(status_code=400, detail="Invalid platform")

        width, height = sizes[platform]
        resized_image = image.resize((width, height))
        buffer = BytesIO()
        resized_image.save(buffer, format="JPEG")
        buffer.seek(0)

        return StreamingResponse(buffer, media_type="image/jpeg", headers={
            "Content-Disposition": f"attachment; filename=resized_{platform}.jpg"
        })
    except Exception as e:
        print("❌ Exception in /resize:", str(e))
        raise HTTPException(status_code=500, detail="Resize failed")
