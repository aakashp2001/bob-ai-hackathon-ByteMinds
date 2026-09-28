import { Tag } from '@carbon/react';
const priorities = {
  high: { label: 'High Investigative Priority', type: 'warm-gray' },
  medium: { label: 'Medium Investigative Priority', type: 'blue' },
  low: { label: 'Low Investigative Priority', type: 'gray' },
};
export default function PriorityBadge({ priority }) {
  const badge = priorities[priority] ?? { label: 'Investigative Priority Not Supplied', type: 'gray' };
  return <Tag type={badge.type} size="md">{badge.label}</Tag>;
}
