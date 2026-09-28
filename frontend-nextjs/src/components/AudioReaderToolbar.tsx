import React, { useState, useEffect } from 'react';

interface AudioToolbarProps {
  textToRead: string;
  subject?: string;
}

export default function AudioReaderToolbar({ textToRead, subject }: AudioToolbarProps) {
  const [isSpeaking, setIsSpeaking] = useState<boolean>(false);
  const [rate, setRate] = useState<number>(1.0);
  const [ambient, setAmbient] = useState<'off' | 'rain' | 'forest'>('off');

  const isHindi = subject?.toLowerCase().includes('hindi');

  // Ambient sound generator using Web Audio API
  useEffect(() => {
    if (ambient === 'off') return;

    let audioCtx: AudioContext | null = null;
    let node: ScriptProcessorNode | null = null;
    let timer: any = null;

    try {
      audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)();
      const bufferSize = 4096;
      node = audioCtx.createScriptProcessor(bufferSize, 1, 1);

      node.onaudioprocess = (e) => {
        const output = e.outputBuffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
          // White noise for rain/forest background
          const white = Math.random() * 2 - 1;
          output[i] = white * (ambient === 'rain' ? 0.03 : 0.015);
        }
      };

      node.connect(audioCtx.destination);
    } catch (err) {
      console.warn('Web Audio API not supported:', err);
    }

    return () => {
      if (audioCtx && audioCtx.state !== 'closed') {
        audioCtx.close();
      }
      if (timer) clearInterval(timer);
    };
  }, [ambient]);

  if (isHindi || !textToRead) return null;

  const handleToggleSpeech = () => {
    if (!('speechSynthesis' in window)) return;

    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    } else {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(textToRead);
      utterance.rate = rate;
      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = () => setIsSpeaking(false);
      window.speechSynthesis.speak(utterance);
      setIsSpeaking(true);
    }
  };

  const changeRate = (newRate: number) => {
    setRate(newRate);
    if (isSpeaking && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(textToRead);
      utterance.rate = newRate;
      utterance.onend = () => setIsSpeaking(false);
      window.speechSynthesis.speak(utterance);
      setIsSpeaking(true);
    }
  };

  return (
    <div className="flex flex-wrap items-center justify-between gap-4 p-4 bg-gradient-to-r from-indigo-50/90 via-teal-50/50 to-indigo-50/90 border border-indigo-200/80 rounded-2xl shadow-xs backdrop-blur-md">
      <div className="flex items-center gap-3">
        <button
          onClick={handleToggleSpeech}
          className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-extrabold rounded-xl shadow-md shadow-indigo-600/20 transition-all hover:scale-[1.02]"
        >
          <span>{isSpeaking ? '⏸ Pause Narration' : '🔊 Listen to Section'}</span>
        </button>
        <span className="text-xs font-bold text-slate-600 hidden sm:inline">
          {isSpeaking ? 'Narrating active study text...' : 'Audio Assistant Ready'}
        </span>
      </div>

      <div className="flex flex-wrap items-center gap-3">
        {/* Speed Controls */}
        <div className="flex items-center gap-1 bg-white px-2.5 py-1.5 rounded-xl border border-slate-200 text-xs font-bold text-slate-700 shadow-xs">
          <span>Speed:</span>
          {[0.75, 1.0, 1.25].map((r) => (
            <button
              key={r}
              onClick={() => changeRate(r)}
              className={`px-2 py-0.5 rounded-lg text-[11px] font-extrabold transition-all ${rate === r ? 'bg-indigo-600 text-white shadow-xs' : 'hover:bg-slate-100 text-slate-600'}`}
            >
              {r}x
            </button>
          ))}
        </div>

        {/* Ambient Soundscapes */}
        <div className="flex items-center gap-1 bg-white px-2.5 py-1.5 rounded-xl border border-slate-200 text-xs font-bold text-slate-700 shadow-xs">
          <span>Ambience:</span>
          <button
            onClick={() => setAmbient('off')}
            className={`px-2 py-0.5 rounded-lg text-[11px] font-bold ${ambient === 'off' ? 'bg-slate-900 text-white' : 'hover:bg-slate-100 text-slate-600'}`}
          >
            Off
          </button>
          <button
            onClick={() => setAmbient('rain')}
            className={`px-2 py-0.5 rounded-lg text-[11px] font-bold ${ambient === 'rain' ? 'bg-teal-600 text-white' : 'hover:bg-slate-100 text-slate-600'}`}
            title="Calming Rainfall Soundscape"
          >
            🌧️ Rain
          </button>
          <button
            onClick={() => setAmbient('forest')}
            className={`px-2 py-0.5 rounded-lg text-[11px] font-bold ${ambient === 'forest' ? 'bg-emerald-600 text-white' : 'hover:bg-slate-100 text-slate-600'}`}
            title="Relaxing Forest Soundscape"
          >
            🍃 Forest
          </button>
        </div>
      </div>
    </div>
  );
}
