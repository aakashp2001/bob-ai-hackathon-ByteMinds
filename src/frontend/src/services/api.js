const API_BASE_URL = "http://127.0.0.1:8000";

async function fetchJSON(path) {
  const res = await fetch(`${API_BASE_URL}${path}`);
  if (!res.ok) throw new Error(`API ${path} failed: ${res.status}`);
  return res.json();
}

function transformProfile(raw) {
  return {
    caseNumber: raw.caseNumber,
    status: 'Active Investigation',
    createdDate: null,
    investigatingUnit: 'Demo Investigation Desk',
    personProfile: {
      name: raw.name,
      age: raw.age,
      gender: 'Not supplied',
      heightCm: raw.physicalDescription.heightCm,
      build: raw.physicalDescription.build,
      hair: raw.physicalDescription.hairColor,
      eyes: raw.physicalDescription.eyeColor,
      identifyingMark: (raw.physicalDescription.identifyingMarks || [])[0] || null,
      clothing: [raw.clothing.top, raw.clothing.bottom, raw.clothing.footwear].filter(Boolean),
      backpack: raw.clothing.backpack,
    },
    lastSeen: {
      date: raw.lastSeen.dateTime.split('T')[0],
      time: raw.lastSeen.dateTime.split('T')[1]?.slice(0, 5),
      timeZone: 'Asia/Kolkata',
      location: raw.lastSeen.location,
      circumstances: 'Not supplied',
    },
    contact: raw.contact || { name: 'Demo Investigation Desk', phone: '+91-00000-00000' },
  };
}

export async function getCase() {
  const profile = await fetchJSON('/case');
  const tips = await fetchJSON('/tips');
  const cctv = await fetchJSON('/cctv');
  const analysis = await fetchJSON('/analyze');

  const transformed = transformProfile(profile);
  transformed.tips = tips;
  transformed.cctvSightings = cctv;
  transformed.leads = analysis.leads;
  transformed.recommendedActions = [
    'Verify source accounts and timestamps before acting on potential leads.',
    'Review original footage associated with the prioritized source records.',
    'Record investigator findings and unresolved conflicts in the case file.',
  ];
  transformed.limitations = [
    'Analysis is based only on supplied records.',
    'CCTV records are descriptive observations and do not establish identity.',
    'Lead prioritization provides decision support only.',
    'All potential leads require investigator verification.',
    'Incomplete or inaccurate source information may affect results.',
  ];

  const p = transformed.personProfile;
  const ls = transformed.lastSeen;
  transformed.publicAppeal = {
    heading: 'PUBLIC APPEAL',
    status: 'Generated Draft',
    draftStatus: 'Generated',
    reviewStatus: 'Required',
    publicationStatus: 'Not Approved',
    reviewNotice: 'Requires Officer Review Before Publication',
    text: `PUBLIC APPEAL\n\nCase Number: ${transformed.caseNumber}\n\n${p.name}, age ${p.age}, was last seen at ${ls.location} on ${ls.date} at ${ls.time} (IST).\n\nPhysical description: ${p.heightCm} cm, ${p.build} build, ${p.hair} hair, ${p.eyes} eyes; ${p.identifyingMark}.\n\nLast known appearance: ${p.clothing.join(', ')}; ${p.backpack}.\n\nAnyone with information may contact the Demo Investigation Desk at +91-00000-00000 and quote the case number.\n\nFictional demonstration only. Requires Officer Review Before Publication.`,
    contact: transformed.contact,
  };

  return transformed;
}

export async function analyzeCase() {
  const data = await fetchJSON('/analyze');
  return { status: 'complete', leads: data.leads };
}


export async function getLeads() {
  const data = await fetchJSON('/analyze');
  return data.leads;
}

export async function getPublicAppeal() {
  const caseInfo = await getCase();
  return caseInfo.publicAppeal;
}

export async function getCaseFile() {
  return getCase();
}
