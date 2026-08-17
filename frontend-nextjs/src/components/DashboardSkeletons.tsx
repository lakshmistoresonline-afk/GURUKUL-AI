import React from 'react';

export function HeaderSkeleton() {
  return (
    <div className="space-y-4 animate-pulse px-4">
      <div className="h-4 w-32 bg-slate-200 rounded-full" />
      <div className="h-12 w-96 bg-slate-200 rounded-2xl" />
    </div>
  );
}

export function NextStepSkeleton() {
  return (
    <div className="h-48 bg-slate-100 rounded-[40px] animate-pulse" />
  );
}

export function MissionSkeleton() {
  return (
    <div className="space-y-6 p-10 bg-white border border-slate-100 rounded-[40px] animate-pulse">
       <div className="h-8 w-64 bg-slate-100 rounded-xl" />
       <div className="space-y-3">
          {[1,2,3].map(i => <div key={i} className="h-16 bg-slate-50 rounded-2xl" />)}
       </div>
    </div>
  );
}

export function CardSkeleton() {
  return (
    <div className="h-64 bg-white border border-slate-100 rounded-[40px] animate-pulse shadow-sm" />
  );
}
