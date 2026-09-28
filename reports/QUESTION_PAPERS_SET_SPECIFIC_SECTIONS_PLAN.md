# GURUKUL AI — QUESTION PAPERS SET-SPECIFIC SECTIONS PLAN

## 1. Objective
To ensure that when a user switches between Question Paper Sets (**Set 1, Set 2, Set 3, etc.**), the available **Section Selector Tabs** (and their corresponding questions) update dynamically to reflect **only the sections belonging to that specific set**.

---

## 2. Technical Analysis & Proposed Fix (`QuestionPapersComponent.tsx`)

### Current Behavior:
- The component currently extracts sections from `currentPaper = papers[activePaperIdx]`.
- However, if state handling or section indexing is global across sets, switching sets might retain previous section indices or assume static section titles.

### Proposed Dynamic Binding Plan:
1. **Set-Specific Section Extraction**:
   - When `activePaperIdx` changes, `activeSectionIdx` automatically resets to `0`.
   - `sections` are derived exclusively from `papers[activePaperIdx]?.sections || []`.
2. **Dynamic Section Tabs**:
   - The section tabs re-render using *only* the sections defined in the currently selected set (`Set 1`, `Set 2`, etc.).
3. **Data Safety**:
   - Zero changes to backend data schemas or persistent JSON files. Pure frontend state isolation per set.

---

## 4. Action
Awaiting your approval before implementing this set-specific section binding in `QuestionPapersComponent.tsx`.
