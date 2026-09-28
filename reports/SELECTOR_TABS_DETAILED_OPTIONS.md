# GURUKUL AI — SELECTOR TABS DETAILED IMPLEMENTATION OPTIONS

## 1. Objective
To provide a comprehensive blueprint for introducing **Selector Tabs** across all dense, multi-section pages (specifically **Notes** and **Master Practice**), ensuring zero long scrolling and maximum cognitive focus.

---

## 2. Page-by-Page Selector Tabs Options

### Option A: Notes Tab (`NotesComponent.tsx` & Subject Notes)
- **Problem**: Textbook notes contain overview paragraphs, detailed section analyses, formulas, glossaries, and real-world applications in one long scroll.
- **Proposed Selector Tabs**:
  - `📖 Chapter Summary`
  - `🔬 Core Concepts & Breakdown`
  - `📐 Formulas & Rules`
  - `📚 Glossary & Vocabulary`
  - `🌍 Real-World Applications`
- **User Experience**: Clicking a tab instantly displays that specific module while keeping the rest hidden, reducing cognitive overload.

### Option B: Master Practice Tab (`MasterComponent.tsx` & Subject Master)
- **Problem**: Master practice contains summaries, character profiles, vocabulary matrices, objective question banks, reading extracts, writing prompts, and grammar exercises.
- **Proposed Selector Tabs**:
  - `⚡ Master Summary & Theme`
  - `📚 Vocabulary & Terms`
  - `📝 Objective Questions`
  - `📖 Reading Extracts`
  - `✍️ Writing & Literature`
  - `📋 Exam Question Bank`
- **User Experience**: A clean segmented control bar at the top of the Master Practice view allows students to switch between theory revision and practice test sections instantly.

---

## 3. Data Safety & Implementation Guarantee
- **Zero Data Impact**: All selector tabs use local React component state (`useState`). Authoritative JSON files, ProcessedContent layers, and backend API contracts remain 100% untouched.
- **Action**: Awaiting your approval before implementing these Selector Tabs across Notes and Master Practice.
