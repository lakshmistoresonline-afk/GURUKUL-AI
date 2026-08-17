'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import { User, Settings, Shield, Bell, LogOut, Award, Save, X, Loader2, CheckCircle2 } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { db } from '@/lib/firebase';
import { doc, updateDoc } from 'firebase/firestore';
import { chapterService } from '@/services/api';
import { motion, AnimatePresence } from 'framer-motion';

import classesData from '@/config/classes.json';

export default function ProfilePage() {
  const { profile, refreshProfile } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [selectedClass, setSelectedClass] = useState('');
  const [showConfirm, setShowConfirm] = useState(false);
  const [isSaving, setIsEditingState] = useState(false);
  const [saveStatus, setSaveStatus] = useState<'idle' | 'success' | 'error'>('idle');

  useEffect(() => {
    if (profile) {
      setSelectedClass(profile.classId);
    }
  }, [profile]);

  const handleSave = async () => {
    if (!profile || !selectedClass) return;

    setIsEditingState(true);
    setSaveStatus('idle');

    try {
      const userRef = doc(db, 'users', profile.uid);
      await updateDoc(userRef, {
        classId: selectedClass
      });

      chapterService.invalidateCache();
      await refreshProfile();
      setSaveStatus('success');
      setTimeout(() => {
        setIsEditing(false);
        setSaveStatus('idle');
        setShowConfirm(false);
      }, 1500);
    } catch (err) {
      console.error("Failed to update profile", err);
      setSaveStatus('error');
    } finally {
      setIsEditingState(false);
    }
  };

  if (!profile) return null;

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
        <TopBar title="My Account" />

        <div className="max-w-4xl mx-auto p-8 space-y-8">
           {/* Profile Header */}
           <section className="bg-white border border-border rounded-3xl p-10 shadow-sm flex flex-col md:flex-row items-center gap-10">
              <div className="w-32 h-32 bg-blue-100 rounded-full flex items-center justify-center text-primary text-4xl font-black border-4 border-white shadow-xl shadow-blue-100">
                {profile.name?.charAt(0).toUpperCase() || 'S'}
              </div>
              <div className="flex-1 text-center md:text-left space-y-2">
                 <h2 className="text-3xl font-black text-slate-800 tracking-tight">{profile.name}</h2>
                 <p className="text-slate-500 font-medium">{profile.email}</p>
                 <div className="flex flex-wrap justify-center md:justify-start gap-2 pt-4">
                    <span className="px-4 py-1.5 bg-blue-50 text-primary rounded-full text-[10px] font-black uppercase tracking-widest border border-blue-100">
                       Class {profile.classId}
                    </span>
                    <span className="px-4 py-1.5 bg-orange-50 text-orange-600 rounded-full text-[10px] font-black uppercase tracking-widest border border-orange-100 flex items-center gap-1.5">
                       <Award size={12} /> {profile.xp} XP
                    </span>
                    <span className="px-4 py-1.5 bg-slate-50 text-slate-500 rounded-full text-[10px] font-black uppercase tracking-widest border border-slate-100">
                       {profile.role}
                    </span>
                 </div>
              </div>
              {!isEditing && (
                <button
                  onClick={() => setIsEditing(true)}
                  className="px-8 py-3 bg-slate-900 text-white rounded-2xl font-black text-sm hover:bg-black transition-all"
                >
                   Edit Profile
                </button>
              )}
           </section>

           <AnimatePresence>
             {isEditing && (
               <motion.section
                 initial={{ opacity: 0, y: -20 }}
                 animate={{ opacity: 1, y: 0 }}
                 exit={{ opacity: 0, y: -20 }}
                 className="bg-white border-2 border-primary/20 rounded-3xl p-10 shadow-xl space-y-8"
               >
                  <div className="flex items-center justify-between">
                     <h3 className="text-xl font-black text-slate-800">Account Settings</h3>
                     <button onClick={() => setIsEditing(false)} className="text-slate-400 hover:text-slate-600"><X size={24} /></button>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                     <div className="space-y-3">
                        <label className="text-xs font-black text-slate-400 uppercase tracking-widest">Current Class</label>
                        <select
                          value={selectedClass}
                          onChange={(e) => setSelectedClass(e.target.value)}
                          className="w-full bg-slate-50 border border-slate-200 rounded-2xl px-6 py-4 font-bold text-slate-800 focus:outline-none focus:ring-4 focus:ring-primary/5 transition-all"
                        >
                           {classesData.map(c => (
                             <option key={c.id} value={c.id}>{c.name}</option>
                           ))}
                        </select>
                        <p className="text-[10px] text-slate-400 font-medium leading-relaxed italic">
                           Note: Changing your class will update your primary curriculum index and multimedia lab.
                        </p>
                     </div>
                  </div>

                  {!showConfirm ? (
                    <div className="pt-6 flex items-center gap-4">
                       <button
                         onClick={() => setShowConfirm(true)}
                         className="flex-1 bg-primary text-white py-4 rounded-2xl font-black text-sm uppercase tracking-widest flex items-center justify-center gap-3 hover:bg-blue-700 transition-all"
                       >
                          Update Class
                       </button>
                       <button
                         onClick={() => setIsEditing(false)}
                         className="px-8 py-4 bg-slate-100 text-slate-600 rounded-2xl font-black text-sm uppercase tracking-widest hover:bg-slate-200 transition-all"
                       >
                          Cancel
                       </button>
                    </div>
                  ) : (
                    <div className="pt-6 space-y-6 bg-blue-50/50 p-8 rounded-3xl border border-blue-100">
                       <div className="space-y-2">
                          <h4 className="font-black text-slate-800">Confirm Class Change</h4>
                          <p className="text-sm text-slate-600 font-medium">
                             Are you sure you want to switch to <strong>Class {selectedClass}</strong>?
                             Your Library, Multimedia Lab and all learning content will be updated to the Class {selectedClass} curriculum.
                          </p>
                       </div>
                       <div className="flex items-center gap-4">
                          <button
                            disabled={isSaving}
                            onClick={handleSave}
                            className="flex-1 bg-primary text-white py-4 rounded-2xl font-black text-sm uppercase tracking-widest flex items-center justify-center gap-3 hover:bg-blue-700 disabled:opacity-50 transition-all"
                          >
                             {isSaving ? <Loader2 className="animate-spin" size={18} /> : saveStatus === 'success' ? <CheckCircle2 size={18} /> : <Save size={18} />}
                             {isSaving ? 'Saving Changes...' : saveStatus === 'success' ? 'Saved Successfully' : 'Yes, Confirm Change'}
                          </button>
                          <button
                            disabled={isSaving}
                            onClick={() => setShowConfirm(false)}
                            className="px-8 py-4 bg-white text-slate-600 border border-slate-200 rounded-2xl font-black text-sm uppercase tracking-widest hover:bg-slate-50 transition-all"
                          >
                             Cancel
                          </button>
                       </div>
                    </div>
                  )}

                  {saveStatus === 'error' && (
                    <p className="text-red-500 text-xs font-bold text-center">Unable to save changes. Please check your connection.</p>
                  )}
               </motion.section>
             )}
           </AnimatePresence>

           <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <SettingsCard icon={Settings} title="Learning Settings" desc="Difficulty, language, and auto-read options." color="blue" />
              <SettingsCard icon={Bell} title="Notifications" desc="Manage alerts for new chapters and assignments." color="orange" />
              <SettingsCard icon={Shield} title="Privacy & Security" desc="Password, session management, and data." color="purple" />
              <SettingsCard icon={LogOut} title="Sign Out" desc="Log out of your current session safely." color="red" danger />
           </div>
        </div>
      </main>
    </div>
  );
}

function SettingsCard({ icon: Icon, title, desc, color, danger }: any) {
  const colors: any = {
    blue: "text-blue-600 bg-blue-50",
    orange: "text-orange-600 bg-orange-50",
    purple: "text-purple-600 bg-purple-50",
    red: "text-red-600 bg-red-50",
  };

  return (
    <div className={`p-8 bg-white border border-border rounded-3xl hover:shadow-lg transition-all cursor-pointer group`}>
       <div className={`w-12 h-12 rounded-2xl flex items-center justify-center mb-6 ${colors[color]}`}>
          <Icon size={24} />
       </div>
       <h4 className={`text-lg font-black mb-2 ${danger ? 'text-red-600' : 'text-slate-800'}`}>{title}</h4>
       <p className="text-slate-500 text-xs font-medium leading-relaxed">{desc}</p>
    </div>
  );
}
