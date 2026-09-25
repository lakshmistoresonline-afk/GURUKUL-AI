package com.gurukul.ai.lms.network

import com.google.gson.Gson
import okhttp3.*
import java.util.concurrent.TimeUnit
import kotlin.math.pow

/**
 * Real-Time WebSocket Synchronization Client.
 * Connects to `ws://10.0.2.2:8080/api/v1/ws/sync` and handles automatic exponential backoff reconnection.
 */
class LmsWebSocketClient(
    private val serverWsUrl: String = "ws://10.0.2.2:8080/api/v1/ws/sync",
    private val gson: Gson = Gson(),
    private val onEventReceived: (eventType: String, payloadJson: String) -> Unit = { _, _ -> }
) {

    private var webSocket: WebSocket? = null
    private val client = OkHttpClient.Builder()
        .readTimeout(0, TimeUnit.MILLISECONDS) // Keep-alive for WebSocket stream
        .build()

    private var reconnectAttempt = 0

    fun connect(authToken: String? = "DEV_TOKEN") {
        val urlWithToken = if (authToken != null) "$serverWsUrl?token=$authToken" else serverWsUrl
        val request = Request.Builder().url(urlWithToken).build()

        webSocket = client.newWebSocket(request, object : WebSocketListener() {
            override fun onOpen(webSocket: WebSocket, response: Response) {
                reconnectAttempt = 0 // Reset reconnect attempt counter on connection
            }

            override fun onMessage(webSocket: WebSocket, text: String) {
                try {
                    val map = gson.fromJson(text, Map::class.java)
                    val eventType = map["eventType"] as? String ?: "UPDATE"
                    val payload = gson.toJson(map["payload"])
                    onEventReceived(eventType, payload)
                } catch (e: Exception) {
                    // Ignore parse errors
                }
            }

            override fun onClosing(webSocket: WebSocket, code: Int, reason: String) {
                webSocket.close(1000, null)
            }

            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                scheduleExponentialReconnection(authToken)
            }
        })
    }

    fun sendSyncEvent(eventType: String, payload: Any) {
        val message = mapOf(
            "eventType" to eventType,
            "payload" to payload,
            "timestamp" to System.currentTimeMillis()
        )
        webSocket?.send(gson.toJson(message))
    }

    private fun scheduleExponentialReconnection(authToken: String?) {
        reconnectAttempt++
        val backoffDelayMs = (2.0.pow(reconnectAttempt.toDouble()) * 1000).toLong().coerceAtMost(30000L)
        Thread {
            try {
                Thread.sleep(backoffDelayMs)
                connect(authToken)
            } catch (e: Exception) {
                // Ignore
            }
        }.start()
    }

    fun disconnect() {
        webSocket?.close(1000, "User logout")
    }
}
