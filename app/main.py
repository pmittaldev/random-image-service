import os
import random
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Random PNG Service")

# Default image folder (env override supported)
DEFAULT_DIR = Path(__file__).parent / "images"
IMAGE_DIR = Path(os.getenv("IMAGE_DIR") or DEFAULT_DIR).resolve()

@app.on_event("startup")
def startup_log():
    logger.info(f"Starting up... using image directory: {IMAGE_DIR}")
    if not IMAGE_DIR.exists():
        logger.warning(f"Image directory {IMAGE_DIR} does not exist yet!")

@app.get("/images/{_:path}", response_class=FileResponse)
def get_random_image():
    logger.info(f"Received request for random image. Checking directory: {IMAGE_DIR}")

    if not IMAGE_DIR.exists():
        logger.error(f"Directory not found: {IMAGE_DIR}")
        raise HTTPException(status_code=404, detail=f"Image directory not found: {IMAGE_DIR}")

    files = [p for p in IMAGE_DIR.iterdir() if p.is_file() and p.suffix.lower() == ".png"]
    logger.info(f"Found {len(files)} PNG")

    if not files:
        logger.warning("No PNG files found in directory.")
        raise HTTPException(status_code=404, detail=f"No PNG images found in {IMAGE_DIR}")

    chosen = random.choice(files)
    logger.info(f"Randomly selected file: {chosen.name}")

    return FileResponse(path=chosen, media_type="image/png", filename=chosen.name)
