import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ButtonLink } from '../components/common/Button.jsx';
import PageHeader from '../components/common/PageHeader.jsx';
import SectionCard from '../components/common/SectionCard.jsx';
import LoadingState from '../components/common/LoadingState.jsx';
import ErrorState from '../components/common/ErrorState.jsx';
import EmptyState from '../components/common/EmptyState.jsx';
import DetailList from '../components/case-file/DetailList.jsx';
import RecordTable from '../components/case-file/RecordTable.jsx';
import LeadSummaryTable from '../components/case-file/LeadSummaryTable.jsx';
import { provided, formatDate, formatRecordTime } from '../utils/formatters.js';
import { getCaseFile } from '../services/api.js';

const sections = [
  ['case-information', 'Case Information'], ['subject-details', 'Subject'],
  ['physical-description', 'Physical Description'], ['appearance', 'Clothing'],
  ['last-known', 'Last Known'], ['investigator-tips', 'Tips'],
  ['cctv-sightings', 'CCTV'], ['investigative-leads', 'Leads'],
  ['follow-up-actions', 'Actions'], ['data-limitations', 'Limitations'],
];

export default function CaseFile({ caseData }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('loading');
  const [attempt, setAttempt] = useState(0);
  const casePath = `/case/${caseData.caseNumber}`;

  useEffect(() => {
    let active = true;
    async function loadFile() {
      setStatus('loading');
      try {
        const result = await getCaseFile();
        if (result != null && (typeof result !== 'object' || Array.isArray(result))) throw new Error('Expected a structured case file');
        if (active) {
          setFile(result);
          setStatus('ready');
        }
      } catch {
        if (active) setStatus('error');
      }
    }
    loadFile();
    return () => { active = false; };
  }, [attempt, caseData.caseNumber]);

  const profile = file?.personProfile ?? {};
  const lastSeen = file?.lastSeen ?? {};
  const clothing = [...(Array.isArray(profile.clothing) ? profile.clothing : []), ...(profile.backpack ? [profile.backpack] : [])];
  const recordTimeColumn = {
    key: 'dateTime', label: 'Date / Time', width: 'w-40',
    render: (record) => formatRecordTime(record.dateTime, lastSeen.timeZone),
  };
  const tipColumns = [
    { key: 'tipId', label: 'Tip ID', width: 'w-20' }, recordTimeColumn,
    { key: 'source', label: 'Source', width: 'w-40' },
    { key: 'description', label: 'Description' },
  ];
  const cctvColumns = [
    { key: 'sightingId', label: 'Sighting ID', width: 'w-24' },
    { key: 'location', label: 'Camera / Location', width: 'w-40' }, recordTimeColumn,
    { key: 'description', label: 'CCTV Sighting Description' },
  ];

  return (
    <div className="min-w-0 space-y-5">
      <PageHeader title="Case File" caseData={caseData} context="Structured Investigation Record" actions={<>
          <span className="rounded border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700">{provided(file?.status ?? caseData.status)}</span>
          <ButtonLink to={casePath}>Back to Case Dashboard</ButtonLink>
      </>} />
      <p className="border-l-4 border-[#547996] bg-white px-5 py-3 text-sm leading-6 text-slate-600">All potential leads require independent investigator verification.</p>

      {status === 'loading' && <SectionCard title="Investigation record"><LoadingState message="Loading case file..." /></SectionCard>}
      {status === 'error' && <SectionCard title="Investigation record"><ErrorState message="Unable to load the case file." onRetry={() => setAttempt((value) => value + 1)} /></SectionCard>}
      {status === 'ready' && !file && <SectionCard title="Investigation record"><EmptyState message="Case file is not available yet." /></SectionCard>}

      {status === 'ready' && file && (
        <>
          <nav aria-label="On this page" className="rounded border border-slate-200 bg-white px-5 py-3">
            <p className="mb-2 text-xs font-semibold text-slate-600">On this page</p>
            <ul className="flex flex-wrap gap-x-5 gap-y-2 text-xs text-[#193b5b]">{sections.map(([id, label]) => <li key={id}><a href={`#${id}`} className="underline decoration-slate-300 underline-offset-4 hover:decoration-slate-600">{label}</a></li>)}</ul>
          </nav>

          <SectionCard id="case-information" title="01 · Case Information" className="scroll-mt-6">
            <DetailList fields={[
              { label: 'Case Number', value: file.caseNumber },
              { label: 'Created Date', value: formatDate(file.createdDate) },
              { label: 'Case Status', value: file.status },
              { label: 'Investigating Unit', value: file.investigatingUnit },
            ]} />
          </SectionCard>

          <SectionCard id="subject-details" title="02 · Subject Details" className="scroll-mt-6">
            <DetailList fields={[
              { label: 'Name', value: profile.name }, { label: 'Age', value: profile.age },
              ...(Object.hasOwn(profile, 'gender') ? [{ label: 'Gender', value: profile.gender }] : []),
            ]} />
          </SectionCard>

          <SectionCard id="physical-description" title="03 · Physical Description" className="scroll-mt-6">
            <DetailList fields={[
              { label: 'Height', value: profile.heightCm == null ? null : `${profile.heightCm} cm` },
              { label: 'Build', value: profile.build }, { label: 'Hair', value: profile.hair },
              { label: 'Eyes', value: profile.eyes }, { label: 'Identifying Mark', value: profile.identifyingMark },
            ]} />
          </SectionCard>

          <SectionCard id="appearance" title="04 · Clothing / Last Known Appearance" className="scroll-mt-6">
            {clothing.length ? <ul className="grid list-disc gap-x-8 gap-y-2 pl-5 text-sm leading-6 text-slate-700 marker:text-slate-400 sm:grid-cols-2">{clothing.map((item, index) => <li key={index} className="break-words first-letter:uppercase">{item}</li>)}</ul> : <EmptyState message="No last known appearance details provided." />}
          </SectionCard>

          <SectionCard id="last-known" title="05 · Last Known Information" className="scroll-mt-6">
            <DetailList fields={[
              { label: 'Date', value: formatDate(lastSeen.date) }, { label: 'Time', value: lastSeen.time },
              { label: 'Time Zone', value: lastSeen.timeZone },
              { label: 'Location', value: lastSeen.location }, { label: 'Circumstances', value: lastSeen.circumstances },
            ]} />
          </SectionCard>

          <SectionCard id="investigator-tips" title="06 · Investigator Tips" className="min-w-0 scroll-mt-6" action={<span className="text-xs text-slate-500">{file.tips?.length ?? 0} records</span>}>
            {lastSeen.timeZone && <p className="mb-3 text-xs text-slate-500">Record times shown in {lastSeen.timeZone}. Descriptions are reproduced as supplied.</p>}
            <RecordTable caption="Investigator tips" records={file.tips} columns={tipColumns} rowKey="tipId" emptyMessage="No investigator tips recorded." />
          </SectionCard>

          <SectionCard id="cctv-sightings" title="07 · CCTV Sightings" className="min-w-0 scroll-mt-6" action={<span className="text-xs text-slate-500">{file.cctvSightings?.length ?? 0} records</span>}>
            <p className="mb-3 text-xs leading-5 text-slate-500">Recorded observations do not establish identity.{lastSeen.timeZone && ` Record times shown in ${lastSeen.timeZone}.`}</p>
            <RecordTable caption="CCTV sighting descriptions" records={file.cctvSightings} columns={cctvColumns} rowKey="sightingId" emptyMessage="No CCTV sighting descriptions recorded." />
          </SectionCard>

          <SectionCard id="investigative-leads" title="08 · Prioritized Investigative Leads" className="min-w-0 scroll-mt-6" action={<Link to={`${casePath}/leads`} className="text-xs font-semibold text-[#193b5b] underline underline-offset-4">View Lead Analysis</Link>}>
            <p className="mb-3 text-xs leading-5 text-slate-500">Potential leads are decision-support outputs and do not establish identity.</p>
            <LeadSummaryTable leads={file.leads} />
          </SectionCard>

          <SectionCard id="follow-up-actions" title="09 · Recommended Follow-up Actions" className="scroll-mt-6">
            {file.recommendedActions?.length ? <ol className="list-decimal space-y-3 pl-5 text-sm leading-6 text-slate-700 marker:font-semibold marker:text-slate-500">{file.recommendedActions.map((action, index) => <li key={index} className="whitespace-pre-line break-words pl-1">{action}</li>)}</ol> : <EmptyState message="No recommended follow-up actions available." />}
          </SectionCard>

          <SectionCard id="data-limitations" title="10 · Data Limitations & Verification Requirements" className="scroll-mt-6 border-l-4 border-l-[#547996]">
            {file.limitations?.length ? <ul className="list-disc space-y-2 pl-5 text-sm leading-6 text-slate-700 marker:text-slate-400">{file.limitations.map((limitation, index) => <li key={index} className="whitespace-pre-line break-words">{limitation}</li>)}</ul> : <EmptyState message="No data limitations provided." />}
          </SectionCard>
        </>
      )}
    </div>
  );
}
