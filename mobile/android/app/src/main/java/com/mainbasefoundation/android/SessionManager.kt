package com.mainbasefoundation.android

import android.content.Context
import android.util.Base64
import org.json.JSONObject
import java.nio.charset.StandardCharsets

class SessionManager(context: Context) {

```
private val preferences = context.getSharedPreferences(
    "main_base_foundation_session",
    Context.MODE_PRIVATE
)

companion object {
    private const val KEY_TOKEN = "access_token"
    private const val KEY_SESSION_ID = "session_id"
    private const val KEY_USER_ID = "user_id"
}

fun saveLoginResponse(responseBody: String): Boolean {
    return try {
        val json = JSONObject(responseBody)

        val token = json.optString("access_token")
            .ifBlank {
                json.optString("token")
            }

        val sessionId = json.optString("session_id")
        val userId = json.optString("user_id")

        if (token.isBlank()) {
            return false
        }

        preferences.edit()
            .putString(KEY_TOKEN, token)
            .putString(KEY_SESSION_ID, sessionId)
            .putString(KEY_USER_ID, userId)
            .apply()

        true

    } catch (_: Exception) {
        false
    }
}

fun getToken(): String? {
    return preferences.getString(KEY_TOKEN, null)
}

fun getSessionId(): String? {
    return preferences.getString(KEY_SESSION_ID, null)
}

fun getUserId(): String? {
    return preferences.getString(KEY_USER_ID, null)
}

fun isLoggedIn(): Boolean {
    return !getToken().isNullOrBlank()
}

fun clear() {
    preferences.edit().clear().apply()
}

/**
 * Basic JWT expiry check.
 *
 * This does NOT replace server-side token validation.
 * The backend remains the authority for authentication.
 */
fun isTokenLocallyExpired(): Boolean {

    val token = getToken() ?: return true

    return try {
        val parts = token.split(".")

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
        val expiry = json.optLong("exp", 0L)

        if (expiry <= 0L) {
            false
        } else {
            System.currentTimeMillis() / 1000L >= expiry
        }

    } catch (_: Exception) {
        false
    }
}
```

}
