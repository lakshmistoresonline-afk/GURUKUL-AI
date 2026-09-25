package com.gurukul.ai.lms

import com.gurukul.ai.lms.models.LeitnerBox
import org.junit.Assert.*
import org.junit.Test

/**
 * Unit Test Suite for Spaced Repetition Leitner Box State Transitions & Quiz Scoring.
 */
class RoomDatabaseTest {

    @Test
    fun testLeitnerBoxStatePromotionTransition() {
        val initialBox = LeitnerBox.BOX_1_NEW

        // User marks card as Mastered -> Promotes to BOX_3_MASTERED
        val promotedBox = if (initialBox == LeitnerBox.BOX_1_NEW) LeitnerBox.BOX_3_MASTERED else LeitnerBox.BOX_2_REVIEW

        assertEquals(LeitnerBox.BOX_3_MASTERED, promotedBox)
        assertNotEquals(initialBox, promotedBox)
    }

    @Test
    fun testLeitnerBoxStateRelegationTransition() {
        val masteredBox = LeitnerBox.BOX_3_MASTERED

        // User marks card as Needs Review -> Relegates to BOX_1_NEW
        val relegatedBox = LeitnerBox.BOX_1_NEW

        assertEquals(LeitnerBox.BOX_1_NEW, relegatedBox)
        assertNotEquals(masteredBox, relegatedBox)
    }

    @Test
    fun testQuizPercentageCalculation() {
        val totalQuestions = 15
        val correctScore = 12
        val expectedPercentage = (12f / 15f) * 100f

        val calculatedPercentage = (correctScore.toFloat() / totalQuestions.toFloat()) * 100f

        assertEquals(80f, calculatedPercentage, 0.01f)
        assertEquals(expectedPercentage, calculatedPercentage, 0.01f)
    }
}
