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

## AI generation endpoint

The frontend may call the backend AI endpoint for Bob-style explanation and
document generation:

```http
POST /ai/generate
Content-Type: application/json
```

Request:

```json
{
  "caseNumber": "MP-2026-0042",
  "mode": "analyse-case"
}
```

Supported modes are `analyse-case`, `public-appeal`, and `case-file`.

Response:

```json
{
  "caseNumber": "MP-2026-0042",
  "mode": "analyse-case",
  "generatedText": "...",
  "structuredOutput": {},
  "modelId": "openai/gpt-oss-20b"
}
```

The endpoint uses the backend's deterministic correlation output as model
context. The model must not be used to create or alter scores. Configure the
provider through environment variables only:

```text
NVIDIA_API_KEY=your_nvidia_api_key_here
NVIDIA_MODEL=openai/gpt-oss-20b
BACKEND_BASE_URL=http://127.0.0.1:8000
```

Do not expose `NVIDIA_API_KEY` to the browser or commit it. The frontend
should display provider errors using `detail.code` and `detail.message`.
