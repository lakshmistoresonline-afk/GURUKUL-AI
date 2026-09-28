# GURUKUL AI — UNIVERSAL TTS & AUDIO NARRATION MASTER PLAN

## 1. Objective
To extend the Audio Narration & Text-to-Speech (TTS) Study Reader from the Overview summary into a **universal audio assistant widget available across all relevant tabs and pages** (Notes, Master Practice, Flashcards, Quiz) for all non-Hindi subjects.

---

## 2. Proposed Implementation Architecture

### Component: Global Audio Assistant Toolbar (`AudioReaderToolbar.tsx`)
- **Placement**: Fixed floating or sticky toolbar in the chapter reader header (`ChapterClient.tsx`).
- **Features**:
  - **Play / Pause / Stop**: Powered by the browser's native Web Speech API (`window.speechSynthesis`).
  - **Context-Aware Extraction**: Automatically extracts and reads the textual content of whichever tab is currently active (`Overview`, `Notes`, `Master`, `Flashcards`).
  - **Speed Controls**: Adjustable narration speed (`0.75x`, `1.0x`, `1.25x`).
  - **Language Guard**: Automatically disables or hides for Hindi (`subject === 'Hindi'`) as requested.

---

## 3. Compliance & Safety
- **Plan Only**: This document outlines the universal TTS audio narration plan. No code changes have been executed.
