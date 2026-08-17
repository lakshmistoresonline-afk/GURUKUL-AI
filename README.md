# Project Gurukul AI

Project Gurukul AI is a production-ready AI-powered learning platform designed for CBSE/NCERT students, starting with Class 5 and 6. It is built upon the **Sunbird ED** foundation to ensure scalability, interoperability, and high-quality educational standards.

## Key Features
- **AI Tutor:** Personalized learning companion powered by Gemini and RAG.
- **Knowledge Graph:** Deep mapping of concepts for NCERT curriculum.
- **Adaptive Learning:** Tailored study plans based on student mastery.
- **Grounded Learning:** Directly integrated with DIKSHA resources and supplementary videos.
- **Modern Web Interface:** Fast, responsive Next.js frontend.
- **Hardened Backend:** High-performance FastAPI backend with multimodal RAG capabilities.

## Technology Stack
- **Frontend:** React (Next.js 14)
- **Backend:** Python (FastAPI, SQLAlchemy)
- **AI:** Google Gemini, Ollama (Local Inference), OpenAI Whisper (Transcriptions)
- **Database:** SQLite (with aiosqlite for async performance)
- **Styling:** Tailwind CSS, Lucide Icons

## Project Structure
- `frontend-nextjs/`: The student and admin web application.
- `backend/`: AI orchestration, curriculum discovery, and RAG services.
- `datasets/`: Authoritative NCERT curriculum manifests and processed content.

## Getting Started
See [RUN_GUIDE.md](RUN_GUIDE.md) for installation and execution steps.

## Documentation
- [Final Release Summary](GURUKUL_FINAL_RELEASE_SUMMARY.md)
- [Architecture & Technology Report](COMPLETE_PROJECT_ARCHITECTURE_AND_TECHNOLOGY_REPORT.md)
- [DIKSHA Integration Report](DIKSHA_GURUKUL_INTEGRATION_REPORT.md)
- [API Documentation](API_DOCUMENTATION.md)
