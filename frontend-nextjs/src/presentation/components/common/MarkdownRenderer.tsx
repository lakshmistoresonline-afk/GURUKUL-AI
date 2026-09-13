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
      className={`prose max-w-none prose-slate prose-p:text-slate-700 prose-headings:font-black prose-strong:text-slate-900 ${className}`}
    >
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          p: ({ children, ...props }) => (
            <p {...props}>{children}</p>
          ),
          li: ({ children, ...props }) => (
            <li {...props}>{children}</li>
          ),
          ul: ({ children, ...props }) => (
            <ul {...props}>{children}</ul>
          ),
          ol: ({ children, ...props }) => (
            <ol {...props}>{children}</ol>
          ),
          table: ({ children, ...props }) => (
            <table {...props}>{children}</table>
          ),
          tbody: ({ children, ...props }) => (
            <tbody {...props}>{children}</tbody>
          ),
          tr: ({ children, ...props }) => (
            <tr {...props}>{children}</tr>
          ),
          td: ({ children, ...props }) => (
            <td {...props}>{children}</td>
          ),
          th: ({ children, ...props }) => (
            <th {...props}>{children}</th>
          ),
        }}
      >
        {displayContent}
      </ReactMarkdown>
    </div>
  );
};
