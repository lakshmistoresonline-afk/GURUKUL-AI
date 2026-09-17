import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

import { sanitizeStudentContent } from '@/core/utils/sanitizer';

interface MarkdownRendererProps {
  content: string;
  className?: string;
  sanitize?: boolean;
}

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content, className = "", sanitize = true }) => {
  if (!content) return null;
  const stringContent = typeof content === 'string' ? content : JSON.stringify(content, null, 2);
  const displayContent = sanitize ? sanitizeStudentContent(stringContent) : stringContent;

  return (
    <div className={`prose max-w-none prose-slate prose-p:text-slate-700 prose-headings:font-black prose-strong:text-slate-900 ${className}`}>
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        {displayContent}
      </ReactMarkdown>
    </div>
  );
};
