import React from 'react';

interface AtmosphereProps {
  ambience: 'off' | 'rain' | 'forest';
}

export default function AmbientAtmosphereOverlay({ ambience }: AtmosphereProps) {
  if (ambience === 'off') return null;

  return (
    <div className="fixed inset-0 pointer-events-none z-45 overflow-hidden transition-all duration-700">
      {ambience === 'rain' && (
        <div className="absolute inset-0 bg-sky-950/10 backdrop-blur-[0.5px]">
          <div className="absolute inset-0 opacity-25 bg-[linear-gradient(to_bottom,transparent_0%,rgba(56,189,248,0.9)_100%)] bg-[length:2px_50px]" />
        </div>
      )}
      {ambience === 'forest' && (
        <div className="absolute inset-0 bg-emerald-950/10 backdrop-blur-[0.5px]">
          <div className="absolute top-0 right-0 w-96 h-96 bg-emerald-500/15 rounded-full blur-3xl animate-pulse" />
          <div className="absolute bottom-0 left-0 w-96 h-96 bg-teal-500/15 rounded-full blur-3xl animate-pulse" />
        </div>
      )}
    </div>
  );
}
