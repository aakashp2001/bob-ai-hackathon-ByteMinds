export default function EmptyState({ message, description, children }) {
  return (
    <div className="py-3">
      <p className="text-sm font-semibold text-slate-800">{message}</p>
      {description && <p className="mt-2 text-sm leading-6 text-slate-500">{description}</p>}
      {children}
    </div>
  );
}
