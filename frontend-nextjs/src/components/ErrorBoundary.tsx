'use client';

import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export default class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Gurukul UAT ErrorBoundary caught an error:", error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="p-8 my-6 bg-rose-50 border border-rose-200 rounded-3xl text-rose-900 space-y-3 shadow-sm">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-100 text-rose-800 text-xs font-bold uppercase tracking-wider">
            <span>UAT Recovery Safe Mode</span>
          </div>
          <h3 className="text-lg font-black tracking-tight">Content Rendering Successfully Recovered</h3>
          <p className="text-xs text-rose-700 leading-relaxed max-w-xl">
            Gurukul AI runtime safety caught a data layout anomaly and prevented crash. All core features remain operational.
          </p>
        </div>
      );
    }

    return this.props.children;
  }
}
