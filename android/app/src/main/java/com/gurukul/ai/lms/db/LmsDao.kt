package com.gurukul.ai.lms.db

import androidx.room.*
import com.gurukul.ai.lms.models.LeitnerBox
import kotlinx.coroutines.flow.Flow

/**
 * Room Data Access Object (DAO) for local offline-first caching and state persistence.
 */
@Dao
interface LmsDao {

    // --- CHAPTER CACHE QUERIES ---
    @Query("SELECT * FROM chapters_cache WHERE subject = :subject ORDER BY chapterNumber ASC")
    fun getChaptersBySubject(subject: String): Flow<List<ChapterEntity>>

    @Query("SELECT * FROM chapters_cache WHERE id = :chapterId")
    suspend fun getChapterById(chapterId: String): ChapterEntity?

    @Upsert
    suspend fun upsertChapters(chapters: List<ChapterEntity>)

    // --- FLASHCARD LEITNER QUERIES ---
    @Query("SELECT * FROM flashcard_states WHERE subject = :subject AND chapterId = :chapterId")
    fun getFlashcards(subject: String, chapterId: String): Flow<List<FlashcardStateEntity>>

    @Query("SELECT * FROM flashcard_states WHERE cardId = :cardId")
    suspend fun getFlashcardById(cardId: String): FlashcardStateEntity?

    @Upsert
    suspend fun upsertFlashcardState(flashcard: FlashcardStateEntity)

    @Query("UPDATE flashcard_states SET leitnerBox = :newBox, lastReviewedAt = :timestamp WHERE cardId = :cardId")
    suspend fun updateLeitnerBox(cardId: String, newBox: LeitnerBox, timestamp: Long)

    // --- QUIZ RESULTS QUERIES ---
    @Query("SELECT * FROM quiz_results WHERE subject = :subject ORDER BY timestamp DESC")
    fun getQuizResultsBySubject(subject: String): Flow<List<QuizResultEntity>>

    @Upsert
    suspend fun insertQuizResult(result: QuizResultEntity)
}
