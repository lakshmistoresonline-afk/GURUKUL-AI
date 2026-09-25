package com.gurukul.ai.lms

import com.gurukul.ai.lms.engine.SpacedRepetitionScheduler
import com.gurukul.ai.lms.models.LeitnerBox
import org.junit.Assert.*
import org.junit.Test

/**
 * Unit Test Suite for SM-2 Spaced Repetition Algorithm Calculations.
 */
class Sm2AlgorithmTest {

    @Test
    fun testFirstReviewCorrectResponse() {
        val result = SpacedRepetitionScheduler.calculateNextReview(
            currentRepetitionCount = 0,
            currentIntervalDays = 0,
            currentEasinessFactor = 2.5f,
            qualityRating = 4 // Good recall
        )

        assertEquals(1, result.repetitionCount)
        assertEquals(1, result.intervalDays)
        assertEquals(2.5f, result.easinessFactor, 0.01f)
        assertEquals(LeitnerBox.BOX_1_NEW, result.leitnerBox)
    }

    @Test
    fun testSecondReviewPerfectResponse() {
        val result = SpacedRepetitionScheduler.calculateNextReview(
            currentRepetitionCount = 1,
            currentIntervalDays = 1,
            currentEasinessFactor = 2.5f,
            qualityRating = 5 // Perfect recall
        )

        assertEquals(2, result.repetitionCount)
        assertEquals(6, result.intervalDays)
        assertTrue(result.easinessFactor > 2.5f)
        assertEquals(LeitnerBox.BOX_2_REVIEW, result.leitnerBox)
    }

    @Test
    fun testFailedReviewResetsInterval() {
        val result = SpacedRepetitionScheduler.calculateNextReview(
            currentRepetitionCount = 3,
            currentIntervalDays = 15,
            currentEasinessFactor = 2.6f,
            qualityRating = 1 // Fail / Incorrect
        )

        assertEquals(0, result.repetitionCount)
        assertEquals(1, result.intervalDays)
        assertTrue(result.easinessFactor < 2.6f)
        assertEquals(LeitnerBox.BOX_1_NEW, result.leitnerBox)
    }
}
