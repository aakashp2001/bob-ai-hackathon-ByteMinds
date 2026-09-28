import json
from datetime import datetime
from pathlib import Path

from src.backend.services.scoring import score_evidence


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"


def load_json(filename):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as file:
        return json.load(file)


def load_data():
    profile = load_json("person_profile.json")
    tips = load_json("tips.json")
    cctv = load_json("cctv.json")

    return profile, tips, cctv


def parse_datetime(value):
    return datetime.fromisoformat(value)


def get_record_id(record):
    if "tipId" in record:
        return record["tipId"]

    if "sightingId" in record:
        return record["sightingId"]

    if "cctvId" in record:
        return record["cctvId"]

    return "UNKNOWN"


def get_record_type(record):
    if "tipId" in record:
        return "tip"

    if "sightingId" in record:
        return "cctv"

    if "cctvId" in record:
        return "cctv"

    return "unknown"


def get_record_location(record):
    return record.get(
        "location",
        record.get("cameraLocation", "")
    )


def get_zone(location):
    """
    Normalize locations into broad geographic zones.
    """

    location = location.lower()

    if "riverfront pedestrian bridge" in location:
        return "riverfront"

    if "east river road" in location:
        return "riverfront"

    if "riverfront parking" in location:
        return "riverfront"

    if "central bus stop" in location:
        return "bus_stop"

    if "railway station" in location:
        return "railway_station"

    if "shopping complex" in location:
        return "shopping_complex"

    if "residential area" in location:
        return "residential"

    if "tea stall" in location:
        return "tea_stall"

    return None


def records_are_related(record_a, record_b):
    """
    Two records are considered related when:
    - they occur within 15 minutes
    - they belong to the same geographic zone
    """

    time_a = parse_datetime(record_a["dateTime"])
    time_b = parse_datetime(record_b["dateTime"])

    difference_minutes = abs(
        (time_a - time_b).total_seconds()
    ) / 60

    if difference_minutes > 15:
        return False

    location_a = get_zone(
        get_record_location(record_a)
    )

    location_b = get_zone(
        get_record_location(record_b)
    )

    if location_a is None or location_b is None:
        return False

    return location_a == location_b


def build_groups(records):
    """
    Build connected groups of related records.

    Each group represents a potential investigative event.
    """

    groups = []
    visited = set()

    for record in records:

        record_id = get_record_id(record)

        if record_id in visited:
            continue

        group = []
        queue = [record]

        while queue:

            current = queue.pop()
            current_id = get_record_id(current)

            if current_id in visited:
                continue

            visited.add(current_id)
            group.append(current)

            for candidate in records:

                candidate_id = get_record_id(candidate)

                if candidate_id in visited:
                    continue

                if records_are_related(
                    current,
                    candidate
                ):
                    queue.append(candidate)

        groups.append(group)

    return groups


def get_title(group):
    """
    Generate a deterministic lead title.
    """

    zones = [
        get_zone(
            get_record_location(record)
        )
        for record in group
    ]

    if "riverfront" in zones:
        return "Riverfront Potential Sighting"

    if "bus_stop" in zones:
        return "Central Bus Stop Potential Sighting"

    if "railway_station" in zones:
        return "Railway Station Potential Sighting"

    if "shopping_complex" in zones:
        return "Shopping Complex Potential Sighting"

    if "tea_stall" in zones:
        return "Tea Stall Potential Sighting"

    if "residential" in zones:
        return "Residential Area Potential Sighting"

    return "Potential Sighting"


def get_priority(score):
    """
    Deterministic investigative priority.

    This is NOT identity confidence.
    """

    if score >= 70:
        return "high"

    if score >= 40:
        return "medium"

    return "low"


def get_uncertainty(
    group,
    score,
    conflicting_evidence
):
    """
    Deterministic uncertainty classification.

    High:
        Explicit conflicting evidence.

    Low:
        High score + multiple corroborating records
        + no conflicts.

    Medium:
        Everything else.
    """

    if conflicting_evidence:
        return "high"

    if score >= 70 and len(group) >= 2:
        return "low"

    return "medium"


def get_next_action(
    group,
    conflicting_evidence
):
    """
    Generate one deterministic next action.
    """

    record_ids = [
        get_record_id(record)
        for record in group
    ]

    tip_ids = [
        get_record_id(record)
        for record in group
        if get_record_type(record) == "tip"
    ]

    cctv_ids = [
        get_record_id(record)
        for record in group
        if get_record_type(record) == "cctv"
    ]

    if conflicting_evidence:

        return (
            "Verify the conflicting evidence in source records "
            f"{', '.join(record_ids)} against the original source "
            "or independent evidence."
        )

    if tip_ids and cctv_ids:

        return (
            f"Verify tip record {tip_ids[0]} against CCTV record "
            f"{cctv_ids[0]} and review the full available footage."
        )

    if len(cctv_ids) >= 2:

        return (
            "Review the full available CCTV footage to establish "
            "the movement sequence between cameras."
        )

    if cctv_ids:

        return (
            f"Review the full available footage for CCTV record "
            f"{cctv_ids[0]}."
        )

    if tip_ids:

        return (
            f"Verify tip record {tip_ids[0]} with an independent "
            "source or nearby CCTV."
        )

    return "Verify the source information independently."


def build_lead(
    group,
    profile,
    lead_id
):
    """
    Build one structured investigative lead.
    """

    scored_records = []

    for record in group:

        result = score_evidence(
            profile,
            record
        )

        scored_records.append(result)

    # The highest individual score represents
    # the deterministic score of the lead.
    best_result = max(
        scored_records,
        key=lambda result: result["score"]
    )

    score = best_result["score"]

    score_breakdown = best_result[
        "scoreBreakdown"
    ]

    matching_evidence = []
    conflicting_evidence = []
    uncertainty_factors = []

    # Combine evidence from every record in the group.
    for result in scored_records:

        for evidence in result.get(
            "matchingEvidence",
            []
        ):

            if evidence not in matching_evidence:
                matching_evidence.append(evidence)

        for evidence in result.get(
            "conflictingEvidence",
            []
        ):

            if evidence not in conflicting_evidence:
                conflicting_evidence.append(evidence)

        for factor in result.get(
            "uncertaintyFactors",
            []
        ):

            if factor not in uncertainty_factors:
                uncertainty_factors.append(factor)

    corroborating_record_count = len(group)

    uncertainty = get_uncertainty(
        group,
        score,
        conflicting_evidence
    )

    priority = get_priority(score)

    return {
        "leadId": lead_id,
        "rank": 0,
        "title": get_title(group),

        "sourceRecordIds": [
            get_record_id(record)
            for record in group
        ],

        "score": score,

        "scoreBreakdown": {
            "name": score_breakdown.get(
                "name",
                0
            ),
            "location": score_breakdown.get(
                "location",
                0
            ),
            "time": score_breakdown.get(
                "time",
                0
            ),
            "clothing": score_breakdown.get(
                "clothing",
                0
            ),
            "physical": score_breakdown.get(
                "physical",
                0
            )
        },

        "priority": priority,

        "matchingEvidence": matching_evidence,

        "conflictingEvidence": conflicting_evidence,

        "uncertainty": uncertainty,

        "uncertaintyFactors": uncertainty_factors,

        "recommendedNextAction": get_next_action(
            group,
            conflicting_evidence
        ),

        "corroboratingRecordCount": corroborating_record_count
    }


def run_correlation():
    """
    Main deterministic correlation pipeline.
    """

    profile, tips, cctv = load_data()

    # Combine all source records.
    records = tips + cctv

    # Group related records.
    groups = build_groups(records)

    leads = []

    for index, group in enumerate(
        groups,
        start=1
    ):

        lead = build_lead(
            group,
            profile,
            f"L{index:03d}"
        )

        leads.append(lead)

    # Deterministic ranking:
    #
    # 1. Higher score
    # 2. More corroborating records
    # 3. Stable source ID as tie-breaker
    leads.sort(
        key=lambda lead: (
            -lead["score"],
            -lead["corroboratingRecordCount"],
            lead["sourceRecordIds"][0]
        )
    )

    # Assign final ranks after sorting.
    for rank, lead in enumerate(
        leads,
        start=1
    ):

        lead["rank"] = rank

    return {
        "caseNumber": profile["caseNumber"],

        "status": "completed",

        "scoringModel": {
            "maxScore": 100,

            "interpretation": (
                "Investigative priority score only; "
                "not identity confidence or probability."
            ),

            "criteria": {
                "name": 30,
                "location": 25,
                "time": 20,
                "clothing": 15,
                "physical": 10
            },

            "priorityThresholds": {
                "high": "70-100",
                "medium": "40-69",
                "low": "0-39"
            }
        },

        "leads": leads
    }


if __name__ == "__main__":

    result = run_correlation()

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )