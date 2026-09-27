const ERROR_MAP = {
  CASE_NOT_FOUND: {
    code: 'CASE_NOT_FOUND',
    message: 'No fictional case found for case number {caseNumber}.'
  },
  BACKEND_UNAVAILABLE: {
    code: 'BACKEND_UNAVAILABLE',
    message: 'The backend case service is unavailable.'
  },
  BACKEND_TIMEOUT: {
    code: 'BACKEND_TIMEOUT',
    message: 'The backend case service timed out.'
  },
  INVALID_BACKEND_RESPONSE: {
    code: 'INVALID_BACKEND_RESPONSE',
    message: 'The backend responded with an unexpected format.'
  },
  CORRELATION_UNAVAILABLE: {
    code: 'CORRELATION_UNAVAILABLE',
    message: 'Correlation results are unavailable for this case.'
  }
};

export function normalizeCaseNumber(caseNumber) {
  if (!caseNumber || typeof caseNumber !== 'string') {
    throw createBackendError('CASE_NOT_FOUND', { caseNumber });
  }
  return caseNumber.trim().toUpperCase();
}

export function createBackendError(code, extra = {}) {
  const template = ERROR_MAP[code] || ERROR_MAP.INVALID_BACKEND_RESPONSE;
  const message = template.message.replace('{caseNumber}', extra.caseNumber || '');
  const err = new Error(message);
  err.code = template.code;
  if (extra.status) err.status = extra.status;
  return err;
}

export function getBackendErrorInfo(code, extra = {}) {
  return createBackendError(code, extra);
}

async function requestBackend(pathname, caseNumber) {
  const normalized = normalizeCaseNumber(caseNumber);
  const controller = new AbortController();
  const backendBaseUrl = (process.env.BACKEND_BASE_URL || 'http://localhost:8000').replace(/\/$/, '');
  const backendTimeoutMs = Number.parseInt(process.env.BACKEND_TIMEOUT_MS || '10000', 10);
  const timeout = setTimeout(() => controller.abort(), backendTimeoutMs);

  try {
    let response;
    try {
      response = await fetch(`${backendBaseUrl}${pathname}`, {
        signal: controller.signal,
        headers: { accept: 'application/json' }
      });
    } catch (error) {
      if (error?.name === 'AbortError') {
        throw createBackendError('BACKEND_TIMEOUT', { caseNumber: normalized });
      }
      throw createBackendError('BACKEND_UNAVAILABLE', { caseNumber: normalized });
    }

    if (response.status === 404) {
      throw createBackendError('CASE_NOT_FOUND', { caseNumber: normalized });
    }

    if (!response.ok) {
      throw createBackendError('BACKEND_UNAVAILABLE', { caseNumber: normalized, status: response.status });
    }

    let payload;
    try {
      payload = await response.json();
    } catch {
      throw createBackendError('INVALID_BACKEND_RESPONSE', { caseNumber: normalized });
    }

    if (payload === null || typeof payload !== 'object') {
      throw createBackendError('INVALID_BACKEND_RESPONSE', { caseNumber: normalized });
    }

    return payload;
  } finally {
    clearTimeout(timeout);
  }
}

function assertCaseNumber(payload, caseNumber) {
  const normalized = normalizeCaseNumber(caseNumber);
  if (payload.caseNumber && normalizeCaseNumber(payload.caseNumber) !== normalized) {
    throw createBackendError('CASE_NOT_FOUND', { caseNumber: normalized });
  }
  return normalized;
}

export async function getPersonProfile(caseNumber) {
  const profile = await requestBackend('/case', caseNumber);
  assertCaseNumber(profile, caseNumber);
  return {
    ...profile,
    sourceType: 'family_provided'
  };
}

export async function getInvestigatorTips(caseNumber) {
  const tips = await requestBackend('/tips', caseNumber);
  const normalized = normalizeCaseNumber(caseNumber);
  if (!Array.isArray(tips)) {
    throw createBackendError('INVALID_BACKEND_RESPONSE', { caseNumber: normalized });
  }
  return {
    caseNumber: normalized,
    sourceType: 'investigator_tips',
    tips
  };
}

export async function getCctvSightings(caseNumber) {
  const sightings = await requestBackend('/cctv', caseNumber);
  const normalized = normalizeCaseNumber(caseNumber);
  if (!Array.isArray(sightings)) {
    throw createBackendError('INVALID_BACKEND_RESPONSE', { caseNumber: normalized });
  }
  return {
    caseNumber: normalized,
    sourceType: 'cctv_sightings',
    sightings
  };
}

export async function getCaseData(caseNumber) {
  const normalized = normalizeCaseNumber(caseNumber);
  const [personProfile, investigatorTips, cctvSightings] = await Promise.all([
    getPersonProfile(normalized),
    getInvestigatorTips(normalized),
    getCctvSightings(normalized)
  ]);
  return {
    caseNumber: normalized,
    personProfile,
    investigatorTips: investigatorTips.tips,
    cctvSightings: cctvSightings.sightings
  };
}

export async function getCorrelationResults(caseNumber) {
  const analysis = await requestBackend('/analyze', caseNumber);
  const normalized = assertCaseNumber(analysis, caseNumber);
  if (!Array.isArray(analysis.leads)) {
    throw createBackendError('CORRELATION_UNAVAILABLE', { caseNumber: normalized });
  }
  return {
    ...analysis,
    caseNumber: normalized
  };
}
