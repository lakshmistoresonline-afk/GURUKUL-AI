'use client';

import React, { useEffect, useState } from 'react';
import { useAuth } from '@/core/context/AuthContext';
import { Layout } from '@/presentation/components/common/Layout';
import { studentApi, Class, Subject } from '@/services/api/student_api';
import { GraduationCap, ArrowRight, Book, Layers, ShieldCheck, Zap, Target, HelpCircle, RefreshCw, Globe, ChevronRight, Search } from 'lucide-react';
import Link from 'next/link';

export default function HomePage() {
  const { user, login, register, resetPassword, loading: authLoading } = useAuth();
  const [classes, setClasses] = useState<Class[]>([]);
  const [selectedClass, setSelectedClass] = useState<Class | null>(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    if (searchQuery.length > 2) {
      setIsSearching(true);
      studentApi.search(searchQuery).then(res => {
        setSearchResults(res);
        setIsSearching(false);
      });
    } else {
      setSearchResults([]);
    }
  }, [searchQuery]);

  // Authentication form state
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [classId, setClassId] = useState('class_5');
  const [isRegistering, setIsRegistering] = useState(false);
  const [isResettingPassword, setIsResettingPassword] = useState(false);
  const [resetMessage, setResetMessage] = useState('');

  const [loginError, setLoginError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    studentApi.getClasses().then(data => {
      setClasses(data);
      setLoading(false);
      // Auto-select class based on user if logged in
      if (user) {
        const userClassId = user.class_id || (user.username.includes('6') ? 'class_6' : 'class_5');
        const found = data.find(c => c.id === userClassId);
        if (found) setSelectedClass(found);
      }
    }).catch(() => setLoading(false));
  }, [user]);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    setLoginError('');
    setResetMessage('');
    setSubmitting(true);

    try {
      if (isResettingPassword) {
        if (!email.trim()) {
          throw new Error('Please enter your email address.');
        }

        await resetPassword(email.trim());

        setResetMessage(
          'Password reset email sent. Please check your inbox.'
        );

        setSubmitting(false);
        return;
      }

      if (isRegistering) {
        await register({
          email: email.trim(),
          password,
          name: name.trim(),
          class_id: classId,
        });
      } else {
        await login(
          email.trim(),
          password
        );
      }
    } catch (err: any) {
      console.error(
        'Firebase authentication failed:',
        err
      );

      const firebaseCode =
        err?.code ||
        err?.response?.data?.code;

      const detail =
        err?.response?.data?.detail;

      let message =
        detail ||
        err?.message ||
        'Authentication failed.';

      if (
        firebaseCode === 'auth/invalid-credential' ||
        firebaseCode === 'auth/wrong-password'
      ) {
        message = 'Invalid email or password. Please verify credentials.';
      }

      if (err?.message?.includes('Network Error') || err?.message?.includes('Failed to fetch') || err?.code === 'ERR_NETWORK') {
        message = 'Backend server offline. Launch backend with `python run_server.py` in backend directory, or navigate directly to /subject/01_english_complete';
      }

      if (firebaseCode === 'auth/user-not-found') {
        message =
          'No Firebase account exists for this email.';
      }

      if (firebaseCode === 'auth/email-already-in-use') {
        message =
          'This email already has a Firebase account. Please use Sign In or Forgot Password.';
      }

      if (firebaseCode === 'auth/weak-password') {
        message =
          'Password must contain at least 6 characters.';
      }

      if (firebaseCode === 'auth/too-many-requests') {
        message =
          'Too many attempts. Please wait and try again.';
      }

      setLoginError(message);
      setSubmitting(false);
    }
  };


  if (!user) {
    return (
      <Layout>
        <div className="min-h-[80vh] flex items-center justify-center px-4 py-12">
          <div className="w-full max-w-md">

            <div className="text-center mb-8">
              <div className="inline-flex items-center rounded-full bg-slate-900 px-6 py-2 text-[10px] font-black uppercase tracking-[0.25em] text-white">
                GURUKUL AI UNIFIED SYSTEM
              </div>

              <h1 className="mt-5 text-5xl font-black italic tracking-tighter uppercase text-slate-900">
                {isResettingPassword
                  ? 'Reset Password'
                  : isRegistering
                    ? 'Student Registration'
                    : 'Student Login'}
              </h1>

              <p className="mt-4 text-sm font-medium text-slate-500">
                Secure Firebase Authentication • Classes 5, 6, and 7
              </p>
            </div>

            <div className="rounded-[32px] border-2 border-slate-100 bg-white p-8 shadow-2xl">

              <form
                onSubmit={handleLogin}
                className="space-y-5"
              >

                {loginError && (
                  <div className="rounded-2xl border border-red-200 bg-red-50 p-4 text-xs font-bold text-red-600">
                    {loginError}
                  </div>
                )}

                {resetMessage && (
                  <div className="rounded-2xl border border-green-200 bg-green-50 p-4 text-xs font-bold text-green-700">
                    {resetMessage}
                  </div>
                )}

                {isRegistering && !isResettingPassword && (
                  <>
                    <div>
                      <label className="mb-2 block text-[11px] font-black uppercase tracking-wider text-slate-500">
                        Full Name
                      </label>

                      <input
                        type="text"
                        value={name}
                        onChange={(e) =>
                          setName(e.target.value)
                        }
                        autoComplete="name"
                        className="w-full rounded-2xl border-2 border-slate-200 bg-slate-50 px-5 py-4 text-sm font-bold text-slate-900 outline-none"
                        required
                      />
                    </div>

                    <div>
                      <label className="mb-2 block text-[11px] font-black uppercase tracking-wider text-slate-500">
                        Class
                      </label>

                      <select
                        value={classId}
                        onChange={(e) =>
                          setClassId(e.target.value)
                        }
                        className="w-full rounded-2xl border-2 border-slate-200 bg-slate-50 px-5 py-4 text-sm font-bold text-slate-900 outline-none"
                        required
                      >
                        <option value="class_5">
                          Class 5
                        </option>

                        <option value="class_6">
                          Class 6
                        </option>

                        <option value="class_7">
                          Class 7
                        </option>
                      </select>
                    </div>
                  </>
                )}

                <div>
                  <label className="mb-2 block text-[11px] font-black uppercase tracking-wider text-slate-500">
                    Email
                  </label>

                  <input
                    type="email"
                    value={email}
                    onChange={(e) =>
                      setEmail(e.target.value)
                    }
                    autoComplete="email"
                    className="w-full rounded-2xl border-2 border-slate-200 bg-slate-50 px-5 py-4 text-sm font-bold text-slate-900 outline-none"
                    required
                  />
                </div>

                {!isResettingPassword && (
                  <div>
                    <label className="mb-2 block text-[11px] font-black uppercase tracking-wider text-slate-500">
                      Password
                    </label>

                    <input
                      type="password"
                      value={password}
                      onChange={(e) =>
                        setPassword(e.target.value)
                      }
                      autoComplete={
                        isRegistering
                          ? 'new-password'
                          : 'current-password'
                      }
                      minLength={6}
                      className="w-full rounded-2xl border-2 border-slate-200 bg-slate-50 px-5 py-4 text-sm font-bold text-slate-900 outline-none"
                      required
                    />
                  </div>
                )}

                <button
                  type="submit"
                  disabled={submitting}
                  className="w-full rounded-2xl bg-blue-600 py-5 text-xs font-black uppercase text-white shadow-xl transition-all hover:bg-blue-700 disabled:opacity-50"
                >
                  {submitting
                    ? 'Processing...'
                    : isResettingPassword
                      ? 'Send Reset Email'
                      : isRegistering
                        ? 'Create Student Account'
                        : 'Authorize Access'}
                </button>

                {!isRegistering && !isResettingPassword && (
                  <div className="pt-1 text-center">
                    <button
                      type="button"
                      onClick={() => {
                        setIsResettingPassword(true);
                        setLoginError('');
                        setResetMessage('');
                        setSubmitting(false);
                      }}
                      className="text-xs font-black uppercase tracking-widest text-slate-500 transition-colors hover:text-blue-600"
                    >
                      Forgot Password?
                    </button>
                  </div>
                )}

              </form>

              <div className="mt-6 border-t border-slate-100 pt-6 text-center">
                <button
                  type="button"
                  onClick={() => {
                    if (isResettingPassword) {
                      setIsResettingPassword(false);
                      setIsRegistering(false);
                    } else {
                      setIsRegistering(
                        (value) => !value
                      );
                    }

                    setLoginError('');
                    setResetMessage('');
                    setSubmitting(false);
                  }}
                  className="text-xs font-black uppercase tracking-widest text-blue-600 transition-colors hover:text-blue-700"
                >
                  {isResettingPassword
                    ? 'Back to Sign In'
                    : isRegistering
                      ? 'Already have an account? Sign in'
                      : 'New student? Create an account'}
                </button>
              </div>

            </div>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-12">
        <header className="space-y-4">
           <h1 className="text-3xl sm:text-5xl font-black tracking-tighter text-slate-900 uppercase italic">Gurukul <span className="text-blue-600">Unified</span> Dashboard</h1>
           <p className="text-lg text-slate-500 font-medium">Select your class to begin your learning journey.</p>

           <div className="pt-4 max-w-xl">
              <div className="relative group">
                 <Search className="absolute left-6 top-1/2 -translate-y-1/2 text-slate-300 group-focus-within:text-blue-600 transition-colors" size={20} />
                 <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search for lessons, questions, or definitions..."
                    className="w-full pl-16 pr-6 py-5 bg-slate-50 border-2 border-slate-100 rounded-[24px] font-bold text-slate-900 outline-none focus:border-blue-600 focus:bg-white transition-all shadow-inner"
                 />
              </div>
              {searchResults.length > 0 && (
                 <div className="absolute mt-2 w-full bg-white border-2 border-slate-100 rounded-[24px] shadow-2xl z-50 p-4 space-y-2 max-h-[400px] overflow-y-auto">
                    {searchResults.map((res: any) => (
                       <Link key={res.id} href={`/chapter/${res.chapter_id}`} className="block p-4 hover:bg-slate-50 rounded-2xl border border-transparent hover:border-slate-100 transition-all">
                          <div className="flex items-center justify-between mb-1">
                             <span className="text-[8px] font-black text-blue-600 uppercase tracking-widest bg-blue-50 px-2 py-0.5 rounded">{res.layer}</span>
                             <span className="text-[8px] font-bold text-slate-400 uppercase">{res.class} â€¢ {res.subject}</span>
                          </div>
                          <p className="text-sm font-black text-slate-900 leading-tight">{res.title || 'Untitled Block'}</p>
                          <p className="text-[10px] text-slate-500 line-clamp-1 mt-1 font-medium">{res.text}</p>
                       </Link>
                    ))}
                 </div>
              )}
           </div>
        </header>

        {/* CLASS SELECTOR */}
        <section className="grid grid-cols-1 sm:grid-cols-3 gap-6">
           {classes.map((cls) => (
              <button
                key={cls.id}
                onClick={() => setSelectedClass(cls)}
                className={`p-8 rounded-[40px] border-4 transition-all text-left space-y-4 group relative overflow-hidden ${selectedClass?.id === cls.id ? 'border-blue-600 bg-blue-50' : 'border-slate-100 bg-white hover:border-slate-200'}`}
              >
                 <div className={`w-12 h-12 rounded-2xl flex items-center justify-center font-black ${selectedClass?.id === cls.id ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-400 group-hover:bg-slate-200'}`}>
                    <GraduationCap size={24} />
                 </div>
                 <div>
                    <h3 className="text-2xl font-black uppercase italic tracking-tighter">{cls.name}</h3>
                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{cls.subjects.length} Subjects Available</p>
                 </div>
                 {selectedClass?.id === cls.id && <div className="absolute top-4 right-8 text-blue-600 font-black text-xs uppercase tracking-widest animate-pulse italic">Active</div>}
              </button>
           ))}
        </section>

        {/* SUBJECT GRID */}
        {selectedClass && (
           <section className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
              <div className="flex items-center gap-4 border-b-2 border-slate-100 pb-4">
                 <h2 className="text-2xl font-black uppercase italic tracking-tighter text-slate-900">{selectedClass.name} Streams</h2>
                 <ArrowRight className="text-blue-600" />
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                 {selectedClass.subjects && selectedClass.subjects.map((subj) => (
                    <Link key={subj.id} href={`/subject/${subj.id}`} className="bg-white border-2 border-slate-100 rounded-[32px] p-6 hover:border-blue-600 hover:shadow-xl transition-all group flex flex-col gap-6">
                       <div className="w-10 h-10 bg-slate-50 rounded-xl flex items-center justify-center text-slate-300 group-hover:bg-blue-600 group-hover:text-white transition-all">
                          <Book size={18} />
                       </div>
                       <div>
                          <h3 className="text-xl font-black text-slate-900 uppercase italic leading-tight">{subj.name}</h3>
                          <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">{subj.chapters?.length || 0} Chapters</p>
                       </div>
                       <span className="text-[10px] font-black text-blue-600 uppercase tracking-widest mt-auto">Explore &rarr;</span>
                    </Link>
                 ))}
              </div>
           </section>
        )}
      </div>
    </Layout>
  );
}
