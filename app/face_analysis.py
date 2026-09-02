"""
Quick-demo face and visible-skin analysis.

This is a prototype. It detects basic visual signals only and does not
diagnose acne, pigmentation, rosacea, or any medical skin condition.
"""

from typing import List, Tuple

import cv2
import mediapipe as mp
import numpy as np

from app.schemas import FaceProfile, FaceShape, SkinFlag, Undertone

mp_face_mesh = mp.solutions.face_mesh

# Key MediaPipe landmark indices used for measurements
LEFT_CHEEK = 234
RIGHT_CHEEK = 454
JAW_LEFT = 172
JAW_RIGHT = 397
CHIN = 152
FOREHEAD_TOP = 10
LEFT_FOREHEAD_SAMPLE = 108
RIGHT_FOREHEAD_SAMPLE = 337
CHEEK_SAMPLE_LEFT = 50
CHEEK_SAMPLE_RIGHT = 280


def _image_quality_metrics(image_bgr: np.ndarray) -> Tuple[int, int, float, float]:
    """Return image dimensions, brightness, and a blur-resistant sharpness measure."""
    height, width = image_bgr.shape[:2]
    gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    brightness = float(gray_image.mean())
    sharpness = float(cv2.Laplacian(gray_image, cv2.CV_64F).var())
    return height, width, brightness, sharpness


def photo_quality_note(image_bgr: np.ndarray, coords: np.ndarray) -> str:
    """Reject unusable selfies and transparently label lower-confidence ones."""
    height, width, brightness, sharpness = _image_quality_metrics(image_bgr)
    face_width = euclidean_distance(coords[LEFT_CHEEK], coords[RIGHT_CHEEK])
    face_coverage = face_width / width

    blocking_issues = []
    if min(height, width) < 320:
        blocking_issues.append("the image is too small")
    if brightness < 40:
        blocking_issues.append("the image is much too dark")
    if brightness > 235:
        blocking_issues.append("the image is much too bright")
    if sharpness < 18:
        blocking_issues.append("the image is too blurry")
    if face_coverage < 0.18:
        blocking_issues.append("the face is too far from the camera")

    if blocking_issues:
        raise ValueError(
            "This selfie cannot be analysed reliably because "
            + ", ".join(blocking_issues)
            + ". Retake it in even daylight with your full face filling more of the frame."
        )

    issues = []

    if min(height, width) < 400:
        issues.append("the image resolution is low")

    if brightness < 65:
        issues.append("the image is too dark")

    if brightness > 210:
        issues.append("the image is too bright")

    if sharpness < 55:
        issues.append("the image is slightly blurry")

    if face_coverage < 0.27:
        issues.append("the face is a little far from the camera")

    if issues:
        return (
            "Lower-confidence result because "
            + ", ".join(issues)
            + ". Retake the selfie in even daylight, with no filters or makeup, "
              "for a more useful result."
        )

    return (
        "Photo quality looks usable for this prototype. Results are visual "
        "signals only, not a medical diagnosis."
    )


def get_landmarks(image_bgr: np.ndarray) -> np.ndarray:
    """Run MediaPipe Face Mesh and return landmark coordinates in pixel space."""
    height, width = image_bgr.shape[:2]

    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
    ) as face_mesh:
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image_rgb)

        if not results.multi_face_landmarks:
            raise ValueError(
                "No face detected. Retake the selfie in clear, even lighting "
                "with your full face visible."
            )

        landmarks = results.multi_face_landmarks[0].landmark

        return np.array(
            [[landmark.x * width, landmark.y * height] for landmark in landmarks]
        )


def euclidean_distance(point_one: np.ndarray, point_two: np.ndarray) -> float:
    return float(np.linalg.norm(point_one - point_two))


def classify_face_shape(coords: np.ndarray) -> FaceShape:
    """Rule-based face-shape classification using landmark ratios."""
    jaw_width = euclidean_distance(coords[JAW_LEFT], coords[JAW_RIGHT])
    cheekbone_width = euclidean_distance(coords[LEFT_CHEEK], coords[RIGHT_CHEEK])
    face_length = euclidean_distance(coords[FOREHEAD_TOP], coords[CHIN])

    length_to_width = face_length / cheekbone_width
    jaw_to_cheek = jaw_width / cheekbone_width

    if length_to_width > 1.35:
        return FaceShape.OBLONG
    if jaw_to_cheek > 0.87 and length_to_width < 1.20:
        return FaceShape.SQUARE
    if jaw_to_cheek < 0.68:
        return FaceShape.HEART
    if length_to_width < 1.12 and jaw_to_cheek > 0.80:
        return FaceShape.ROUND
    if jaw_to_cheek < 0.76:
        return FaceShape.DIAMOND

    return FaceShape.OVAL


def sample_region_color(
    image_bgr: np.ndarray,
    coords: np.ndarray,
    indices: List[int],
    patch_size: int = 5,
) -> np.ndarray:
    """Average BGR colour from small face-skin sample regions."""
    samples = []
    height, width = image_bgr.shape[:2]

    for index in indices:
        x, y = int(coords[index][0]), int(coords[index][1])

        x_start = max(0, x - patch_size)
        x_end = min(width, x + patch_size)
        y_start = max(0, y - patch_size)
        y_end = min(height, y + patch_size)

        patch = image_bgr[y_start:y_end, x_start:x_end]

        if patch.size > 0:
            samples.append(patch.reshape(-1, 3).mean(axis=0))

    if not samples:
        return np.array([128, 128, 128])

    return np.mean(samples, axis=0)


def build_cheek_skin_mask(image_bgr: np.ndarray, coords: np.ndarray) -> np.ndarray:
    """
    Build a landmark-bounded mask for both cheek areas.

    This avoids skin-colour thresholds, which can be unreliable across skin
    tones and lighting. MediaPipe landmarks instead keep measurements away
    from hair, clothing, and background.
    """
    height, width = image_bgr.shape[:2]
    face_outline = cv2.convexHull(coords.astype(np.int32))
    face_mask = np.zeros((height, width), dtype=np.uint8)
    cv2.fillConvexPoly(face_mask, face_outline, 255)

    cheek_mask = np.zeros((height, width), dtype=np.uint8)
    face_width = euclidean_distance(coords[LEFT_CHEEK], coords[RIGHT_CHEEK])
    radius = max(12, int(face_width * 0.095))

    for index in (CHEEK_SAMPLE_LEFT, CHEEK_SAMPLE_RIGHT):
        center = tuple(coords[index].astype(int))
        cv2.ellipse(cheek_mask, center, (radius, int(radius * 0.82)), 0, 0, 360, 255, -1)

    return cv2.bitwise_and(face_mask, cheek_mask)


def classify_skin_tone_and_undertone(
    image_bgr: np.ndarray,
    coords: np.ndarray,
) -> Tuple[str, Undertone, float, float]:
    """Estimate tone depth and undertone from cheek and forehead samples."""
    avg_bgr = sample_region_color(
        image_bgr,
        coords,
        [
            LEFT_FOREHEAD_SAMPLE,
            RIGHT_FOREHEAD_SAMPLE,
            CHEEK_SAMPLE_LEFT,
            CHEEK_SAMPLE_RIGHT,
        ],
    )

    blue, green, red = avg_bgr
    luminance = 0.299 * red + 0.587 * green + 0.114 * blue

    if luminance > 175:
        depth = "light"
    elif luminance > 150:
        depth = "light-medium"
    elif luminance > 128:
        depth = "medium"
    elif luminance > 105:
        depth = "medium-deep"
    else:
        depth = "deep"

    warm_score = red - blue

    if warm_score > 30:
        undertone = Undertone.WARM
    elif warm_score < -10:
        undertone = Undertone.COOL
    else:
        undertone = Undertone.NEUTRAL

    return depth, undertone, warm_score, luminance


def detect_visible_skin_signals(
    image_bgr: np.ndarray,
    coords: np.ndarray,
) -> List[SkinFlag]:
    """
    Detect basic visible signals from landmark-bounded cheek regions.

    These are unvalidated prototype heuristics. They can be affected by
    lighting, camera processing, makeup, and image quality.
    """
    flags = []
    cheek_mask = build_cheek_skin_mask(image_bgr, coords)
    skin_pixels = image_bgr[cheek_mask > 0]

    if len(skin_pixels) < 250:
        return flags

    gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    texture_map = cv2.Laplacian(gray_image, cv2.CV_64F)
    texture_variance = float(texture_map[cheek_mask > 0].var())

    if texture_variance > 150:
        flags.append(SkinFlag.TEXTURE)

    blue_mean, green_mean, red_mean = skin_pixels.mean(axis=0)

    if red_mean - green_mean > 55:
        flags.append(SkinFlag.REDNESS)

    lab_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
    lightness_variation = float(lab_image[:, :, 0][cheek_mask > 0].std())

    if lightness_variation > 20:
        flags.append(SkinFlag.UNEVEN_TONE)

    return flags


def analyze_face(image_bgr: np.ndarray) -> FaceProfile:
    """Main entry point: image in, structured prototype profile out."""
    coords = get_landmarks(image_bgr)
    quality_note = photo_quality_note(image_bgr, coords)

    face_shape = classify_face_shape(coords)
    skin_depth, undertone, warm_score, luminance = classify_skin_tone_and_undertone(image_bgr, coords)
    skin_flags = detect_visible_skin_signals(image_bgr, coords)

    return FaceProfile(
        face_shape=face_shape,
        undertone=undertone,
        skin_tone_depth=skin_depth,
        skin_flags=skin_flags,
        confidence_note=quality_note,
        warm_score=warm_score,
        luminance=luminance,
    )

def get_debug_metrics(image_bgr: np.ndarray) -> dict:
    """
    Returns raw computed values used in classification, for calibration purposes.
    Not used in the real /analyze flow — only for tuning thresholds against real photos.
    """
    coords = get_landmarks(image_bgr)

    jaw_width = euclidean_distance(coords[JAW_LEFT], coords[JAW_RIGHT])
    cheekbone_width = euclidean_distance(coords[LEFT_CHEEK], coords[RIGHT_CHEEK])
    face_length = euclidean_distance(coords[FOREHEAD_TOP], coords[CHIN])

    avg_bgr = sample_region_color(
        image_bgr, coords,
        [LEFT_FOREHEAD_SAMPLE, RIGHT_FOREHEAD_SAMPLE, CHEEK_SAMPLE_LEFT, CHEEK_SAMPLE_RIGHT]
    )
    blue, green, red = avg_bgr
    luminance = 0.299 * red + 0.587 * green + 0.114 * blue
    warm_score = red - blue

    x, y = int(coords[CHEEK_SAMPLE_LEFT][0]), int(coords[CHEEK_SAMPLE_LEFT][1])
    patch_size = 24
    h, w = image_bgr.shape[:2]
    x0, x1 = max(0, x - patch_size), min(w, x + patch_size)
    y0, y1 = max(0, y - patch_size), min(h, y + patch_size)
    cheek_patch = image_bgr[y0:y1, x0:x1]
    gray_patch = cv2.cvtColor(cheek_patch, cv2.COLOR_BGR2GRAY)
    texture_variance = float(cv2.Laplacian(gray_patch, cv2.CV_64F).var())
    b_mean, g_mean, r_mean = cheek_patch.reshape(-1, 3).mean(axis=0)

    lab_patch = cv2.cvtColor(cheek_patch, cv2.COLOR_BGR2LAB)
    lightness_variation = float(lab_patch[:, :, 0].std())

    return {
        "jaw_width": round(jaw_width, 2),
        "cheekbone_width": round(cheekbone_width, 2),
        "face_length": round(face_length, 2),
        "length_to_width_ratio": round(face_length / cheekbone_width, 3),
        "jaw_to_cheek_ratio": round(jaw_width / cheekbone_width, 3),
        "luminance": round(luminance, 1),
        "warm_score_r_minus_b": round(warm_score, 1),
        "texture_variance": round(texture_variance, 1),
        "red_minus_green": round(r_mean - g_mean, 1),
        "lightness_variation_std": round(lightness_variation, 1),
    }
