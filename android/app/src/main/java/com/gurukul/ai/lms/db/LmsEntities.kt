package com.gurukul.ai.lms.db

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.gurukul.ai.lms.models.LeitnerBox

/**
 * 1. Room Entity: Local cache for raw and parsed chapter notes.
 */
@Entity(tableName = "chapters_cache")
data class ChapterEntity(
    @PrimaryKey val id: String,
    val subject: String,
    val chapterNumber: Int,
    val title: String,
    val unitTitle: String,
    val payloadJson: String,
    val lastUpdatedTimestamp: Long
)

/**
 * 2. Room Entity: Spaced Repetition Leitner Box progress persistence.
 */
@Entity(tableName = "flashcard_states")
data class FlashcardStateEntity(
    @PrimaryKey val cardId: String,
    val subject: String,
    val chapterId: String,
    val frontText: String,
    val backText: String,
    val leitnerBox: LeitnerBox,
    val lastReviewedAt: Long
)

/**
 * 3. Room Entity: Quiz submission and score history persistence.
 */
@Entity(tableName = "quiz_results")
data class QuizResultEntity(
    @PrimaryKey val quizId: String,
    val subject: String,
    val chapterId: String,
    val score: Int,
    val totalQuestions: Int,
    val percentage: Float,
    val taxonomyBreakdownJson: String,
    val timestamp: Long
)
