import Button, { ButtonLink } from '../components/common/Button.jsx';
import PageHeader from '../components/common/PageHeader.jsx';
import EmptyState from '../components/common/EmptyState.jsx';
import { provided } from '../utils/formatters.js';
import CaseInfoCard from '../components/case/CaseInfoCard.jsx';
import EvidenceSummary from '../components/case/EvidenceSummary.jsx';
import AnalysisStatus from '../components/case/AnalysisStatus.jsx';
import SectionCard from '../components/common/SectionCard.jsx';
import { analyzeCase } from '../services/api.js';

export default function CaseDashboard({ caseData, analysisStatus, setAnalysisStatus }) {
  const { personProfile, tips, cctvSightings, leads } = caseData;
  const isAnalyzing = analysisStatus === 'analyzing';
  const physicalDetails = [
    ['Height', personProfile.heightCm == null ? null : `${personProfile.heightCm} cm`],
    ['Build', personProfile.build],
    ['Hair', personProfile.hair],
    ['Eyes', personProfile.eyes],
  ];
  const clothing = [...(Array.isArray(personProfile.clothing) ? personProfile.clothing : []), ...(personProfile.backpack ? [personProfile.backpack] : [])];

  async function handleAnalyze() {
    if (isAnalyzing) return;
    setAnalysisStatus('analyzing');
    try {
      const result = await analyzeCase();
      if (result.status !== 'complete') throw new Error('Analysis did not complete');
      setAnalysisStatus('complete');
    } catch {
      setAnalysisStatus('error');
    }
  }

  return (
    <div className="space-y-5">
      <PageHeader title="Case Dashboard" caseData={caseData} context="Case overview and investigative records" actions={
        <span className="inline-flex items-center gap-2 rounded border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700">
          <span aria-hidden="true" className="h-1.5 w-1.5 rounded-full bg-[#356784]" />
          {provided(caseData.status)}
        </span>
      } />

      <CaseInfoCard caseData={caseData} />
      <EvidenceSummary tips={tips} cctvSightings={cctvSightings} leads={leads} />

      <div className="grid items-start gap-5 xl:grid-cols-[1.2fr_1fr]">
        <SectionCard title="Subject / Last Known Appearance">
          <h3 className="text-xs font-semibold text-slate-700">Physical Description</h3>
          <dl className="mt-3 grid grid-cols-2 gap-x-5 gap-y-3 sm:grid-cols-4 xl:grid-cols-2 2xl:grid-cols-4">
            {physicalDetails.map(([label, value]) => (
              <div key={label}>
                <dt className="text-xs text-slate-500">{label}</dt>
                <dd className="mt-1 break-words text-sm text-slate-800 first-letter:uppercase">{provided(value)}</dd>
              </div>
            ))}
          </dl>
          <dl className="mt-4">
            <dt className="text-xs text-slate-500">Identifying Mark</dt>
            <dd className="mt-1 break-words text-sm leading-6 text-slate-800 first-letter:uppercase">{provided(personProfile.identifyingMark)}</dd>
          </dl>
          <div className="mt-5 border-t border-slate-100 pt-4">
            <h3 className="text-xs font-semibold text-slate-700">Clothing &amp; belongings</h3>
            {clothing.length ? <ul className="mt-3 grid list-inside list-disc gap-2 text-sm text-slate-700 marker:text-slate-400 sm:grid-cols-2 xl:grid-cols-1 2xl:grid-cols-2">
              {clothing.map((item, index) => <li key={index} className="break-words first-letter:uppercase">{item}</li>)}
            </ul> : <EmptyState message="No last known appearance details provided." />}
          </div>
        </SectionCard>

        <SectionCard title="Case analysis" action={<AnalysisStatus status={analysisStatus} />}>
          <p className="text-sm leading-6 text-slate-600">Review the supplied records to surface potential leads for investigator review.</p>
          <p className="mt-2 text-xs leading-5 text-slate-500">Demo workflow · Uses the provided mock analysis results.</p>

          <div className="mt-5 flex flex-wrap gap-3">
            <Button onClick={handleAnalyze} disabled={isAnalyzing}>
              {isAnalyzing ? 'Analysis in progress...' : 'Analyze Case'}
            </Button>
            {analysisStatus === 'complete' && (
              <ButtonLink to={`/case/${caseData.caseNumber}/leads`}>
                View Lead Analysis <span aria-hidden="true" className="ml-2">→</span>
              </ButtonLink>
            )}
          </div>

          <div role="status" aria-live="polite" aria-atomic="true" className="mt-3 min-h-6 text-sm leading-6">
            {analysisStatus === 'idle' && <p className="text-slate-500">Ready to analyze the supplied records.</p>}
            {isAnalyzing && <p className="text-slate-600">Analysis in progress...</p>}
            {analysisStatus === 'complete' && <p className="font-medium text-emerald-800">Analysis complete</p>}
            {analysisStatus === 'error' && <p className="text-red-800">Unable to analyze the case. Please try again.</p>}
          </div>

          <div className="mt-4 border-t border-slate-100 pt-4 text-xs leading-5 text-slate-500">
            <p>Analysis provides investigative decision support and requires investigator verification.</p>
            <p className="mt-2">The system does not establish identity. Potential leads require independent investigator verification.</p>
          </div>
        </SectionCard>
      </div>
    </div>
  );
}
