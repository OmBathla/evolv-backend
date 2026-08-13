"""
Evolv backend - v1 API entry point.

POST /analyze accepts:
- a front-facing selfie
- optional self-reported skin concerns
- gender (used to select men's vs women's haircut recommendations)

The photo provides visible signals, while the user's selected concerns
and gender make the recommendations more personal.
"""

import os
import shutil
import tempfile

import cv2
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.face_analysis import analyze_face, get_debug_metrics
from app.recommendation_engine import generate_recommendations
from app.schemas import RecommendationResponse, SkinFlag, Gender

app = FastAPI(title="Evolv API", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def home():
    return FileResponse("web/index.html")


@app.get("/health")
def health_check():
    return {"status": "ok"}


def parse_skin_concerns(raw_concerns: str) -> list[SkinFlag]:
    """
    Converts a comma-separated form value into SkinFlag values.

    Example:
    breakout_like_spots,dark_spot_like_areas
    """
    if not raw_concerns.strip():
        return []

    flags = []

    for concern in raw_concerns.split(","):
        cleaned_concern = concern.strip().lower()

        try:
            flag = SkinFlag(cleaned_concern)
        except ValueError:
            allowed = ", ".join(flag.value for flag in SkinFlag)
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Unknown skin concern: '{cleaned_concern}'. "
                    f"Use one or more of: {allowed}"
                ),
            )

        if flag not in flags:
            flags.append(flag)

    return flags


def parse_gender(raw_gender: str) -> Gender:
    """Converts the form value into a Gender enum, defaulting safely if unrecognized."""
    cleaned = raw_gender.strip().lower()
    try:
        return Gender(cleaned)
    except ValueError:
        return Gender.PREFER_NOT_TO_SAY


@app.post("/analyze", response_model=RecommendationResponse)
async def analyze(
    front_image: UploadFile = File(...),
    skin_concerns: str = Form(""),
    gender: str = Form("prefer_not_to_say"),
):
    """
    Takes a selfie plus optional self-reported concerns and gender.

    The photo detects only basic visible signals. The optional concerns field
    improves personalization and does not attempt to diagnose skin conditions.
    Gender is used only to select between men's and women's haircut suggestions.
    """
    if not front_image.content_type or not front_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        shutil.copyfileobj(front_image.file, tmp)
        tmp_path = tmp.name

    try:
        image_bgr = cv2.imread(tmp_path)

        if image_bgr is None:
            raise HTTPException(status_code=400, detail="Could not read image file")

        profile = analyze_face(image_bgr)

        profile.gender = parse_gender(gender)

        user_reported_flags = parse_skin_concerns(skin_concerns)

        for flag in user_reported_flags:
            if flag not in profile.skin_flags:
                profile.skin_flags.append(flag)

        return generate_recommendations(profile)

    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error))

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.post("/debug-analyze")
async def debug_analyze(front_image: UploadFile = File(...)):
    """Temporary calibration endpoint - shows raw numbers behind each classification."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        shutil.copyfileobj(front_image.file, tmp)
        tmp_path = tmp.name
    try:
        image_bgr = cv2.imread(tmp_path)
        if image_bgr is None:
            raise HTTPException(status_code=400, detail="Could not read image file")
        return get_debug_metrics(image_bgr)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)