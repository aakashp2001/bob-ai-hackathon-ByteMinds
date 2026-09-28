import { useId } from 'react';
import { Tile } from '@carbon/react';

export default function SectionCard({ title, children, action, className = '', id }) {
  const headingId = useId();

  return (
    <section id={id} aria-labelledby={headingId} className={`case-section ${className}`}>
      <Tile className="case-tile">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 px-5 py-4">
        <h2 id={headingId} className="text-sm font-semibold text-slate-900">{title}</h2>
        {action}
      </div>
      <div className="p-5">{children}</div>
      </Tile>
    </section>
  );
}
