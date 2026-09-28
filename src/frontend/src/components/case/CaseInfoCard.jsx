import SectionCard from '../common/SectionCard.jsx';
import { formatDate, provided } from '../../utils/formatters.js';

export default function CaseInfoCard({ caseData }) {
  const { caseNumber, personProfile, lastSeen } = caseData;
  const formattedDate = formatDate(lastSeen.date);

  return (
    <SectionCard title="Case information">
      <dl className="grid gap-x-6 gap-y-5 sm:grid-cols-3">
        <div>
          <dt className="text-xs text-slate-500">Case Number</dt>
          <dd className="mt-1.5 font-mono text-sm font-semibold text-slate-800">{caseNumber}</dd>
        </div>
        <div>
          <dt className="text-xs text-slate-500">Subject Name</dt>
          <dd className="mt-1 break-words text-lg font-semibold text-slate-900">{provided(personProfile.name)}</dd>
        </div>
        <div>
          <dt className="text-xs text-slate-500">Age</dt>
          <dd className="mt-1.5 text-sm font-medium text-slate-800">{personProfile.age == null ? 'Not provided' : `${personProfile.age} years`}</dd>
        </div>
      </dl>
      <dl className="mt-5 grid gap-x-6 gap-y-5 border-t border-slate-100 pt-5 sm:grid-cols-2">
        <div>
          <dt className="text-xs text-slate-500">Last Known Location</dt>
          <dd className="mt-1.5 break-words text-sm font-medium leading-6 text-slate-800">{provided(lastSeen.location)}</dd>
        </div>
        <div>
          <dt className="text-xs text-slate-500">Last Known Date/Time</dt>
          <dd className="mt-1.5 text-sm font-medium leading-6 text-slate-800">{formattedDate}, {provided(lastSeen.time)}{lastSeen.timeZone && <span className="ml-1 font-normal text-slate-500">({lastSeen.timeZone === 'Asia/Kolkata' ? 'IST' : lastSeen.timeZone})</span>}</dd>
        </div>
      </dl>
    </SectionCard>
  );
}
