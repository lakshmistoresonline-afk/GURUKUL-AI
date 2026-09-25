package com.gurukul.ai.lms.models

import androidx.compose.runtime.Immutable
import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Supported Class 5 Subject Taxonomy.
 */
enum class LmsSubject(val displayName: String, val code: String) {
    ENGLISH("English", "ENG"),
    HINDI("Hindi (हिंदी)", "HIN"),
    MATHS("Mathematics", "MAT"),
    SCIENCE("Science / EVS", "SCI")
}

/**
 * Spaced Repetition Leitner Box Classification.
 */
enum class LeitnerBox {
    BOX_1_NEW,
    BOX_2_REVIEW,
    BOX_3_MASTERED
}

/**
 * Bloom's Taxonomy Cognitive Complexity Rating.
 */
enum class TaxonomyLevel {
    REMEMBER,
    UNDERSTAND,
    APPLY,
    ANALYZE,
    EVALUATE,
    CREATE
}

/**
 * Room Entity: Flashcard Spaced Repetition State Persistence.
 */
@Entity(tableName = "flashcard_states")
data class FlashcardStateEntity(
    @PrimaryKey val flashcardId: String,
    val subjectCode: String,
    val chapterId: String,
    val leitnerBox: LeitnerBox,
    val lastReviewedTimestamp: Long,
    val reviewCount: Int
)

/**
 * Room Entity: Quiz Scoring History Persistence.
 */
@Entity(tableName = "quiz_scores")
data class QuizScoreEntity(
    @PrimaryKey val scoreRecordId: String,
    val subjectCode: String,
    val chapterId: String,
    val scoreAchieved: Int,
    val totalQuestions: Int,
    val percentage: Float,
    val timestamp: Long
)

/**
 * 1. Master Chapter Note Domain Model.
 */
@Immutable
data class ChapterNote(
    val id: String,
    val subject: LmsSubject,
    val chapterNumber: Int,
    val chapterName: String,
    val unitTitle: String,
    val markdownBody: String,
    val overviewSummary: String,
    val centralTheme: String,
    val keyTerms: List<KeyTerm> = emptyList(),
    val pedagogyRefId: String? = null
)

@Immutable
data class KeyTerm(
    val term: String,
    val definition: String,
    val usageExample: String? = null,
    val synonyms: List<String> = emptyList(),
    val antonyms: List<String> = emptyList(),
    val ashuddhCorrection: String? = null
)

/**
 * 2. Interactive Flashcard Domain Model.
 */
@Immutable
data class Flashcard(
    val id: String,
    val subject: LmsSubject,
    val chapterId: String,
    val frontText: String,
    val backText: String,
    val difficulty: String = "Medium",
    val leitnerBox: LeitnerBox = LeitnerBox.BOX_1_NEW
)

/**
 * 3. Concept Mindmap Graph Domain Model.
 */
@Immutable
data class MindmapNode(
    val id: String,
    val label: String,
    val parentId: String? = null,
    val category: String = "Core Concept",
    val isExpanded: Boolean = true,
    val xPosition: Float = 0f,
    val yPosition: Float = 0f
)

@Immutable
data class MindmapEdge(
    val fromNodeId: String,
    val toNodeId: String,
    val relationshipLabel: String? = null
)

@Immutable
data class Mindmap(
    val id: String,
    val subject: LmsSubject,
    val chapterId: String,
    val rootTitle: String,
    val nodes: List<MindmapNode>,
    val edges: List<MindmapEdge> = emptyList()
)

/**
 * 4. Question / Quiz Bank Domain Model.
 */
@Immutable
data class QuizQuestion(
    val id: String,
    val subject: LmsSubject,
    val chapterId: String,
    val questionText: String,
    val options: List<String>,
    val correctAnswerIndex: Int,
    val explanation: String,
    val taxonomyLevel: TaxonomyLevel = TaxonomyLevel.UNDERSTAND,
    val containsLatex: Boolean = false,
    val formattedLatexTokens: List<String> = emptyList()
)

/**
 * 5. Pedagogical Guide Domain Model.
 */
@Immutable
data class PedagogyGuide(
    val id: String,
    val subject: LmsSubject,
    val unitTitle: String,
    val curriculumCode: String,
    val learningObjectives: List<String>,
    val teachingTips: List<String>,
    val bloomTargets: List<TaxonomyLevel> = emptyList()
)
