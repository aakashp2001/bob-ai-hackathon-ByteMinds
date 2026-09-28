"""
Interactive CLI Demo Runner for IBM Bob AI Case Coordination Agent.

Run this script to demonstrate Bob in action:
    python -m src.bob.run_demo
"""

import sys
import time
from src.bob.agent import BobCaseCoordinator


def print_banner():
    print("=" * 70)
    print("  IBM BOB HACKATHON -- MISSING PERSON INVESTIGATION ASSISTANT")
    print("  Bob AI Agent & MCP Tool Coordination Demo")
    print("=" * 70)
    print()


def run_demo():
    print_banner()

    coordinator = BobCaseCoordinator()

    print("[1/5] Ingesting verified family-provided profile via MCP tool...")
    time.sleep(0.5)
    print("      -> Subject: Aarav Shah (Age 22, Medical Alert: Asthma Inhaler)")

    print("\n[2/5] Ingesting mock investigator tips and CCTV sighting descriptions...")
    time.sleep(0.5)
    print("      -> Ingested 9 tip records and 6 CCTV camera sighting feeds")

    print("\n[3/5] Executing Bob's deterministic correlation & priority scoring engine...")
    time.sleep(0.8)
    briefing = coordinator.coordinate_case("MP-2026-0042")
    leads = briefing.get("prioritizedLeads", [])
    print(f"      -> Correlated {len(leads)} distinct investigative leads")

    print("\n" + "-" * 70)
    print("  BOB'S PRIORITIZED INVESTIGATIVE LEADS")
    print("-" * 70)
    for lead in leads[:3]:
        print(f"\n[Rank {lead['rank']}] {lead['title']}")
        print(f"  Priority Score : {lead['score']}/100 ({lead['priority'].upper()})")
        print(f"  Corroboration  : {len(lead.get('sourceRecordIds', []))} sources ({', '.join(lead.get('sourceRecordIds', []))})")
        print(f"  Next Action    : {lead['recommendedNextAction']}")
        if lead.get('matchingEvidence'):
            print(f"  Key Match      : {lead['matchingEvidence'][0]}")

    print("\n" + "-" * 70)
    print("  DRAFTED PUBLIC APPEAL NOTICE (COMMUNITY & SOCIAL MEDIA)")
    print("-" * 70)
    appeal = briefing.get("publicAppealNotice", {})
    print(f"Urgency : {appeal.get('urgencyLevel')}")
    print(f"Social  : {appeal.get('socialMediaBroadcast')}")

    print("\n" + "-" * 70)
    print("  AUTO-FILLED POLICE CASE FILE (FIRST INFORMATION REPORT)")
    print("-" * 70)
    case_file = briefing.get("policeCaseFile", {})
    print(f"FIR Type  : {case_file.get('firType')}")
    print(f"Dossier # : {case_file.get('caseFileNumber')}")
    print(f"Station   : {case_file.get('jurisdiction', {}).get('policeStation')}")
    print(f"Status    : {case_file.get('status')}")

    print("\n" + "=" * 70)
    print("  DEMO COMPLETE")
    print(f"  Artifacts saved to: output/bob_briefing_{briefing['caseNumber']}.md")
    print(f"  Artifacts saved to: output/bob_briefing_{briefing['caseNumber']}.json")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
