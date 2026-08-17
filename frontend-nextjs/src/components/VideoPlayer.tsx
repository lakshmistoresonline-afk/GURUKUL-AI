'use client';

import React from 'react';

interface VideoPlayerProps {
  url: string;
  poster?: string;
  subtitlesUrl?: string;
}

export default function VideoPlayer({ url, poster, subtitlesUrl }: VideoPlayerProps) {
  // Map internal /media/ path to backend URL
  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

  if (!url) {
    return (
      <div className="w-full aspect-video bg-slate-900 rounded-2xl flex items-center justify-center text-slate-500 font-medium italic">
        Video content is currently being processed or unavailable.
      </div>
    );
  }

  const fullUrl = url.startsWith('http') ? url : `${backendUrl}${url}`;
  const fullSubtitlesUrl = subtitlesUrl ? (subtitlesUrl.startsWith('http') ? subtitlesUrl : `${backendUrl}${subtitlesUrl}`) : null;

  return (
    <div className="w-full aspect-video bg-black rounded-2xl overflow-hidden shadow-2xl">
      <video
        src={fullUrl}
        poster={poster}
        controls
        className="w-full h-full"
      >
        {fullSubtitlesUrl && (
          <track
            src={fullSubtitlesUrl}
            kind="subtitles"
            srcLang="en"
            label="English"
            default
          />
        )}
        Your browser does not support the video tag.
      </video>
    </div>
  );
}
