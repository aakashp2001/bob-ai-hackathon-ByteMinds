// Fictional frontend fixtures, not investigator findings.
// Profile fields follow the supplied canonical case. Additional record contents
// and fixed lead values must be reconciled with the backend/MCP team's fixtures.
const personProfile = {
  name: 'Aarav Shah',
  age: 22,
  gender: 'Not supplied',
  heightCm: 178,
  build: 'medium',
  hair: 'black',
  eyes: 'brown',
  identifyingMark: 'small scar above right eyebrow',
  clothing: ['blue hoodie', 'black jeans', 'white sneakers'],
  backpack: 'black backpack with grey stripe',
};

const lastSeen = {
  date: '2026-09-23',
  time: '18:10',
  timeZone: 'Asia/Kolkata',
  location: 'Riverfront Park, Ahmedabad',
  circumstances: 'Not supplied',
};

const caseNumber = 'MP-2026-0042';

export const caseData = {
  caseNumber,
  status: 'Active Investigation',
  createdDate: null, // Not supplied in the canonical case.
  investigatingUnit: 'Demo Investigation Desk',
  personProfile,
  lastSeen,
  tips: [
    { tipId: 'T001', dateTime: '2026-09-23T18:15:00+05:30', source: 'Mock park visitor', description: 'Reported a person in a blue hoodie near the park exit; face not visible.' },
    { tipId: 'T002', dateTime: '2026-09-23T18:25:00+05:30', source: 'Mock kiosk attendant', description: 'Reported a blue hoodie, black jeans and a striped black backpack on the riverfront walkway.' },
    { tipId: 'T003', dateTime: '2026-09-23T18:40:00+05:30', source: 'Mock commuter', description: 'Reported a person with a black backpack near a bus stop; clothing details unavailable.' },
    { tipId: 'T004', dateTime: '2026-09-23T19:00:00+05:30', source: 'Mock shop attendant', description: 'Reported a blue top and dark trousers on a nearby market road; backpack appeared red.' },
    { tipId: 'T005', dateTime: '2026-09-23T19:20:00+05:30', source: 'Mock driver', description: 'Reported a passenger in a dark jacket; exact boarding location not recorded.' },
    { tipId: 'T006', dateTime: '2026-09-23T19:35:00+05:30', source: 'Mock pedestrian', description: 'Reported white sneakers near a footbridge; no other description available.' },
    { tipId: 'T007', dateTime: '2026-09-23T20:00:00+05:30', source: 'Mock security attendant', description: 'Reported a person with a light shirt near a station entrance; observation was brief.' },
    { tipId: 'T008', dateTime: '2026-09-24T08:10:00+05:30', source: 'Mock caller', description: 'Reported a blue hoodie the next morning; location and time are approximate.' },
  ],
  cctvSightings: [
    { sightingId: 'C001', location: 'Riverfront Park exit', dateTime: '2026-09-23T18:16:00+05:30', description: 'Blue upper garment visible; face obscured by camera angle.' },
    { sightingId: 'C002', location: 'Riverfront bus stop', dateTime: '2026-09-23T18:42:00+05:30', description: 'Person carrying a dark backpack; clothing and physical details unclear.' },
    { sightingId: 'C003', location: 'Riverfront walkway', dateTime: '2026-09-23T18:27:00+05:30', description: 'Blue hoodie, black jeans and white shoes; estimated medium build. Backpack stripe unclear.' },
    { sightingId: 'C004', location: 'Nearby market road', dateTime: '2026-09-23T19:03:00+05:30', description: 'Blue top and dark trousers; reddish bag visible in low light.' },
    { sightingId: 'C005', location: 'Footbridge approach', dateTime: '2026-09-23T19:37:00+05:30', description: 'White footwear visible in a partial frame; upper body out of view.' },
    { sightingId: 'C006', location: 'Station entrance', dateTime: '2026-09-23T20:04:00+05:30', description: 'Light shirt visible; face and identifying marks cannot be assessed.' },
  ],
  // Display-only values. No frontend correlation, scoring or ranking.
  leads: [
    {
      leadId: 'L001', rank: 1, title: 'Potential sighting on riverfront walkway',
      sourceRecordIds: ['T002', 'C003'], score: 70,
      scoreBreakdown: { name: 0, location: 25, time: 20, clothing: 15, physical: 10 },
      priority: 'high',
      matchingEvidence: ['Reported location is near the last known location.', 'Descriptions mention a blue hoodie and black jeans.'],
      conflictingEvidence: ['No explicit conflict recorded in these mock descriptions.'],
      uncertainty: 'medium',
      recommendedNextAction: 'Review the original footage and verify the witness account independently.',
    },
    {
      leadId: 'L002', rank: 2, title: 'Potential sighting near riverfront bus stop',
      sourceRecordIds: ['T003', 'C002'], score: 45,
      scoreBreakdown: { name: 0, location: 25, time: 15, clothing: 5, physical: 0 },
      priority: 'medium',
      matchingEvidence: ['Both descriptions place a person with a dark backpack near the bus stop.'],
      conflictingEvidence: ['No explicit conflict recorded; clothing details are incomplete.'],
      uncertainty: 'high',
      recommendedNextAction: 'Verify the observation time and request clearer footage for investigator review.',
    },
    {
      leadId: 'L003', rank: 3, title: 'Potential sighting on nearby market road',
      sourceRecordIds: ['T004', 'C004'], score: 25,
      scoreBreakdown: { name: 0, location: 10, time: 10, clothing: 5, physical: 0 },
      priority: 'low',
      matchingEvidence: ['Descriptions mention a blue top and dark trousers.'],
      conflictingEvidence: ['Reported reddish bag differs from the supplied black backpack with grey stripe.'],
      uncertainty: 'high',
      recommendedNextAction: 'Clarify the bag description with the source before pursuing this potential lead.',
    },
  ],
  publicAppeal: {
    heading: 'PUBLIC APPEAL',
    status: 'Generated Draft',
    draftStatus: 'Generated',
    reviewStatus: 'Required',
    publicationStatus: 'Not Approved',
    reviewNotice: 'Requires Officer Review Before Publication',
    // Static mock copy, composed here from canonical fields to avoid drift.
    text: `PUBLIC APPEAL\n\nCase Number: ${caseNumber}\n\n${personProfile.name}, age ${personProfile.age}, was last seen at ${lastSeen.location} on ${lastSeen.date} at ${lastSeen.time} (IST).\n\nPhysical description: ${personProfile.heightCm} cm, ${personProfile.build} build, ${personProfile.hair} hair, ${personProfile.eyes} eyes; ${personProfile.identifyingMark}.\n\nLast known appearance: ${personProfile.clothing.join(', ')}; ${personProfile.backpack}.\n\nAnyone with information may contact the Demo Investigation Desk at +91-00000-00000 and quote the case number.\n\nFictional demonstration only. Requires Officer Review Before Publication.`,
    contact: { name: 'Demo Investigation Desk', phone: '+91-00000-00000' },
  },
  recommendedActions: [
    'Verify source accounts and timestamps before acting on potential leads.',
    'Review original footage associated with the prioritized source records.',
    'Record investigator findings and unresolved conflicts in the case file.',
  ],
  limitations: [
    'Analysis is based only on supplied records.',
    'CCTV records are descriptive observations and do not establish identity.',
    'Lead prioritization provides decision support only.',
    'All potential leads require investigator verification.',
    'Incomplete or inaccurate source information may affect results.',
  ],
};
