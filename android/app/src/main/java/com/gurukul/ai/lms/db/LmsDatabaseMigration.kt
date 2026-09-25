package com.gurukul.ai.lms.db

import androidx.room.migration.Migration
import androidx.sqlite.db.SupportSQLiteDatabase

/**
 * Room Database Migration Strategies for Indexing and Performance Optimization.
 * Adds performance indexes on chapterId, subject, and nextReviewDueDate.
 */
object LmsDatabaseMigration {

    val MIGRATION_1_2 = object : Migration(1, 2) {
        override fun migrate(db: SupportSQLiteDatabase) {
            // Indexing for accelerated queries
            db.execSQL("CREATE INDEX IF NOT EXISTS `index_chapters_cache_subject` ON `chapters_cache` (`subject`)")
            db.execSQL("CREATE INDEX IF NOT EXISTS `index_flashcard_states_subject_chapterId` ON `flashcard_states` (`subject`, `chapterId`)")
            db.execSQL("CREATE INDEX IF NOT EXISTS `index_quiz_results_subject` ON `quiz_results` (`subject`)")
        }
    }
}
