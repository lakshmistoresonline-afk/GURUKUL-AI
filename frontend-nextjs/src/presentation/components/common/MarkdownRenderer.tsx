import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

import { sanitizeStudentContent } from '@/core/utils/sanitizer';

interface MarkdownRendererProps {
  content: string;
  className?: string;
  sanitize?: boolean;
}

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({
  content,
  className = "",
  sanitize = true
}) => {
  if (!content) return null;

  const stringContent =
    typeof content === 'string'
      ? content
      : JSON.stringify(content, null, 2);

  const displayContent = sanitize
    ? sanitizeStudentContent(stringContent)
    : stringContent;

  return (
    <div
      className={`prose max-w-none prose-slate prose-p:text-slate-800 prose-p:leading-relaxed prose-headings:font-bold prose-strong:text-slate-900 prose-table:w-full prose-table:overflow-x-auto ${className}`}
    >
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          p: ({ children, ...props }) => (
            <p className="text-base sm:text-lg leading-relaxed text-slate-800 my-2" {...props}>{children}</p>
          ),
          li: ({ children, ...props }) => (
            <li className="text-base sm:text-lg leading-relaxed text-slate-800 my-1" {...props}>{children}</li>
          ),
          ul: ({ children, ...props }) => (
            <ul className="list-disc list-inside my-2 space-y-1 text-slate-800" {...props}>{children}</ul>
          ),
          ol: ({ children, ...props }) => (
            <ol className="list-decimal list-inside my-2 space-y-1 text-slate-800" {...props}>{children}</ol>
          ),
          table: ({ children, ...props }) => (
            <div className="overflow-x-auto my-4 border border-slate-200 rounded-2xl shadow-sm">
              <table className="min-w-full divide-y divide-slate-200 text-sm sm:text-base text-left text-slate-800" {...props}>{children}</table>
            </div>
          ),
          tbody: ({ children, ...props }) => (
            <tbody className="divide-y divide-slate-100 bg-white" {...props}>{children}</tbody>
          ),
          tr: ({ children, ...props }) => (
            <tr className="hover:bg-slate-50 transition-colors" {...props}>{children}</tr>
          ),
          td: ({ children, ...props }) => (
            <td className="px-4 py-3 font-medium text-slate-800" {...props}>{children}</td>
          ),
          th: ({ children, ...props }) => (
            <th className="px-4 py-3 font-bold bg-slate-100 text-slate-900 uppercase text-xs tracking-wider" {...props}>{children}</th>
          ),
        }}
      >
        {displayContent}
      </ReactMarkdown>
    </div>
  );
};
