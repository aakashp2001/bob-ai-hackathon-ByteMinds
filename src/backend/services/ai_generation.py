
import json
import os
from typing import Any

import requests

from src.backend.services.correlation import load_data, run_correlation


class AIServiceError(Exception):
    """Raised when the configured NVIDIA provider cannot generate output."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def _required_setting(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise AIServiceError(
            "AI_NOT_CONFIGURED",
            f"Missing required AI configuration: {name}."
        )

    return value


def _request_json(
    url: str,
    method: str,
    data: bytes,
    headers: dict[str, str]
) -> dict[str, Any]:
    """Send a JSON request to NVIDIA and return the decoded response."""

    timeout = float(os.getenv("NVIDIA_TIMEOUT_SECONDS", "30"))

    try:
        response = requests.request(
            method=method,
            url=url,
            data=data,
            headers=headers,
            timeout=timeout
        )

        if not response.ok:
            raise AIServiceError(
                "AI_PROVIDER_ERROR",
                f"NVIDIA API returned HTTP {response.status_code}: "
                f"{response.text[:300]}"
            )

        try:
            payload = response.json()
        except ValueError as error:
            raise AIServiceError(
                "AI_INVALID_PROVIDER_RESPONSE",
                "The NVIDIA API returned invalid JSON."
            ) from error

        if not isinstance(payload, dict):
            raise AIServiceError(
                "AI_INVALID_PROVIDER_RESPONSE",
                "The NVIDIA API returned an unexpected response format."
            )

        return payload

    except AIServiceError:
        raise

    except requests.Timeout as error:
        raise AIServiceError(
            "AI_PROVIDER_UNAVAILABLE",
            "The NVIDIA API request timed out."
        ) from error

    except requests.RequestException as error:
        raise AIServiceError(
            "AI_PROVIDER_UNAVAILABLE",
            f"The NVIDIA API could not be reached: {error}"
        ) from error


def _build_prompt(
    mode: str,
    profile: dict[str, Any],
    tips: list[dict[str, Any]],
    cctv: list[dict[str, Any]],
    analysis: dict[str, Any]
) -> str:
    """Build the prompt sent to the NVIDIA model."""

    context = json.dumps(
        {
            "personProfile": profile,
            "investigatorTips": tips,
            "cctvSightings": cctv,
            "correlationResults": analysis
        },
        ensure_ascii=True
    )

    shared = (
        "This is a fictional missing-person case coordination prototype. "
        "CCTV descriptions never confirm identity. "
        "Never claim a person is definitely the missing person. "
        "Do not recalculate or modify backend scores. "
        "Preserve every leadId, score, sourceRecordIds, matchingEvidence, "
        "conflictingEvidence, and recommendedNextAction exactly as supplied. "
        "Use uncertainty and requires verification language.\n\n"
    )

    if mode == "analyse-case":
        task = (
            "Return JSON only with keys caseNumber, leadExplanations, "
            "and limitations. "
            "Each lead explanation must include leadId, investigativePriority, "
            "sourceRecordIds, score, explanation, matchingEvidence, "
            "conflictingEvidence, uncertainty, and recommendedNextAction. "
            "The score must be copied from correlationResults."
        )

    elif mode == "public-appeal":
        task = (
            "Write a concise professional public appeal using only "
            "personProfile. Include case number, name, age, physical "
            "description, clothing, last known date/time and location, "
            "and contact details. "
            "Do not use tips or CCTV as facts."
        )

    elif mode == "case-file":
        task = (
            "Return JSON only with keys caseNumber, caseInformation, "
            "subjectDetails, physicalDescription, "
            "clothingLastKnownAppearance, lastKnownInformation, "
            "investigatorTips, cctvSightings, "
            "prioritisedInvestigativeLeads, recommendedFollowUpActions, "
            "and dataLimitations. "
            "Keep source records separate from generated analysis."
        )

    else:
        raise AIServiceError(
            "INVALID_MODE",
            f"Unsupported AI generation mode: {mode}."
        )

    return f"{shared}{task}\n\nCase data:\n{context}"


def _parse_json_output(generated_text: str) -> dict[str, Any] | None:
    """Parse JSON returned directly or inside a Markdown code fence."""

    json_text = generated_text.strip()

    if json_text.startswith("```"):
        lines = json_text.splitlines()

        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        json_text = "\n".join(lines).strip()

    try:
        parsed = json.loads(json_text)
    except json.JSONDecodeError:
        return None

    if not isinstance(parsed, dict):
        return None

    return parsed


def generate_ai_output(
    case_number: str,
    mode: str
) -> dict[str, Any]:
    """Generate Bob's AI-assisted case output using NVIDIA."""

    api_key = _required_setting("NVIDIA_API_KEY")
    model_id = _required_setting("NVIDIA_MODEL")

    profile, tips, cctv = load_data()

    requested_case = case_number.strip().upper()
    actual_case = profile.get("caseNumber", "").strip().upper()

    if actual_case != requested_case:
        raise AIServiceError(
            "CASE_NOT_FOUND",
            f"No fictional case found for case number {case_number}."
        )

    # The deterministic backend remains the source of truth.
    analysis = run_correlation()

    prompt = _build_prompt(
        mode=mode,
        profile=profile,
        tips=tips,
        cctv=cctv,
        analysis=analysis
    )

    endpoint = "https://integrate.api.nvidia.com/v1/chat/completions"

    request_payload = {
        "model": model_id,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Bob, a careful case coordination assistant. "
                    "Return only the requested output."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": 1800
    }

    provider_response = _request_json(
        endpoint,
        "POST",
        json.dumps(request_payload).encode("utf-8"),
        {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    )

    choices = provider_response.get("choices")

    if (
        not isinstance(choices, list)
        or not choices
        or not isinstance(choices[0], dict)
    ):
        raise AIServiceError(
            "AI_INVALID_PROVIDER_RESPONSE",
            "The NVIDIA API did not return a generated result."
        )

    message = choices[0].get("message")

    generated_text = (
        message.get("content")
        if isinstance(message, dict)
        else None
    )

    if not isinstance(generated_text, str) or not generated_text.strip():
        raise AIServiceError(
            "AI_INVALID_PROVIDER_RESPONSE",
            "The NVIDIA API returned an empty generated result."
        )

    response: dict[str, Any] = {
        "caseNumber": profile["caseNumber"],
        "mode": mode,
        "generatedText": generated_text.strip(),
        "modelId": model_id
    }

    if mode in {"analyse-case", "case-file"}:
        structured_output = _parse_json_output(generated_text)

        if structured_output is not None:
            response["structuredOutput"] = structured_output
        else:
            response["structuredOutput"] = None
            response["parseWarning"] = (
                "The model response was not valid JSON."
            )

    return response
