from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from PIL import Image
import io
from PIL import Image, UnidentifiedImageError
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific domains in prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Platform dimensions
platform_sizes = {
    "youtube_thumbnail": (1280, 720),
    "youtube_shorts": (720, 1280),
    "instagram_post": (1080, 1080),
    "instagram_story": (1080, 1920)
}



@app.post("/resize")
async def resize_image(platform: str, file: UploadFile = File(...)):
    try:
        if platform not in platform_sizes:
            return {"error": "Invalid platform"}

        # Read file bytes safely
        contents = await file.read()
        img_io = io.BytesIO(contents)

        try:
            img = Image.open(img_io).convert("RGB")  # Convert to RGB for JPEG
        except UnidentifiedImageError:
            return {"error": "Cannot identify image file"}

        resized = img.resize(platform_sizes[platform])

        output_io = io.BytesIO()
        resized.save(output_io, format="JPEG", quality=90)
        output_io.seek(0)

        return StreamingResponse(output_io, media_type="image/jpeg")

    except Exception as e:
        print("❌ Resize error:", e)
        return {"error": str(e)}

