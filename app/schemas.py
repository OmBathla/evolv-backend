"""
Data models shared across the face analysis pipeline and recommendation engine.
This is the "contract" between ML pipeline output and recommendation engine input -
keep this schema stable so both engineers can build against it independently.
"""

from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class FaceShape(str, Enum):
    OVAL = "oval"
    ROUND = "round"
    SQUARE = "square"
    HEART = "heart"
    DIAMOND = "diamond"
    OBLONG = "oblong"


class Undertone(str, Enum):
    WARM = "warm"
    COOL = "cool"
    NEUTRAL = "neutral"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non_binary"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class SkinFlag(str, Enum):
    DRYNESS = "dryness"
    OILINESS = "oiliness"
    UNEVEN_TONE = "uneven_tone"
    REDNESS = "redness"
    TEXTURE = "visible_texture"
    BREAKOUTS = "breakout_like_spots"
    DARK_SPOTS = "dark_spot_like_areas"
    TANNING = "sun_exposure_unevenness"


class FaceProfile(BaseModel):
    face_shape: FaceShape
    undertone: Undertone
    skin_tone_depth: str
    skin_flags: List[SkinFlag]
    confidence_note: Optional[str] = None
    warm_score: float = 0.0
    luminance: float = 0.0
    gender: Gender = Gender.PREFER_NOT_TO_SAY


class HaircutSuggestion(BaseModel):
    name: str
    reason: str


class SkincareStep(BaseModel):
    step: str
    budget_product: str
    premium_product: str
    reason: str


class ColorPaletteItem(BaseModel):
    color_name: str
    hex: str
    reason: str


class RecommendationResponse(BaseModel):
    face_profile: FaceProfile
    haircuts: List[HaircutSuggestion]
    skincare_routine: List[SkincareStep]
    color_palette: List[ColorPaletteItem]