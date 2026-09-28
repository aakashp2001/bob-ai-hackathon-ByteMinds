import { useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';

export default function PageHeader({ title, caseData, context, actions, className = '' }) {
  const headingRef = useRef(null);
  const { pathname } = useLocation();

  useEffect(() => {
    document.title = `${title} | Missing Person Investigation Assistant`;
    // Do not reset scroll for in-page Case File anchors.
    if (!window.location.hash) window.scrollTo(0, 0);
    headingRef.current?.focus({ preventScroll: true });
  }, [pathname, title]);

  return (
    <div className={`flex flex-wrap items-start justify-between gap-4 ${className}`}>
      <div className="min-w-0">
        <h1 ref={headingRef} tabIndex={-1} className="page-heading text-2xl font-semibold tracking-tight text-slate-900">{title}</h1>
        <p className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-sm leading-6 text-slate-500">
          <span>Case: <span className="break-all font-mono text-slate-700">{caseData.caseNumber}</span></span>
          <span>Subject: <span className="break-words font-medium text-slate-700">{caseData.personProfile.name || 'Not provided'}</span></span>
        </p>
        {context && <p className="mt-2 text-xs text-slate-500">{context}</p>}
      </div>
      {actions && <div className="flex max-w-full flex-wrap items-center gap-3">{actions}</div>}
    </div>
  );
}
