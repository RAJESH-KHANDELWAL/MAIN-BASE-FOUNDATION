package com.mainbasefoundation.android

import android.content.Context
import android.util.Base64
import org.json.JSONObject
import java.nio.charset.StandardCharsets

class SessionManager(context: Context) {

    private val secureStore = SecureSessionStore(context)

    companion object {
        private const val LEGACY_PREFERENCES =
            "main_base_foundation_session"
    }

    init {
        /*
         * Remove the old plaintext session store.
         *
         * Existing sessions from the previous implementation
         * are intentionally not migrated because their values
         * were stored outside the secure store.
         */
        context.getSharedPreferences(
            LEGACY_PREFERENCES,
            Context.MODE_PRIVATE
        ).edit()
            .clear()
            .apply()
    }

    /**
     * Save authentication response returned by the backend.
     *
     * Supported token fields:
     * - access_token
     * - token
     *
     * Optional fields:
     * - session_id
     * - user_id
     */
    fun saveLoginResponse(
        responseBody: String
    ): Boolean {

        return try {

            val json = JSONObject(responseBody)

            val token = json.optString("access_token")
                .ifBlank {
                    json.optString("token")
                }

            if (token.isBlank()) {
                return false
            }

            val sessionId = json
                .optString("session_id")
                .ifBlank {
                    null
                }

            val userId = json
                .optString("user_id")
                .ifBlank {
                    null
                }

            secureStore.saveToken(token)
            secureStore.saveSessionId(sessionId)
            secureStore.saveUserId(userId)

            true

        } catch (_: Exception) {

            false
        }
    }

    /**
     * Return the currently stored access token.
     */
    fun getToken(): String? {
        return secureStore.getToken()
    }

    /**
     * Return the backend session ID.
     */
    fun getSessionId(): String? {
        return secureStore.getSessionId()
    }

    /**
     * Return the authenticated user ID.
     */
    fun getUserId(): String? {
        return secureStore.getUserId()
    }

    /**
     * Check whether a token is currently stored.
     */
    fun isLoggedIn(): Boolean {
        return secureStore.isLoggedIn()
    }

    /**
     * Clear the complete local authentication session.
     */
    fun clear() {
        secureStore.clear()
    }

    /**
     * Basic local JWT expiry check.
     *
     * This is only a local convenience check.
     * Server-side token validation remains authoritative.
     */
    fun isTokenLocallyExpired(): Boolean {

        val token = getToken() ?: return true

        return try {

            val parts = token.split(".")

            /*
             * A JWT normally contains:
             * header.payload.signature
             */
            if (parts.size != 3) {
                return false
            }

            val payload = String(
                Base64.decode(
                    parts[1],
                    Base64.URL_SAFE or
                            Base64.NO_WRAP or
                            Base64.NO_PADDING
                ),
                StandardCharsets.UTF_8
            )

            val json = JSONObject(payload)

            val expiry = json.optLong(
                "exp",
                0L
            )

            /*
             * If the token does not contain an exp claim,
             * do not locally reject it.
             *
             * The backend remains responsible for validation.
             */
            if (expiry <= 0L) {
                false
            } else {
                System.currentTimeMillis() / 1000L >= expiry
            }

        } catch (_: Exception) {

            /*
             * Parsing failure does not automatically mean
             * the server considers the token invalid.
             */
            false
        }
    }

    /**
     * Clear the session when the token is known to be invalid
     * or expired.
     */
    fun clearIfLocallyExpired(): Boolean {

        if (isTokenLocallyExpired()) {
            clear()
            return true
        }

        return false
    }
}
