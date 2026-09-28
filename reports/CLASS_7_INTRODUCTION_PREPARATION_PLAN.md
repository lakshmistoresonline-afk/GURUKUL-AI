# GURUKUL AI — CLASS 7 INTRODUCTION & PREPARATION PLAN (MULTI-BOOK ARCHITECTURE)

## 1. Executive Summary
This document provides an updated architectural plan for introducing **Class 7**, specifically accommodating the NCERT dual-textbook curriculum structure where Mathematics and Social Science are divided into **Maths I & Maths II** and **Social I & Social II**.

**Constraint Compliance**: As instructed, **no code changes or file modifications have been made**. This report is for planning and analysis only.

---

## 2. Updated Subject Directory Structure (`Contents/Class 7/`)
To handle dual-textbook subjects without naming collisions, subject directories will be explicitly mapped as separate curriculum entities:
```text
Contents/
└── Class 7/
    ├── English/
    ├── Hindi/
    ├── Maths I/
    ├── Maths II/
    ├── Science/
    ├── Social I/
    └── Social II/
```

---

## 3. Detailed Preparation Roadmap

### Step 1: Backend Subject Discovery & Routing
- Update FastAPI discovery endpoints (`discover_classes`, `get_grade_subjects`) to recognize `Maths I`, `Maths II`, `Social I`, and `Social II` as independent, first-class subjects under Class 7.

### Step 2: Modular Class 7 Backend Package (`backend/src/curriculum/class7/`)
- Create isolated package subdirectories corresponding to each book:
  - `class7/english/`
  - `class7/hindi/`
  - `class7/maths_i/`
  - `class7/maths_ii/`
  - `class7/science/`
  - `class7/social_i/`
  - `class7/social_ii/`
- Each subpackage will have its own independent loader, chapter resolver, and processor, ensuring zero cross-contamination.

### Step 3: Frontend Subject Selector & Icons (`page.tsx`)
- Update frontend subject selector configuration to display dual-book subjects clearly:
  - **Maths I** & **Maths II** (📐)
  - **Social I** (History 🏛️) & **Social II** (Civics/Geography 🌍)

---

## 4. Conclusion
- This multi-book design guarantees 100% data fidelity with NCERT Class 7 textbooks while preserving complete architectural independence per book.
