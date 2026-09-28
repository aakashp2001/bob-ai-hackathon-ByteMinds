export default function EvidenceList({ title, items, type }) {
  const isConflict = type === 'conflicting';
  const emptyMessage = isConflict
    ? 'No conflicting evidence recorded in the available structured data.'
    : 'No matching evidence recorded in the available structured data.';

  return (
    <div>
      <h3 className="text-xs font-semibold text-slate-800">{title}</h3>
      {!Array.isArray(items) ? (
        <p className="mt-3 text-sm leading-6 text-slate-500">Evidence data not supplied.</p>
      ) : items.length === 0 ? (
        <p className="mt-3 text-sm leading-6 text-slate-500">{emptyMessage}</p>
      ) : (
        <ul className="mt-3 space-y-3 text-sm leading-6 text-slate-600">
          {items.map((item, index) => (
            <li key={`${index}-${item}`} className="flex items-start gap-2.5">
              <span aria-hidden="true" className={`mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full ${isConflict ? 'bg-amber-600' : 'bg-[#4d7975]'}`} />
              <span className="min-w-0 whitespace-pre-line break-words">{item}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
