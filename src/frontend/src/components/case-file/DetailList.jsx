import { provided } from '../../utils/formatters.js';

export default function DetailList({ fields }) {
  return (
    <dl className="grid gap-x-8 gap-y-5 sm:grid-cols-2 xl:grid-cols-3">
      {fields.map(({ label, value }) => (
        <div key={label} className="min-w-0">
          <dt className="text-xs text-slate-500">{label}</dt>
          <dd className="mt-1.5 whitespace-pre-line break-words text-sm font-medium leading-6 text-slate-800 first-letter:uppercase">{provided(value)}</dd>
        </div>
      ))}
    </dl>
  );
}
