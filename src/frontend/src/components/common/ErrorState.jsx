import { InlineNotification } from '@carbon/react';
import Button from './Button.jsx';
export default function ErrorState({ message, onRetry }) {
  return <div className="py-3">
    <InlineNotification kind="error" title="Unable to load" subtitle={message} hideCloseButton lowContrast />
    {onRetry && <Button variant="secondary" onClick={onRetry} className="mt-4">Try again</Button>}
  </div>;
}
