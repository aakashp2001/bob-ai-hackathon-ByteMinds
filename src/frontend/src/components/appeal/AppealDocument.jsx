export default function AppealDocument({ appeal, caseNumber, personProfile }) {
  // Format the supplied text as paragraphs. Render its opening heading once;
  // do not summarize, rewrite, or supplement the provided public message.
  const paragraphs = appeal.text.split(/\n\s*\n/);
  const hasOpeningHeading = paragraphs[0]?.trim() === appeal.heading;
  const bodyParagraphs = hasOpeningHeading ? paragraphs.slice(1) : paragraphs;

  return (
    <article aria-labelledby="appeal-document-heading" className="appeal-document mx-auto w-full max-w-[210mm] border border-slate-300 bg-white px-6 py-8 shadow-sm sm:px-10 sm:py-10 lg:px-12">
      <header className="appeal-document-header border-b-2 border-[#193b5b] pb-6">
        <div className="flex flex-wrap justify-between gap-2 text-[11px] font-medium uppercase tracking-wider text-slate-500">
          <p>Fictional demonstration notice</p>
          <p>Case Reference: <span className="font-mono">{caseNumber}</span></p>
        </div>
        <h2 id="appeal-document-heading" className="mt-7 text-center text-2xl font-semibold tracking-[0.12em] text-[#193b5b]">{appeal.heading || 'Public Appeal'}</h2>
        <p className="mt-5 text-center text-3xl font-semibold tracking-tight text-slate-900">{personProfile.name}</p>
        <p className="mt-2 text-center text-sm text-slate-600">Age: {personProfile.age}</p>
      </header>

      <dl className="appeal-document-status my-5 grid gap-3 border-b border-slate-200 pb-5 text-xs sm:grid-cols-3">
        {[
          ['Draft Status', appeal.draftStatus],
          ['Review', appeal.reviewStatus],
          ['Publication', appeal.publicationStatus],
        ].map(([label, value]) => (
          <div key={label}>
            <dt className="text-slate-500">{label}</dt>
            <dd className="mt-1 font-semibold text-slate-800">{value || 'Not supplied'}</dd>
          </div>
        ))}
      </dl>

      <section aria-labelledby="public-message-heading" className="appeal-message">
        <h3 id="public-message-heading" className="text-xs font-semibold uppercase tracking-wider text-slate-600">Public Message</h3>
        <div className="mt-4 space-y-4 font-serif text-base leading-7 text-slate-800">
          {bodyParagraphs.map((paragraph, index) => <p key={index} className="whitespace-pre-line break-words">{paragraph}</p>)}
        </div>
      </section>

      <footer className="appeal-document-footer mt-7 border-t border-slate-300 pt-5">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-600">Contact</h3>
        <p className="mt-2 text-sm font-semibold text-slate-800">{appeal.contact?.name || 'Not supplied'}</p>
        <p className="mt-1 font-mono text-base text-[#193b5b]">{appeal.contact?.phone || 'Not supplied'}</p>
        <p className="mt-4 text-xs font-semibold text-slate-700">{appeal.reviewNotice || 'Review status not supplied.'}</p>
        <p className="mt-1 text-xs leading-5 text-slate-500">Source: Verified case-profile information · Fictional demo data</p>
      </footer>
    </article>
  );
}
