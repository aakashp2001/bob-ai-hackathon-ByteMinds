import json
from datetime import datetime

from src.backend.services.scoring import calculate_score


# =========================================================
# DATA LOADING
# =========================================================

def load_json(path):
    """
    Loads a JSON file.
    """

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_case_data():
    """
    Loads the complete fictional case.
    """

    profile = load_json(
        "src/data/person_profile.json"
    )

    tips = load_json(
        "src/data/tips.json"
    )

    cctv = load_json(
        "src/data/cctv.json"
    )

    return profile, tips, cctv


# =========================================================
# TIME HELPERS
# =========================================================

def parse_datetime(value):
    """
    Converts ISO datetime text into a datetime object.
    """

    try:
        return datetime.fromisoformat(value)

    except (ValueError, TypeError):
        return None


def time_difference_minutes(time_a, time_b):
    """
    Returns the absolute difference between two timestamps.
    """

    dt_a = parse_datetime(time_a)
    dt_b = parse_datetime(time_b)

    if not dt_a or not dt_b:
        return None

    return abs(
        (dt_a - dt_b).total_seconds()
    ) / 60


# =========================================================
# LOCATION NORMALIZATION
# =========================================================

def normalize_location(location):
    """
    Converts different descriptions of nearby places
    into broader location zones.

    This is intentionally deterministic.
    """

    if not location:
        return ""

    location = location.lower()

    if (
        "riverfront" in location
        or "pedestrian bridge" in location
        or "east river" in location
    ):
        return "riverfront"

    if (
        "bus stop" in location
    ):
        return "bus_stop"

    if (
        "railway" in location
        or "station" in location
    ):
        return "railway_station"

    if (
        "shopping complex" in location
    ):
        return "shopping_complex"

    if (
        "residential" in location
        or "tea stall" in location
    ):
        return "residential"

    return location


# =========================================================
# LOCATION RELATIONSHIP
# =========================================================

def locations_are_related(location_a, location_b):
    """
    Determines whether two locations belong to the
    same broad geographic zone.
    """

    zone_a = normalize_location(location_a)
    zone_b = normalize_location(location_b)

    if not zone_a or not zone_b:
        return False

    return zone_a == zone_b


# =========================================================
# EVIDENCE CONVERSION
# =========================================================

def extract_tip_location(tip):
    """
    Tips do not currently contain a dedicated location field.

    We infer a supported location from the description.
    """

    description = tip["description"].lower()

    known_locations = [
        "riverfront park",
        "pedestrian bridge",
        "city bus stop",
        "railway station",
        "tea stall",
        "shopping complex",
        "residential area"
    ]

    for location in known_locations:

        if location in description:

            # Convert description phrases into
            # standardized locations.

            if location == "pedestrian bridge":
                return "Riverfront Pedestrian Bridge"

            if location == "city bus stop":
                return "Central Bus Stop"

            if location == "railway station":
                return "Railway Station"

            return location.title()

    return ""


def tip_to_evidence(tip):
    """
    Converts an investigator tip into common evidence format.
    """

    return {
        "id": tip["tipId"],
        "type": "tip",
        "datetime": tip["dateTime"],
        "location": extract_tip_location(tip),
        "description": tip["description"]
    }


def cctv_to_evidence(sighting):
    """
    Converts a CCTV sighting into common evidence format.
    """

    return {
        "id": sighting["sightingId"],
        "type": "cctv",
        "datetime": sighting["dateTime"],
        "location": sighting["cameraLocation"],
        "description": sighting["description"]
    }


# =========================================================
# SCORE EVIDENCE
# =========================================================

def score_evidence(profile, evidence):
    """
    Runs the deterministic scoring engine against one
    evidence record.
    """

    result = calculate_score(
        profile=profile,
        evidence_text=evidence["description"],
        evidence_location=evidence["location"],
        evidence_datetime=evidence["datetime"]
    )

    return {
        "recordId": evidence["id"],
        "recordType": evidence["type"],
        "dateTime": evidence["datetime"],
        "location": evidence["location"],
        "description": evidence["description"],
        "score": result["totalScore"],
        "matchingEvidence": result["matchingEvidence"],
        "conflictingEvidence": result["conflictingEvidence"]
    }


# =========================================================
# EVIDENCE RELATIONSHIP
# =========================================================

def evidence_is_related(evidence_a, evidence_b):
    """
    Determines whether two records can belong to the same
    investigative movement chain.

    Rules:

    1. Maximum time gap = 15 minutes.
    2. Locations must belong to the same broad zone.

    OR

    3. If locations are unknown, records can still connect
       when their descriptions share strong identifying
       evidence.
    """

    time_difference = time_difference_minutes(
        evidence_a["datetime"],
        evidence_b["datetime"]
    )

    if time_difference is None:
        return False

    if time_difference > 15:
        return False

    # Strong location relationship
    if locations_are_related(
        evidence_a["location"],
        evidence_b["location"]
    ):
        return True

    # If both records have no useful location,
    # compare textual evidence.
    if (
        not evidence_a["location"]
        and not evidence_b["location"]
    ):

        text_a = evidence_a["description"].lower()
        text_b = evidence_b["description"].lower()

        shared_indicators = [
            "blue hoodie",
            "black jeans",
            "black backpack",
            "grey stripe",
            "black hair",
            "medium build",
            "white shoes",
            "aarav"
        ]

        shared_count = 0

        for indicator in shared_indicators:

            if (
                indicator in text_a
                and indicator in text_b
            ):
                shared_count += 1

        if shared_count >= 1:
            return True

    return False


# =========================================================
# MOVEMENT CHAIN GROUPING
# =========================================================

def group_evidence(evidence_list):
    """
    Builds connected evidence clusters.

    If A is related to B and B is related to C,
    A, B and C can belong to the same movement chain.

    This is a simple graph traversal rather than requiring
    every record to directly match every other record.
    """

    # Build relationship graph

    graph = {
        evidence["id"]: []
        for evidence in evidence_list
    }

    for i in range(len(evidence_list)):

        for j in range(i + 1, len(evidence_list)):

            first = evidence_list[i]
            second = evidence_list[j]

            if evidence_is_related(
                first,
                second
            ):

                graph[first["id"]].append(
                    second["id"]
                )

                graph[second["id"]].append(
                    first["id"]
                )

    evidence_by_id = {
        evidence["id"]: evidence
        for evidence in evidence_list
    }

    groups = []
    visited = set()

    # Find connected components

    for evidence in evidence_list:

        evidence_id = evidence["id"]

        if evidence_id in visited:
            continue

        group = []
        stack = [evidence_id]

        visited.add(evidence_id)

        while stack:

            current_id = stack.pop()

            group.append(
                evidence_by_id[current_id]
            )

            for neighbour in graph[current_id]:

                if neighbour not in visited:

                    visited.add(neighbour)
                    stack.append(neighbour)

        groups.append(group)

    return groups


# =========================================================
# CORROBORATION BONUS
# =========================================================

def calculate_corroboration_bonus(scored_records):
    """
    Adds a small bonus when multiple independent records
    support the same lead.

    We deliberately cap the bonus so that a large number
    of weak records cannot create an artificially huge score.
    """

    record_count = len(scored_records)

    if record_count <= 1:
        return 0

    # Maximum bonus = 20
    bonus = min(
        20,
        (record_count - 1) * 5
    )

    return bonus


# =========================================================
# CREATE INVESTIGATIVE LEAD
# =========================================================

def create_lead(group, profile):

    scored_records = []

    for evidence in group:

        scored = score_evidence(
            profile,
            evidence
        )

        scored_records.append(
            scored
        )

    # Highest individual evidence score is the
    # foundation of the lead score.

    highest_score = max(
        record["score"]
        for record in scored_records
    )

    corroboration_bonus = calculate_corroboration_bonus(
        scored_records
    )

    lead_score = min(
        100,
        highest_score + corroboration_bonus
    )

    # Collect matching/conflicting evidence

    matching_evidence = []
    conflicting_evidence = []

    for record in scored_records:

        matching_evidence.extend(
            record["matchingEvidence"]
        )

        conflicting_evidence.extend(
            record["conflictingEvidence"]
        )

    # Remove duplicates

    matching_evidence = list(
        dict.fromkeys(
            matching_evidence
        )
    )

    conflicting_evidence = list(
        dict.fromkeys(
            conflicting_evidence
        )
    )

    # Determine recommended action

    if conflicting_evidence:

        action = (
            "Review the conflicting observation, "
            "verify the source record, and seek "
            "independent corroboration before treating "
            "this lead as consistent with the known profile."
        )

    elif lead_score >= 60:

        action = (
            "Prioritize verification of this movement chain "
            "using available CCTV footage, witness follow-up, "
            "and timeline confirmation."
        )

    elif lead_score >= 30:

        action = (
            "Review the linked evidence and verify the "
            "location and timeline with additional sources."
        )

    else:

        action = (
            "Keep as a low-priority lead and seek "
            "independent corroboration before escalation."
        )

    # Sort records chronologically

    scored_records.sort(
        key=lambda record: record["dateTime"]
    )

    return {
        "score": lead_score,
        "baseScore": highest_score,
        "corroborationBonus": corroboration_bonus,
        "sourceRecordIds": [
            record["recordId"]
            for record in scored_records
        ],
        "matchingEvidence": matching_evidence,
        "conflictingEvidence": conflicting_evidence,
        "recommendedNextAction": action,
        "records": scored_records
    }


# =========================================================
# COMPLETE CORRELATION
# =========================================================

def run_correlation():

    profile, tips, cctv = load_case_data()

    evidence = []

    # Convert investigator tips

    for tip in tips:

        evidence.append(
            tip_to_evidence(tip)
        )

    # Convert CCTV sightings

    for sighting in cctv:

        evidence.append(
            cctv_to_evidence(sighting)
        )

    # Sort chronologically

    evidence.sort(
        key=lambda item: item["datetime"]
    )

    # Build movement chains

    groups = group_evidence(
        evidence
    )

    leads = []

    for index, group in enumerate(
        groups,
        start=1
    ):

        lead = create_lead(
            group,
            profile
        )

        lead["leadId"] = f"L{index:03d}"

        leads.append(
            lead
        )

    # Highest priority first

    leads.sort(
        key=lambda lead: lead["score"],
        reverse=True
    )

    # Re-number after sorting

    for index, lead in enumerate(
        leads,
        start=1
    ):

        lead["leadId"] = f"L{index:03d}"

    return {
        "caseNumber": profile["caseNumber"],
        "totalEvidenceRecords": len(evidence),
        "totalLeads": len(leads),
        "leads": leads
    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    result = run_correlation()

    print("=" * 70)
    print("CORRELATION ENGINE")
    print("=" * 70)

    print(
        f"Case: {result['caseNumber']}"
    )

    print(
        f"Evidence records: "
        f"{result['totalEvidenceRecords']}"
    )

    print(
        f"Investigative leads: "
        f"{result['totalLeads']}"
    )

    for lead in result["leads"]:

        print("\n" + "-" * 70)

        print(
            f"Lead: {lead['leadId']}"
        )

        print(
            f"Source records: "
            f"{lead['sourceRecordIds']}"
        )

        print(
            f"Base score: "
            f"{lead['baseScore']}/100"
        )

        print(
            f"Corroboration bonus: "
            f"+{lead['corroborationBonus']}"
        )

        print(
            f"Lead score: "
            f"{lead['score']}/100"
        )

        print(
            "Matching evidence:",
            lead["matchingEvidence"]
        )

        print(
            "Conflicting evidence:",
            lead["conflictingEvidence"]
        )

        print(
            "Recommended action:",
            lead["recommendedNextAction"]
        )

        print(
            "Timeline:"
        )

        for record in lead["records"]:

            print(
                f"  {record['dateTime']} | "
                f"{record['recordId']} | "
                f"{record['recordType']} | "
                f"{record['location']}"
            )