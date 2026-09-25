package com.gurukul.ai.lms.network

import com.gurukul.ai.lms.models.LmsSubject
import okhttp3.Interceptor
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Path
import retrofit2.http.Query
import java.util.concurrent.TimeUnit

/**
 * Retrofit REST API Interface for Local Server Bridge (10.0.2.2:8080).
 */
interface LmsApiService {

    @GET("api/v1/health")
    suspend fun checkHealth(): Response<Map<String, Any>>

    @GET("api/v1/subjects")
    suspend fun getSubjects(): Response<Map<String, Any>>

    @GET("api/v1/subjects/{subjectName}")
    suspend fun getSubjectDataset(
        @Path("subjectName") subjectName: String
    ): Response<Map<String, Any>>

    @GET("api/v1/subjects/{subjectName}/chapters/{chapterId}")
    suspend fun getChapterPayload(
        @Path("subjectName") subjectName: String,
        @Path("chapterId") chapterId: String
    ): Response<Map<String, Any>>

    companion object {
        // Android Emulator Loopback to Host PC
        const val BASE_URL = "http://10.0.2.2:8080/"

        fun create(authTokenProvider: () -> String?): LmsApiService {
            val authInterceptor = Interceptor { chain ->
                val token = authTokenProvider()
                val requestBuilder = chain.request().newBuilder()
                    .header("Accept", "application/json; charset=utf-8")
                
                if (!token.isNullOrEmpty()) {
                    requestBuilder.header("Authorization", "Bearer $token")
                }
                chain.proceed(requestBuilder.build())
            }

            val logging = HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            }

            val client = OkHttpClient.Builder()
                .addInterceptor(authInterceptor)
                .addInterceptor(logging)
                .connectTimeout(15, TimeUnit.SECONDS)
                .readTimeout(15, TimeUnit.SECONDS)
                .build()

            return Retrofit.Builder()
                .baseUrl(BASE_URL)
                .client(client)
                .addConverterFactory(GsonConverterFactory.create())
                .build()
                .create(LmsApiService::class.java)
        }
    }
}
