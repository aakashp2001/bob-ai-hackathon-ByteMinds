import { useEffect, useState } from 'react';
import { ButtonLink } from '../components/common/Button.jsx';
import PageHeader from '../components/common/PageHeader.jsx';
import LeadCard from '../components/leads/LeadCard.jsx';
import SectionCard from '../components/common/SectionCard.jsx';
import LoadingState from '../components/common/LoadingState.jsx';
import ErrorState from '../components/common/ErrorState.jsx';
import EmptyState from '../components/common/EmptyState.jsx';
import { getLeads } from '../services/api.js';

export default function LeadAnalysis({ caseData }) {
  const [leads, setLeads] = useState([]);
  const [status, setStatus] = useState('loading');
  const [attempt, setAttempt] = useState(0);
  const dashboardPath = `/case/${caseData.caseNumber}`;

  useEffect(() => {
    let active = true;
    async function loadLeads() {
      setStatus('loading');
      try {
        const result = await getLeads();
        if (!Array.isArray(result)) throw new Error('Expected a lead array');
        if (active) {
          setLeads(result);
          setStatus('ready');
        }
      } catch {
        if (active) setStatus('error');
      }
    }
    loadLeads();
    return () => { active = false; };
  }, [attempt, caseData.caseNumber]);

  return (
    <div className="space-y-5">
      <PageHeader title="Lead Analysis" caseData={caseData} actions={<ButtonLink to={dashboardPath}>Back to Case Dashboard</ButtonLink>} />

      <div className="rounded border border-slate-200 border-l-4 border-l-[#547996] bg-white px-5 py-4">
        <p className="text-sm leading-6 text-slate-700">Potential leads are based on correlation of available records and require independent investigator verification.</p>
        <p className="mt-2 text-xs leading-5 text-slate-500">Investigative Priority Scores support case triage only and do not establish identity.</p>
      </div>

      {status === 'loading' && <SectionCard title="Potential leads"><LoadingState message="Loading lead analysis..." /></SectionCard>}
      {status === 'error' && <SectionCard title="Potential leads"><ErrorState message="Unable to load lead analysis." onRetry={() => setAttempt((value) => value + 1)} /></SectionCard>}
      {status === 'ready' && (leads.length === 0 ? (
        <SectionCard title="Potential leads">
          <EmptyState message="No prioritized leads available yet." description="Run case analysis from the Case Dashboard to generate investigative leads.">
            <ButtonLink to={dashboardPath} className="mt-4">Go to Case Dashboard</ButtonLink>
          </EmptyState>
        </SectionCard>
      ) : (
        <>
          <p className="text-xs text-slate-500"><span className="font-semibold text-slate-700">{leads.length} potential leads</span> · Supplied mock results · Investigator Review Required</p>
          {/* The service supplies rank order. Preserve its array and rank values. */}
          <div className="space-y-5">{leads.map((lead) => <LeadCard key={lead.leadId} lead={lead} />)}</div>
        </>
      ))}
    </div>
  );
}
