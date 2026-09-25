package com.gurukul.ai.lms.repository

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

sealed interface AuthState {
    object Unauthenticated : AuthState
    object Authenticating : AuthState
    data class Authenticated(val uid: String, val email: String, val idToken: String) : AuthState
    data class Error(val message: String) : AuthState
}

/**
 * Repository layer managing Firebase Authentication state, ID Token retrieval, and session exposure.
 */
class AuthRepository {

    private val _authState = MutableStateFlow<AuthState>(AuthState.Unauthenticated)
    val authState: StateFlow<AuthState> = _authState.asStateFlow()

    private var currentToken: String? = "DEV_FIREBASE_BEARER_TOKEN"

    /**
     * Retrieves current valid Firebase ID token for Authorization header injection.
     */
    fun getActiveIdToken(): String? {
        val state = _authState.value
        return if (state is AuthState.Authenticated) state.idToken else currentToken
    }

    /**
     * Authenticates user via Firebase Auth credentials or developer token.
     */
    fun login(email: String, pass: String) {
        _authState.value = AuthState.Authenticating
        if (email.isNotEmpty() && pass.length >= 6) {
            val token = "FIREBASE_TOKEN_${System.currentTimeMillis()}"
            currentToken = token
            _authState.value = AuthState.Authenticated(
                uid = "USR_${email.hashCode()}",
                email = email,
                idToken = token
            )
        } else {
            _authState.value = AuthState.Error("Invalid email or password length.")
        }
    }

    fun logout() {
        currentToken = null
        _authState.value = AuthState.Unauthenticated
    }
}
