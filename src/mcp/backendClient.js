import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..', '..');
const dataFilePath = path.join(projectRoot, 'src', 'integration', 'mockCaseData.json');

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

async function readCaseDataFile() {
  const raw = await fs.readFile(dataFilePath, 'utf8');
  return JSON.parse(raw);
}

function extractCaseRecord(caseNumber, dataset) {
  const normalized = normalizeCaseNumber(caseNumber);
  const caseRecord = dataset?.caseNumber === normalized ? dataset : null;
  if (!caseRecord) {
    throw createBackendError('CASE_NOT_FOUND', { caseNumber: normalized });
  }
  return caseRecord;
}

export async function getPersonProfile(caseNumber) {
  const dataset = await readCaseDataFile();
  const caseRecord = extractCaseRecord(caseNumber, dataset);
  return caseRecord.personProfile;
}

export async function getInvestigatorTips(caseNumber) {
  const dataset = await readCaseDataFile();
  const caseRecord = extractCaseRecord(caseNumber, dataset);
  return {
    caseNumber: caseRecord.caseNumber,
    sourceType: 'investigator_tips',
    tips: caseRecord.investigatorTips
  };
}

export async function getCctvSightings(caseNumber) {
  const dataset = await readCaseDataFile();
  const caseRecord = extractCaseRecord(caseNumber, dataset);
  return {
    caseNumber: caseRecord.caseNumber,
    sourceType: 'cctv_sightings',
    sightings: caseRecord.cctvSightings
  };
}

export async function getCaseData(caseNumber) {
  const dataset = await readCaseDataFile();
  const caseRecord = extractCaseRecord(caseNumber, dataset);
  return {
    caseNumber: caseRecord.caseNumber,
    personProfile: caseRecord.personProfile,
    investigatorTips: caseRecord.investigatorTips,
    cctvSightings: caseRecord.cctvSightings
  };
}

export async function getCorrelationResults(caseNumber) {
  const dataset = await readCaseDataFile();
  const caseRecord = extractCaseRecord(caseNumber, dataset);
  if (!caseRecord.analysis || !caseRecord.analysis.leads) {
    throw createBackendError('CORRELATION_UNAVAILABLE', { caseNumber });
  }
  return {
    caseNumber: caseRecord.analysis.caseNumber,
    scoringVersion: caseRecord.analysis.scoringVersion,
    generatedAt: caseRecord.analysis.generatedAt,
    leads: caseRecord.analysis.leads
  };
}
