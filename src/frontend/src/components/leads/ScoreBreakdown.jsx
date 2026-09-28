// Display denominators from the supplied contract, not scoring rules.
const fields = [
  ['name', 'Name', 30],
  ['location', 'Location', 25],
  ['time', 'Time', 20],
  ['clothing', 'Clothing', 15],
  ['physical', 'Physical', 10],
];

export default function ScoreBreakdown({ breakdown }) {
  return (
    <div>
      <h3 className="text-xs font-semibold text-slate-800">Score Breakdown</h3>
      <dl className="mt-3 divide-y divide-slate-200/70 text-sm">
        {fields.map(([key, label, maximum]) => (
          <div key={key} className="flex items-baseline justify-between gap-4 py-2">
            <dt className="text-slate-600">{label}</dt>
            <dd className="font-medium tabular-nums text-slate-800">{breakdown?.[key] ?? 'Not supplied'} <span className="font-normal text-slate-500">/ {maximum}</span></dd>
          </div>
        ))}
      </dl>
      <p className="mt-3 text-xs leading-5 text-slate-500">Provided values · Display only</p>
    </div>
  );
}
