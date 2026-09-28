import { useEffect, useState } from 'react';
import Button, { ButtonLink } from '../components/common/Button.jsx';
import PageHeader from '../components/common/PageHeader.jsx';
import AppealDocument from '../components/appeal/AppealDocument.jsx';
import SectionCard from '../components/common/SectionCard.jsx';
import LoadingState from '../components/common/LoadingState.jsx';
import ErrorState from '../components/common/ErrorState.jsx';
import EmptyState from '../components/common/EmptyState.jsx';
import { getPublicAppeal } from '../services/api.js';

export default function PublicAppeal({ caseData }) {
  const [appeal, setAppeal] = useState(null);
  const [status, setStatus] = useState('loading');
  const [attempt, setAttempt] = useState(0);
  const [copyStatus, setCopyStatus] = useState('idle');
  const [printError, setPrintError] = useState(false);
  const casePath = `/case/${caseData.caseNumber}`;

  useEffect(() => {
    let active = true;
    async function loadAppeal() {
      setStatus('loading');
      setCopyStatus('idle');
      setPrintError(false);
      try {
        const result = await getPublicAppeal();
        if (active) {
          setAppeal(result);
          setStatus('ready');
        }
      } catch {
        if (active) setStatus('error');
      }
    }
    loadAppeal();
    return () => { active = false; };
  }, [attempt, caseData.caseNumber]);

  useEffect(() => {
    if (copyStatus !== 'copied') return;
    const timer = setTimeout(() => setCopyStatus('idle'), 3000);
    return () => clearTimeout(timer);
  }, [copyStatus]);

  const hasDraft = status === 'ready' && typeof appeal?.text === 'string' && appeal.text.trim().length > 0;

  async function copyText() {
    if (!hasDraft || copyStatus === 'copying') return;
    setCopyStatus('copying');
    try {
      await navigator.clipboard.writeText(appeal.text);
      setCopyStatus('copied');
    } catch {
      setCopyStatus('error');
    }
  }

  function printAppeal() {
    setPrintError(false);
    try {
      window.print();
    } catch {
      setPrintError(true);
    }
  }

  return (
    <div className="public-appeal-page space-y-5">
      <PageHeader title="Public Appeal" caseData={caseData} className="appeal-screen-only" actions={<ButtonLink to={`${casePath}/leads`}>Back to Lead Analysis</ButtonLink>} />

      <div className="appeal-screen-only border-l-4 border-amber-300 bg-amber-50/60 px-5 py-4">
        <p className="text-sm font-semibold text-amber-950">Requires Officer Review Before Publication</p>
        <p className="mt-2 text-xs leading-5 text-slate-600">This draft is generated from verified case-profile information only and must be reviewed before public release.</p>
      </div>

      {status === 'loading' && <SectionCard title="Public appeal draft"><LoadingState message="Loading public appeal..." /></SectionCard>}
      {status === 'error' && <SectionCard title="Public appeal draft"><ErrorState message="Unable to load the public appeal draft." onRetry={() => setAttempt((value) => value + 1)} /></SectionCard>}
      {status === 'ready' && !hasDraft && <SectionCard title="Public appeal draft"><EmptyState message="Public appeal draft is not available yet." description="Generate the case analysis before preparing the public appeal."><ButtonLink to={casePath} className="mt-4">Go to Case Dashboard</ButtonLink></EmptyState></SectionCard>}

      {hasDraft && (
        <>
          <div className="appeal-screen-only flex flex-wrap items-center justify-between gap-3">
            <span className="rounded border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700">{appeal.status || 'Status not supplied'}</span>
            <div className="flex flex-wrap items-center gap-3">
              <Button variant="secondary" onClick={copyText} disabled={copyStatus === 'copying'}>{copyStatus === 'copying' ? 'Copying...' : 'Copy Text'}</Button>
              <Button onClick={printAppeal}>Print</Button>
            </div>
          </div>
          <div role="status" aria-live="polite" aria-atomic="true" className="appeal-screen-only min-h-6 text-sm leading-6">
            {copyStatus === 'copied' && <p className="text-emerald-800">Appeal text copied</p>}
            {copyStatus === 'error' && <p className="text-slate-700">Unable to copy the appeal text. Select the public message and copy it manually.</p>}
            {printError && <p className="text-slate-700">Unable to open printing. Try your browser’s Print command.</p>}
          </div>
          <AppealDocument appeal={appeal} caseNumber={caseData.caseNumber} personProfile={caseData.personProfile} />
        </>
      )}
    </div>
  );
}
