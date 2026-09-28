import { useEffect, useState } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import Sidebar from './components/layout/Sidebar.jsx';
import Header from './components/layout/Header.jsx';
import CaseDashboard from './pages/CaseDashboard.jsx';
import LeadAnalysis from './pages/LeadAnalysis.jsx';
import PublicAppeal from './pages/PublicAppeal.jsx';
import CaseFile from './pages/CaseFile.jsx';
import { getCase } from './services/api.js';
import SectionCard from './components/common/SectionCard.jsx';
import LoadingState from './components/common/LoadingState.jsx';
import ErrorState from './components/common/ErrorState.jsx';
import EmptyState from './components/common/EmptyState.jsx';
import Button from './components/common/Button.jsx';

export default function App() {
  const [caseData, setCaseData] = useState(null);
  const [status, setStatus] = useState('loading');
  const [attempt, setAttempt] = useState(0);
  // Keep workflow status during route changes; a browser refresh starts a new demo session.
  const [analysisStatus, setAnalysisStatus] = useState('idle');

  useEffect(() => {
    let active = true;
    setStatus('loading');
    getCase().then((data) => {
      if (data != null && (!data.caseNumber || !data.personProfile || !data.lastSeen)) throw new Error('Incomplete case structure');
      if (active) { setCaseData(data); setStatus('ready'); }
    }).catch(() => { if (active) setStatus('error'); });
    return () => { active = false; };
  }, [attempt]);

  if (status !== 'ready' || !caseData) return (
    <main className="mx-auto max-w-2xl px-6 py-12">
      <h1 className="mb-5 text-2xl font-semibold text-slate-900">Missing Person Investigation Assistant</h1>
      <SectionCard title="Case workspace">
        {status === 'loading' && <LoadingState message="Loading case information..." />}
        {status === 'error' && <ErrorState message="Unable to load case information." onRetry={() => setAttempt((value) => value + 1)} />}
        {status === 'ready' && <EmptyState message="Case information is not available yet." description="Try loading the case again."><Button variant="secondary" className="mt-4" onClick={() => setAttempt((value) => value + 1)}>Try again</Button></EmptyState>}
      </SectionCard>
    </main>
  );

  const casePath = `/case/${caseData.caseNumber}`;

  return (
    <div className="app-shell min-h-screen md:flex">
      <a href="#main-content" className="skip-link sr-only fixed left-4 top-4 z-50 rounded bg-white p-3 text-sm focus:not-sr-only">Skip to main content</a>
      <Sidebar caseNumber={caseData.caseNumber} />
      <div className="app-content flex min-w-0 flex-1 flex-col">
        <Header caseNumber={caseData.caseNumber} />
        <main id="main-content" tabIndex={-1} className="mx-auto w-full max-w-7xl flex-1 px-6 py-8 outline-none lg:px-9">
          <Routes>
            <Route path={casePath} element={<CaseDashboard caseData={caseData} analysisStatus={analysisStatus} setAnalysisStatus={setAnalysisStatus} />} />
            <Route path={`${casePath}/leads`} element={<LeadAnalysis caseData={caseData} />} />
            <Route path={`${casePath}/public-appeal`} element={<PublicAppeal caseData={caseData} />} />
            <Route path={`${casePath}/case-file`} element={<CaseFile caseData={caseData} />} />
            <Route path="*" element={<Navigate to={casePath} replace />} />
          </Routes>
        </main>
        <footer className="app-footer border-t border-slate-200 px-6 py-4 text-xs leading-5 text-slate-500 lg:px-9">Analysis provides investigative decision support. Potential leads require independent investigator verification.</footer>
      </div>
    </div>
  );
}
