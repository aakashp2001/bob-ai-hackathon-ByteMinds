"""
Model Context Protocol (MCP) Server for Missing Person Investigation Assistant.

This server exposes standard MCP Tools, Resources, and Prompts to IBM Bob,
allowing Bob (or any MCP-compatible agent) to:
1. Retrieve family-provided case profiles, investigator tips, and CCTV sightings.
2. Execute the deterministic correlation engine to obtain ranked investigative leads.
3. Draft urgent public appeal notices for social media and broadcast.
4. Auto-fill formal police missing person case files (FIRs).

Transports supported:
- stdio (default, for CLI / Claude Desktop / Bob IDE / MCP Inspector)
- sse (Server-Sent Events on HTTP)
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# MCP Server import with fallback for v1 / v2
try:
    from mcp.server.mcpserver import MCPServer
except ImportError:
    from mcp.server.fastmcp import FastMCP as MCPServer

# Internal service imports
DATA_DIR = Path(__file__).resolve().parents[1] / "data"

from src.backend.services.correlation import run_correlation
from src.backend.services.synthesis import generate_public_appeal, generate_police_case_file

# Initialize MCP Server
mcp_server = MCPServer(
    name="Missing Person Investigation Assistant",
    instructions=(
        "You are an investigative assistant coordinating a missing person case during the critical first 24 hours. "
        "Use deterministic correlation tools to prioritize leads, highlight matching and conflicting evidence, "
        "and generate structured public appeal notices and formal police case files."
    )
)


def _load_json_file(filename: str) -> Any:
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Data file {filename} not found at {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# MCP Tools
# ---------------------------------------------------------------------------

@mcp_server.tool()
def get_case_profile(case_number: str = "MP-2026-0042") -> Dict[str, Any]:
    """
    Retrieve verified family-provided data for a missing person case.
    Includes physical description, last seen details, clothing, and medical vulnerabilities.
    """
    data = _load_json_file("person_profile.json")
    return data


@mcp_server.tool()
def get_investigator_tips(case_number: str = "MP-2026-0042") -> List[Dict[str, Any]]:
    """
    Retrieve all mock investigator tip logs submitted by the public, patrol officers,
    and social media signals.
    """
    data = _load_json_file("tips.json")
    return data


@mcp_server.tool()
def get_cctv_sightings(case_number: str = "MP-2026-0042") -> List[Dict[str, Any]]:
    """
    Retrieve municipal and private CCTV camera sightings and descriptions near the last seen location.
    """
    data = _load_json_file("cctv.json")
    return data


@mcp_server.tool()
def analyze_investigative_leads(case_number: str = "MP-2026-0042") -> Dict[str, Any]:
    """
    Run the deterministic correlation and scoring pipeline.
    Correlates family profile, investigator tips, and CCTV sightings into prioritized leads
    with score breakdown, matching evidence, conflicting evidence, uncertainty notes,
    and recommended next actions.
    """
    result = run_correlation()
    return result


@mcp_server.tool()
def draft_public_appeal(case_number: str = "MP-2026-0042") -> Dict[str, Any]:
    """
    Generate an urgent, broadcast-ready Public Appeal Notice for community alerts
    and social media broadcast, synthesized from verified profile data and top correlated leads.
    """
    profile_data = _load_json_file("person_profile.json")
    analysis = run_correlation()
    leads = analysis.get("leads", [])
    appeal = generate_public_appeal(profile_data, leads)
    return appeal


@mcp_server.tool()
def autofill_police_case_file(case_number: str = "MP-2026-0042") -> Dict[str, Any]:
    """
    Auto-fill a formal Missing Person Police Case File / First Information Report (FIR dossier)
    with statutory complainant data, subject physical specs, chronological sighting summaries,
    and officer action checklist.
    """
    profile_data = _load_json_file("person_profile.json")
    analysis = run_correlation()
    leads = analysis.get("leads", [])
    case_file = generate_police_case_file(profile_data, leads)
    return case_file


# ---------------------------------------------------------------------------
# MCP Resources
# ---------------------------------------------------------------------------

@mcp_server.resource("case://MP-2026-0042/profile")
def resource_profile() -> str:
    """Family-provided profile resource for case MP-2026-0042."""
    data = _load_json_file("person_profile.json")
    return json.dumps(data, indent=2)


@mcp_server.resource("case://MP-2026-0042/leads")
def resource_leads() -> str:
    """Latest correlated investigative leads resource for case MP-2026-0042."""
    data = run_correlation()
    return json.dumps(data, indent=2)


# ---------------------------------------------------------------------------
# MCP Prompts
# ---------------------------------------------------------------------------

@mcp_server.prompt()
def review_investigation_status(case_number: str = "MP-2026-0042") -> str:
    """Prompt for Bob to perform an executive briefing of the missing person case."""
    return (
        f"You are Bob, an AI Case Coordination Assistant. "
        f"Review the latest case profile and correlated leads for case {case_number}. "
        f"1. Summarize the missing person's status and critical vulnerabilities. "
        f"2. Detail the top 3 investigative leads, citing corroborating CCTV and tip evidence. "
        f"3. Note any conflicting evidence or uncertainties. "
        f"4. Propose immediate field actions for the investigating officers."
    )


# ---------------------------------------------------------------------------
# Custom HTTP Routes (so opening http://localhost:8001/ doesn't return 404)
# ---------------------------------------------------------------------------

from starlette.responses import JSONResponse

@mcp_server.custom_route("/", methods=["GET"])
async def mcp_home(request):
    """Informational landing page for browsers opening the MCP server port."""
    return JSONResponse({
        "server": "Missing Person Investigation Assistant MCP Server",
        "status": "online",
        "protocol": "Model Context Protocol (MCP)",
        "sseEndpoint": "/sse",
        "messagesEndpoint": "/messages/",
        "instructions": (
            "This is an MCP SSE Server. Connect your MCP client (Bob, Claude Desktop, or Inspector) "
            "to the /sse endpoint."
        ),
        "availableTools": [
            "get_case_profile",
            "get_investigator_tips",
            "get_cctv_sightings",
            "analyze_investigative_leads",
            "draft_public_appeal",
            "autofill_police_case_file"
        ]
    })



# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description="MCP Server for Missing Person Investigation Assistant")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport protocol to use (default: stdio)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8001,
        help="Port for SSE transport (default: 8001)"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host for SSE transport (default: 127.0.0.1)"
    )

    args = parser.parse_args()

    if args.transport == "stdio":
        # Print info on stderr so stdio JSON-RPC remains clean
        sys.stderr.write("Starting Missing Person MCP Server on stdio transport...\n")
        mcp_server.run(transport="stdio")
    elif args.transport == "sse":
        sys.stderr.write(f"Starting Missing Person MCP Server on SSE transport (http://{args.host}:{args.port}/sse)...\n")
        mcp_server.run(transport="sse", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
