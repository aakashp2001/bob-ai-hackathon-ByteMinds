import { Button as CarbonButton } from '@carbon/react';
import { Link } from 'react-router-dom';
export default function Button({ variant = 'primary', type = 'button', ...props }) {
  return <CarbonButton type={type} kind={variant === 'secondary' ? 'tertiary' : 'primary'} size="md" {...props} />;
}
export function ButtonLink({ variant = 'secondary', ...props }) {
  return <CarbonButton as={Link} kind={variant === 'secondary' ? 'tertiary' : 'primary'} size="md" {...props} />;
}
