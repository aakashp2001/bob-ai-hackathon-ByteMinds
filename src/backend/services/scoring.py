import re
from datetime import datetime


# =========================================================
# 1. TEXT NORMALIZATION
# =========================================================

def normalize_text(text):
    """
    Converts text into a standard format.
    """

    if not text:
        return ""

    text = text.lower()

    # Treat hyphens as spaces
    text = text.replace("-", " ")

    # Remove punctuation
    text = re.sub(r"[^a-z0-9\s]", "", text)

    # Replace multiple spaces with one
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def text_contains(text, phrase):
    """
    Checks whether a phrase exists as complete words
    inside the normalized text.
    """

    text = normalize_text(text)
    phrase = normalize_text(phrase)

    if not text or not phrase:
        return False

    text_words = set(text.split())
    phrase_words = phrase.split()

    return all(word in text_words for word in phrase_words)


# =========================================================
# 2. NAME / ALIAS
# Maximum: 30
# =========================================================

def name_match_score(profile, evidence_text):

    text = normalize_text(evidence_text)

    name = normalize_text(profile["name"])

    if name and name in text:
        return 30

    for alias in profile.get("aliases", []):
        alias = normalize_text(alias)

        if alias and alias in text:
            return 30

    return 0


# =========================================================
# 3. LOCATION
# Maximum: 25
# =========================================================

def location_match_score(profile, evidence_location):

    if not evidence_location:
        return 0

    location = normalize_text(evidence_location)
    last_seen = normalize_text(profile["lastSeen"]["location"])

    # Exact location
    if location == last_seen:
        return 25

    # Clearly connected Riverfront locations
    riverfront_locations = [
        "riverfront pedestrian bridge",
        "east river road",
        "riverfront parking"
    ]

    if location in riverfront_locations:
        return 20

    # Broader nearby location
    nearby_locations = [
        "central bus stop"
    ]

    if location in nearby_locations:
        return 10

    return 0


# =========================================================
# 4. TIME
# Maximum: 20
# =========================================================

def time_match_score(profile, evidence_datetime):

    if not evidence_datetime:
        return 0

    try:
        last_seen = datetime.fromisoformat(
            profile["lastSeen"]["dateTime"]
        )

        evidence_time = datetime.fromisoformat(
            evidence_datetime
        )

    except (ValueError, TypeError):
        return 0

    if evidence_time < last_seen:
        return 0

    difference_minutes = (
        evidence_time - last_seen
    ).total_seconds() / 60

    if difference_minutes <= 30:
        return 20

    if difference_minutes <= 60:
        return 15

    if difference_minutes <= 120:
        return 10

    if difference_minutes <= 240:
        return 5

    return 0


# =========================================================
# 5. CLOTHING
# Maximum: 15
#
# Top    = 5
# Bottom = 4
# Shoes  = 3
# Bag    = 3
# =========================================================

def clothing_match_score(profile, evidence_text):

    text = normalize_text(evidence_text)

    clothing = profile.get("clothing", {})

    score = 0

    # -----------------------------------------------------
    # TOP
    # -----------------------------------------------------

    top = normalize_text(clothing.get("top", ""))

    if top:
        top_words = top.split()

        if all(word in text.split() for word in top_words):
            score += 5

    # -----------------------------------------------------
    # BOTTOM
    # -----------------------------------------------------

    bottom = normalize_text(clothing.get("bottom", ""))

    if bottom:
        bottom_words = bottom.split()

        if all(word in text.split() for word in bottom_words):
            score += 4

    # -----------------------------------------------------
    # SHOES
    # -----------------------------------------------------

    shoes = normalize_text(clothing.get("shoes", ""))

    if shoes:
        shoe_words = shoes.split()

        if all(word in text.split() for word in shoe_words):
            score += 3

    # -----------------------------------------------------
    # BAG
    # -----------------------------------------------------

    bag = normalize_text(clothing.get("bag", ""))

    if bag:
        bag_words = bag.split()

        if all(word in text.split() for word in bag_words):
            score += 3

    return score


# =========================================================
# 6. PHYSICAL CHARACTERISTICS
# Maximum: 10
#
# Hair  = 3
# Build = 3
# Height = 2
# Eyes = 2
# =========================================================

def physical_match_score(profile, evidence_text):

    text = normalize_text(evidence_text)

    score = 0

    physical = profile.get(
        "physicalDescription",
        {}
    )

    words = set(text.split())

    # -----------------------------------------------------
    # HAIR
    # -----------------------------------------------------

    hair = normalize_text(
        physical.get("hairColor", "")
    )

    # Require the word "hair" to be near the color
    if hair:
        hair_phrases = [
            f"{hair} hair",
            f"hair {hair}"
        ]

        if any(
            phrase in text
            for phrase in hair_phrases
        ):
            score += 3

    # -----------------------------------------------------
    # BUILD
    # -----------------------------------------------------

    build = normalize_text(
        physical.get("build", "")
    )

    if build:
        build_phrases = [
            f"{build} build",
            f"build {build}"
        ]

        if any(
            phrase in text
            for phrase in build_phrases
        ):
            score += 3

    # -----------------------------------------------------
    # HEIGHT
    # -----------------------------------------------------

    height = physical.get("heightCm")

    if height and str(height) in words:
        score += 2

    # -----------------------------------------------------
    # EYES
    # -----------------------------------------------------

    eyes = normalize_text(
        physical.get("eyeColor", "")
    )

    if eyes:
        eye_phrases = [
            f"{eyes} eyes",
            f"eyes {eyes}"
        ]

        if any(
            phrase in text
            for phrase in eye_phrases
        ):
            score += 2

    return score


# =========================================================
# 7. MATCHING EVIDENCE
# =========================================================

def find_matching_evidence(profile, evidence_text):

    text = normalize_text(evidence_text)

    matches = []

    clothing = profile.get("clothing", {})
    physical = profile.get(
        "physicalDescription",
        {}
    )

    # -----------------------------------------------------
    # NAME
    # -----------------------------------------------------

    if normalize_text(profile["name"]) in text:
        matches.append(
            f"Name: {profile['name']}"
        )

    for alias in profile.get("aliases", []):

        if normalize_text(alias) in text:
            matches.append(
                f"Alias: {alias}"
            )

    # -----------------------------------------------------
    # CLOTHING
    # -----------------------------------------------------

    clothing_fields = [
        ("top", "Top"),
        ("bottom", "Bottom"),
        ("shoes", "Shoes"),
        ("bag", "Bag")
    ]

    for field, label in clothing_fields:

        value = normalize_text(
            clothing.get(field, "")
        )

        if value:
            value_words = value.split()

            if all(
                word in text.split()
                for word in value_words
            ):
                matches.append(
                    f"{label}: {clothing[field]}"
                )

    # -----------------------------------------------------
    # HAIR
    # -----------------------------------------------------

    hair = normalize_text(
        physical.get("hairColor", "")
    )

    if hair and f"{hair} hair" in text:
        matches.append(
            f"Hair: {physical['hairColor']}"
        )

    # -----------------------------------------------------
    # BUILD
    # -----------------------------------------------------

    build = normalize_text(
        physical.get("build", "")
    )

    if build and f"{build} build" in text:
        matches.append(
            f"Build: {physical['build']}"
        )

    # -----------------------------------------------------
    # EYES
    # -----------------------------------------------------

    eyes = normalize_text(
        physical.get("eyeColor", "")
    )

    if eyes and f"{eyes} eyes" in text:
        matches.append(
            f"Eyes: {physical['eyeColor']}"
        )

    # -----------------------------------------------------
    # HEIGHT
    # -----------------------------------------------------

    height = physical.get("heightCm")

    if height and str(height) in text.split():
        matches.append(
            f"Height: {height} cm"
        )

    return matches


# =========================================================
# 8. CONFLICT DETECTION
# =========================================================

def find_conflicts(profile, evidence_text):

    text = normalize_text(evidence_text)

    conflicts = []

    clothing = profile.get("clothing", {})
    physical = profile.get(
        "physicalDescription",
        {}
    )

    expected_top = normalize_text(
        clothing.get("top", "")
    )

    expected_hair = normalize_text(
        physical.get("hairColor", "")
    )

    expected_build = normalize_text(
        physical.get("build", "")
    )

    # -----------------------------------------------------
    # TOP CONFLICT
    # -----------------------------------------------------

    if (
        "red jacket" in text
        and expected_top != "red jacket"
    ):
        conflicts.append(
            "Evidence mentions a red jacket, "
            "while the known clothing is a blue hoodie."
        )

    # -----------------------------------------------------
    # HAIR CONFLICT
    # -----------------------------------------------------

    if (
        "blonde hair" in text
        and expected_hair != "blonde"
    ):
        conflicts.append(
            "Evidence mentions blonde hair, "
            "while the known hair color is black."
        )

    # -----------------------------------------------------
    # BUILD CONFLICT
    # -----------------------------------------------------

    if (
        "slim build" in text
        and expected_build != "slim"
    ):
        conflicts.append(
            "Evidence mentions a slim build, "
            "while the known build is medium."
        )

    if (
        "heavy build" in text
        and expected_build != "heavy"
    ):
        conflicts.append(
            "Evidence mentions a heavy build, "
            "while the known build is medium."
        )

    return conflicts


# =========================================================
# 9. COMPLETE SCORE
# Maximum = 100
# =========================================================

def calculate_score(
    profile,
    evidence_text,
    evidence_location=None,
    evidence_datetime=None
):

    name_score = name_match_score(
        profile,
        evidence_text
    )

    location_score = location_match_score(
        profile,
        evidence_location
    )

    time_score = time_match_score(
        profile,
        evidence_datetime
    )

    clothing_score = clothing_match_score(
        profile,
        evidence_text
    )

    physical_score = physical_match_score(
        profile,
        evidence_text
    )

    total_score = (
        name_score
        + location_score
        + time_score
        + clothing_score
        + physical_score
    )

    return {
        "nameScore": name_score,
        "locationScore": location_score,
        "timeScore": time_score,
        "clothingScore": clothing_score,
        "physicalScore": physical_score,
        "totalScore": total_score,
        "matchingEvidence": find_matching_evidence(
            profile,
            evidence_text
        ),
        "conflictingEvidence": find_conflicts(
            profile,
            evidence_text
        )
    }


# =========================================================
# 10. TESTS
# =========================================================

if __name__ == "__main__":

    profile = {
        "name": "Aarav Shah",
        "aliases": ["Aarav"],

        "physicalDescription": {
            "heightCm": 178,
            "build": "medium",
            "hairColor": "black",
            "eyeColor": "brown",
            "identifyingMarks": [
                "small scar above right eyebrow"
            ]
        },

        "clothing": {
            "top": "blue hoodie",
            "bottom": "black jeans",
            "shoes": "white sneakers",
            "bag": "black backpack with grey stripe"
        },

        "lastSeen": {
            "dateTime": "2026-09-23T18:10:00",
            "location": "Riverfront Park, Ahmedabad"
        }
    }


    # -----------------------------------------------------
    # BASIC TESTS
    # -----------------------------------------------------

    print("=" * 60)
    print("NORMALIZATION TEST")
    print("=" * 60)

    print(
        "Blue Hoodie ->",
        normalize_text("Blue Hoodie")
    )

    print(
        "BLACK   JEANS ->",
        normalize_text("BLACK   JEANS")
    )


    # -----------------------------------------------------
    # COMPLETE EVIDENCE TESTS
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("COMPLETE EVIDENCE TESTS")
    print("=" * 60)

    evidence_examples = [

        {
            "id": "T001",
            "text": (
                "A young man wearing a blue hoodie "
                "and black jeans was seen walking "
                "toward the pedestrian bridge "
                "near Riverfront Park."
            ),
            "location": "Riverfront Pedestrian Bridge",
            "datetime": "2026-09-23T18:32:00"
        },

        {
            "id": "T003",
            "text": (
                "A person carrying a black backpack "
                "with a grey stripe passed the shop "
                "near the pedestrian bridge."
            ),
            "location": "Riverfront Pedestrian Bridge",
            "datetime": "2026-09-23T18:51:00"
        },

        {
            "id": "T004",
            "text": (
                "A person wearing a red jacket "
                "was seen near the railway station."
            ),
            "location": "Railway Station Gate 2",
            "datetime": "2026-09-23T20:20:00"
        },

        {
            "id": "T005",
            "text": (
                "A person with black hair "
                "and a medium build was seen "
                "near a tea stall."
            ),
            "location": "Tea Stall",
            "datetime": "2026-09-24T09:10:00"
        },

        {
            "id": "T007",
            "text": (
                "Someone named Aarav may have "
                "been seen near a shopping complex."
            ),
            "location": "Shopping Complex",
            "datetime": "2026-09-23T21:30:00"
        }
    ]


    for evidence in evidence_examples:

        result = calculate_score(
            profile=profile,
            evidence_text=evidence["text"],
            evidence_location=evidence["location"],
            evidence_datetime=evidence["datetime"]
        )

        print(f"\nRecord: {evidence['id']}")

        print(
            f"Name:     {result['nameScore']}/30"
        )

        print(
            f"Location: {result['locationScore']}/25"
        )

        print(
            f"Time:     {result['timeScore']}/20"
        )

        print(
            f"Clothing: {result['clothingScore']}/15"
        )

        print(
            f"Physical: {result['physicalScore']}/10"
        )

        print(
            f"TOTAL:    {result['totalScore']}/100"
        )

        print(
            "Matching:",
            result["matchingEvidence"]
        )

        print(
            "Conflicts:",
            result["conflictingEvidence"]
        )