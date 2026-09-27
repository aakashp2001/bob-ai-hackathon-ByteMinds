import test from 'node:test';
import assert from 'node:assert/strict';

import {
  getPersonProfile,
  getInvestigatorTips,
  getCctvSightings,
  getCaseData,
  getCorrelationResults,
  getBackendErrorInfo,
  normalizeCaseNumber
} from '../../src/mcp/backendClient.js';

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
  assert.equal(result.scoringVersion, '1.0');
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
