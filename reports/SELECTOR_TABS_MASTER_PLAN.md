# GURUKUL AI — SELECTOR TABS MASTER PRESENTATION PLAN

## 1. Objective
To eradicate long vertical scrolling and merged clutter across all curriculum tabs by introducing intuitive, high-end **Selector Tabs** wherever multi-part data exists in chapter sections.

---

## 2. Comprehensive Page-by-Page Selector Tabs Plan

### A. Question Papers Tab (`QuestionPapersComponent.tsx`) — *Already Implemented*
- **Structure**: Dual-tier tabs (`Set 1, Set 2, Set 3...` top tier; `Section A, Section B, Section C...` bottom tier).
- **Benefit**: Zero long scrolling; clean paper-by-paper and section-by-section focus.

### B. Master Practice Tab (`MasterComponent.tsx` / Subject Master Components)
- **Multi-Part Data**: Master practice contains multiple distinct sections (Summary, Vocabulary Matrix, Stanza/Concept Explanations, Character Sketches, Grammar Practice, and Question Bank Categories).
- **Proposed Selector Tabs**:
  - Tab Bar: `📖 Summary & Theme` | `📚 Vocabulary` | `⚡ Concept Analysis` | `✍️ Grammar & Practice` | `📋 Question Bank`.
- **Benefit**: Students can navigate between master study units instantly without scrolling past lengthy text blocks.

### C. Notes Tab (`NotesComponent.tsx` / Subject Notes Components)
- **Multi-Part Data**: Notes contain chapter overviews, detailed section breakdowns, formulas/rules, glossary terms, and real-world applications.
- **Proposed Selector Tabs**:
  - Tab Bar: `Overview & Theme` | `Core Concepts` | `Formulas & Rules` | `Glossary & Terms` | `Applications`.
- **Benefit**: Clean chunking of dense textbook notes into bite-sized, digestible tabs.

### D. Flashcards Tab (`FlashcardsComponent.tsx`)
- **Multi-Part Data**: Decks of 20+ flashcards.
- **Proposed Selector Tabs**:
  - Category Filter Pills: `All Cards` | `Literature / Concepts` | `Vocabulary` | `Grammar` | `Review Queue`.
- **Benefit**: Allows students to filter flashcards by specific conceptual categories.

---

## 3. Implementation Protocol
- **Zero Data Impact**: All selector tabs operate purely in the frontend presentation state layer (`useState`). Authoritative JSON files and backend APIs remain 100% untouched.
- **Action**: Awaiting your approval before executing code changes.
