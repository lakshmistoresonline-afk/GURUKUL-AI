package com.gurukul.ai.lms

import com.gurukul.ai.lms.etl.Class5EtlPipeline
import org.junit.Assert.*
import org.junit.Test
import java.nio.charset.StandardCharsets

/**
 * Unit Test Suite for Devanagari UTF-8 Integrity and KaTeX Tokenization.
 */
class UnicodeAndLatexParsingTest {

    @Test
    fun testDevanagariUtf8StringRoundtrip() {
        val devanagariText = "किरन - न्याय की कुर्सी - शुद्धि-वर्तनी"
        val rawBytes = devanagariText.toByteArray(StandardCharsets.UTF_8)
        
        val decodedText = Class5EtlPipeline.ingestHindiContent(rawBytes)

        assertEquals(devanagariText, decodedText)
        assertTrue(decodedText.contains("किरन"))
        assertTrue(decodedText.contains("न्याय की कुर्सी"))
    }

    @Test
    fun testKaTexMathTokenExtraction() {
        val rawMathQuestion = "Calculate the sum: $\\frac{1}{2} + \\frac{1}{4}$ in Class 5 Fractions."
        val tokens = Class5EtlPipeline.parseMathsLatexTokens(rawMathQuestion)

        assertNotNull(tokens)
        assertTrue(tokens.isNotEmpty())
        assertTrue(tokens.any { it.contains("[MATH_FORMULA:") })
        assertTrue(tokens.any { it.contains("Calculate the sum:") })
    }
}
