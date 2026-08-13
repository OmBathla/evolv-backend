"""
Curated reference data used to ground recommendations.

Each skincare need maps to MULTIPLE product options (3 each) across a range
of brands - drugstore/Indian-market brands (The Derma Co, Minimalist,
Dot & Key, Re'equil, Pilgrim, Plix, CeraVe) plus a few international/premium
picks (SkinCeuticals, The Ordinary, La Roche-Posay, Dr. Jart+, Paula's
Choice, La Mer). Selection between options is handled in
recommendation_engine.py using a deterministic profile-based selector - so
the same person always gets the same result on retest (reproducible), but
different people with different face shapes, undertones, tone depths, or
skin flags will genuinely get different product picks.

This is a STARTER dataset. Expand/refine with real dermatologist-informed
input before production launch - these are reasonable, commonly-used
products for their categories, not medical prescriptions.
"""

HAIRCUT_BY_FACE_SHAPE_MEN = {
    "oval": [
        {"name": "Textured Crop", "reason": "A versatile, low-maintenance cut with natural texture on top that works with almost any oval face."},
        {"name": "Classic Side Part", "reason": "A polished, timeless cut with tapered sides — flatters oval faces without fighting their natural balance."},
        {"name": "French Crop", "reason": "A short fringe with faded sides that suits the balanced proportions of an oval face."},
        {"name": "Curtain Fringe", "reason": "Center-parted, face-framing length that pairs naturally with oval symmetry."},
        {"name": "Caesar Cut", "reason": "A uniform short length with a forward fringe, clean and structured on an oval face."},
    ],
    "round": [
        {"name": "Textured Quiff", "reason": "Height and volume at the crown add vertical length, breaking up roundness."},
        {"name": "High Fade with Length on Top", "reason": "Shorter sides with more length up top create the illusion of a longer face."},
        {"name": "Angular Fringe", "reason": "A sharper, side-swept fringe adds definition that softens a round outline."},
        {"name": "Pompadour", "reason": "Height at the front elongates a round face shape."},
        {"name": "Warrior Cut", "reason": "Short tight sides with longer textured layers on top add strong vertical lines."},
    ],
    "square": [
        {"name": "Curtain Hair", "reason": "Center-parted, face-framing lengths soften a square jaw's sharp angles."},
        {"name": "Soft Layered Crop", "reason": "Gentle layers around the temples take the edge off a strong jawline."},
        {"name": "Side Part with Soft Fringe", "reason": "A relaxed side part with textured fringe balances square proportions."},
        {"name": "Textured Crop", "reason": "Piecey texture on top draws the eye upward, away from jaw angles."},
        {"name": "Low Taper with Fringe", "reason": "Subtle fade paired with forward texture softens strong facial angles."},
    ],
    "heart": [
        {"name": "Modern Mullet", "reason": "Volume on top and length in back help balance a wider forehead with a narrower chin."},
        {"name": "Textured Fringe", "reason": "A fringe draws attention to the upper face and balances a heart-shaped jawline."},
        {"name": "Side-Swept Crop", "reason": "Asymmetrical volume shifts focus away from a narrower chin."},
        {"name": "Caesar Cut", "reason": "Uniform short length with forward fringe keeps proportions balanced on a heart face."},
        {"name": "Low Fade with Textured Top", "reason": "Adds width perception at the crown to offset a heart-shaped taper toward the chin."},
    ],
    "diamond": [
        {"name": "French Crop", "reason": "Horizontal fringe with fade softens prominent cheekbones on a diamond face."},
        {"name": "Textured Crop with Fringe", "reason": "Width at the forehead balances the narrower chin and forehead typical of diamond faces."},
        {"name": "Side Part", "reason": "A classic part adds structure that complements angular diamond features."},
        {"name": "Curtain Fringe", "reason": "Face-framing length softens the sharper contours of a diamond face shape."},
        {"name": "Low Taper Fade", "reason": "Clean, subtle sides keep focus balanced rather than emphasizing cheekbone width."},
    ],
    "oblong": [
        {"name": "Fringe-Forward Crop", "reason": "A fringe visually shortens an elongated face."},
        {"name": "Textured Crop with Width", "reason": "Volume at the sides adds horizontal balance to counter face length."},
        {"name": "Caesar Cut", "reason": "Short, uniform length with forward fringe helps balance an oblong silhouette."},
        {"name": "Curtain Hair", "reason": "Face-framing sides add width perception to a longer face shape."},
        {"name": "Soft Layered Mullet", "reason": "Layers and length in back balance vertical face length."},
    ],
}

HAIRCUT_BY_FACE_SHAPE_WOMEN = {
    "oval": [
        {"name": "Most styles work well", "reason": "Oval face shapes have balanced proportions, offering flexibility across nearly any cut."},
        {"name": "Curtain Bangs with Layers", "reason": "Soft, face-framing bangs blend seamlessly into an oval face's natural balance."},
        {"name": "Blunt Bob", "reason": "A sharp, clean line works cleanly with balanced oval proportions."},
        {"name": "Butterfly Layers", "reason": "Cascading layers add movement without disrupting oval symmetry."},
        {"name": "Modern Shag", "reason": "Layered texture and volume suit the flexibility of an oval face."},
    ],
    "round": [
        {"name": "Layered Lob with Side Bangs", "reason": "Side-swept bangs and length past the chin elongate a round face."},
        {"name": "Asymmetrical Lob", "reason": "Uneven lengths break up roundness and add angularity."},
        {"name": "Long Layers", "reason": "Length and layering add vertical lines that slim a round silhouette."},
        {"name": "Jawline Bob", "reason": "A precise cut at the jaw creates definition against soft round features."},
        {"name": "Side-Part Glam Cut", "reason": "Asymmetry and body from a deep side part add structure to a round face."},
    ],
    "square": [
        {"name": "Curtain Bangs", "reason": "Soft, face-framing bangs ease the sharpness of a square jawline."},
        {"name": "Butterfly Layers", "reason": "Soft cascading layers soften strong square angles."},
        {"name": "Rounded Bob with Bangs", "reason": "A rounded silhouette balances square jaw definition."},
        {"name": "Long Layers with Soft Fringe", "reason": "Movement and softness around the face counter angular features."},
        {"name": "Side-Swept Lob", "reason": "Asymmetrical framing draws focus away from strong jaw angles."},
    ],
    "heart": [
        {"name": "Chin-Length Bob", "reason": "Width at the jaw balances a heart face's wider forehead and narrower chin."},
        {"name": "Side-Swept Layers", "reason": "Volume near the jaw offsets a narrower chin."},
        {"name": "Curtain Bangs", "reason": "Softens a wider forehead, a common heart-shape feature."},
        {"name": "Textured Lob", "reason": "Adds fullness lower on the face to balance heart-shaped proportions."},
        {"name": "Rounded Bob", "reason": "Width at the jawline complements a heart face's narrower chin."},
    ],
    "diamond": [
        {"name": "Chin-Length Bob", "reason": "Adds width at the jaw and forehead to balance narrow diamond chin proportions."},
        {"name": "Fringe with Forehead Width", "reason": "Softens prominent cheekbones typical of a diamond face."},
        {"name": "Side-Part Waves", "reason": "Asymmetry balances angular diamond cheekbone structure."},
        {"name": "Textured Lob", "reason": "Adds volume at jaw level to soften a narrower chin."},
        {"name": "Curtain Bangs", "reason": "Frames prominent cheekbones gently."},
    ],
    "oblong": [
        {"name": "Blunt Bob with Bangs", "reason": "A fringe and blunt line shorten the visual length of an oblong face."},
        {"name": "Layered Lob", "reason": "Width-adding layers balance an elongated face shape."},
        {"name": "Curtain Bangs", "reason": "Softens face length and adds horizontal framing."},
        {"name": "Rounded Bob", "reason": "A fuller, rounded shape counters vertical face length."},
        {"name": "Shoulder-Length Waves with Fringe", "reason": "Fringe plus width at the sides balances an oblong silhouette."},
    ],
}

# Master color pool. Each entry's own warmth and brightness are computed
# automatically from its hex value in recommendation_engine.py, then
# compared against the user's real detected skin warmth/luminance to
# score the best matches - not a fixed per-undertone lookup.
MASTER_COLOR_PALETTE = [
    {"color_name": "Olive Green", "hex": "#556B2F"},
    {"color_name": "Terracotta", "hex": "#E2725B"},
    {"color_name": "Mustard Yellow", "hex": "#D4AC0D"},
    {"color_name": "Rust Orange", "hex": "#B7410E"},
    {"color_name": "Camel Brown", "hex": "#C19A6B"},
    {"color_name": "Warm Coral", "hex": "#FF7F50"},
    {"color_name": "Navy Blue", "hex": "#1B2A4A"},
    {"color_name": "Emerald Green", "hex": "#046307"},
    {"color_name": "Icy Lavender", "hex": "#C9B6E4"},
    {"color_name": "Sapphire Blue", "hex": "#0F52BA"},
    {"color_name": "Fuchsia Pink", "hex": "#C154C1"},
    {"color_name": "Slate Grey", "hex": "#708090"},
    {"color_name": "Soft White", "hex": "#F5F5F0"},
    {"color_name": "Charcoal Grey", "hex": "#36454F"},
    {"color_name": "Dusty Rose", "hex": "#C08081"},
    {"color_name": "Sage Green", "hex": "#9CAF88"},
    {"color_name": "Taupe", "hex": "#8B8589"},
    {"color_name": "Denim Blue", "hex": "#4A6D8C"},
    {"color_name": "Burgundy", "hex": "#800020"},
    {"color_name": "Forest Green", "hex": "#228B22"},
    {"color_name": "Blush Pink", "hex": "#F9C5D1"},
    {"color_name": "Cream", "hex": "#FFFDD0"},
    {"color_name": "Deep Teal", "hex": "#014D4E"},
    {"color_name": "Amber", "hex": "#FFBF00"},
]

CLEANSER_OPTIONS = {
    "oily": [
        {"step": "cleanser", "budget_product": "CeraVe Foaming Facial Cleanser", "premium_product": "SkinCeuticals Simply Clean",
         "reason": "A foaming formula helps manage excess oil without over-stripping skin."},
        {"step": "cleanser", "budget_product": "The Derma Co 1% Salicylic Acid Cleanser", "premium_product": "Minimalist 2% Salicylic Acid Cleanser",
         "reason": "Salicylic acid-based cleansers help control oil and keep pores clearer over time."},
        {"step": "cleanser", "budget_product": "Plix 2% Salicylic Acid Face Wash", "premium_product": "Re'equil Oil Free Foaming Face Wash",
         "reason": "A lightweight oil-control cleanser suited to oilier skin types."},
    ],
    "dry": [
        {"step": "cleanser", "budget_product": "CeraVe Hydrating Facial Cleanser", "premium_product": "SkinCeuticals Gentle Cleanser",
         "reason": "A gentle, non-foaming cleanser avoids stripping moisture from already-dry skin."},
        {"step": "cleanser", "budget_product": "Minimalist 3% Ceramide Cleanser", "premium_product": "Dot & Key Watermelon Hydrating Cleanser",
         "reason": "Ceramide and hydration-focused cleansers help support the skin barrier on drier skin."},
        {"step": "cleanser", "budget_product": "The Derma Co Rice Cleanser", "premium_product": "Pilgrim Ceramide Barrier Repair Cleanser",
         "reason": "A hydrating cleanser formulated to avoid worsening dryness."},
    ],
    "normal": [
        {"step": "cleanser", "budget_product": "Plix The Vitamin C Foaming Face Wash", "premium_product": "SkinCeuticals Gentle Cleanser",
         "reason": "A balanced, gentle cleanser works well as a daily baseline for normal skin."},
        {"step": "cleanser", "budget_product": "Pilgrim Korean Ginseng & Amino Acid Cleanser", "premium_product": "Dot & Key Vitamin C Gentle Cleanser",
         "reason": "A mild daily cleanser that supports skin without disrupting its natural balance."},
        {"step": "cleanser", "budget_product": "Minimalist Sepicalm Micellar Gel Cleanser", "premium_product": "Re'equil Gentle Cleanser",
         "reason": "A mild, everyday cleanser well suited to balanced skin."},
    ],
}

SUNSCREEN_OPTIONS = {
    "light": [
        {"step": "sunscreen (AM)", "budget_product": "La Roche-Posay Anthelios Melt-in Milk SPF 60", "premium_product": "SkinCeuticals Physical Fusion UV Defense SPF 50",
         "reason": "A daily broad-spectrum SPF suited to lighter skin tones."},
        {"step": "sunscreen (AM)", "budget_product": "Minimalist SPF 50 PA++++ Sunscreen", "premium_product": "Re'equil Oil Free Matte Look Sunscreen SPF 50",
         "reason": "A lightweight daily SPF that layers well under makeup."},
        {"step": "sunscreen (AM)", "budget_product": "Dot & Key Vitamin C SPF 40 Sunscreen", "premium_product": "The Derma Co 1% Hyaluronic Sunscreen SPF 50",
         "reason": "A hydrating daily SPF suited to lighter skin tones."},
    ],
    "medium": [
        {"step": "sunscreen (AM)", "budget_product": "Re'equil Ultra Matte Look Sunscreen SPF 50", "premium_product": "SkinCeuticals Physical Fusion UV Defense SPF 50",
         "reason": "A matte-finish SPF formulated to sit well on medium skin tones without residue."},
        {"step": "sunscreen (AM)", "budget_product": "The Derma Co 1% Hyaluronic Sunscreen SPF 50", "premium_product": "Dot & Key Vitamin C SPF 40 Sunscreen",
         "reason": "A daily SPF with added hydration, suited to medium skin tones."},
        {"step": "sunscreen (AM)", "budget_product": "Minimalist SPF 50 PA++++ Sunscreen", "premium_product": "Pilgrim Retinol + SPF 30 Sunscreen",
         "reason": "A daily broad-spectrum SPF option for medium skin tones."},
    ],
    "deep": [
        {"step": "sunscreen (AM)", "budget_product": "Re'equil Oil Free Matte Look Sunscreen SPF 50", "premium_product": "Dot & Key Vitamin C SPF 40 Sunscreen",
         "reason": "A no-white-cast formula that blends well into deeper skin tones."},
        {"step": "sunscreen (AM)", "budget_product": "Minimalist SPF 50 PA++++ Sunscreen", "premium_product": "Pilgrim Retinol + SPF 30 Sunscreen",
         "reason": "A daily SPF chosen for a residue-free finish on deeper skin tones."},
        {"step": "sunscreen (AM)", "budget_product": "The Derma Co 1% Hyaluronic Sunscreen SPF 50", "premium_product": "SkinCeuticals Physical Fusion UV Defense SPF 50",
         "reason": "A hydrating, residue-free SPF suited to deeper skin tones."},
    ],
}

SKINCARE_BY_FLAG = {
    "dryness": [
        {"step": "moisturizer", "budget_product": "CeraVe Moisturizing Cream", "premium_product": "La Mer Moisturizing Cream",
         "reason": "Ceramide and hyaluronic acid formulas help restore the moisture barrier."},
        {"step": "moisturizer", "budget_product": "Minimalist 3% Ceramide Moisturizer", "premium_product": "Dot & Key Watermelon Hydrating Gel Cream",
         "reason": "A ceramide-rich moisturizer helps rebuild the skin barrier on drier skin."},
        {"step": "moisturizer", "budget_product": "The Derma Co Ceramide Barrier Repair Moisturizer", "premium_product": "Pilgrim Ceramide Barrier Repair Moisturizer",
         "reason": "A barrier-repair-focused moisturizer for skin prone to dryness."},
    ],
    "oiliness": [
        {"step": "moisturizer", "budget_product": "Minimalist 2% Niacinamide Oil-Free Moisturizer", "premium_product": "SkinCeuticals Oil Control Gel",
         "reason": "A lightweight, oil-free gel moisturizer hydrates without adding excess shine."},
        {"step": "moisturizer", "budget_product": "Re'equil Oil Free Moisturizer", "premium_product": "Dot & Key 2% Niacinamide Oil Control Gel",
         "reason": "An oil-free formula helps balance shine while still keeping skin hydrated."},
        {"step": "moisturizer", "budget_product": "The Derma Co Oil Free Moisturizer", "premium_product": "Plix 1% Niacinamide Oil Control Gel",
         "reason": "A gel-based, oil-free moisturizer suited to oilier skin types."},
    ],
    "uneven_tone": [
        {"step": "serum", "budget_product": "The Ordinary Niacinamide 10% + Zinc 1%", "premium_product": "SkinCeuticals Discoloration Defense",
         "reason": "Niacinamide is well-supported for improving tone evenness over time."},
        {"step": "serum", "budget_product": "Minimalist 10% Niacinamide Face Serum", "premium_product": "Dot & Key 10% Niacinamide Serum",
         "reason": "A niacinamide serum can help even out visible tone irregularities gradually."},
        {"step": "serum", "budget_product": "The Derma Co 10% Niacinamide Serum", "premium_product": "Pilgrim 10% Niacinamide Face Serum",
         "reason": "A niacinamide-based serum aimed at improving overall tone consistency."},
    ],
    "redness": [
        {"step": "serum", "budget_product": "The Ordinary Azelaic Acid Suspension 10%", "premium_product": "Dr. Jart+ Cicapair Tiger Grass Serum",
         "reason": "Azelaic acid and centella-based formulas are commonly used to calm visible redness."},
        {"step": "serum", "budget_product": "Re'equil Redness Rescue Serum", "premium_product": "Dot & Key Centella Redness Rescue Serum",
         "reason": "Centella-based formulas are frequently used to soothe visible redness and sensitivity."},
        {"step": "serum", "budget_product": "Minimalist 1% Alpha Bisabolol Redness Corrector", "premium_product": "Pilgrim Centella Redness Relief Serum",
         "reason": "A calming, redness-targeted serum for sensitive-leaning skin."},
    ],
    "visible_texture": [
        {"step": "exfoliant", "budget_product": "The Ordinary Salicylic Acid 2% Solution", "premium_product": "Paula's Choice Skin Perfecting 2% BHA Liquid",
         "reason": "BHA exfoliants help address visible texture and clogged pores."},
        {"step": "exfoliant", "budget_product": "Minimalist 2% Salicylic Acid Serum", "premium_product": "The Derma Co 2% Salicylic Acid Serum",
         "reason": "A salicylic acid exfoliant can help smooth visible texture with regular use."},
        {"step": "exfoliant", "budget_product": "Plix 2% Salicylic Acid Serum", "premium_product": "Re'equil 2% Salicylic Acid Serum",
         "reason": "A gentle chemical exfoliant aimed at reducing visible texture over time."},
    ],
    "breakout_like_spots": [
        {"step": "spot treatment", "budget_product": "La Roche-Posay Effaclar Duo", "premium_product": "SkinCeuticals Blemish + Age Defense",
         "reason": "Benzoyl peroxide and salicylic acid-based formulas are commonly used to target breakout-prone areas."},
        {"step": "spot treatment", "budget_product": "The Derma Co 10% Niacinamide + Salicylic Spot Gel", "premium_product": "Minimalist 10% Salicylic Acid Spot Treatment",
         "reason": "A targeted spot treatment can help calm and reduce breakout-prone areas."},
        {"step": "spot treatment", "budget_product": "Pilgrim Tea Tree Blemish Gel", "premium_product": "Dot & Key Salicylic Acid Spot Corrector",
         "reason": "A tea-tree or salicylic-based spot gel for targeting individual breakout-prone spots."},
    ],
    "dark_spot_like_areas": [
        {"step": "serum", "budget_product": "The Ordinary Alpha Arbutin 2% + HA", "premium_product": "SkinCeuticals Discoloration Defense",
         "reason": "Alpha arbutin and similar brightening ingredients are commonly used to help even out dark spot-prone areas."},
        {"step": "serum", "budget_product": "Minimalist 2% Alpha Arbutin Face Serum", "premium_product": "Dot & Key Vitamin C Dark Spot Serum",
         "reason": "A brightening serum can help gradually fade dark spot-prone areas with consistent use."},
        {"step": "serum", "budget_product": "The Derma Co 2% Alpha Arbutin Face Serum", "premium_product": "Pilgrim Vitamin C Dark Spot Serum",
         "reason": "A brightening, dark-spot-targeted serum for gradual, consistent use."},
    ],
}

# Distinct descriptive character for each color, used to make recommendation
# text feel genuinely unique per color rather than a template with swapped words.
COLOR_DESCRIPTORS = {
    "Olive Green": "an earthy, grounded shade with a muted green depth",
    "Terracotta": "a sun-baked orange with warm, clay-like richness",
    "Mustard Yellow": "a bold golden shade with vintage warmth",
    "Rust Orange": "a deep burnt orange with autumnal intensity",
    "Camel Brown": "a soft, sandy brown with understated warmth",
    "Warm Coral": "a lively pink-orange with sun-kissed energy",
    "Navy Blue": "a deep, classic blue with quiet confidence",
    "Emerald Green": "a rich jewel-toned green with striking depth",
    "Icy Lavender": "a pale, cool purple with delicate softness",
    "Sapphire Blue": "a vivid, saturated blue with gemstone brilliance",
    "Fuchsia Pink": "a bold, electric pink that commands attention",
    "Slate Grey": "a cool-toned grey with industrial calm",
    "Soft White": "a clean, crisp white with minimalist ease",
    "Charcoal Grey": "a deep, smoky grey with understated sharpness",
    "Dusty Rose": "a muted pink with soft, faded warmth",
    "Sage Green": "a quiet, herbal green with calming presence",
    "Taupe": "a warm-grey neutral with quiet versatility",
    "Denim Blue": "a washed, casual blue with relaxed familiarity",
    "Burgundy": "a deep wine red with dramatic richness",
    "Forest Green": "a dense, woodland green with natural depth",
    "Blush Pink": "a soft, powdery pink with gentle warmth",
    "Cream": "a warm off-white with subtle golden undertones",
    "Deep Teal": "a dark blue-green with moody sophistication",
    "Amber": "a glowing golden-orange with warm luminosity",
}