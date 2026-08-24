'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import {
  signInWithEmailAndPassword,
  signInWithPopup,
  GoogleAuthProvider,
  createUserWithEmailAndPassword
} from 'firebase/auth';
import { auth, db } from '@/lib/firebase';
import { doc, setDoc, getDoc } from 'firebase/firestore';
import {
  GraduationCap, Mail, Lock, ArrowRight,
  AlertTriangle, Sparkles, RefreshCw
} from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { motion } from 'framer-motion';

export default function LoginPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();

  const [email, setEmail] = useState('student@gurukul.ai');
  const [password, setPassword] = useState('password123');
  const [authError, setAuthError] = useState('');
  const [isAuthenticating, setIsAuthenticating] = useState(false);

  // Simple Redirect after login
  useEffect(() => {
    if (!authLoading && user) {
      router.replace('/dashboard');
    }
  }, [user, authLoading, router]);

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsAuthenticating(true);
    setAuthError('');

    try {
      let userCredential;
      try {
        userCredential = await signInWithEmailAndPassword(auth, email, password);
      } catch (authErr: any) {
        if (authErr.code === 'auth/user-not-found' || authErr.code === 'auth/invalid-credential') {
          userCredential = await createUserWithEmailAndPassword(auth, email, password);
        } else {
          throw authErr;
        }
      }

      const loggedUser = userCredential.user;

      // Ensure Firestore record exists (Bootstrap if needed)
      const userRef = doc(db, 'users', loggedUser.uid);
      const userSnap = await getDoc(userRef);

      if (!userSnap.exists()) {
        await setDoc(userRef, {
          uid: loggedUser.uid,
          email: loggedUser.email,
          name: email.split('@')[0],
          role: 'student',
          classId: '5', // Default for new users
          xp: 0,
          badges: [],
          createdAt: new Date().toISOString(),
        });
      }

      router.push('/dashboard');
    } catch (err: any) {
      console.error("Login Error:", err);
      setAuthError(err.message || 'Authentication failed');
      setIsAuthenticating(false);
    }
  };

  const handleGoogleLogin = async () => {
    try {
      const provider = new GoogleAuthProvider();
      await signInWithPopup(auth, provider);
    } catch (err: any) {
      setAuthError(err.message || 'Google login failed');
    }
  };

  if (authLoading) {
    return (
       <div className="min-h-screen bg-slate-50 flex items-center justify-center font-black text-slate-400 uppercase tracking-widest text-[10px]">
          Initializing Hub...
       </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#F8FAFC] flex items-center justify-center p-6 relative overflow-hidden">

      {/* Background Ornaments */}
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-primary/5 rounded-full blur-[120px] -mr-64 -mt-64" />
      <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-indigo-500/5 rounded-full blur-[120px] -ml-64 -mb-64" />

      <div className="max-w-md w-full space-y-8 relative z-10">
        <header className="text-center space-y-4">
          <motion.div
            initial={{ scale: 0.5, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="inline-flex items-center justify-center w-20 h-20 bg-primary rounded-[32px] text-white mb-2 shadow-2xl shadow-primary/20"
          >
            <GraduationCap size={40} />
          </motion.div>
          <div className="space-y-1">
            <h1 className="text-3xl font-black text-slate-900 tracking-tight">Gurukul AI</h1>
            <p className="text-slate-500 font-bold uppercase tracking-[0.2em] text-[10px]">Your Intelligent Classroom</p>
          </div>
        </header>

        <div className="bg-white p-10 rounded-[48px] border border-slate-200/60 shadow-2xl shadow-slate-200/50">
          <div className="space-y-8">
            <div className="space-y-2">
              <h2 className="text-2xl font-black text-slate-900">Welcome Back</h2>
              <p className="text-slate-500 font-medium text-sm">Sign in to start your learning journey.</p>
            </div>

            <form onSubmit={handleAuth} className="space-y-5">
              <div className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-[10px] font-black uppercase tracking-widest text-slate-400 ml-1">Email Address</label>
                  <div className="relative">
                    <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="w-full pl-12 pr-4 py-4 bg-slate-50 border border-slate-100 rounded-2xl focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all font-bold text-slate-700"
                      placeholder="student@gurukul.ai"
                      required
                    />
                  </div>
                </div>

                <div className="space-y-1.5">
                  <label className="text-[10px] font-black uppercase tracking-widest text-slate-400 ml-1">Password</label>
                  <div className="relative">
                    <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                    <input
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="w-full pl-12 pr-4 py-4 bg-slate-50 border border-slate-100 rounded-2xl focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all font-bold text-slate-700"
                      placeholder="••••••••"
                      required
                    />
                  </div>
                </div>
              </div>

              {authError && (
                <div className="p-4 bg-red-50 border border-red-100 rounded-2xl flex gap-3 text-red-600 text-xs font-bold leading-relaxed">
                  <AlertTriangle size={18} className="shrink-0" />
                  <p>{authError}</p>
                </div>
              )}

              <button
                type="submit"
                disabled={isAuthenticating}
                className="w-full bg-primary text-white py-5 rounded-2xl font-black text-xs uppercase tracking-widest hover:bg-blue-700 transition-all shadow-xl shadow-primary/20 active:scale-[0.98] disabled:opacity-50 flex items-center justify-center gap-3"
              >
                {isAuthenticating ? 'Verifying...' : 'Sign In to Hub'}
                {!isAuthenticating && <ArrowRight size={16} />}
              </button>
            </form>

            <div className="relative flex items-center justify-center">
              <div className="w-full border-t border-slate-100" />
              <span className="bg-white px-4 text-[10px] font-black text-slate-300 uppercase tracking-widest absolute">Or Quick Access</span>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <button
                onClick={handleGoogleLogin}
                className="flex items-center justify-center gap-3 py-4 bg-white border border-slate-200 rounded-2xl hover:bg-slate-50 transition-all shadow-sm group"
              >
                <Image src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" width={18} height={18} alt="Google" />
                <span className="text-[10px] font-black uppercase tracking-widest text-slate-600 group-hover:text-slate-900">Google</span>
              </button>
              <button
                onClick={() => router.push('/dashboard')}
                className="flex items-center justify-center gap-3 py-4 bg-slate-50 border border-slate-100 rounded-2xl hover:bg-slate-100 transition-all group"
              >
                <Sparkles size={16} className="text-indigo-500" />
                <span className="text-[10px] font-black uppercase tracking-widest text-slate-600 group-hover:text-slate-900">Guest</span>
              </button>
            </div>
          </div>
        </div>

        <p className="text-center text-slate-400 text-sm font-medium">
          Don&apos;t have an account? <span className="text-primary font-bold cursor-pointer hover:underline">Register now</span>
        </p>
      </div>
    </div>
  );
}
