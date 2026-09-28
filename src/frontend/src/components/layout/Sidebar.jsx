import { NavLink } from 'react-router-dom';
import { Dashboard, Analytics, Bullhorn, Document } from '@carbon/react/icons';

const navigation = [
  { label: 'Case Dashboard', path: '', icon: Dashboard },
  { label: 'Lead Analysis', path: '/leads', icon: Analytics },
  { label: 'Public Appeal', path: '/public-appeal', icon: Bullhorn },
  { label: 'Case File', path: '/case-file', icon: Document },
];

export default function Sidebar({ caseNumber }) {
  return (
    <aside className="app-sidebar flex flex-col bg-[#122337] text-slate-200 md:sticky md:top-0 md:h-dvh md:w-56 md:shrink-0 md:overflow-y-auto lg:w-60">
      <div className="shrink-0 border-b border-white/10 px-6 py-5 lg:py-7">
        <div aria-hidden="true" className="mb-5 flex h-9 w-9 items-center justify-center rounded border border-slate-500 text-sm font-semibold">MP</div>
        <p className="text-lg font-semibold tracking-tight text-white">Missing Person</p>
        <p className="mt-1 text-xs text-slate-400">Investigation Assistant</p>
      </div>
      <div className="px-6 pb-3 pt-6 text-[10px] font-semibold tracking-[0.18em] text-slate-400">CASE WORKSPACE</div>
      <nav aria-label="Main navigation" className="grid shrink-0 grid-cols-2 gap-1 px-3 pb-5 md:grid-cols-1">
        {navigation.map(({ label, path, icon: Icon }) => (
          <NavLink key={label} to={`/case/${caseNumber}${path}`} end={path === ''}
            className={({ isActive }) => `flex items-center gap-3 rounded px-3 py-3 text-sm ${isActive ? 'bg-[#263d55] font-semibold text-white shadow-[inset_3px_0_0_#81b3db]' : 'text-slate-300 hover:bg-white/5 hover:text-white'}`}>
            <Icon size={20} aria-hidden="true" className="shrink-0" />
            {label}
          </NavLink>
        ))}
      </nav>
      <div className="mx-6 mb-6 shrink-0 border-t border-white/10 pt-5 md:mt-auto">
        <p className="text-xs text-slate-400">Current Case</p>
        <p className="mt-2 font-mono text-sm font-medium text-white">{caseNumber}</p>
        <p className="mt-4 text-[11px] text-slate-400">IBM Bob Hackathon · Prototype</p>
      </div>
    </aside>
  );
}
