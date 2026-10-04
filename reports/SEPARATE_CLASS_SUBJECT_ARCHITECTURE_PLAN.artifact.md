# GURUKUL AI — SEPARATE CLASS & SUBJECT CURRICULUM ARCHITECTURE PLAN

This architecture document defines the blueprint for maintaining strictly isolated, modular processors, loaders, resolvers, and renderers for every class (Class 5, Class 6, Class 7) and every subject (English, Hindi, Maths, Science/EVS, Social Science).

---

## 1. Modular Backend Architecture Map

To ensure zero cross-contamination and 100% schema fidelity per subject and class:

```
backend/src/curriculum/
├── class5/
│   ├── english/ (loader.py, resolver.py, mapper.py, processor.py, validator.py)
│   ├── hindi/   (loader.py, resolver.py, mapper.py, processor.py, validator.py)
│   ├── maths/   (loader.py, resolver.py, mapper.py, processor.py, validator.py)
│   └── science/ (loader.py, resolver.py, mapper.py, processor.py, validator.py)
├── class6/
│   ├── english/ (loader.py, resolver.py, mapper.py, processor.py, validator.py)
│   ├── hindi/   (loader.py, resolver.py, mapper.py, processor.py, validator.py)
│   ├── maths/   (loader.py, resolver.py, mapper.py, processor.py, validator.py)
│   ├── science/ (loader.py, resolver.py, mapper.py, processor.py, validator.py)
│   └── social/  (loader.py, resolver.py, mapper.py, processor.py, validator.py)
└── class7/
    ├── english/ (loader.py, resolver.py, mapper.py, processor.py, validator.py)
    ├── hindi/   (loader.py, resolver.py, mapper.py, processor.py, validator.py)
    ├── mathsi/  (loader.py, resolver.py, mapper.py, processor.py, validator.py)
    ├── mathsii/ (loader.py, resolver.py, mapper.py, processor.py, validator.py)
    ├── science/ (loader.py, resolver.py, mapper.py, processor.py, validator.py)
    ├── sociali/ (loader.py, resolver.py, mapper.py, processor.py, validator.py)
    └── socialii/(loader.py, resolver.py, mapper.py, processor.py, validator.py)
```

---

## 2. Modular Frontend Presentation Components

```
frontend-nextjs/src/components/presentation/
├── Class5/ (English, Hindi, Maths, Science components)
├── Class6/ (English, Hindi, Maths, Science, Social components)
└── Class7/ (English, Hindi, MathsI, MathsII, Science, SocialI, SocialII components)
```

---

## 3. Implementation Blueprint

1. **Dedicated Subject Loaders**: Each subject package inspects its specific JSON files (`Overview.json`, `Notes.json`, `Master.json`, `Flashcards.json`, `Mindmaps.json`, `Quiz.json`, `Question Papers.json`, `Foundational.json`) using isolated schema keys.
2. **Specialized Renderers**: Frontend dynamic routers map incoming subject and grade parameters directly to the corresponding class/subject renderer component, guaranteeing perfect rendering for every tab (*Overview*, *Notes*, *Master Practice*, *Flashcards*, *Mindmaps*, *Quiz*, *Question Papers*, *Foundational Core*).
3. **Build Instruction**: *(Per your instructions, build command execution is deferred for manual execution).*
