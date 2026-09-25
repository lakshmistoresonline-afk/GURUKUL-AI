package com.gurukul.ai.lms.etl

import com.gurukul.ai.lms.models.*
import java.nio.charset.StandardCharsets

/**
 * Class 5 Subject-Specific ETL Ingestion Pipeline Rules.
 */
object Class5EtlPipeline {

    /**
     * 1. Hindi (Devanagari) UTF-8 Ingestion.
     * Ensures strict UTF-8 string encoding when parsing notes (e.g. Veena & NCERT master sets)
     * and flashcards to preserve script integrity without Mojibake corruption.
     */
    fun ingestHindiContent(rawJsonBytes: ByteArray): String {
        return String(rawJsonBytes, StandardCharsets.UTF_8)
    }

    /**
     * 2. Maths KaTeX / LaTeX Tokenization.
     * Parses KaTeX string variables from quiz questions and step-by-step reasoning blocks
     * into renderable Compose text tokens.
     */
    fun parseMathsLatexTokens(rawLatexQuestion: String): List<String> {
        val regex = Regex("""\$([^$]+)\$""")
        val tokens = mutableListOf<String>()
        var lastIndex = 0

        regex.findAll(rawLatexQuestion).forEach { matchResult ->
            if (matchResult.range.first > lastIndex) {
                tokens.add(rawLatexQuestion.substring(lastIndex, matchResult.range.first))
            }
            tokens.add("[MATH_FORMULA: ${matchResult.groupValues[1]}]")
            lastIndex = matchResult.range.last + 1
        }

        if (lastIndex < rawLatexQuestion.length) {
            tokens.add(rawLatexQuestion.substring(lastIndex))
        }

        return tokens.ifEmpty { listOf(rawLatexQuestion) }
    }

    /**
     * 3. English & Science (EVS) Pedagogy Ref ID Linking.
     * Links pedagogy objectives from `santoor_pedagogy_master_v2` directly to corresponding
     * chapter notes, flashcards, and mindmap graph root nodes.
     */
    fun linkPedagogyRefId(
        note: ChapterNote,
        pedagogyMaster: List<PedagogyGuide>
    ): ChapterNote {
        val matchedGuide = pedagogyMaster.firstOrNull { it.unitTitle == note.unitTitle }
        return note.copy(pedagogyRefId = matchedGuide?.id ?: "CG_DEFAULT")
    }
}
