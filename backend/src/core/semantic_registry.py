from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class ContentTypeDefinition(BaseModel):
    semanticType: str
    learningStage: str          # 'overview', 'learn', 'practice', 'revision', 'assessment'
    presentationSection: str    # 'overview', 'learn', 'practice', 'flashcards', 'mindmap', 'quiz'
    rendererKey: str            # React renderer key
    assessmentRole: str = "practice"  # 'practice' vs 'final'
    supportsChapterScope: bool = True
    supportsUnitScope: bool = True
    supportsCurriculumScope: bool = True
    ordering: int = 10

class SemanticContentRegistry:
    """
    Central universal registry mapping semantic content types to learning stages,
    presentation sections, and renderer keys independently of source file names.
    """

    _registry: Dict[str, ContentTypeDefinition] = {
        "overview": ContentTypeDefinition(
            semanticType="overview",
            learningStage="overview",
            presentationSection="overview",
            rendererKey="overview",
            ordering=10
        ),
        "keyTerminology": ContentTypeDefinition(
            semanticType="keyTerminology",
            learningStage="learn",
            presentationSection="learn",
            rendererKey="terminology",
            ordering=20
        ),
        "terminology": ContentTypeDefinition(
            semanticType="terminology",
            learningStage="learn",
            presentationSection="learn",
            rendererKey="terminology",
            ordering=20
        ),
        "vocabulary": ContentTypeDefinition(
            semanticType="vocabulary",
            learningStage="learn",
            presentationSection="learn",
            rendererKey="vocabulary",
            ordering=25
        ),
        "detailedBreakdown": ContentTypeDefinition(
            semanticType="detailedBreakdown",
            learningStage="learn",
            presentationSection="learn",
            rendererKey="text-section",
            ordering=30
        ),
        "importantTakeaways": ContentTypeDefinition(
            semanticType="importantTakeaways",
            learningStage="learn",
            presentationSection="learn",
            rendererKey="text-section",
            ordering=40
        ),
        "studyQuestions": ContentTypeDefinition(
            semanticType="studyQuestions",
            learningStage="practice",
            presentationSection="practice",
            rendererKey="study-questions",
            assessmentRole="practice",
            ordering=50
        ),
        "fill_in_the_blanks": ContentTypeDefinition(
            semanticType="fill_in_the_blanks",
            learningStage="practice",
            presentationSection="practice",
            rendererKey="fill_in_the_blanks",
            assessmentRole="practice",
            ordering=55
        ),
        "master_testbank": ContentTypeDefinition(
            semanticType="master_testbank",
            learningStage="practice",
            presentationSection="practice",
            rendererKey="study-questions",
            assessmentRole="practice",
            ordering=58
        ),
        "model_question_bank": ContentTypeDefinition(
            semanticType="model_question_bank",
            learningStage="practice",
            presentationSection="practice",
            rendererKey="study-questions",
            assessmentRole="practice",
            ordering=59
        ),
        "flashcards": ContentTypeDefinition(
            semanticType="flashcards",
            learningStage="revision",
            presentationSection="flashcards",
            rendererKey="flashcard-deck",
            ordering=70
        ),
        "flashcard": ContentTypeDefinition(
            semanticType="flashcard",
            learningStage="revision",
            presentationSection="flashcards",
            rendererKey="flashcard-deck",
            ordering=70
        ),
        "mindmap": ContentTypeDefinition(
            semanticType="mindmap",
            learningStage="revision",
            presentationSection="mindmap",
            rendererKey="mindmap",
            ordering=80
        ),
        "quiz": ContentTypeDefinition(
            semanticType="quiz",
            learningStage="assessment",
            presentationSection="quiz",
            rendererKey="quiz",
            assessmentRole="final",
            ordering=90
        ),
        "unknown": ContentTypeDefinition(
            semanticType="unknown",
            learningStage="learn",
            presentationSection="generic",
            rendererKey="generic-structured",
            ordering=999
        ),
    }

    @classmethod
    def register(cls, definition: ContentTypeDefinition):
        cls._registry[definition.semanticType] = definition

    @classmethod
    def get_definition(cls, semantic_type: str) -> ContentTypeDefinition:
        return cls._registry.get(semantic_type, cls._registry["unknown"])

    @classmethod
    def list_all(cls) -> Dict[str, ContentTypeDefinition]:
        return cls._registry
