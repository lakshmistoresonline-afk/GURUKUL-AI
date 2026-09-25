package com.gurukul.ai.lms.engine

import com.gurukul.ai.lms.db.FlashcardStateEntity
import com.gurukul.ai.lms.models.LeitnerBox
import kotlin.math.max

/**
 * SuperMemo-2 (SM-2) Spaced Repetition Scheduler Engine.
 * Computes card review intervals, easiness factors, and next due dates
 * based on user recall quality ratings (0 to 5).
 */
data class Sm2Result(
    val intervalDays: Int,
    val repetitionCount: Int,
    val easinessFactor: Float,
    val nextReviewDueDate: Long,
    val leitnerBox: LeitnerBox
)

object SpacedRepetitionScheduler {

    const val DEFAULT_EASINESS_FACTOR = 2.5f
    const val ONE_DAY_MS = 86_400_000L

    /**
     * Computes next review schedule using the SM-2 algorithm.
     * @param qualityRating 0..5 (0-2: Fail, 3: Hard, 4: Good, 5: Easy)
     */
    fun calculateNextReview(
        currentRepetitionCount: Int,
        currentIntervalDays: Int,
        currentEasinessFactor: Float,
        qualityRating: Int,
        currentTimestamp: Long = System.currentTimeMillis()
    ): Sm2Result {
        val rating = qualityRating.coerceIn(0, 5)

        // 1. Calculate new Easiness Factor (EF)
        // EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        val newEf = max(
            1.3f,
            currentEasinessFactor + (0.1f - (5 - rating) * (0.08f + (5 - rating) * 0.02f))
        )

        // 2. Calculate Repetitions and Interval Days
        val (newReps, newInterval) = if (rating >= 3) {
            when (currentRepetitionCount) {
                0 -> 1 to 1
                1 -> 2 to 6
                else -> (currentRepetitionCount + 1) to (currentIntervalDays * newEf).toInt()
            }
        } else {
            // Incorrect response / Reset interval to 1 day
            0 to 1
        }

        val dueDate = currentTimestamp + (newInterval * ONE_DAY_MS)

        val newBox = when {
            newInterval >= 14 -> LeitnerBox.BOX_3_MASTERED
            newInterval >= 3 -> LeitnerBox.BOX_2_REVIEW
            else -> LeitnerBox.BOX_1_NEW
        }

        return Sm2Result(
            intervalDays = newInterval,
            repetitionCount = newReps,
            easinessFactor = newEf,
            nextReviewDueDate = dueDate,
            leitnerBox = newBox
        )
    }
}
