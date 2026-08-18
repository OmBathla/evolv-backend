"""
Free recommendation engine.

Uses the curated knowledge base directly, so it needs no API key,
no internet connection, and no paid AI credits.

Personalization approach:
- Haircuts: gender selects which curated list to pull from (men's vs
  women's named cuts), then a deterministic profile-hash picks 3 distinct
  suggestions out of that face shape's pool.
- Cleanser: chosen based on detected oiliness/dryness signal, then a
  deterministic profile-hash picks one of several options in that bucket.
- Sunscreen: chosen based on detected skin tone depth, then a deterministic
  profile-hash picks one of several options in that bucket.
- Flag-triggered skincare (redness, texture, dark spots, etc.): each flag has
  several product options; a deterministic profile-hash picks one per flag.
  Steps are deduplicated so e.g. sunscreen never appears twice.
- Color palette: every candidate color in a master pool is individually
  scored against the person's REAL detected skin warmth and luminance
  (not just a rounded "warm/cool/neutral" label), so two people who share
  an undertone label but differ in actual tone will get different results.
  Each color's reason line uses a per-color descriptor plus a hashed
  sentence structure, so wording varies across colors, not just values.

Same profile in -> same result out (reproducible on retest), but different
profiles (including different gender selections) produce genuinely
different recommendations across the board.
"""

import hashlib

from app.schemas import (
    FaceProfile,
    RecommendationResponse,
    HaircutSuggestion,
    SkincareStep,
    ColorPaletteItem,
)
from app.knowledge_base import (
    HAIRCUT_BY_FACE_SHAPE_MEN,
    HAIRCUT_BY_FACE_SHAPE_WOMEN,
    MASTER_COLOR_PALETTE,
    COLOR_DESCRIPTORS,
    SKINCARE_BY_FLAG,
    CLEANSER_OPTIONS,
    SUNSCREEN_OPTIONS,
)


# ---------------------------------------------------------------------------
# Deterministic selection helpers
# ---------------------------------------------------------------------------

def _profile_base_key(profile: FaceProfile, salt: str) -> str:
    flags_key = ",".join(sorted(f.value for f in profile.skin_flags))
    return f"{profile.face_shape.value}-{profile.undertone.value}-{profile.skin_tone_depth}-{profile.gender.value}-{flags_key}-{salt}"


def _pick_option(options: list, profile: FaceProfile, salt: str):
    """
    Deterministically pick ONE option from a list based on the user's full
    profile. Same profile + same salt always returns the same index
    (reproducible on retest), but different profiles land on a different
    option far more reliably since the hash key includes the full flag list.
    """
    if not options:
        return None
    if len(options) == 1:
        return options[0]

    key = _profile_base_key(profile, salt)
    digest = hashlib.sha256(key.encode()).hexdigest()
    index = int(digest, 16) % len(options)
    return options[index]


def _pick_option_multi(options: list, profile: FaceProfile, salt: str, count: int = 3) -> list:
    """
    Deterministically pick MULTIPLE distinct options from a list, personalized
    to the profile. Scores every option via its own hash and returns the
    top `count`, so different profiles get a different subset and ordering.
    """
    if len(options) <= count:
        return options

    base_key = _profile_base_key(profile, salt)
    scored = []
    for option in options:
        # use a stable identifying field for each option type
        identifier = option.get("name") or option.get("color_name") or str(option)
        item_key = f"{base_key}-{identifier}"
        digest = hashlib.sha256(item_key.encode()).hexdigest()
        scored.append((int(digest, 16), option))

    scored.sort(key=lambda pair: pair[0])
    return [option for _, option in scored[:count]]


def _pick_cleanser(profile: FaceProfile) -> dict:
    flag_values = [f.value for f in profile.skin_flags]
    if "oiliness" in flag_values:
        skin_type = "oily"
    elif "dryness" in flag_values:
        skin_type = "dry"
    else:
        skin_type = "normal"
    return _pick_option(CLEANSER_OPTIONS[skin_type], profile, salt="cleanser")


def _pick_sunscreen(profile: FaceProfile) -> dict:
    depth = profile.skin_tone_depth
    if depth in ("light", "light-medium"):
        bucket = "light"
    elif depth == "medium":
        bucket = "medium"
    else:
        bucket = "deep"
    return _pick_option(SUNSCREEN_OPTIONS[bucket], profile, salt="sunscreen")


def _pick_haircuts(profile: FaceProfile, count: int = 3) -> list:
    if profile.gender.value == "female":
        all_haircuts = HAIRCUT_BY_FACE_SHAPE_WOMEN.get(profile.face_shape.value, [])
    elif profile.gender.value == "male":
        all_haircuts = HAIRCUT_BY_FACE_SHAPE_MEN.get(profile.face_shape.value, [])
    else:
        all_haircuts = (
            HAIRCUT_BY_FACE_SHAPE_MEN.get(profile.face_shape.value, [])
            + HAIRCUT_BY_FACE_SHAPE_WOMEN.get(profile.face_shape.value, [])
        )
    return _pick_option_multi(all_haircuts, profile, salt="haircuts", count=count)


# ---------------------------------------------------------------------------
# Color scoring (compares every candidate color against the person's real
# detected skin warmth + luminance, not a fixed per-undertone lookup)
# ---------------------------------------------------------------------------

def _hex_to_rgb(hex_code: str) -> tuple:
    hex_code = hex_code.lstrip("#")
    return tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))


def _color_warmth_and_luminance(hex_code: str) -> tuple:
    r, g, b = _hex_to_rgb(hex_code)
    warmth = r - b
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return warmth, luminance


def _score_color_for_profile(color: dict, profile: FaceProfile) -> float:
    """
    Lower score = better match.
      - Undertone harmony: the color's own warmth direction should broadly
        agree with the user's warm_score direction.
      - Brightness contrast: a moderate contrast against skin luminance
        tends to be flattering; colors nearly identical to skin tone, or
        at an extreme opposite, score worse.
    """
    color_warmth, color_luminance = _color_warmth_and_luminance(color["hex"])

    if profile.warm_score > 15:  # warm undertone
        undertone_penalty = 0 if color_warmth > -10 else abs(color_warmth) * 0.5
    elif profile.warm_score < -5:  # cool undertone
        undertone_penalty = 0 if color_warmth < 20 else color_warmth * 0.5
    else:  # neutral - mild penalty either direction
        undertone_penalty = abs(color_warmth) * 0.15

    contrast = abs(color_luminance - profile.luminance)
    ideal_contrast = 90
    contrast_penalty = abs(contrast - ideal_contrast) * 0.6

    return undertone_penalty + contrast_penalty


def _build_color_reason(color: dict, profile: FaceProfile) -> str:
    color_warmth, color_luminance = _color_warmth_and_luminance(color["hex"])
    contrast = abs(color_luminance - profile.luminance)
    descriptor = COLOR_DESCRIPTORS.get(color["color_name"], "a distinctive shade")

    if profile.warm_score > 15 and color_warmth > -10:
        undertone_fit = "warm"
    elif profile.warm_score < -5 and color_warmth < 20:
        undertone_fit = "cool"
    else:
        undertone_fit = "balanced"

    if contrast > 110:
        contrast_tier = "high"
    elif contrast > 60:
        contrast_tier = "medium"
    else:
        contrast_tier = "low"

    structure_index = int(hashlib.sha256(color["color_name"].encode()).hexdigest(), 16) % 3

    templates = {
        ("warm", "high"): [
            f"{color['color_name']} is {descriptor}, and its warmth stands out sharply against your skin, giving a bold, statement-making effect.",
            f"Against your warm undertone, {color['color_name']} reads as {descriptor} that pops with real visual punch.",
            f"With {descriptor}, {color['color_name']} plays well off your warm undertone and creates a striking, high-impact look.",
        ],
        ("warm", "medium"): [
            f"{color['color_name']} brings {descriptor}, sitting comfortably alongside your warm undertone with a flattering, noticeable lift.",
            f"As {descriptor}, {color['color_name']} pairs naturally with your warm undertone for a look that feels put-together without trying too hard.",
            f"{color['color_name']} — {descriptor} — complements your warm undertone with just enough contrast to stand out.",
        ],
        ("warm", "low"): [
            f"{color['color_name']} offers {descriptor} that blends smoothly into your warm undertone for a soft, tonal effect.",
            f"With {descriptor}, {color['color_name']} sits close to your natural warmth, ideal for an understated everyday look.",
            f"{color['color_name']} — {descriptor} — melts gently into your warm undertone rather than contrasting against it.",
        ],
        ("cool", "high"): [
            f"{color['color_name']} is {descriptor}, and it contrasts vividly with your cool undertone for a sharp, eye-catching finish.",
            f"Against your cool undertone, {color['color_name']} reads as {descriptor} with striking, high-visibility impact.",
            f"With {descriptor}, {color['color_name']} creates real drama against your cool undertone.",
        ],
        ("cool", "medium"): [
            f"{color['color_name']} brings {descriptor}, complementing your cool undertone with a clean, balanced lift.",
            f"As {descriptor}, {color['color_name']} works naturally with your cool undertone for an easy, polished look.",
            f"{color['color_name']} — {descriptor} — pairs well with your cool undertone without overwhelming it.",
        ],
        ("cool", "low"): [
            f"{color['color_name']} offers {descriptor} that sits gently against your cool undertone for a soft, cohesive look.",
            f"With {descriptor}, {color['color_name']} stays close to your natural coolness for a subtle, low-key effect.",
            f"{color['color_name']} — {descriptor} — blends quietly with your cool undertone.",
        ],
        ("balanced", "high"): [
            f"{color['color_name']} is {descriptor}, standing out with strong contrast that works well against a balanced undertone.",
            f"Against your neutral undertone, {color['color_name']} reads as {descriptor} with bold visual presence.",
            f"With {descriptor}, {color['color_name']} makes a confident statement against your balanced undertone.",
        ],
        ("balanced", "medium"): [
            f"{color['color_name']} brings {descriptor}, offering a flattering middle ground against your balanced undertone.",
            f"As {descriptor}, {color['color_name']} suits your neutral undertone with an easy, versatile appeal.",
            f"{color['color_name']} — {descriptor} — reads as a natural, adaptable choice for a balanced undertone.",
        ],
        ("balanced", "low"): [
            f"{color['color_name']} offers {descriptor} that stays close in tone to a balanced undertone for a soft, subtle look.",
            f"With {descriptor}, {color['color_name']} sits gently against a neutral undertone for a low-contrast, understated effect.",
            f"{color['color_name']} — {descriptor} — blends smoothly with a balanced undertone.",
        ],
    }

    options = templates[(undertone_fit, contrast_tier)]
    return options[structure_index]


def _pick_best_colors(profile: FaceProfile, count: int = 4) -> list:
    scored = [
        (_score_color_for_profile(color, profile), dict(color))
        for color in MASTER_COLOR_PALETTE
    ]
    scored.sort(key=lambda pair: pair[0])
    top_colors = [color for _, color in scored[:count]]

    for color in top_colors:
        color["reason"] = _build_color_reason(color, profile)

    return top_colors


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def generate_recommendations(profile: FaceProfile) -> RecommendationResponse:
    """Create fully personalized recommendations from the local knowledge base."""

    haircut_data = _pick_haircuts(profile, count=3)

    skincare_data = []
    existing_step_names = set()

    cleanser = _pick_cleanser(profile)
    skincare_data.append(cleanser)
    existing_step_names.add(cleanser["step"])

    sunscreen = _pick_sunscreen(profile)
    skincare_data.append(sunscreen)
    existing_step_names.add(sunscreen["step"])

    for skin_flag in profile.skin_flags:
        options = SKINCARE_BY_FLAG.get(skin_flag.value)
        if not options:
            continue
        picked = _pick_option(options, profile, salt=skin_flag.value)
        if picked and picked["step"] not in existing_step_names:
            skincare_data.append(picked)
            existing_step_names.add(picked["step"])

    palette_data = _pick_best_colors(profile, count=4)

    return RecommendationResponse(
        face_profile=profile,
        haircuts=[HaircutSuggestion(**item) for item in haircut_data],
        skincare_routine=[SkincareStep(**item) for item in skincare_data],
        color_palette=[ColorPaletteItem(**item) for item in palette_data],
    )
