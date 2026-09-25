# GURUKUL AI — CLASS 5 PROCESSING CODE INVENTORY

## Code Inventory & Pipeline Responsibility
1. **`ContentLoaderService`** (`backend/src/services/content_loader.py`): Multi-file JSON discovery and lossless fusion across English, Hindi, Maths, and Science.
2. **`EnglishMasterAdapter`** (`backend/src/adapters/english/english_master_adapter.py`): Subject-specific processor for English ensuring 320 flashcards (32/chapter), Master practice sub-categories, vocabulary enrichment, and summary/theme variants.
3. **`HindiMasterAdapter`** (`backend/src/adapters/hindi/hindi_master_adapter.py`): Subject-specific processor for Hindi ensuring stanza-wise explanations, Devanagari grammar, shabdart, shuddhi vartani, and comprehension extracts.
4. **`MathsMasterAdapter`** (`backend/src/adapters/maths/maths_master_adapter.py`): Subject-specific processor for Maths ensuring dynamic counter calculation (`flashcardCount`, `quizCount`).
5. **`ScienceMasterAdapter`** (`backend/src/adapters/science/science_master_adapter.py`): Subject-specific processor for Science ensuring lossless separation of canonical ContentBlocks and stage records.
6. **`SectionRenderer`** (`frontend-nextjs/src/renderers/SectionRenderer.tsx`): Universal rich object renderer for detailed breakdowns, scenes, stanza analysis, grammar cards, and activities.
7. **`StudyQuestionsRenderer`** (`frontend-nextjs/src/renderers/StudyQuestionsRenderer.tsx`): Universal practice question renderer supporting MCQs, Fill-in-the-Blanks, True/False, Match Following, Reading Extracts, and Grammar Exercises.
8. **`FlashcardDeck`** (`frontend-nextjs/src/renderers/FlashcardDeck.tsx`): 3D flip card revision renderer supporting all 1,082 effective flashcards.
9. **`MindMapRenderer`** (`frontend-nextjs/src/renderers/MindMapRenderer.tsx`): Hierarchical concept tree renderer.
10. **`QuizRenderer`** (`frontend-nextjs/src/renderers/QuizRenderer.tsx`): Final assessment stage quiz renderer (strictly last).
