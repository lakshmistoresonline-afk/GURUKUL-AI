class VoiceService {
  private synth: SpeechSynthesis | null = null;
  private voice: SpeechSynthesisVoice | null = null;

  constructor() {
    if (typeof window !== 'undefined') {
      this.synth = window.speechSynthesis;
      this.loadVoice();
    }
  }

  private loadVoice() {
    if (!this.synth) return;
    const voices = this.synth.getVoices();
    // Prefer English/Indian accent or standard English
    this.voice = voices.find(v => v.lang.includes('en-IN')) || voices.find(v => v.lang.includes('en-US')) || voices[0];
  }

  speak(text: string) {
    if (!this.synth) return;
    this.synth.cancel(); // Stop any current speech
    const utterance = new SpeechSynthesisUtterance(text);
    if (this.voice) utterance.voice = this.voice;
    utterance.rate = 0.9;
    utterance.pitch = 1.0;
    this.synth.speak(utterance);
  }

  stop() {
    if (this.synth) this.synth.cancel();
  }
}

export const voiceService = new VoiceService();
