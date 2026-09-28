"""
Bob Case Coordination Agent.

Bob is the AI Case Coordination Assistant that orchestrates the investigation:
- Ingests family-provided data, mock investigator tips, and CCTV records.
- Drives the deterministic correlation engine to prioritize investigative leads.
- Drafts public appeal notices for rapid community dissemination.
- Auto-fills the formal police missing person case file (FIR).
- Optionally connects to IBM watsonx.ai (Granite model) when credentials are provided.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import MCP tools directly for native Python invocation
from src.mcp.server import (
    get_case_profile,
    get_investigator_tips,
    get_cctv_sightings,
    analyze_investigative_leads,
    draft_public_appeal,
    autofill_police_case_file,
)


class BobCaseCoordinator:
    """
    Bob AI Case Coordination Agent for Missing Person Investigations.
    """

    def __init__(self):
        self.watsonx_api_key = os.getenv("WATSONX_API_KEY")
        self.watsonx_project_id = os.getenv("WATSONX_PROJECT_ID")
        self.watsonx_url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        self.use_watsonx = bool(
            self.watsonx_api_key and 
            self.watsonx_project_id and 
            self.watsonx_api_key != "your_api_key_here"
        )

    def _call_watsonx_enrichment(self, prompt: str) -> Optional[str]:
        """
        Invoke IBM watsonx.ai REST endpoint if configured.
        """
        if not self.use_watsonx:
            return None

        try:
            import httpx
            # Obtain IAM token or call watsonx generation API
            # For hackathon demonstration, this handles watsonx REST call
            headers = {
                "Authorization": f"Bearer {self.watsonx_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model_id": "ibm/granite-13b-chat-v2",
                "project_id": self.watsonx_project_id,
                "input": prompt,
                "parameters": {
                    "decoding_method": "greedy",
                    "max_new_tokens": 300,
                    "repetition_penalty": 1.1
                }
            }
            resp = httpx.post(
                f"{self.watsonx_url}/ml/v1/text/generation?version=2023-05-29",
                headers=headers,
                json=payload,
                timeout=15.0
            )
            if resp.status_code == 200:
                result = resp.json()
                return result.get("results", [{}])[0].get("generated_text")
        except Exception as e:
            # Fall back safely without crashing
            return f"[Watsonx connection offline: {str(e)}]"
        return None

    def coordinate_case(self, case_number: str = "MP-2026-0042") -> Dict[str, Any]:
        """
        Execute full end-to-end case coordination using MCP tools and Bob synthesis.
        """
        # Step 1: Ingest family profile
        profile = get_case_profile(case_number)

        # Step 2: Ingest investigator tips and CCTV
        tips = get_investigator_tips(case_number)
        cctv = get_cctv_sightings(case_number)

        # Step 3: Run deterministic correlation and lead ranking
        analysis = analyze_investigative_leads(case_number)
        leads = analysis.get("leads", [])

        # Step 4: Draft urgent public appeal
        appeal = draft_public_appeal(case_number)

        # Step 5: Auto-fill formal police case file
        case_file = autofill_police_case_file(case_number)

        # Step 6: Formulate Bob's Executive Briefing
        top_leads = leads[:3]
        executive_summary = (
            f"Bob AI Case Coordination Briefing for Case {case_number}:\n"
            f"- Subject: {profile.get('name')}, age {profile.get('age')}\n"
            f"- Critical Vulnerability: Asthma inhaler required daily; immediate search window active.\n"
            f"- Correlated Data Sources: {len(tips)} investigator tips and {len(cctv)} CCTV records evaluated.\n"
            f"- Highest Priority Lead: {top_leads[0]['title'] if top_leads else 'None'} "
            f"(Investigative Priority Score: {top_leads[0]['score'] if top_leads else 0}/100).\n"
            f"- Immediate Action Required: Dispatch patrol unit to Riverfront pedestrian corridor and preserve CCTV reels."
        )

        # Check for optional watsonx enrichment
        watsonx_notes = None
        if self.use_watsonx:
            watsonx_notes = self._call_watsonx_enrichment(
                f"You are Bob, an AI assistant coordinating missing person investigation {case_number}. "
                f"Summarize immediate priorities for: {executive_summary}"
            )

        briefing = {
            "caseNumber": case_number,
            "timestamp": datetime.now().isoformat(),
            "coordinator": "Bob AI Investigation Assistant (IBM Bob Hackathon)",
            "watsonxEnabled": self.use_watsonx,
            "executiveSummary": executive_summary,
            "watsonxEnrichment": watsonx_notes,
            "personProfile": profile,
            "totalTipsProcessed": len(tips),
            "totalCctvRecordsProcessed": len(cctv),
            "prioritizedLeads": leads,
            "publicAppealNotice": appeal,
            "policeCaseFile": case_file
        }

        # Save briefing artifacts to output folder
        output_dir = Path(__file__).resolve().parents[2] / "output"
        output_dir.mkdir(parents=True, exist_ok=True)

        json_path = output_dir / f"bob_briefing_{case_number}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(briefing, f, indent=2)

        md_path = output_dir / f"bob_briefing_{case_number}.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# Bob AI Investigation Briefing — Case {case_number}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Subject:** {profile.get('name')} (Age: {profile.get('age')})\n\n")
            f.write("## Executive Summary\n\n")
            f.write(f"{executive_summary}\n\n")
            f.write("## Correlated Investigative Leads\n\n")
            for lead in top_leads:
                f.write(f"### Rank {lead.get('rank')}: {lead.get('title')} (Score: {lead.get('score')}/100 - {lead.get('priority').upper()})\n")
                f.write(f"- **Sources:** {', '.join(lead.get('sourceRecordIds', []))}\n")
                f.write(f"- **Recommended Next Action:** {lead.get('recommendedNextAction')}\n")
                f.write(f"- **Matching Evidence:** {', '.join(lead.get('matchingEvidence', [])) or 'None'}\n")
                f.write(f"- **Conflicting Evidence:** {', '.join(lead.get('conflictingEvidence', [])) or 'None'}\n\n")
            f.write("## Public Appeal Notice (Draft)\n\n")
            f.write(f"```\n{appeal.get('fullAppealText')}\n```\n\n")
            f.write("## Police Case File (Auto-Filled FIR)\n\n")
            f.write(f"- **Case Dossier:** {case_file.get('caseFileNumber')} ({case_file.get('firType')})\n")
            f.write(f"- **Jurisdiction:** {case_file.get('jurisdiction', {}).get('policeStation')}\n")
            f.write(f"- **Investigating Officer:** {case_file.get('officerInCharge', {}).get('name')}\n")

        return briefing


if __name__ == "__main__":
    coordinator = BobCaseCoordinator()
    print("Running Bob AI Case Coordinator...")
    res = coordinator.coordinate_case("MP-2026-0042")
    print(f"[SUCCESS] Case {res['caseNumber']} coordinated successfully!")
    print(f"Top Lead: {res['prioritizedLeads'][0]['title']} (Score: {res['prioritizedLeads'][0]['score']})")
    print(f"Artifacts saved to: output/bob_briefing_{res['caseNumber']}.json and .md")
