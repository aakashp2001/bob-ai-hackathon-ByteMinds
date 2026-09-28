import { Tag } from '@carbon/react';
export default function Header({ caseNumber }) {
  return (
    <header className="app-header flex min-h-16 flex-wrap items-center justify-between gap-3 border-b border-slate-200 bg-white px-6 py-4 lg:px-9">
      <p className="text-xs text-slate-500">Case workspace <span aria-hidden="true" className="mx-3 text-slate-300">/</span><span className="font-mono font-medium text-slate-700">{caseNumber}</span></p>
      <Tag type="gray" size="sm">Fictional demo data</Tag>
    </header>
  );
}
