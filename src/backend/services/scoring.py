import re
from datetime import datetime


def normalize_text(value):
    """
    Normalize text for deterministic comparisons.
    """
    if value is None:
        return ""

    value = str(value).lower()

    replacements = {
        "-": " ",
        "_": " ",
    }

    for old, new in replacements.items():
        value = value.replace(old, new)

    value = re.sub(r"[^\w\s]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()

    return value


def text_tokens(value):
    return set(normalize_text(value).split())


def same_text(observed, expected):
    """
    Returns True when two descriptions are equivalent or
    one is a subset of the other.
    """
    if not observed or not expected:
        return False

    observed_normalized = normalize_text(observed)
    expected_normalized = normalize_text(expected)

    if observed_normalized == expected_normalized:
        return True

    observed_tokens = text_tokens(observed)
    expected_tokens = text_tokens(expected)

    if observed_tokens and observed_tokens.issubset(expected_tokens):
        return True

    if expected_tokens and expected_tokens.issubset(observed_tokens):
        return True

    return False


def compatible_clothing(observed, expected):
    """
    Determines whether an observed clothing description
    is compatible with the missing person's profile.

    This is deterministic and does not infer identity.
    """
    if not observed or not expected:
        return False

    if same_text(observed, expected):
        return True

    footwear_groups = [
        {"shoe", "shoes", "sneaker", "sneakers"},
        {"trainer", "trainers"},
    ]

    observed_tokens = text_tokens(observed)
    expected_tokens = text_tokens(expected)

    for group in footwear_groups:
        if (
            observed_tokens.intersection(group)
            and expected_tokens.intersection(group)
        ):
            observed_without_type = observed_tokens - group
            expected_without_type = expected_tokens - group

            if observed_without_type == expected_without_type:
                return True

    # "black backpack" is compatible with "black backpack with grey stripe"
    if "backpack" in observed_tokens and "backpack" in expected_tokens:
        return True

    # Generic dark clothing is NOT treated as a positive match.
    # It will be handled as uncertainty in score_evidence().
    return False


def clothing_conflict(observed, expected, field):
    """
    Determines whether a clothing observation is an actual
    contradiction rather than merely incomplete/general information.
    """
    if not observed or not expected:
        return False

    if compatible_clothing(observed, expected):
        return False

    observed_normalized = normalize_text(observed)
    expected_normalized = normalize_text(expected)

    generic_descriptions = {
        "dark clothing",
        "dark clothes",
        "casual clothing",
        "casual clothes",
        "clothing",
        "unknown",
    }

    if observed_normalized in generic_descriptions:
        return False

    if expected_normalized in generic_descriptions:
        return False

    return True


def score_evidence(profile, evidence):
    """
    Score one evidence record against the missing-person profile.

    Maximum score = 100

    Name       = 30
    Location   = 25
    Time       = 20
    Clothing   = 15
    Physical   = 10

    The result is an investigative priority score only.
    It is NOT an identity confidence or probability.
    """

    score_breakdown = {
        "name": 0,
        "location": 0,
        "time": 0,
        "clothing": 0,
        "physical": 0,
    }

    matching_evidence = []
    conflicting_evidence = []
    uncertainty_factors = []

    last_seen = datetime.fromisoformat(
        profile["lastSeen"]["dateTime"]
    )

    observed_time = datetime.fromisoformat(
        evidence["dateTime"]
    )

    # =========================================================
    # NAME — 30 points
    # =========================================================

    observed_name = evidence.get("observedName")

    if observed_name:
        normalized_observed = normalize_text(observed_name)
        normalized_name = normalize_text(profile["name"])

        aliases = [
            normalize_text(alias)
            for alias in profile.get("aliases", [])
        ]

        if (
            normalized_observed == normalized_name
            or normalized_observed in aliases
        ):
            score_breakdown["name"] = 30

            matching_evidence.append(
                f"Observed name '{observed_name}' matches "
                "the case name or alias."
            )

        else:
            conflicting_evidence.append(
                f"Observed name '{observed_name}' does not match "
                "the case name or aliases."
            )

    else:
        uncertainty_factors.append(
            "No observed name was provided."
        )

    # =========================================================
    # LOCATION — 25 points
    # =========================================================

    observed_location = normalize_text(
        evidence.get("location")
    )

    last_location = normalize_text(
        profile["lastSeen"]["location"]
    )

    if observed_location and observed_location == last_location:

        score_breakdown["location"] = 25

        matching_evidence.append(
            "Observed location matches the last known location."
        )

    elif observed_location:

        riverfront_locations = [
            "riverfront pedestrian bridge",
            "east river road",
            "riverfront parking",
        ]

        if any(
            location in observed_location
            for location in riverfront_locations
        ):
            score_breakdown["location"] = 20

            matching_evidence.append(
                "Observed location is within the Riverfront area."
            )

        elif "central bus stop" in observed_location:

            score_breakdown["location"] = 10

            matching_evidence.append(
                "Observed location is a nearby public transit location."
            )

        else:

            uncertainty_factors.append(
                "Observed location is not a known relevant location."
            )

    else:

        uncertainty_factors.append(
            "No location was provided."
        )

    # =========================================================
    # TIME — 20 points
    # =========================================================

    if observed_time >= last_seen:

        difference_minutes = (
            observed_time - last_seen
        ).total_seconds() / 60

        if difference_minutes <= 30:

            score_breakdown["time"] = 20

        elif difference_minutes <= 60:

            score_breakdown["time"] = 15

        elif difference_minutes <= 120:

            score_breakdown["time"] = 10

        elif difference_minutes <= 240:

            score_breakdown["time"] = 5

        else:

            score_breakdown["time"] = 0

        if score_breakdown["time"] > 0:

            matching_evidence.append(
                f"Observation occurred "
                f"{int(difference_minutes)} minutes after "
                "the last known sighting."
            )

        else:

            uncertainty_factors.append(
                "Observation occurred more than four hours "
                "after the last known sighting."
            )

    else:

        uncertainty_factors.append(
            "Observation occurred before the recorded "
            "last-seen time."
        )

    # =========================================================
    # CLOTHING — 15 points
    #
    # Top       = 5
    # Bottom    = 4
    # Footwear  = 3
    # Backpack  = 3
    #
    # Generic descriptions such as "dark clothing"
    # receive 0 points and are treated as uncertainty.
    # =========================================================

    profile_clothing = profile.get(
        "clothing",
        {}
    )

    evidence_clothing = evidence.get(
        "clothing",
        {}
    )

    clothing_fields = [
        ("top", 5, "top"),
        ("bottom", 4, "bottom"),
        ("footwear", 3, "footwear"),
        ("backpack", 3, "backpack"),
    ]

    generic_clothing_descriptions = {
        "dark clothing",
        "dark clothes",
        "casual clothing",
        "casual clothes",
        "clothing",
        "unknown",
    }

    for evidence_field, points, profile_field in clothing_fields:

        observed = evidence_clothing.get(
            evidence_field
        )

        expected = profile_clothing.get(
            profile_field
        )

        # No observation = no score.
        if not observed:
            continue

        observed_normalized = normalize_text(
            observed
        )

        # -----------------------------------------------------
        # Generic clothing description
        # -----------------------------------------------------

        if observed_normalized in generic_clothing_descriptions:

            uncertainty_factors.append(
                f"Clothing description '{observed}' "
                f"is too general to receive matching points "
                f"for {evidence_field}."
            )

            continue

        # -----------------------------------------------------
        # Positive clothing match
        # -----------------------------------------------------

        if compatible_clothing(
            observed,
            expected
        ):

            score_breakdown["clothing"] += points

            matching_evidence.append(
                f"Clothing match: "
                f"{evidence_field} = {observed}."
            )

        # -----------------------------------------------------
        # Actual clothing conflict
        # -----------------------------------------------------

        elif clothing_conflict(
            observed,
            expected,
            evidence_field
        ):

            conflicting_evidence.append(
                f"Clothing mismatch: observed "
                f"{evidence_field} = {observed}, "
                f"expected {profile_field} = {expected}."
            )

        # -----------------------------------------------------
        # Insufficient information
        # -----------------------------------------------------

        else:

            uncertainty_factors.append(
                f"Clothing description is insufficiently "
                f"specific for {evidence_field}."
            )

    # =========================================================
    # PHYSICAL — 10 points
    #
    # Hair  = 3
    # Build = 3
    # Height = 2
    # Eyes = 2
    #
    # Identifying mark is evidence only and is not scored.
    # =========================================================

    profile_physical = profile.get(
        "physicalDescription",
        {}
    )

    evidence_physical = evidence.get(
        "physical",
        {}
    )

    # ---------------------------------------------------------
    # Hair — 3
    # ---------------------------------------------------------

    observed_hair = evidence_physical.get(
        "hair"
    )

    expected_hair = profile_physical.get(
        "hairColor"
    )

    if observed_hair:

        if same_text(
            observed_hair,
            expected_hair
        ):

            score_breakdown["physical"] += 3

            matching_evidence.append(
                f"Physical match: hair = {observed_hair}."
            )

        else:

            conflicting_evidence.append(
                f"Physical mismatch: observed hair = "
                f"{observed_hair}, expected hair = "
                f"{expected_hair}."
            )

    else:

        uncertainty_factors.append(
            "No hair color observation was provided."
        )

    # ---------------------------------------------------------
    # Build — 3
    # ---------------------------------------------------------

    observed_build = evidence_physical.get(
        "build"
    )

    expected_build = profile_physical.get(
        "build"
    )

    if observed_build:

        if same_text(
            observed_build,
            expected_build
        ):

            score_breakdown["physical"] += 3

            matching_evidence.append(
                f"Physical match: build = {observed_build}."
            )

        else:

            conflicting_evidence.append(
                f"Physical mismatch: observed build = "
                f"{observed_build}, expected build = "
                f"{expected_build}."
            )

    else:

        uncertainty_factors.append(
            "No build observation was provided."
        )

    # ---------------------------------------------------------
    # Height — 2
    # ---------------------------------------------------------

    observed_height = evidence_physical.get(
        "heightCm"
    )

    expected_height = profile_physical.get(
        "heightCm"
    )

    if observed_height is not None:

        try:

            observed_height = float(
                observed_height
            )

            expected_height = float(
                expected_height
            )

            height_difference = abs(
                observed_height - expected_height
            )

            if height_difference <= 5:

                score_breakdown["physical"] += 2

                matching_evidence.append(
                    f"Physical match: observed height "
                    f"{int(observed_height)} cm is within "
                    "5 cm of the profile height."
                )

            else:

                conflicting_evidence.append(
                    f"Physical mismatch: observed height "
                    f"{int(observed_height)} cm differs from "
                    f"profile height {int(expected_height)} cm."
                )

        except (
            TypeError,
            ValueError
        ):

            uncertainty_factors.append(
                "Height observation could not be evaluated."
            )

    else:

        uncertainty_factors.append(
            "No height observation was provided."
        )

    # ---------------------------------------------------------
    # Eyes — 2
    # ---------------------------------------------------------

    observed_eyes = evidence_physical.get(
        "eyes"
    )

    expected_eyes = profile_physical.get(
        "eyeColor"
    )

    if observed_eyes:

        if same_text(
            observed_eyes,
            expected_eyes
        ):

            score_breakdown["physical"] += 2

            matching_evidence.append(
                f"Physical match: eyes = {observed_eyes}."
            )

        else:

            conflicting_evidence.append(
                f"Physical mismatch: observed eyes = "
                f"{observed_eyes}, expected eyes = "
                f"{expected_eyes}."
            )

    else:

        uncertainty_factors.append(
            "No eye color observation was provided."
        )

    # =========================================================
    # IDENTIFYING MARK
    #
    # The identifying mark is not scored.
    # It can still contribute to matching/conflicting evidence.
    # =========================================================

    observed_mark = evidence_physical.get(
        "identifyingMark"
    )

    expected_marks = profile_physical.get(
        "identifyingMarks",
        []
    )

    if observed_mark:

        normalized_observed_mark = normalize_text(
            observed_mark
        )

        mark_match = False

        for expected_mark in expected_marks:

            if same_text(
                observed_mark,
                expected_mark
            ):

                mark_match = True

                matching_evidence.append(
                    f"Identifying mark observation matches "
                    f"profile information: {observed_mark}."
                )

                break

        if not mark_match:

            conflicting_evidence.append(
                f"Observed identifying mark '{observed_mark}' "
                "does not match the recorded identifying marks."
            )

    else:

        uncertainty_factors.append(
            "No identifying mark was observed."
        )

    # =========================================================
    # FINAL SCORE
    # =========================================================

    total_score = sum(
        score_breakdown.values()
    )

    return {
        "score": total_score,
        "scoreBreakdown": {
            "name": score_breakdown["name"],
            "location": score_breakdown["location"],
            "time": score_breakdown["time"],
            "clothing": score_breakdown["clothing"],
            "physical": score_breakdown["physical"],
        },
        "matchingEvidence": matching_evidence,
        "conflictingEvidence": conflicting_evidence,
        "uncertaintyFactors": uncertainty_factors,
    }


if __name__ == "__main__":
    print(
        "scoring.py loaded successfully."
    )