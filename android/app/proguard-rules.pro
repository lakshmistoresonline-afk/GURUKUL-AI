# Gurukul AI LMS Production R8 / ProGuard Obfuscation & Retention Rules

# Preserve Domain Models & Data Transfer Objects
-keep class com.gurukul.ai.lms.models.** { *; }
-keepclassmembers class com.gurukul.ai.lms.models.** { *; }

# Preserve Retrofit API Interfaces & Interceptors
-keep class com.gurukul.ai.lms.network.** { *; }
-keepclassmembers class com.gurukul.ai.lms.network.** { *; }

# Preserve Room DB Entities, DAOs, & Migrations
-keep class com.gurukul.ai.lms.db.** { *; }
-keepclassmembers class com.gurukul.ai.lms.db.** { *; }

# Preserve Gson Serialization Annotations & Fields
-keepattributes Signature, *Annotation*, EnclosingMethod, InnerClasses
-keepclassmembers class * {
    @com.google.gson.annotations.SerializedName <fields>;
}

# Preserve WebView KaTeX JavaScript Interface & WebClients
-keepclassmembers class * extends android.webkit.WebViewClient {
    public void *(...);
}
-keepclassmembers class * extends android.webkit.WebChromeClient {
    public void *(...);
}

# Preserve Kotlin Coroutines
-keep class kotlinx.coroutines.** { *; }

# Preserve Firebase Auth SDK
-keep class com.google.firebase.auth.** { *; }
