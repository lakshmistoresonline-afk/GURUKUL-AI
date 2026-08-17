'use client';

import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface FormattedTextProps {
  content: string;
  className?: string;
}

/**
 * A kid-friendly markdown renderer that handles AI-generated text formatting.
 * Optimized for high readability, contrast, and Hindi character support.
 */
export default function FormattedText({ content, className = '' }: FormattedTextProps) {
  if (!content) return null;

  // Pre-process common AI formatting quirks
  let processedContent = content
    .replace(/\*\s\*\*/g, '\n* **') // Ensure bullets start on new lines
    .replace(/(\d+)\.\s\*\*/g, '\n$1. **'); // Ensure numbered lists start on new lines

  // AGGRESSIVE Hindi character spacing fix
  // This removes all spaces that occur immediately before or after a Hindi vowel sign (matra)
  // or a halant, ensuring characters like 'धक्का' don't render as 'ध क -का'
  processedContent = processedContent
    // Remove spaces between consonants and vowel signs
    .replace(/([\u0905-\u0939])\s+([\u093E-\u094D])/g, '$1$2')
    // Remove spaces between vowel signs and other characters (aggressive join)
    .replace(/([\u093E-\u094D])\s+([\u0905-\u0939])/g, '$1$2');

  const isInverted = className.includes('prose-invert');

  return (
    <div className={`prose max-w-none transition-all duration-300
      ${isInverted
        ? 'prose-invert prose-p:text-slate-50 prose-li:text-slate-50 prose-strong:text-white prose-headings:text-white prose-blockquote:border-primary prose-blockquote:text-slate-200'
        : 'prose-slate prose-p:text-slate-800 prose-li:text-slate-800 prose-strong:text-slate-950 prose-headings:text-slate-900'}
      prose-p:leading-[1.8] prose-p:text-2xl md:prose-p:text-3xl
      prose-li:text-2xl md:prose-li:text-3xl
      prose-strong:font-black
      prose-headings:font-black
      prose-img:rounded-[40px]
      ${className}`}>
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        {processedContent}
      </ReactMarkdown>
    </div>
  );
}
