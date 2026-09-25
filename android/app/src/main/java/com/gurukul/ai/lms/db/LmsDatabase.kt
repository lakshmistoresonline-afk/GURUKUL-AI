package com.gurukul.ai.lms.db

import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.TypeConverters

/**
 * Room Database Definition for Gurukul Class 5 Offline Engine.
 */
@Database(
    entities = [
        ChapterEntity::class,
        FlashcardStateEntity::class,
        QuizResultEntity::class
    ],
    version = 1,
    exportSchema = false
)
abstract class LmsDatabase : RoomDatabase() {
    abstract fun lmsDao(): LmsDao
}
