'use client';

import React from 'react';
import Link from 'next/link';
import { ChevronRight, Home } from 'lucide-react';

interface BreadcrumbItem {
  label: string;
  href: string;
}

export default function Breadcrumbs({ items }: { items: BreadcrumbItem[] }) {
  return (
    <nav className="flex items-center gap-3 text-xs font-bold uppercase tracking-wider text-slate-500 mb-8">
      <Link href="/dashboard" className="hover:text-blue-600 transition-colors flex items-center gap-1.5">
        <Home size={14} />
      </Link>
      {items.map((item, i) => (
        <React.Fragment key={item.href}>
          <ChevronRight size={12} className="text-slate-300" />
          <Link
            href={item.href}
            className={`hover:text-blue-600 transition-colors ${i === items.length - 1 ? 'text-slate-900 font-black' : ''}`}
          >
            {item.label}
          </Link>
        </React.Fragment>
      ))}
    </nav>
  );
}
