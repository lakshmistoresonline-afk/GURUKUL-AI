package com.gurukul.ai.lms.network

import okhttp3.Interceptor
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

/**
 * Local PC Debug Retrofit Client.
 * Targets Local PC FastAPI Server running on `0.0.0.0:8080` (Emulator Loopback: `http://10.0.2.2:8080/`).
 * Features dynamic LAN IP fallback, HttpLoggingInterceptor (Level.BODY), and offline debug auth token injection.
 */
object RetrofitClient {

    // Default Emulator Loopback URL
    const val DEFAULT_EMULATOR_URL = "http://10.0.2.2:8080/"

    // Dynamic Wi-Fi LAN IP Override (for USB/Wi-Fi physical device debug)
    private var dynamicBaseUrl: String = DEFAULT_EMULATOR_URL

    fun setCustomLanIp(lanIp: String, port: Int = 8080) {
        dynamicBaseUrl = "http://$lanIp:$port/"
    }

    private fun createOkHttpClient(debugToken: String = "LOCAL_DEV_USER"): OkHttpClient {
        val authInterceptor = Interceptor { chain ->
            val request = chain.request().newBuilder()
                .header("Accept", "application/json; charset=utf-8")
                .header("Authorization", "Bearer $debugToken")
                .build()
            chain.proceed(request)
        }

        val loggingInterceptor = HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        }

        return OkHttpClient.Builder()
            .addInterceptor(authInterceptor)
            .addInterceptor(loggingInterceptor)
            .connectTimeout(15, TimeUnit.SECONDS)
            .readTimeout(15, TimeUnit.SECONDS)
            .writeTimeout(15, TimeUnit.SECONDS)
            .build()
    }

    fun getApiService(baseUrlOverride: String? = null): LmsApiService {
        val targetUrl = baseUrlOverride ?: dynamicBaseUrl
        return Retrofit.Builder()
            .baseUrl(targetUrl)
            .client(createOkHttpClient())
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(LmsApiService::class.java)
    }
}
