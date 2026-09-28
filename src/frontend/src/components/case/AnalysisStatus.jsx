import { Tag } from '@carbon/react';
const labels = { idle: 'Not Analyzed', analyzing: 'Analyzing', complete: 'Analysis Complete', error: 'Analysis Failed' };
export default function AnalysisStatus({ status }) {
  return <Tag type={status === 'complete' ? 'green' : status === 'error' ? 'red' : 'gray'}>{labels[status]}</Tag>;
}
