import os

reports_dir = r"D:\GURUKUL\reports"
os.makedirs(reports_dir, exist_ok=True)

design_md = """# GURUKUL AI — STUDENT UX DESIGN SPECIFICATION

## 1. Option C + B Unified Design Tokens

- **Page Background**: Cloud White / Soft Blue-Gray (`#F8FAFC` / `bg-slate-50`)
- **Reading Surfaces**: Pure White (`#FFFFFF`) with subtle border (`border-slate-200`)
- **Main Text**: Deep Charcoal / Very Dark Blue-Gray (`#0F172A` / `text-slate-900`)
- **Primary Accent / Action**: Calm Indigo (`#4F46E5` / `bg-indigo-600`)
- **Secondary Accent**: Soft Sage / Muted Teal (`#0D9488` / `text-teal-600` / `bg-teal-500/10`)
- **Success State**: Soft Green (`#10B981`)
- **Warning State**: Muted Amber (`#F59E0B`)
- **Error State**: Clear Accessible Red (`#EF4444`)

---

## 2. Dashboard Design Specification

```
GURUKUL AI

Good morning, Learner 👋

CONTINUE LEARNING
┌─────────────────────────────────────────────┐
│ Papa's Spectacles                           │
│ English • Unit 1 • Chapter 1                │
│ Continue where you stopped        Continue →│
└─────────────────────────────────────────────┘

YOUR SUBJECTS
[ English ]   [ Hindi ]   [ Maths ]   [ Science ]

YOUR CHAPTERS
Unit 1 — Let's Have Fun
  Papa's Spectacles                       Open Chapter →
  Gone with the Scooter                   Open Chapter →

Unit 2 — My Colourful World
  The Rainbow                             Open Chapter →
  The Wise Parrot                         Open Chapter →
```

---

## 3. Chapter Page Design Specification

```
Papa's Spectacles
English • Unit 1 • Chapter 1

Overview | Learn | Practice | Revision | Quiz

--------------------------------------------------

OVERVIEW
About this chapter
[Short orientation summary]

What you'll learn
[Existing learning objectives]

Key idea
[Existing core takeaway]

                                     Start Learning →

--------------------------------------------------

LEARN
Lesson
[Comfortable readable lesson text]

Concepts
[Core concepts]

Examples
[Step-by-step examples]

Vocabulary
[Expandable word meanings]

                                     Continue →
```

---

## 4. Reading Comfort & Typography
- **Aa Reading Comfort Control**:
  - Text Size: Medium (17px), Large (19px), Extra Large (21px).
  - Line Spacing: Normal (1.5), Comfortable (1.7), Spacious (1.9).
  - Themes: Calm Light (`#F8FAFC`), Warm Reading (`#FFFBEB`), Dark Comfortable (`#020617`).
  - Prose Column Width: $680\text{--}760\text{ px}$ with left alignment.
- **Devanagari Line Padding**: Enforces `lineHeight = 28.sp` / `leading-relaxed` / `leading-loose` to prevent vertical matra clipping (e.g. `किरन`, `न्याय की कुर्सी`).
"""

with open(os.path.join(reports_dir, "GURUKUL_STUDENT_UX_DESIGN.md"), "w", encoding="utf-8") as f:
    f.write(design_md)

with open(r"D:\GURUKUL\GURUKUL_STUDENT_UX_DESIGN.md", "w", encoding="utf-8") as f:
    f.write(design_md)

print("DESIGN COMPLETED! GURUKUL_STUDENT_UX_DESIGN.md generated in D:\\GURUKUL\\reports\\ and D:\\GURUKUL\\")
