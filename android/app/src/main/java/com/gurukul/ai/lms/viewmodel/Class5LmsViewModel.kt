package com.gurukul.ai.lms.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.gurukul.ai.lms.models.*
import com.gurukul.ai.lms.ui.DashboardTab
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

/**
 * Sealed Interface for Unidirectional Data Flow (UDF) Dashboard UI State.
 */
sealed interface LmsUiState {
    object Loading : LmsUiState
    data class Error(val message: String) : LmsUiState
    data class Success(
        val selectedSubject: LmsSubject,
        val activeTab: DashboardTab,
        val chapterNote: ChapterNote,
        val flashcards: List<Flashcard>,
        val mindmap: Mindmap,
        val quizQuestions: List<QuizQuestion>,
        val pedagogyGuides: List<PedagogyGuide>,
        val currentQuizIndex: Int = 0,
        val quizScore: Int = 0,
        val selectedQuizAnswers: Map<Int, Int> = emptyMap()
    ) : LmsUiState
}

/**
 * Class 5 LMS ViewModel Architecture.
 * Manages UDF state flow, subject switching, tab navigation, Leitner box updates, and quiz score tracking.
 */
class Class5LmsViewModel : ViewModel() {

    private val _uiState = MutableStateFlow<LmsUiState>(LmsUiState.Loading)
    val uiState: StateFlow<LmsUiState> = _uiState.asStateFlow()

    init {
        selectSubject(LmsSubject.ENGLISH)
    }

    /**
     * Switch Active Subject and Reload Catalog Data.
     */
    fun selectSubject(subject: LmsSubject) {
        viewModelScope.launch {
            _uiState.value = LmsUiState.Loading
            loadSubjectData(subject, DashboardTab.NOTES)
        }
    }

    /**
     * Switch Active Dashboard Tab.
     */
    fun selectTab(tab: DashboardTab) {
        val currentState = _uiState.value
        if (currentState is LmsUiState.Success) {
            _uiState.value = currentState.copy(activeTab = tab)
        }
    }

    /**
     * Update Spaced Repetition Leitner Box State for a Flashcard.
     */
    fun updateFlashcardLeitner(flashcardId: String, newBox: LeitnerBox) {
        val currentState = _uiState.value
        if (currentState is LmsUiState.Success) {
            val updatedFlashcards = currentState.flashcards.map { card ->
                if (card.id == flashcardId) card.copy(leitnerBox = newBox) else card
            }
            _uiState.value = currentState.copy(flashcards = updatedFlashcards)
        }
    }

    /**
     * Answer a Quiz Question and Update Score.
     */
    fun answerQuizQuestion(questionIndex: Int, optionIndex: Int) {
        val currentState = _uiState.value
        if (currentState is LmsUiState.Success) {
            if (!currentState.selectedQuizAnswers.containsKey(questionIndex)) {
                val isCorrect = optionIndex == currentState.quizQuestions[questionIndex].correctAnswerIndex
                val newScore = if (isCorrect) currentState.quizScore + 1 else currentState.quizScore
                val updatedAnswers = currentState.selectedQuizAnswers + (questionIndex to optionIndex)

                _uiState.value = currentState.copy(
                    quizScore = newScore,
                    selectedQuizAnswers = updatedAnswers,
                    currentQuizIndex = (questionIndex + 1).coerceAtMost(currentState.quizQuestions.size - 1)
                )
            }
        }
    }

    /**
     * Ingest and Load Subject Domain Models.
     */
    private fun loadSubjectData(subject: LmsSubject, activeTab: DashboardTab) {
        viewModelScope.launch {
            try {
                val sampleNote = ChapterNote(
                    id = "G5-${subject.code}-C01",
                    subject = subject,
                    chapterNumber = 1,
                    chapterName = when (subject) {
                        LmsSubject.ENGLISH -> "Papa’s Spectacles"
                        LmsSubject.HINDI -> "किरन"
                        LmsSubject.MATHS -> "Travelling, Now and Then"
                        LmsSubject.SCIENCE -> "Water — The Essence of Life"
                    },
                    unitTitle = "Unit 1",
                    markdownBody = "Full structured chapter text...",
                    overviewSummary = "Comprehensive overview summary for ${subject.displayName} Chapter 1.",
                    centralTheme = "Core thematic learning outcomes and ethical values."
                )

                val sampleFlashcards = listOf(
                    Flashcard("f1", subject, "C01", "Key Term 1", "Definition for Term 1", leitnerBox = LeitnerBox.BOX_1_NEW),
                    Flashcard("f2", subject, "C01", "Key Term 2", "Definition for Term 2", leitnerBox = LeitnerBox.BOX_1_NEW)
                )

                val sampleMindmap = Mindmap(
                    id = "mm1",
                    subject = subject,
                    chapterId = "C01",
                    rootTitle = sampleNote.chapterName,
                    nodes = listOf(
                        MindmapNode("n1", sampleNote.chapterName, null, "Root"),
                        MindmapNode("n2", "Grammar & Methods", "n1", "Grammar Focus"),
                        MindmapNode("n3", "Practical Tasks", "n1", "Activities")
                    )
                )

                val sampleQuestions = listOf(
                    QuizQuestion(
                        id = "q1",
                        subject = subject,
                        chapterId = "C01",
                        questionText = "What is the primary theme of Chapter 1?",
                        options = listOf("Option A", "Option B", "Option C", "Option D"),
                        correctAnswerIndex = 0,
                        explanation = "Step-by-step solution explaining Option A.",
                        taxonomyLevel = TaxonomyLevel.UNDERSTAND,
                        containsLatex = subject == LmsSubject.MATHS,
                        formattedLatexTokens = if (subject == LmsSubject.MATHS) listOf("$$\\frac{1}{2} + \\frac{1}{4} = \\frac{3}{4}$$") else emptyList()
                    )
                )

                val sampleGuides = listOf(
                    PedagogyGuide(
                        id = "pg1",
                        subject = subject,
                        unitTitle = "Unit 1 Curriculum Framework",
                        curriculumCode = "CG1",
                        learningObjectives = listOf("Develop oral fluency and expression", "Enhance text comprehension"),
                        teachingTips = listOf("Facilitate interactive group discussions", "Utilize concept mindmaps")
                    )
                )

                _uiState.value = LmsUiState.Success(
                    selectedSubject = subject,
                    activeTab = activeTab,
                    chapterNote = sampleNote,
                    flashcards = sampleFlashcards,
                    mindmap = sampleMindmap,
                    quizQuestions = sampleQuestions,
                    pedagogyGuides = sampleGuides
                )
            } catch (e: Exception) {
                _uiState.value = LmsUiState.Error("Failed to load ${subject.displayName} content: ${e.message}")
            }
        }
    }
}
