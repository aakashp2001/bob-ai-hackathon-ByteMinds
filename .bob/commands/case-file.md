# case-file

For the supplied case number:

1. Call `get_case_data` once.
2. Call `get_correlation_results` once.
3. Return a structured case file with: Case Information, Subject Details, Physical Description, Clothing / Last Known Appearance, Last Known Information, Investigator Tips, CCTV Sightings, Prioritised Investigative Leads, Recommended Follow-up Actions, and Data Limitations / Uncertainty.
4. Keep source records separate from Bob-generated analysis.
5. Every lead must include its backend `sourceRecordIds` and unchanged numeric `score`.
6. Never claim that a CCTV sighting confirms identity.
