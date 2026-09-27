# analyse-case

For the supplied case number:

1. Call `get_case_data` once to retrieve the complete source context.
2. Call `get_correlation_results` once to retrieve deterministic backend results.
3. Do not call or recreate a scoring algorithm.
4. Produce JSON matching the `leadExplanations` shape in `src/bob/system-prompt.md`.
5. Copy every lead ID, score, sourceRecordIds, matchingEvidence, conflictingEvidence, and recommendedNextAction from the backend unchanged.
6. Add an investigative priority label and a plain-language explanation for each lead.
7. State uncertainty and limitations. Never claim identity confirmation.
