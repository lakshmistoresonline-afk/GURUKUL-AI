# NCERT Learning Guidelines & AI Pedagogy

This document outlines the pedagogical framework for Project Gurukul AI, specifically how the NCERT curriculum mapping interacts with our AI Tutor (Gemini).

## 1. Curriculum Structure
The platform follows the NCERT Class 5 and 6 syllabus exactly as per official textbooks:
- **Class 5:** Mathematics (Math-Magic), EVS (Looking Around), English (Marigold).
- **Class 6:** Mathematics, Science, English (Honeysuckle).

## 2. AI Tutoring Principles (Socratic Method)
Our AI Tutor (`AiTutorService`) is instructed to follow these guidelines:
- **Scaffolding:** If a student asks for an answer, the AI first checks the student's mastery of prerequisites. If prerequisites are weak, the AI provides a hint related to the foundational concept.
- **Inquiry-Based Learning:** Instead of saying "The answer is 10," the AI asks "If you have 2 groups of 5, how many do you have in total?"
- **Textbook Context:** The AI uses examples and terminology found in NCERT textbooks (e.g., mentioning "The Fish Tale" when teaching large numbers in Class 5 Math).

## 3. Learning Objectives Mapping
Each `ConceptNode` includes `learningObjectives`. These objectives are injected into the AI's system prompt to ensure the tutoring remains focused on the curriculum goals:
- **Remembering:** Recall facts and basic concepts.
- **Understanding:** Explain ideas or concepts.
- **Applying:** Use information in new situations.

## 4. OCR Integration
When a student scans a question from a physical NCERT textbook:
1. The `OcrService` extracts the text.
2. The `AiTutorChatScreen` receives the text as an `initialQuery`.
3. The AI analyzes the text, identifies the relevant NCERT topic, and begins a Socratic dialogue to help the student solve it.

## 5. Continuous Improvement
As students interact with the platform, their `Mastery` data is used to further refine the AI's responses, ensuring that the difficulty level is always "just right" (Zone of Proximal Development).
