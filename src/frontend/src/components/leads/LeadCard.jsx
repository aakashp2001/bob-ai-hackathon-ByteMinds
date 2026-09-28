import { useId } from 'react';
import PriorityBadge from './PriorityBadge.jsx';
import ScoreBreakdown from './ScoreBreakdown.jsx';
import EvidenceList from './EvidenceList.jsx';

export default function LeadCard({ lead }) {
  const headingId = useId();

  return (
    <article aria-labelledby={headingId} className="min-w-0 overflow-hidden rounded-lg border border-slate-200 bg-white">
      <div className="flex flex-col gap-5 border-b border-slate-200 p-5 lg:flex-row lg:justify-between">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-3">
            <span className="text-xs font-semibold text-slate-600">#{lead.rank} Potential Lead</span>
            <span className="rounded border border-slate-200 bg-slate-50 px-2 py-0.5 font-mono text-xs text-slate-600">{lead.leadId}</span>
          </div>
          <h2 id={headingId} className="mt-3 break-words text-lg font-semibold leading-7 text-slate-900">{lead.title}</h2>
          <div className="mt-3 flex flex-wrap items-center gap-2">
            <span className="mr-1 text-xs text-slate-500">Source Records</span>
            {lead.sourceRecordIds?.length ? lead.sourceRecordIds.map((id, index) => (
              <span key={`${id}-${index}`} className="max-w-full break-all rounded border border-slate-200 px-2 py-0.5 font-mono text-xs text-slate-700">{id}</span>
            )) : <span className="text-xs text-slate-500">Not supplied</span>}
          </div>
        </div>
        <div className="shrink-0 lg:w-60 lg:border-l lg:border-slate-200 lg:pl-5">
          <p className="text-xs font-medium text-slate-600">Investigative Priority Score</p>
          <p className="mb-2 mt-1 text-3xl font-semibold tabular-nums tracking-tight text-[#193b5b]">{lead.score ?? 'Not supplied'} <span className="text-base font-normal text-slate-500">/ 100</span></p>
          <PriorityBadge priority={lead.priority} />
        </div>
      </div>

      <div className="grid lg:grid-cols-[190px_minmax(0,1fr)]">
        <div className="border-b border-slate-200 bg-slate-50/70 p-5 lg:border-b-0 lg:border-r">
          <ScoreBreakdown breakdown={lead.scoreBreakdown} />
        </div>
        <div className="min-w-0 p-5">
          <div className="grid gap-6 xl:grid-cols-2">
            <EvidenceList title="Matching Evidence" type="matching" items={lead.matchingEvidence} />
            <EvidenceList title="Conflicting Evidence" type="conflicting" items={lead.conflictingEvidence} />
          </div>
          <div className="mt-5 border-t border-slate-100 pt-4">
            <div className="flex flex-wrap items-center gap-3">
              <h3 className="text-xs font-semibold text-slate-800">Uncertainty</h3>
              <span className="rounded border border-slate-200 bg-slate-50 px-2 py-0.5 text-xs font-medium capitalize text-slate-700">{lead.uncertainty || 'Not supplied'}</span>
            </div>
            <p className="mt-2 text-xs leading-5 text-slate-600">Requires investigator verification.</p>
            <p className="mt-1 text-xs leading-5 text-slate-500">Uncertainty reflects limitations in the available source records.</p>
          </div>
        </div>
      </div>

      <div className="border-t border-slate-200 bg-[#f5f8fb] px-5 py-4">
        <h3 className="text-xs font-semibold text-[#193b5b]">Recommended Next Action</h3>
        <p className="mt-2 whitespace-pre-line break-words text-sm leading-6 text-slate-700">{lead.recommendedNextAction || 'No recommended next action supplied.'}</p>
      </div>
    </article>
  );
}
