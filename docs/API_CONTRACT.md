# API Contract — Missing Person Case Coordination Backend

> **Version:** 1.1.0
> **Base URL:** `http://localhost:8000`
>
> This document is the shared contract between Person 1 (MCP/Bob),
> Person 2 (Backend), and Person 3 (Frontend).

---

## Endpoints

---

### `GET /`

**Purpose:** Health check.

**Response (200):**

```json
{
  "message": "Missing Person Case Coordination API is running",
  "status": "ok"
}
```

---

### `GET /case`

**Purpose:** Return the verified family-provided person profile.

**Response (200):**

```json
{
  "caseNumber": "MP-2026-0042",
  "name": "Aarav Shah",
  "aliases": ["Aarav"],
  "dateOfBirth": "2004-03-14",
  "age": 22,
  "physicalDescription": {
    "heightCm": 178,
    "build": "medium",
    "hairColor": "black",
    "eyeColor": "brown",
    "identifyingMarks": ["small scar above right eyebrow"]
  },
  "clothing": {
    "top": "blue hoodie",
    "bottom": "black jeans",
    "footwear": "white sneakers",
    "backpack": "black backpack with grey stripe"
  },
  "lastSeen": {
    "dateTime": "2026-09-23T18:10:00",
    "location": "Riverfront Park, Ahmedabad"
  },
  "contact": {
    "name": "Meera Shah",
    "phone": "+91-90000-00001"
  },
  "notes": "Family reports no confirmed contact since last known sighting."
}
```

**Error (500):**

```json
{
  "detail": "Required data file not found: <path>"
}
```

---

### `GET /tips`

**Purpose:** Return all investigator tip records.

**Response (200):** Array of tip objects.

```json
[
  {
    "tipId": "T001",
    "dateTime": "2026-09-23T18:32:00",
    "source": "Witness",
    "description": "...",
    "observedName": null,
    "location": "Riverfront Pedestrian Bridge, Ahmedabad",
    "clothing": {
      "top": "blue hoodie",
      "bottom": "black jeans",
      "footwear": null,
      "backpack": null
    },
    "physical": {
      "heightCm": null,
      "build": "medium",
      "hair": "black",
      "eyes": null,
      "identifyingMark": null
    }
  }
]
```

**Error (500):**

```json
{
  "detail": "Required data file not found: <path>"
}
```

---

### `GET /cctv`

**Purpose:** Return all CCTV sighting descriptions.

**Response (200):** Array of CCTV sighting objects.

```json
[
  {
    "sightingId": "C001",
    "dateTime": "2026-09-23T18:36:00",
    "cameraLocation": "Riverfront Pedestrian Bridge, Ahmedabad",
    "description": "...",
    "imageUrl": "mock://cctv/C001",
    "observedName": null,
    "location": "Riverfront Pedestrian Bridge, Ahmedabad",
    "clothing": {
      "top": "blue hoodie",
      "bottom": "black jeans",
      "footwear": "white sneakers",
      "backpack": "black backpack with grey stripe"
    },
    "physical": {
      "heightCm": 177,
      "build": "medium",
      "hair": "black",
      "eyes": null,
      "identifyingMark": null
    }
  }
]
```

**Error (500):**

```json
{
  "detail": "Required data file not found: <path>"
}
```

---

### `GET /analyze`

**Purpose:** Run deterministic correlation and return prioritized investigative leads.

**Response (200):**

```json
{
  "caseNumber": "MP-2026-0042",
  "status": "completed",
  "scoringModel": {
    "maxScore": 100,
    "interpretation": "Investigative priority score only; not identity confidence or probability.",
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
  "leads": [
    {
      "leadId": "L001",
      "rank": 1,
      "title": "Riverfront Potential Sighting",
      "sourceRecordIds": ["T001", "C001"],
      "score": 82,
      "scoreBreakdown": {
        "name": 0,
        "location": 25,
        "time": 20,
        "clothing": 15,
        "physical": 10
      },
      "priority": "high",
      "matchingEvidence": [
        "Observed location matches the last known location.",
        "Clothing match: top = blue hoodie."
      ],
      "conflictingEvidence": [],
      "uncertainty": "low",
      "uncertaintyFactors": [
        "No observed name was provided."
      ],
      "recommendedNextAction": "Verify tip record T001 against CCTV record C001 and review the full available footage.",
      "corroboratingRecordCount": 2
    }
  ]
}
```

> **Note:** `score` values in this example are illustrative.
> The actual scores are computed deterministically by the scoring engine.

**Error (500):**

```json
{
  "detail": "Correlation analysis failed: <message>"
}
```

---

## Scoring Model

| Category | Max Points | Notes |
|---|---|---|
| Name | 30 | Exact match against name or aliases |
| Location | 25 | 25 = exact match, 20 = same zone, 10 = nearby transit |
| Time | 20 | 20/15/10/5/0 based on time window from last seen |
| Clothing | 15 | top=5, bottom=4, footwear=3, backpack=3 |
| Physical | 10 | hair=3, build=3, height=2, eyes=2 |

The identifying mark is **not scored** but contributes to matching/conflicting evidence.

---

## Lead Grouping

Records are grouped into leads when they:
- Occur within **15 minutes** of each other
- Belong to the **same geographic zone**

The lead score is the **highest individual record score** within the group.

---

## Extra Fields (Backend Additions)

These fields are not in the original brief but provide useful context:

| Field | Type | Purpose |
|---|---|---|
| `uncertaintyFactors` | `string[]` | List of specific uncertainty reasons |
| `corroboratingRecordCount` | `int` | Number of source records in the lead |
| `scoringModel` | `object` | Metadata about the scoring system |

---

## Data Field Naming

All JSON responses use **camelCase**. The clothing and physical field names
are consistent across the profile, tips, and CCTV schemas:

| Field | Profile | Tips | CCTV |
|---|---|---|---|
| Top | `clothing.top` | `clothing.top` | `clothing.top` |
| Bottom | `clothing.bottom` | `clothing.bottom` | `clothing.bottom` |
| Footwear | `clothing.footwear` | `clothing.footwear` | `clothing.footwear` |
| Backpack | `clothing.backpack` | `clothing.backpack` | `clothing.backpack` |
| Tip ID | — | `tipId` | — |
| Sighting ID | — | — | `sightingId` |

---

## Additional Endpoints (v1.2.0)

### `GET /case/appeal`

**Purpose:** Return the drafted public appeal notice for broadcast and social media.

**Response (200):**
```json
{
  "caseNumber": "MP-2026-0042",
  "title": "URGENT PUBLIC APPEAL: Aarav Shah (22)",
  "urgencyLevel": "CRITICAL - FIRST 24 HOURS",
  "subjectName": "Aarav Shah",
  "age": 22,
  "physicalSummary": { ... },
  "fullAppealText": "...",
  "socialMediaBroadcast": "...",
  "contactInformation": { ... }
}
```

---

### `GET /case/file`

**Purpose:** Return the auto-filled police missing person case file (FIR dossier).

**Response (200):**
```json
{
  "caseFileNumber": "MP-2026-0042",
  "firType": "Form 57 - Missing Person Initial Registration",
  "jurisdiction": { ... },
  "victimParticulars": { ... },
  "correlatedLeadsSummary": [ ... ],
  "investigativeActionChecklist": [ ... ],
  "officerInCharge": { ... }
}
```

---

### `GET /mcp/tools`

**Purpose:** Returns the catalog of registered Model Context Protocol tools for Bob inspection.

---

## MCP Server Specification

- **Server:** `src/mcp/server.py`
- **Supported Transports:** `stdio` (CLI/Claude/Bob IDE) and `sse` (HTTP)
- **Tools Registered:**
  1. `get_case_profile`
  2. `get_investigator_tips`
  3. `get_cctv_sightings`
  4. `analyze_investigative_leads`
  5. `draft_public_appeal`
  6. `autofill_police_case_file`
- **Resources:** `case://MP-2026-0042/profile`, `case://MP-2026-0042/leads`
- **Prompts:** `review_investigation_status`
