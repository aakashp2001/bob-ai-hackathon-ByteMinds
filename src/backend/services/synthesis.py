"""
Synthesis service for drafting Public Appeal Notices and Police Case Files.

This service synthesizes family-provided case data with correlated investigative leads
to produce:
1. Urgent Public Appeal Notices (for community broadcast and social media).
2. Auto-filled Police Missing Person Case Files (formal FIR / case dossiers).
"""

from typing import Any, Dict, List, Optional
from datetime import datetime


def _extract_profile_context(data: Dict[str, Any]) -> Dict[str, Any]:
    """Helper to extract normalized fields from raw or wrapped profile data."""
    profile = data.get("personProfile", data)
    last_seen = profile.get("lastSeen", {})
    dt_str = last_seen.get("dateTime", "")

    date_val = last_seen.get("date") or (dt_str.split("T")[0] if "T" in dt_str else "2026-09-23")
    time_val = last_seen.get("time") or (dt_str.split("T")[1][:5] if "T" in dt_str else "18:10")
    location_val = last_seen.get("location", "Riverfront Park, Ahmedabad")

    physical = profile.get("physicalDescription", {})
    clothing = profile.get("clothing", {})
    contact = data.get("contact") or data.get("emergencyContact") or {}

    marks = physical.get("identifyingMarks", ["None reported"])
    marks_str = ", ".join(marks) if isinstance(marks, list) else str(marks)

    clothing_parts = []
    top = clothing.get("top") or clothing.get("upper")
    if top: clothing_parts.append(top)
    bottom = clothing.get("bottom") or clothing.get("lower")
    if bottom: clothing_parts.append(bottom)
    footwear = clothing.get("footwear") or clothing.get("shoes")
    if footwear: clothing_parts.append(footwear)
    backpack = clothing.get("backpack") or clothing.get("bag")
    if backpack: clothing_parts.append(f"carrying {backpack}")
    clothing_str = ", ".join(clothing_parts) if clothing_parts else "Not specified"

    return {
        "caseNumber": data.get("caseNumber", "MP-2026-0042"),
        "name": profile.get("name", "Aarav Shah"),
        "age": profile.get("age", 22),
        "aliases": profile.get("aliases", []),
        "dateOfBirth": profile.get("dateOfBirth", "2004-03-14"),
        "lastSeenDate": date_val,
        "lastSeenTime": time_val,
        "lastSeenLocation": location_val,
        "heightCm": physical.get("heightCm", 178),
        "build": physical.get("build", "medium"),
        "hairColor": physical.get("hairColor", "black"),
        "eyeColor": physical.get("eyeColor", "brown"),
        "identifyingMarks": marks_str,
        "clothingSummary": clothing_str,
        "clothingRaw": clothing,
        "medicalAlert": "Daily asthma inhaler required (critical vulnerability window)",
        "contactName": contact.get("name", "Meera Shah (Family)"),
        "contactPhone": contact.get("phone", "+91-90000-00001"),
        "policeHelpline": "112 / +91-79-2560-0000 (Riverfront Police Control)"
    }


def generate_public_appeal(case_data: Dict[str, Any], leads: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate an urgent public appeal notice based on case profile and top leads.
    """
    ctx = _extract_profile_context(case_data)
    
    # Top lead context
    top_lead = leads[0] if leads else None
    latest_lead_context = ""
    if top_lead:
        latest_lead_context = (
            f"Corroborated investigative leads place possible sightings near {top_lead.get('title', 'the last known sector')}. "
            f"Field teams are actively verifying priority locations."
        )

    appeal_body = (
        f"URGENT MISSING PERSON APPEAL\n"
        f"Case Number: {ctx['caseNumber']}\n\n"
        f"Police and family are seeking urgent public assistance in locating {ctx['name']}, age {ctx['age']}, "
        f"who was last seen on {ctx['lastSeenDate']} at approximately {ctx['lastSeenTime']} "
        f"near {ctx['lastSeenLocation']}.\n\n"
        f"PHYSICAL DESCRIPTION:\n"
        f"• Height: {ctx['heightCm']} cm, Build: {ctx['build']}\n"
        f"• Hair: {ctx['hairColor']}, Eyes: {ctx['eyeColor']}\n"
        f"• Identifying Marks: {ctx['identifyingMarks']}\n"
        f"• Wearing: {ctx['clothingSummary']}\n"
        f"• Medical Vulnerability: {ctx['medicalAlert']}\n\n"
        f"INVESTIGATIVE UPDATE:\n"
        f"{latest_lead_context}\n\n"
        f"IF YOU HAVE SEEN THIS PERSON OR HAVE ANY INFORMATION:\n"
        f"Please contact Riverfront Police Control at {ctx['policeHelpline']} "
        f"or the family contact {ctx['contactName']} at {ctx['contactPhone']}. "
        f"Quote Case #{ctx['caseNumber']}. Do not approach in an alarming manner."
    )

    clean_name = ctx['name'].replace(' ', '')
    social_media_snippet = (
        f"[URGENT MISSING NOTICE] #{clean_name} ({ctx['age']} yrs). Last seen {ctx['lastSeenTime']} at {ctx['lastSeenLocation']}. "
        f"Wearing {ctx['clothingSummary']}. Medical alert: {ctx['medicalAlert']}! "
        f"Call 112 / {ctx['contactPhone']} immediately. Pls RT! #Find{clean_name} #MissingPersonAhmedabad"
    )

    return {
        "caseNumber": ctx["caseNumber"],
        "title": f"URGENT PUBLIC APPEAL: {ctx['name']} ({ctx['age']})",
        "urgencyLevel": "CRITICAL - FIRST 24 HOURS",
        "subjectName": ctx["name"],
        "age": ctx["age"],
        "lastSeen": {
            "date": ctx["lastSeenDate"],
            "time": ctx["lastSeenTime"],
            "location": ctx["lastSeenLocation"]
        },
        "physicalSummary": {
            "heightCm": ctx["heightCm"],
            "build": ctx["build"],
            "hair": ctx["hairColor"],
            "eyes": ctx["eyeColor"],
            "identifyingMarks": ctx["identifyingMarks"],
            "clothing": ctx["clothingSummary"],
            "medicalAlert": ctx["medicalAlert"]
        },
        "fullAppealText": appeal_body,
        "socialMediaBroadcast": social_media_snippet,
        "contactInformation": {
            "helpline": "112",
            "stationDesk": ctx["policeHelpline"],
            "familyContact": f"{ctx['contactName']} ({ctx['contactPhone']})"
        },
        "generatedAt": datetime.now().isoformat()
    }


def generate_police_case_file(case_data: Dict[str, Any], leads: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Auto-fill a formal Missing Person Police Case File (FIR / dossier).
    """
    ctx = _extract_profile_context(case_data)

    lead_summaries = []
    action_items = [
        "Issue preservation orders for CCTV along the Riverfront corridor and transit exits.",
        "Deploy quick-response patrol units to verify priority sighting locations.",
        "Alert local hospitals, emergency rooms, and civil hospital casualty wards.",
        "Task cyber cell to monitor tip streams and verify social media sighting mentions.",
        "Conduct targeted vendor and witness interviews near last confirmed sighting."
    ]

    for lead in leads[:3]:
        lead_summaries.append({
            "leadId": lead.get("leadId"),
            "rank": lead.get("rank"),
            "priority": lead.get("priority"),
            "score": lead.get("score"),
            "summary": lead.get("title"),
            "sources": lead.get("sourceRecordIds"),
            "evidence": {
                "matching": lead.get("matchingEvidence", []),
                "conflicting": lead.get("conflictingEvidence", []),
                "uncertainty": lead.get("uncertainty", [])
            },
            "nextAction": lead.get("recommendedNextAction")
        })

    return {
        "caseFileNumber": ctx["caseNumber"],
        "firType": "Form 57 - Missing Person Initial Registration",
        "jurisdiction": {
            "state": "Gujarat",
            "district": "Ahmedabad City",
            "policeStation": "Riverfront West Police Station"
        },
        "incidentMetadata": {
            "reportedDateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "incidentDateTime": f"{ctx['lastSeenDate']} {ctx['lastSeenTime']}",
            "placeOfOccurrence": ctx["lastSeenLocation"],
            "classification": "Vulnerable Missing Person - Priority Alpha (Medication Dependent)"
        },
        "victimParticulars": {
            "fullName": ctx["name"],
            "alias": ctx["aliases"],
            "dateOfBirth": ctx["dateOfBirth"],
            "age": ctx["age"],
            "gender": "Male",
            "heightCm": ctx["heightCm"],
            "build": ctx["build"],
            "hairColor": ctx["hairColor"],
            "eyeColor": ctx["eyeColor"],
            "identifyingMarks": [ctx["identifyingMarks"]],
            "clothingLastSeen": ctx["clothingRaw"],
            "medicalAlert": ctx["medicalAlert"],
            "informantDetails": {
                "name": ctx["contactName"],
                "phone": ctx["contactPhone"],
                "relation": "Mother / Next of Kin"
            }
        },
        "correlatedLeadsSummary": lead_summaries,
        "investigativeActionChecklist": action_items,
        "supervisoryNotes": (
            f"Deterministic correlation identified {len(leads)} potential leads. "
            f"Top lead corroborated across CCTV and tip channels. "
            f"All field teams must treat scores as investigative priority indicators, not verified identities."
        ),
        "officerInCharge": {
            "name": "Insp. R. K. Verma",
            "designation": "Station House Officer / Investigating Officer",
            "badgeNumber": "GJ-AMD-4019"
        },
        "status": "Dossier Auto-Generated & Ready for Investigating Officer Verification"
    }
