'use client';

import React from 'react';
import {
  Youtube,
  ExternalLink,
  CheckCircle2,
  Search,
  Clock,
  Video,
  PlayCircle,
  AlertCircle
} from 'lucide-react';
import { isYouTubeSearchUrl, normalizeVideoUrl } from '@/utils/youtube';

interface VideoResource {
  title: string;
  channel: string;
  published?: string;
  url: string;
  resource_type: string;
  is_direct?: boolean;
}

interface ChapterVideoResourcesProps {
  verifiedVideos: VideoResource[];
  discoveryLinks: VideoResource[];
}

export default function ChapterVideoResources({ verifiedVideos, discoveryLinks }: ChapterVideoResourcesProps) {
  // Combine and sort properly if needed, but let's keep sections
  // Ensure we only show direct videos in the "Verified" section
  const directVideos = verifiedVideos.filter(v => v.is_direct !== false && !isYouTubeSearchUrl(v.url));

  // Discovery links are things that are explicitly marked as non-direct or search URLs
  const searchResources = discoveryLinks.filter(d => d.is_direct === false || isYouTubeSearchUrl(d.url));

  return (
    <div className="space-y-12">
      {/* 1. Verified Video Lessons */}
      {directVideos.length > 0 && (
        <div className="space-y-6">
          <div className="flex items-center gap-3 px-2">
            <div className="w-10 h-10 rounded-2xl bg-emerald-50 flex items-center justify-center text-emerald-600 border border-emerald-100 shadow-sm">
              <CheckCircle2 size={20} />
            </div>
            <div>
               <h3 className="text-xl font-black text-slate-900 uppercase tracking-tight">Verified Video Lessons</h3>
               <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Curated Educational Multimedia</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {directVideos.map((video, idx) => {
              const directUrl = normalizeVideoUrl(video.url) || video.url;
              return (
                <a
                  key={idx}
                  href={directUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group p-8 bg-white border border-slate-200/60 rounded-[40px] hover:border-emerald-500/40 transition-all hover:shadow-2xl relative overflow-hidden flex flex-col justify-between h-full shadow-sm"
                >
                  <div className="space-y-6 relative z-10">
                    <div className="flex items-start justify-between">
                      <span className="px-4 py-1.5 bg-emerald-50 text-emerald-700 rounded-full text-[9px] font-black uppercase tracking-widest border border-emerald-100 flex items-center gap-2">
                        <PlayCircle size={12} /> {video.resource_type.replace('_', ' ')}
                      </span>
                      <div className="w-10 h-10 rounded-full bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-emerald-50 group-hover:text-emerald-600 transition-all">
                        <ExternalLink size={18} />
                      </div>
                    </div>

                    <h4 className="text-xl font-black text-slate-800 leading-snug group-hover:text-primary transition-colors line-clamp-2">
                      {video.title}
                    </h4>

                    <div className="flex items-center gap-5 text-[11px] font-bold text-slate-500">
                      <span className="flex items-center gap-2">
                        <Youtube size={14} className="text-red-600" /> {video.channel}
                      </span>
                      {video.published && (
                        <span className="flex items-center gap-2 border-l border-slate-200 pl-5">
                          <Clock size={14} /> {video.published}
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="mt-8 pt-6 border-t border-slate-50 flex items-center justify-center">
                     <span className="text-[10px] font-black text-emerald-600 uppercase tracking-[0.2em] group-hover:underline">▶ Watch Lesson</span>
                  </div>

                  <div className="absolute -bottom-12 -right-12 w-32 h-32 bg-emerald-500/5 rounded-full blur-3xl opacity-0 group-hover:opacity-100 transition-opacity" />
                </a>
              );
            })}
          </div>
        </div>
      )}

      {/* 2. Search & Discovery Assistant */}
      {searchResources.length > 0 && (
        <div className="space-y-6">
          <div className="flex items-center gap-3 px-2">
            <div className="w-10 h-10 rounded-2xl bg-blue-50 flex items-center justify-center text-blue-600 border border-blue-100 shadow-sm">
              <Search size={20} />
            </div>
            <div>
               <h3 className="text-xl font-black text-slate-900 uppercase tracking-tight">Explore More on YouTube</h3>
               <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Find additional explanations and reviews</p>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {searchResources.map((link, idx) => (
              <a
                key={idx}
                href={link.url}
                target="_blank"
                rel="noopener noreferrer"
                className="p-6 bg-slate-50 border border-slate-200/60 rounded-[32px] hover:bg-white hover:border-primary/40 transition-all hover:shadow-lg group flex flex-col items-center text-center gap-4"
              >
                <div className="w-16 h-16 bg-white rounded-2xl flex items-center justify-center text-slate-300 group-hover:bg-primary group-hover:text-white transition-all shadow-sm border border-slate-100 group-hover:rotate-6">
                  <Youtube size={32} />
                </div>
                <div>
                  <p className="text-xs font-black text-slate-700 uppercase tracking-wider group-hover:text-primary transition-colors">{link.resource_type.replace('_', ' ')}</p>
                  <p className="text-[9px] font-black text-slate-400 uppercase tracking-widest mt-1">Smart Search</p>
                </div>
              </a>
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {directVideos.length === 0 && searchResources.length === 0 && (
        <div className="py-24 text-center border-2 border-dashed border-slate-200 rounded-[60px] bg-slate-50/50">
          <Video size={56} className="mx-auto text-slate-200 mb-6" />
          <h4 className="text-lg font-black text-slate-400 uppercase tracking-widest">Multimedia Indexing</h4>
          <p className="text-slate-400 text-xs font-bold uppercase tracking-[0.2em] mt-2">Neural verification in progress for this module.</p>
        </div>
      )}
    </div>
  );
}
