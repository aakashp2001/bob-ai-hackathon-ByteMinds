import { InlineLoading } from '@carbon/react';
export default function LoadingState({ message = 'Loading...' }) {
  return <InlineLoading description={message} status="active" className="py-5" />;
}
