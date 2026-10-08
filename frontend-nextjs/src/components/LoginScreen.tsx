'use client';

import React, { useState } from 'react';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../lib/firebase';

interface LoginScreenProps {
  onLoginSuccess: () => void;
}

export default function LoginScreen({ onLoginSuccess }: LoginScreenProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Strict production security: production mode NEVER permits demo auth regardless of public env overrides
  const isDevMode = process.env.NODE_ENV !== 'production' && (process.env.NODE_ENV === 'development' || process.env.NEXT_PUBLIC_ENABLE_DEMO_AUTH === 'true');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await signInWithEmailAndPassword(auth, email, password);
      onLoginSuccess();
    } catch (err: any) {
      setError('We couldn’t sign you in. Please check your email and password and try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDemoBypass = (role: string, classId: string, name: string, email: string) => {
    if (process.env.NODE_ENV === 'production') {
      setError('Demo authentication is disabled in production.');
      return;
    }
    const demoUser = { uid: 'demo-' + role, role, classId, name, email };
    localStorage.setItem('gurukul_demo_user', JSON.stringify(demoUser));
    onLoginSuccess();
    window.location.reload();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-950 via-slate-900 to-indigo-900 flex items-center justify-center p-4 selection:bg-indigo-500 selection:text-white">
      <div className="w-full max-w-md bg-white/15 backdrop-blur-2xl border border-white/20 rounded-3xl p-8 shadow-2xl space-y-6">
        <div className="text-center space-y-2">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-indigo-600/60 border border-indigo-400/40 text-indigo-200 text-xs font-bold uppercase tracking-wider">
            <span>Gurukul AI Portal</span>
          </div>
          <h2 className="text-3xl font-black text-white tracking-tight">Welcome Back</h2>
          <p className="text-indigo-200 text-xs">Sign in to access your class curriculum & study modules.</p>
        </div>

        {error && (
          <div className="p-4 bg-rose-500/20 border border-rose-500/40 rounded-2xl text-xs text-rose-200 font-bold space-y-1">
            <div>{error}</div>
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          <div className="space-y-1">
            <label className="text-xs font-bold text-indigo-200">Email Address</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="e.g. tssrisha2015@gmail.com"
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-2xl text-sm text-white placeholder-indigo-300 focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs font-bold text-indigo-200">Password</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-2xl text-sm text-white placeholder-indigo-300 focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 bg-indigo-600 hover:bg-indigo-500 text-white font-black text-xs uppercase tracking-wider rounded-2xl shadow-lg transition-all disabled:opacity-50"
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        {isDevMode && (
          <div className="pt-4 border-t border-white/10 space-y-3">
            <div className="text-[11px] font-bold text-indigo-300 uppercase tracking-widest text-center">🚀 Instant Demo Bypass Login (Dev Only)</div>
            <div className="grid grid-cols-1 gap-2">
              <button
                type="button"
                onClick={() => handleDemoBypass('student', '6', 'Srisha T S', 'tssrisha2015@gmail.com')}
                className="p-3 bg-indigo-600/40 hover:bg-indigo-600/60 border border-indigo-400/40 rounded-xl text-left text-xs text-white flex items-center justify-between transition-all"
              >
                <div>
                  <strong className="block text-white font-black">Login as Srisha T S (Class 6)</strong>
                  <span className="text-[10px] text-indigo-200">tssrisha2015@gmail.com</span>
                </div>
                <span className="text-[10px] bg-indigo-500 px-2.5 py-1 rounded-lg text-white font-bold">Class 6</span>
              </button>

              <button
                type="button"
                onClick={() => handleDemoBypass('student', '5', 'Srinav T S', 'tssrisha2015@gmail.com')}
                className="p-3 bg-teal-600/40 hover:bg-teal-600/60 border border-teal-400/40 rounded-xl text-left text-xs text-white flex items-center justify-between transition-all"
              >
                <div>
                  <strong className="block text-white font-black">Login as Srinav T S (Class 5)</strong>
                  <span className="text-[10px] text-teal-200">srinavts2016@gmail.com</span>
                </div>
                <span className="text-[10px] bg-teal-500 px-2.5 py-1 rounded-lg text-white font-bold">Class 5</span>
              </button>

              <button
                type="button"
                onClick={() => handleDemoBypass('admin', 'all', 'Admin', 'admin@gurukul.com')}
                className="p-3 bg-amber-600/40 hover:bg-amber-600/60 border border-amber-400/40 rounded-xl text-left text-xs text-white flex items-center justify-between transition-all"
              >
                <div>
                  <strong className="block text-white font-black">Login as Admin (All Classes)</strong>
                  <span className="text-[10px] text-amber-200">admin@gurukul.com</span>
                </div>
                <span className="text-[10px] bg-amber-500 px-2.5 py-1 rounded-lg text-white font-bold">Admin</span>
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
