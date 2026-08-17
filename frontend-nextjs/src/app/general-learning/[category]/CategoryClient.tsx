'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Sidebar from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import { generalLearningService } from '@/services/api';
import { useAuth } from '@/context/AuthContext';
import {
  ArrowLeft,
  Book,
  Globe,
  Brain,
  CheckCircle2,
  Play,
  ChevronRight,
  Search,
  BookOpen,
  Sparkles,
  Target,
  Zap
} from 'lucide-react';
import Link from 'next/link';
import { motion } from 'framer-motion';

export default function CategoryClient() {
  const { category } = useParams() as { category: string };
  const { profile, loading: authLoading } = useAuth();
  const router = useRouter();
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    if (authLoading || !profile) return;

    const fetchContent = async () => {
      try {
        const data = await generalLearningService.getCategory(category);
        setItems(data);
      } catch (err) {
        console.error("Failed to load category content", err);
      } finally {
        setLoading(false);
      }
    };
    fetchContent();
  }, [authLoading, profile, category]);

  if (authLoading || loading) return (
    <div className="flex min-h-screen bg-[#F8FAFC] items-center justify-center">
       <div className="animate-pulse flex flex-col items-center gap-4">
          <BookOpen size={40} className="text-primary" />
          <p className="text-sm font-bold text-slate-500 uppercase tracking-widest">Opening subject index...</p>
       </div>
    </div>
  );

  const getHeader = () => {
    switch(category) {
      case 'english_vocabulary': return { title: 'English Vocabulary', icon: Book, color: 'blue' };
      case 'general_knowledge': return { title: 'General Knowledge', icon: Globe, color: 'emerald' };
      case 'science_facts': return { title: 'Science Facts', icon: Sparkles, color: 'purple' };
      case 'maths_quick_practice': return { title: 'Maths Quick Practice', icon: Target, color: 'orange' };
      case 'india_and_world': return { title: 'India & World', icon: Globe, color: 'blue' };
      case 'life_skills': return { title: 'Life Skills', icon: Zap, color: 'emerald' };
      case 'logic_and_reasoning': return { title: 'Logic & Reasoning', icon: Brain, color: 'orange' };
      default: return { title: 'Learning', icon: Globe, color: 'blue' };
    }
  };

  const header = getHeader();
  const filtered = items.filter(i =>
    (i.title || i.word || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
    (i.topic || '').toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="flex min-h-screen bg-[#F8FAFC] text-slate-900 selection:bg-primary/10">
      <Sidebar />
      <main className="flex-1 overflow-y-auto pb-24">
        <TopBar title={header.title} />

        <div className="max-w-7xl mx-auto p-6 md:p-10 space-y-12">
           <div className="flex items-center justify-between">
              <button
                onClick={() => router.push('/general-learning')}
                className="flex items-center gap-3 px-6 py-3 bg-white border border-slate-200 rounded-2xl text-xs font-bold uppercase tracking-widest text-slate-600 hover:text-primary transition-all shadow-sm"
              >
                 <ArrowLeft size={16} /> Back to Hub
              </button>

              <div className="relative group">
                 <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-primary transition-colors" size={18} />
                 <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder={`Search ${category.replace('_', ' ')}...`}
                    className="pl-12 pr-6 py-3 bg-white border border-slate-200 rounded-2xl text-sm font-medium focus:outline-none focus:ring-4 focus:ring-primary/5 w-80 transition-all shadow-sm"
                 />
              </div>
           </div>

           {/* Hero Section */}
           <section className="bg-white border border-slate-200/60 rounded-[48px] p-10 md:p-16 shadow-sm relative overflow-hidden flex flex-col md:flex-row items-center gap-12">
              <div className={`w-24 h-24 rounded-[32px] bg-${header.color}-50 flex items-center justify-center text-${header.color}-600 border border-${header.color}-100 shadow-inner`}>
                 <header.icon size={48} />
              </div>
              <div className="space-y-4 text-center md:text-left flex-1">
                 <h2 className="text-4xl md:text-5xl font-black tracking-tight text-slate-900">{header.title}</h2>
                 <p className="text-slate-500 text-xl font-medium max-w-2xl leading-relaxed">
                    Personalized learning modules for your current level. Discover, practice and master.
                 </p>
              </div>
              <div className="px-10 py-6 bg-slate-50 rounded-[32px] border border-slate-100 text-center min-w-[200px]">
                 <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Available Modules</p>
                 <p className="text-4xl font-black text-slate-900">{items.length}</p>
              </div>
           </section>

           {/* Grid */}
           <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {filtered.map((item) => (
                <ItemCard key={item.id} item={item} category={category} color={header.color} />
              ))}
           </div>

        </div>
      </main>
    </div>
  );
}

function ItemCard({ item, category, color }: any) {
  const router = useRouter();
  const title = item.title || item.word || item.topic;

  const getIcon = () => {
    switch(category) {
      case 'english_vocabulary': return <Book size={20} />;
      case 'general_knowledge': return <Globe size={20} />;
      case 'science_facts': return <Sparkles size={20} />;
      case 'maths_quick_practice': return <Target size={20} />;
      case 'india_and_world': return <Globe size={20} />;
      case 'life_skills': return <Zap size={20} />;
      case 'logic_and_reasoning': return <Brain size={20} />;
      default: return <BookOpen size={20} />;
    }
  };

  return (
    <motion.div
      whileHover={{ y: -5 }}
      onClick={() => router.push(`/general-learning/learn/${item.id}`)}
      className="bg-white border border-slate-200/60 rounded-[32px] p-8 hover:shadow-xl hover:border-primary/20 transition-all cursor-pointer group flex flex-col justify-between h-full shadow-sm"
    >
       <div className="space-y-6">
          <div className="flex items-center justify-between">
             <div className={`w-10 h-10 rounded-xl bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-${color}-50 group-hover:text-${color}-600 transition-all`}>
                {getIcon()}
             </div>
             <div className="px-2 py-1 bg-slate-50 border border-slate-100 rounded-lg text-[9px] font-black text-slate-400 uppercase tracking-widest group-hover:text-primary transition-colors">Ready</div>
          </div>
          <div>
             <h4 className="text-xl font-black text-slate-900 leading-tight group-hover:text-primary transition-colors line-clamp-2">{title}</h4>
             <p className="text-xs text-slate-500 font-bold mt-2 line-clamp-2 uppercase tracking-tighter opacity-60">
                {item.meaning || item.topic}
             </p>
          </div>
       </div>

       <div className="pt-6 mt-6 border-t border-slate-100 flex items-center justify-between">
          <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">General Learning</span>
          <div className="w-8 h-8 rounded-full bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-primary group-hover:text-white transition-all shadow-sm">
             <Play size={14} fill="currentColor" />
          </div>
       </div>
    </motion.div>
  );
}
