'use client';

import React, { useState } from 'react';
import { createUserWithEmailAndPassword } from 'firebase/auth';
import { auth, db } from '@/lib/firebase';
import { doc, setDoc } from 'firebase/firestore';
import { ShieldCheck, UserPlus, AlertCircle, CheckCircle2, Loader2 } from 'lucide-react';

const SEED_USERS = [
  {
    email: 'srinavts2016@gmail.com',
    password: 'Gurukul@123',
    classId: '5',
    name: 'Srinav Class 5'
  },
  {
    email: 'tssrisha2015@gmail.com',
    password: 'Gurukul@123',
    classId: '6',
    name: 'Srisha Class 6'
  }
];

export default function SetupUsersPage() {
  const [status, setStatus] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [complete, setComplete] = useState(false);

  const runSeeding = async () => {
    setLoading(true);
    const results = [];

    for (const user of SEED_USERS) {
      try {
        // 1. Create Auth User
        const userCredential = await createUserWithEmailAndPassword(auth, user.email, user.password);
        const fbUser = userCredential.user;

        // 2. Create Firestore Profile
        await setDoc(doc(db, 'users', fbUser.uid), {
          uid: fbUser.uid,
          email: user.email,
          name: user.name,
          role: 'student',
          classId: user.classId,
          xp: 0,
          badges: [],
          createdAt: new Date().toISOString(),
        });

        results.push({ email: user.email, status: 'success', message: `Created Class ${user.classId} User` });
      } catch (error: any) {
        if (error.code === 'auth/email-already-in-use') {
          results.push({ email: user.email, status: 'info', message: 'User already exists in Firebase' });
        } else {
          results.push({ email: user.email, status: 'error', message: error.message });
        }
      }
    }

    setStatus(results);
    setLoading(false);
    setComplete(true);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center p-6">
      <div className="max-w-2xl w-full space-y-12">
        <div className="text-center space-y-4">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-primary/20 text-primary rounded-[32px] mb-6 border border-primary/20 shadow-glow shadow-primary/10">
            <ShieldCheck size={40} />
          </div>
          <h1 className="text-4xl font-black tracking-tight">System Initialization</h1>
          <p className="text-slate-400 font-medium">Populate Firebase Authentication and Firestore profiles for the Class 5 & 6 test users.</p>
        </div>

        <div className="bg-slate-900 border border-white/5 rounded-[48px] p-12 shadow-2xl">
          {!complete ? (
            <div className="space-y-10 text-center">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {SEED_USERS.map(u => (
                  <div key={u.email} className="p-6 bg-white/5 rounded-3xl border border-white/5 text-left space-y-2">
                    <p className="text-[10px] font-black text-primary uppercase tracking-widest">Class {u.classId} Profile</p>
                    <p className="font-bold text-slate-200 text-sm truncate">{u.email}</p>
                    <p className="text-[10px] text-slate-500 font-medium font-mono">Password: Gurukul@123</p>
                  </div>
                ))}
              </div>

              <button
                onClick={runSeeding}
                disabled={loading}
                className="w-full py-6 bg-primary text-white rounded-[24px] font-black uppercase tracking-widest text-xs hover:bg-blue-600 transition-all flex items-center justify-center gap-3 shadow-2xl shadow-primary/20 disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <Loader2 className="animate-spin" size={20} />
                    Initializing Records...
                  </>
                ) : (
                  <>
                    <UserPlus size={20} />
                    Start Population
                  </>
                )}
              </button>
            </div>
          ) : (
            <div className="space-y-8">
              <div className="space-y-4">
                {status.map((res, i) => (
                  <div key={i} className={`p-6 rounded-3xl border flex items-center gap-6 ${
                    res.status === 'success' ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' :
                    res.status === 'info' ? 'bg-blue-500/10 border-blue-500/20 text-blue-400' :
                    'bg-red-500/10 border-red-500/20 text-red-400'
                  }`}>
                    {res.status === 'success' ? <CheckCircle2 size={24} /> :
                     res.status === 'info' ? <CheckCircle2 size={24} /> :
                     <AlertCircle size={24} />}
                    <div className="flex-1 min-w-0">
                       <p className="font-black text-xs uppercase tracking-widest opacity-60 mb-1">{res.email}</p>
                       <p className="font-bold text-sm">{res.message}</p>
                    </div>
                  </div>
                ))}
              </div>

              <div className="pt-8 border-t border-white/5 flex flex-col gap-4">
                 <a href="/login" className="w-full py-5 bg-white text-slate-900 rounded-[24px] font-black uppercase tracking-widest text-xs text-center hover:bg-slate-100 transition-all">Go to Login</a>
                 <p className="text-center text-[10px] text-slate-500 font-bold uppercase tracking-[0.2em]">Population Cycle Complete</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
