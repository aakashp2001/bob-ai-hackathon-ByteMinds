import PriorityBadge from '../leads/PriorityBadge.jsx';
import RecordTable from './RecordTable.jsx';
import { provided } from '../../utils/formatters.js';

const columns = [
  { key: 'rank', label: 'Rank', width: 'w-16', render: (lead) => lead.rank == null ? 'Not provided' : `#${lead.rank}` },
  { key: 'leadId', label: 'Lead ID', width: 'w-20' },
  { key: 'title', label: 'Lead Title' },
  { key: 'score', label: 'Investigative Priority Score', width: 'w-32', render: (lead) => <span className="font-semibold tabular-nums text-slate-800">{provided(lead.score)} / 100</span> },
  { key: 'priority', label: 'Priority', width: 'w-40', render: (lead) => <PriorityBadge priority={lead.priority} /> },
  { key: 'sourceRecordIds', label: 'Source Record IDs', width: 'w-28', render: (lead) => (
    <div className="flex flex-wrap gap-1.5">{lead.sourceRecordIds?.length ? lead.sourceRecordIds.map((id, index) => <span key={`${id}-${index}`} className="max-w-full break-all rounded border border-slate-200 bg-slate-50 px-1.5 font-mono text-xs leading-6 text-slate-700">{id}</span>) : 'Not provided'}</div>
  ) },
  { key: 'uncertainty', label: 'Uncertainty', width: 'w-28', render: (lead) => <span className="capitalize">{provided(lead.uncertainty)}</span> },
];

export default function LeadSummaryTable({ leads }) {
  // Preserve the supplied array order and rank values without recalculation.
  return <RecordTable caption="Prioritized investigative leads" records={leads} columns={columns} rowKey="leadId" emptyMessage="No prioritized leads available." wide />;
}
