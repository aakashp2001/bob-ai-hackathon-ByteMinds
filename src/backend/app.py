from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path

from src.backend.services.correlation import run_correlation
from src.backend.services.synthesis import generate_public_appeal, generate_police_case_file


# ---------------------------------------------------------------------------
# Resolve data directory relative to this file so the server works
# regardless of the working directory.
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]  # → src/
DATA_DIR = BASE_DIR / "data"


app = FastAPI(
    title="Missing Person Case Coordination API",
    description=(
        "Deterministic backend for the IBM Bob Hackathon "
        "Missing Person Investigation Assistant prototype."
    ),
    version="1.1.0"
)


# ---------------------------------------------------------------------------
# CORS — allow frontend and MCP layer to reach the API.
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_json(filename):
    """Load a JSON data file from the data directory."""
    path = DATA_DIR / filename

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail=f"Required data file not found: {path}"
        )

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid JSON data file: {path}"
        )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Missing Person Case Coordination API is running",
        "status": "ok"
    }


@app.get("/case")
def get_case():
    """Return the verified family-provided person profile."""
    return load_json("person_profile.json")


@app.get("/tips")
def get_tips():
    """Return all investigator tip records."""
    return load_json("tips.json")


@app.get("/cctv")
def get_cctv():
    """Return all CCTV sighting descriptions."""
    return load_json("cctv.json")


@app.get("/analyze")
def analyze_case():
    """Run deterministic correlation and return prioritized leads."""
    try:
        return run_correlation()

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Correlation analysis failed: {str(exc)}"
        )


@app.get("/case/appeal")
def get_public_appeal():
    """Generate and return the drafted public appeal notice for the case."""
    try:
        profile = load_json("person_profile.json")
        correlation_result = run_correlation()
        leads = correlation_result.get("leads", [])
        return generate_public_appeal(profile, leads)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate public appeal: {str(exc)}"
        )


@app.get("/case/file")
def get_police_case_file():
    """Generate and return the auto-filled police missing person case file (FIR dossier)."""
    try:
        profile = load_json("person_profile.json")
        correlation_result = run_correlation()
        leads = correlation_result.get("leads", [])
        return generate_police_case_file(profile, leads)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate police case file: {str(exc)}"
        )


@app.get("/mcp/tools")
def list_mcp_tools():
    """Return catalog of available MCP tools for Bob and external agents."""
    return {
        "server": "Missing Person Investigation Assistant",
        "protocol": "Model Context Protocol (MCP)",
        "transports": ["stdio", "sse"],
        "tools": [
            {
                "name": "get_case_profile",
                "description": "Retrieve verified family-provided profile data for a missing person case."
            },
            {
                "name": "get_investigator_tips",
                "description": "Retrieve all mock investigator tip logs submitted by public and patrol officers."
            },
            {
                "name": "get_cctv_sightings",
                "description": "Retrieve municipal and private CCTV camera sightings near last seen location."
            },
            {
                "name": "analyze_investigative_leads",
                "description": "Run deterministic correlation & scoring engine; returns ranked leads with matching/conflicting evidence."
            },
            {
                "name": "draft_public_appeal",
                "description": "Generate an urgent, broadcast-ready Public Appeal Notice for community alerts."
            },
            {
                "name": "autofill_police_case_file",
                "description": "Auto-fill a formal Missing Person Police Case File (FIR dossier) with timeline and action items."
            }
        ]
    }