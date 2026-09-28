# GURUKUL AI — HINDI SUBJECT DEEP ANALYSIS & ENHANCEMENT PLAN

## 1. Executive Summary
This report analyzes Hindi curriculum subjects across Class 5 and Class 6, verifying schema alignment, Devanagari typography rendering, sub-section selector tabs, and unmerged question paper displays.

---

## 2. Identified Hindi-Specific Gaps & Proposed Solutions

### A. Hindi Notes Component (`HindiNotesComponent.tsx` & `Class6HindiNotesComponent.tsx`)
- **Gap**: Hindi notes require dedicated sub-section selector tabs (`📖 सारांश एवं भावार्थ` | `📚 शब्दार्थ एवं पर्यायवाची` | `✍️ व्याकरण अभ्यास` | `📋 प्रश्न-उत्तर`) to match the unmerged tabbed design of English and Science.
- **Proposed Solution**: Embed sub-section selector tabs inside Hindi notes and master practice views.

### B. Hindi Master Practice Component (`HindiMasterComponent.tsx` & `Class6HindiMasterComponent.tsx`)
- **Gap**: Master views for Hindi poetry and prose need structured breakdown cards for central themes (`केंद्रीय भाव`), word meanings (`शब्दार्थ`), and grammar (`भाषा की बात`).
- **Proposed Solution**: Ensure Devanagari typography styling and clean card separation.

### C. Hindi Mindmaps (`HindiMasterComponent` / `Class6HindiMindmapComponent`)
- **Gap**: Hindi mindmaps require the same node tree traversal (`central_theme` and `branches` with sub-branches) as English and Maths.

---

## 3. Action Plan (Zero Data Impact)
- All enhancements are strictly frontend presentation improvements. No authoritative JSON files or backend processors will be modified.
- Awaiting your approval to implement these Hindi enhancements.
