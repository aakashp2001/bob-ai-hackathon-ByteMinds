import test from 'node:test';
import assert from 'node:assert/strict';
import { getCase, getLeads, getPublicAppeal, getCaseFile, analyzeCase } from '../src/services/api.js';
import { provided, formatDate, formatRecordTime } from '../src/utils/formatters.js';

test('all mock services preserve the canonical case and supplied lead order', async () => {
  const [caseData, file, leads, appeal, analysis] = await Promise.all([getCase(), getCaseFile(), getLeads(), getPublicAppeal(), analyzeCase()]);
  assert.equal(caseData.caseNumber, 'MP-2026-0042');
  assert.equal(caseData.personProfile.name, 'Aarav Shah');
  assert.equal(caseData.personProfile.age, 22);
  assert.equal(caseData.lastSeen.location, 'Riverfront Park, Ahmedabad');
  assert.equal(caseData.lastSeen.date, '2026-09-23');
  assert.equal(caseData.lastSeen.time, '18:10');
  assert.equal(caseData.tips.length, 8);
  assert.equal(caseData.cctvSightings.length, 6);
  assert.deepEqual(file, caseData);
  assert.deepEqual(leads, caseData.leads);
  assert.deepEqual(appeal, caseData.publicAppeal);
  assert.deepEqual(analysis, { status: 'complete', leads });
  assert.deepEqual(leads.map(({ rank, score }) => [rank, score]), [[1, 70], [2, 45], [3, 25]]);
  const sourceIds = new Set([...caseData.tips.map((tip) => tip.tipId), ...caseData.cctvSightings.map((record) => record.sightingId)]);
  for (const lead of leads) for (const id of lead.sourceRecordIds) assert.ok(sourceIds.has(id), `Missing source ${id}`);
});

test('consumer edits cannot mutate subsequent mock results', async () => {
  const original = await getCase();
  const changed = await getCase();
  changed.personProfile.name = 'Edited locally';
  changed.tips.pop();
  const leads = await getLeads();
  leads[0].sourceRecordIds.push('local-only');
  const appeal = await getPublicAppeal();
  appeal.text = 'Changed';
  assert.deepEqual(await getCase(), original);
  assert.deepEqual(await getCaseFile(), original);
  assert.deepEqual(await getLeads(), original.leads);
  assert.deepEqual(await getPublicAppeal(), original.publicAppeal);
});

test('public copy keeps review notices and excludes investigative scores and source IDs', async () => {
  const appeal = await getPublicAppeal();
  assert.match(appeal.text, /Aarav Shah/);
  assert.match(appeal.text, /MP-2026-0042/);
  assert.equal(appeal.publicationStatus, 'Not Approved');
  assert.equal(appeal.reviewStatus, 'Required');
  assert.doesNotMatch(appeal.text, /\b[TCL]00[1-8]\b|priority score|identity confirmed|confirmed sighting/i);
});

test('presentation preserves missing facts, zero scores, and unrecognized date/time input', () => {
  assert.equal(provided(0), 0);
  assert.equal(provided(null), 'Not provided');
  assert.equal(provided('Not supplied'), 'Not provided');
  assert.equal(formatDate(null), 'Not provided');
  assert.equal(formatDate('unknown-date'), 'unknown-date');
  assert.match(formatDate('2026-09-23'), /23 Sept? 2026/);
  const timestamp = '2026-09-23T18:15:00+05:30';
  assert.match(formatRecordTime(timestamp, 'Asia/Kolkata'), /18:15/);
  assert.equal(formatRecordTime(timestamp, 'Unknown/Zone'), timestamp);
  assert.equal(formatRecordTime(timestamp), timestamp);
  assert.equal(formatRecordTime('unknown-time', 'Asia/Kolkata'), 'unknown-time');
});
