import EmptyState from '../common/EmptyState.jsx';
import { Table, TableHead, TableBody, TableRow, TableCell } from '@carbon/react';
import { provided } from '../../utils/formatters.js';

export default function RecordTable({ caption, records, columns, rowKey, emptyMessage, wide = false }) {
  if (!records?.length) return <EmptyState message={emptyMessage} />;

  return (
    <div role="region" aria-label={`${caption} table — scroll horizontally if needed`} tabIndex={0} className="max-w-full overflow-x-auto rounded border border-slate-200">
      <Table size="lg" className={`case-record-table w-full table-fixed text-left text-sm ${wide ? 'min-w-[920px]' : 'min-w-[700px]'}`}>
        <caption className="sr-only">{caption}</caption>
        <TableHead>
          <tr>{columns.map((column) => <th key={column.key} scope="col" className={`px-4 py-3 font-semibold ${column.width || ''}`}>{column.label}</th>)}</tr>
        </TableHead>
        <TableBody>
          {records.map((record) => (
            <TableRow key={record[rowKey]} className="align-top">
              {columns.map((column) => {
                const content = column.render ? column.render(record) : provided(record[column.key]);
                return column.key === rowKey
                  ? <th key={column.key} scope="row" className="break-words px-4 py-4 font-mono text-xs font-medium leading-6 text-slate-800">{content}</th>
                  : <TableCell key={column.key} className="whitespace-pre-line break-words leading-6">{content}</TableCell>;
              })}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
