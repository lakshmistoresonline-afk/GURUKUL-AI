'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  signInWithEmailAndPassword,
  signInWithPopup,
  GoogleAuthProvider,
  createUserWithEmailAndPassword
} from 'firebase/auth';
import { auth, db } from '@/lib/firebase';
import { doc, setDoc, getDoc } from 'firebase/firestore';
import { GraduationCap, Mail, Lock, ArrowRight, AlertTriangle } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';

export default function LoginPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState('student@gurukul.ai');
  const [password, setPassword] = useState('password123');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  React.useEffect(() => {
    if (!authLoading && user) {
      router.replace('/dashboard');
    }
  }, [user, authLoading, router]);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // 1. Try to Login
      let userCredential;
      try {
        userCredential = await signInWithEmailAndPassword(auth, email, password);
      } catch (authErr: any) {
        // 2. If user doesn't exist, try to auto-create (Bootstrap mode)
        if (authErr.code === 'auth/user-not-found' || authErr.code === 'auth/invalid-credential') {
          // Note: Newer Firebase versions might not return user-not-found for security
          userCredential = await createUserWithEmailAndPassword(auth, email, password);
        } else {
          throw authErr;
        }
      }

      const user = userCredential.user;

      // 3. Ensure Firestore record exists (Update in Firestore)
      const userRef = doc(db, 'users', user.uid);
      const userSnap = await getDoc(userRef);

      if (!userSnap.exists()) {
        // Determine class based on email (Smart Bootstrap)
        let assignedClass = '5';
        if (email.toLowerCase().includes('2015')) assignedClass = '6';
        if (email.toLowerCase().includes('tssrisha')) assignedClass = '6';

        await setDoc(userRef, {
          uid: user.uid,
          email: user.email,
          name: email.split('@')[0],
          role: 'student',
          classId: assignedClass,
          xp: 0,
          badges: [],
          createdAt: new Date().toISOString(),
        });
      }

      router.push('/dashboard');
    } catch (err: any) {
      console.error("Login Error:", err);
      let msg = err.message;
      if (err.code === 'auth/configuration-not-found') {
        msg = "Firebase Authentication is not enabled. Please go to Firebase Console > Authentication and click 'Get Started'.";
      }
      setError(msg || 'Failed to login');
    } finally {
      setLoading(false);
    }
  };

  if (authLoading) {
     return (
        <div className="min-h-screen bg-slate-50 flex items-center justify-center font-black text-slate-400 uppercase tracking-widest text-[10px]">
           Checking credentials...
        </div>
     );
  }

  const handleGoogleLogin = async () => {
    try {
      const provider = new GoogleAuthProvider();
      await signInWithPopup(auth, provider);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Failed to login with Google');
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary rounded-2xl text-white mb-6 shadow-xl shadow-blue-200">
            <GraduationCap size={32} />
          </div>
          <h1 className="text-3xl font-black text-slate-900 tracking-tight">Welcome back</h1>
          <p className="text-slate-500 mt-2 font-medium">Continue your learning journey with Gurukul AI</p>
        </div>

        <div className="bg-white p-8 rounded-3xl border border-border shadow-xl shadow-slate-200/50">
          <form onSubmit={handleLogin} className="space-y-5">
            <div>
              <label className="block text-xs font-black uppercase tracking-widest text-slate-400 mb-2 px-1">Email Address</label>
              <div className="relative">
                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full pl-12 pr-4 py-3.5 bg-slate-50 border border-border rounded-2xl focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all font-medium text-slate-700"
                  placeholder="student@gurukul.ai"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-black uppercase tracking-widest text-slate-400 mb-2 px-1">Password</label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-12 pr-4 py-3.5 bg-slate-50 border border-border rounded-2xl focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all font-medium text-slate-700"
                  placeholder="••••••••"
                  required
                />
              </div>
            </div>

            {error && (
              <div className="p-4 bg-red-50 border border-red-100 rounded-2xl flex gap-3 text-red-600 text-xs font-bold leading-relaxed mb-4 animate-in fade-in zoom-in duration-300">
                <AlertTriangle size={18} className="flex-shrink-0" />
                <p>{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-primary text-white py-4 rounded-2xl font-black text-sm uppercase tracking-widest hover:bg-blue-700 transition-all shadow-lg shadow-blue-100 active:scale-[0.98] disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {loading ? 'Authenticating...' : 'Sign In to Hub'}
              {!loading && <ArrowRight size={16} />}
            </button>
          </form>

          <div className="mt-8 relative">
            <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-border"></div></div>
            <div className="relative flex justify-center text-xs uppercase font-black tracking-widest text-slate-400">
              <span className="bg-white px-4">Or Quick Start</span>
            </div>
          </div>

          <div className="mt-8 space-y-3">
             <button
                onClick={handleGoogleLogin}
                className="w-full bg-white border border-border text-slate-700 py-3.5 rounded-2xl font-bold text-sm hover:bg-slate-50 transition-all flex items-center justify-center gap-3"
             >
                <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" className="w-5 h-5" alt="Google" />
                Sign in with Google
             </button>

             <button
                onClick={() => router.push('/dashboard')}
                className="w-full bg-blue-50 text-primary py-3.5 rounded-2xl font-bold text-sm hover:bg-blue-100 transition-all flex items-center justify-center gap-2"
             >
                Enter as Guest Scholar
             </button>
          </div>
        </div>

        <p className="text-center text-slate-400 text-sm font-medium">
          Don&apos;t have an account? <span className="text-primary font-bold cursor-pointer hover:underline">Sign up now</span>
        </p>
      </div>
    </div>
  );
}
