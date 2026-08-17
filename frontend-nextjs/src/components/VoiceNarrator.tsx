'use client';

import React, { useState, useEffect } from 'react';
import { Volume2, VolumeX, Play, Pause, RotateCcw } from 'lucide-react';
import { motion } from 'framer-motion';

interface VoiceNarratorProps {
  text: string;
  lang?: 'en-IN' | 'hi-IN';
}

export default function VoiceNarrator({ text, lang = 'en-IN' }: VoiceNarratorProps) {
  const [isPaused, setIsPaused] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [supported, setSupported] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined' && window.speechSynthesis) {
      setSupported(true);
    }
  }, []);

  const speak = () => {
    if (!supported) return;

    // Cancel any ongoing speech
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);

    // Attempt to find a natural-sounding voice for the language
    const voices = window.speechSynthesis.getVoices();
    const voice = voices.find(v => v.lang.startsWith(lang.split('-')[0])) || voices[0];

    if (voice) {
      utterance.voice = voice;
    }

    utterance.lang = lang;
    utterance.rate = 0.9; // Slightly slower for better comprehension
    utterance.pitch = 1.0;

    utterance.onstart = () => setIsPlaying(true);
    utterance.onend = () => {
      setIsPlaying(false);
      setIsPaused(false);
    };
    utterance.onerror = () => {
      setIsPlaying(false);
      setIsPaused(false);
    };

    window.speechSynthesis.speak(utterance);
  };

  const togglePause = () => {
    if (isPaused) {
      window.speechSynthesis.resume();
      setIsPaused(false);
    } else {
      window.speechSynthesis.pause();
      setIsPaused(true);
    }
  };

  const stop = () => {
    window.speechSynthesis.cancel();
    setIsPlaying(false);
    setIsPaused(false);
  };

  if (!supported) return null;

  return (
    <div className="flex items-center gap-3 bg-white/5 border border-white/10 p-2 rounded-2xl backdrop-blur-md">
      {!isPlaying ? (
        <button
          onClick={speak}
          className="flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-blue-600 transition-all shadow-lg shadow-primary/20"
        >
          <Volume2 size={16} /> Listen to Lesson
        </button>
      ) : (
        <div className="flex items-center gap-2">
          <button
            onClick={togglePause}
            className="p-2 bg-white/10 text-white rounded-xl hover:bg-white/20 transition-all"
            title={isPaused ? "Resume" : "Pause"}
          >
            {isPaused ? <Play size={16} fill="currentColor" /> : <Pause size={16} fill="currentColor" />}
          </button>
          <button
            onClick={stop}
            className="p-2 bg-red-500/20 text-red-400 rounded-xl hover:bg-red-500/30 transition-all"
            title="Stop"
          >
            <RotateCcw size={16} />
          </button>
          <div className="flex gap-1 px-2">
             {[1,2,3].map(i => (
               <motion.div
                 key={i}
                 animate={{ height: [4, 12, 4] }}
                 transition={{ duration: 0.8, repeat: Infinity, delay: i * 0.2 }}
                 className="w-1 bg-primary rounded-full"
               />
             ))}
          </div>
        </div>
      )}
    </div>
  );
}
