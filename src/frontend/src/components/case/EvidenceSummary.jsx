export default function EvidenceSummary({ tips, cctvSightings, leads }) {
  const summaries = [
    { label: 'Investigator Tips', value: Array.isArray(tips) ? tips.length : 'Not provided', description: 'Supplied tip records' },
    { label: 'CCTV Records', value: Array.isArray(cctvSightings) ? cctvSightings.length : 'Not provided', description: 'Descriptive observations' },
    { label: 'Prioritized Leads', value: Array.isArray(leads) ? leads.length : 'Not provided', description: 'Provided mock leads' },
  ];

  return (
    <section aria-labelledby="evidence-summary-heading">
      <h2 id="evidence-summary-heading" className="sr-only">Evidence summary</h2>
      <dl className="grid gap-4 sm:grid-cols-3">
        {summaries.map(({ label, value, description }) => (
          <div key={label} className="rounded-lg border border-slate-200 bg-white px-5 py-4">
            <dt className="text-xs font-medium text-slate-600">{label}</dt>
            <dd className={`mt-2 font-semibold tabular-nums tracking-tight text-slate-900 ${typeof value === 'number' ? 'text-3xl' : 'text-sm'}`}>{value}</dd>
            <dd className="mt-2 text-xs leading-5 text-slate-500">{description}</dd>
          </div>
        ))}
      </dl>
    </section>
  );
}
