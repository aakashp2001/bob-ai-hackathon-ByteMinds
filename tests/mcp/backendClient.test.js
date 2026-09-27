import test from 'node:test';
import assert from 'node:assert/strict';
import { createServer } from 'node:http';

import {
  getPersonProfile,
  getInvestigatorTips,
  getCctvSightings,
  getCaseData,
  getCorrelationResults,
  getBackendErrorInfo,
  normalizeCaseNumber
} from '../../src/mcp/backendClient.js';

const backendPayloads = {
  profile: {
    caseNumber: 'MP-2026-0042',
    name: 'Aarav Shah',
    aliases: ['Aarav']
  },
  tips: [{ tipId: 'T001', description: 'Blue hoodie near the bridge.' }],
  cctv: [{ sightingId: 'C001', cameraLocation: 'Riverfront Pedestrian Bridge' }],
  analysis: {
    caseNumber: 'MP-2026-0042',
    totalEvidenceRecords: 2,
    totalLeads: 1,
    leads: [{
      leadId: 'L001',
      sourceRecordIds: ['T001', 'C001'],
      score: 85,
      matchingEvidence: ['Blue hoodie'],
      conflictingEvidence: [],
      recommendedNextAction: 'Verify the sighting.'
    }]
  }
};

const backendServer = createServer((request, response) => {
  const payloads = {
    '/case': backendPayloads.profile,
    '/tips': backendPayloads.tips,
    '/cctv': backendPayloads.cctv,
    '/analyze': backendPayloads.analysis
  };
  const payload = payloads[request.url];
  if (!payload) {
    response.writeHead(404, { 'content-type': 'application/json' });
    response.end(JSON.stringify({ detail: 'Not found' }));
    return;
  }
  response.writeHead(200, { 'content-type': 'application/json' });
  response.end(JSON.stringify(payload));
});

await new Promise((resolve) => backendServer.listen(0, '127.0.0.1', resolve));
process.env.BACKEND_BASE_URL = `http://127.0.0.1:${backendServer.address().port}`;
process.env.BACKEND_TIMEOUT_MS = '1000';

test.after(() => backendServer.close());

test('normalizeCaseNumber trims and uppercases case numbers', () => {
  assert.equal(normalizeCaseNumber(' mp-2026-0042 '), 'MP-2026-0042');
});

test('getPersonProfile returns the family profile for the fictional case', async () => {
  const result = await getPersonProfile('MP-2026-0042');
  assert.equal(result.caseNumber, 'MP-2026-0042');
  assert.equal(result.sourceType, 'family_provided');
  assert.equal(result.name, 'Aarav Shah');
  assert.ok(Array.isArray(result.aliases));
});

test('getInvestigatorTips returns the original tip records without modification', async () => {
  const result = await getInvestigatorTips('MP-2026-0042');
  assert.equal(result.sourceType, 'investigator_tips');
  assert.ok(Array.isArray(result.tips));
  assert.equal(result.tips[0].tipId, 'T001');
});

test('getCctvSightings preserves sighting IDs', async () => {
  const result = await getCctvSightings('MP-2026-0042');
  assert.equal(result.sourceType, 'cctv_sightings');
  assert.equal(result.sightings[0].sightingId, 'C001');
});

test('getCaseData returns the combined case context', async () => {
  const result = await getCaseData('MP-2026-0042');
  assert.equal(result.caseNumber, 'MP-2026-0042');
  assert.ok(result.personProfile);
  assert.ok(Array.isArray(result.investigatorTips));
  assert.ok(Array.isArray(result.cctvSightings));
});

test('getCorrelationResults returns the backend score unchanged', async () => {
  const result = await getCorrelationResults('MP-2026-0042');
  assert.equal(result.caseNumber, 'MP-2026-0042');
  assert.equal(result.leads[0].score, 85);
});

test('unknown cases produce a clear CASE_NOT_FOUND error shape', async () => {
  await assert.rejects(
    () => getPersonProfile('MP-9999'),
    (error) => {
      assert.equal(error.code, 'CASE_NOT_FOUND');
      assert.match(error.message, /No fictional case found/i);
      return true;
    }
  );
});

test('backend errors map to machine-readable codes', () => {
  const err = getBackendErrorInfo('CASE_NOT_FOUND');
  assert.equal(err.code, 'CASE_NOT_FOUND');
  assert.match(err.message, /No fictional case found/i);
});
