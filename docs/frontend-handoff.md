# Frontend Handoff

## Integration boundary

The frontend should consume the backend API for source data and deterministic leads. Bob/MCP is responsible for natural-language explanations and document generation. The frontend must not implement or recalculate scoring.

Backend base URL: `http://localhost:8000`

| Purpose | Method | Endpoint | Response |
|---|---|---|---|
| Person profile | GET | `/case` | Profile object with `caseNumber`, name, physical description, clothing, lastSeen, and contact |
| Investigator tips | GET | `/tips` | Array of records with `tipId`, `dateTime`, `source`, and `description` |
| CCTV sightings | GET | `/cctv` | Array of records with `sightingId`, `cameraLocation`, `dateTime`, `description`, and `imageUrl` |
| Correlation results | GET | `/analyze` | `{ caseNumber, totalEvidenceRecords, totalLeads, leads }` |

The current backend serves the fictional case `MP-2026-0042` and does not accept a case-number query parameter. The MCP adapter validates the returned `caseNumber` before exposing data to Bob.

## Lead rendering contract

Each backend lead contains:

```json
{
  "leadId": "L001",
  "score": 69,
  "sourceRecordIds": ["C005", "T001", "C001", "T003", "C003"],
  "matchingEvidence": [],
  "conflictingEvidence": [],
  "recommendedNextAction": ""
}
```

Render the numeric `score` exactly as returned. Treat it as an investigative priority signal, not identity confidence or proof. Use `sourceRecordIds` to link the lead back to tips and CCTV rows.

## Bob output boundary

Bob analysis should be treated as generated explanation, not source truth. When the Bob workflow returns JSON, expect:

```json
{
  "caseNumber": "MP-2026-0042",
  "leadExplanations": [
    {
      "leadId": "L001",
      "investigativePriority": "high",
      "sourceRecordIds": [],
      "score": 69,
      "explanation": "",
      "matchingEvidence": [],
      "conflictingEvidence": [],
      "uncertainty": "",
      "recommendedNextAction": ""
    }
  ],
  "limitations": []
}
```

Do not display Bob-generated wording as confirmation of identity. Include visible uncertainty and verification language in lead details.

## Local run

```powershell
.\.venv\Scripts\python.exe -m uvicorn src.backend.app:app --host 127.0.0.1 --port 8000
npm start
```

The frontend can use the backend directly at `http://127.0.0.1:8000`; Bob connects to the MCP server through `.bob/mcp.json`.
