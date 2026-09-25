package com.gurukul.ai.lms.repository

import com.google.gson.Gson
import com.gurukul.ai.lms.db.*
import com.gurukul.ai.lms.models.*
import com.gurukul.ai.lms.network.LmsApiService
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.withContext

/**
 * Single Source of Truth (SSOT) Repository implementing Offline-First Synchronization.
 * 1. Emits local Room DB cached state immediately.
 * 2. Attempts background fetch from local server bridge (10.0.2.2:8080).
 * 3. On API success, upserts Room DB to trigger UI auto-updates via Kotlin Flow.
 * 4. On network error, gracefully maintains offline Room DB state without UI failure.
 */
class LmsRepository(
    private val dao: LmsDao,
    private val apiService: LmsApiService,
    private val gson: Gson = Gson()
) {

    /**
     * Reactive Stream of Chapter Notes by Subject (SSOT).
     */
    fun getChaptersStream(subject: LmsSubject): Flow<List<ChapterNote>> {
        return dao.getChaptersBySubject(subject.displayName).map { entities ->
            entities.map { entity ->
                ChapterNote(
                    id = entity.id,
                    subject = subject,
                    chapterNumber = entity.chapterNumber,
                    chapterName = entity.title,
                    unitTitle = entity.unitTitle,
                    markdownBody = entity.payloadJson,
                    overviewSummary = "Summary for ${entity.title}",
                    centralTheme = "Central Theme for ${entity.title}"
                )
            }
        }
    }

    /**
     * Background Network Sync Trigger.
     */
    suspend fun syncSubjectFromNetwork(subject: LmsSubject): Result<Unit> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.getSubjectDataset(subject.displayName)
            if (response.isSuccessful && response.body() != null) {
                val dataset = response.body()!!
                val chaptersRaw = (
                    dataset["chapters"] as? List<Map<*, *>> ?:
                    dataset["chapters_master_data"] as? List<Map<*, *>> ?:
                    dataset["chapter_notes"] as? List<Map<*, *>> ?:
                    emptyList()
                )

                val entities = chaptersRaw.mapIndexed { idx, ch ->
                    val chNum = (ch["chapterNumber"] as? Double)?.toInt() ?: (ch["chapter_number"] as? Double)?.toInt() ?: (idx + 1)
                    val chTitle = (ch["chapterTitle"] as? String) ?: (ch["chapter_title"] as? String) ?: "Chapter $chNum"
                    val chId = "G5-${subject.code}-C${chNum.toString().padStart(2, '0')}"

                    ChapterEntity(
                        id = chId,
                        subject = subject.displayName,
                        chapterNumber = chNum,
                        title = chTitle,
                        unitTitle = "Unit ${((chNum - 1) / 3) + 1}",
                        payloadJson = gson.toJson(ch),
                        lastUpdatedTimestamp = System.currentTimeMillis()
                    )
                }

                dao.upsertChapters(entities)
                Result.success(Unit)
            } else {
                Result.failure(Exception("HTTP ${response.code()}: ${response.message()}"))
            }
        } catch (e: Exception) {
            // Offline fallback: maintain Room cache
            Result.failure(e)
        }
    }

    /**
     * Update Spaced Repetition Leitner Box Position for a Flashcard.
     */
    suspend fun updateFlashcardLeitnerBox(
        cardId: String,
        newBox: LeitnerBox
    ) = withContext(Dispatchers.IO) {
        dao.updateLeitnerBox(cardId, newBox, System.currentTimeMillis())
    }

    /**
     * Record Quiz Assessment Result into Local Room DB.
     */
    suspend fun recordQuizResult(
        quizId: String,
        subject: LmsSubject,
        chapterId: String,
        score: Int,
        totalQuestions: Int,
        taxonomyBreakdown: Map<TaxonomyLevel, Int>
    ) = withContext(Dispatchers.IO) {
        val pct = if (totalQuestions > 0) (score.toFloat() / totalQuestions) * 100f else 0f
        val entity = QuizResultEntity(
            quizId = quizId,
            subject = subject.displayName,
            chapterId = chapterId,
            score = score,
            totalQuestions = totalQuestions,
            percentage = pct,
            taxonomyBreakdownJson = gson.toJson(taxonomyBreakdown),
            timestamp = System.currentTimeMillis()
        )
        dao.insertQuizResult(entity)
    }
}
