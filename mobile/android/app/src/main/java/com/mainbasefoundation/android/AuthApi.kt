package com.mainbasefoundation.android

import org.json.JSONObject

object AuthApi {

    /**
     * Existing MAIN-BASE-FOUNDATION endpoint:
     * GET /auth/initialize
     */
    fun initialize(): ApiResponse {
        return ApiClient.get(
            ApiConfig.AUTH_PATH + "/initialize"
        )
    }

    /**
     * Existing endpoint:
     * POST /auth/login
     *
     * Backend accepts:
     * username
     * password
     * master_id
     */
    fun login(
        username: String? = null,
        password: String? = null,
        masterId: String? = null
    ): ApiResponse {

        val body = JSONObject().apply {

            if (!username.isNullOrBlank()) {
                put("username", username)
            }

            if (!password.isNullOrBlank()) {
                put("password", password)
            }

            if (!masterId.isNullOrBlank()) {
                put("master_id", masterId)
            }
        }

        return ApiClient.post(
            ApiConfig.AUTH_PATH + "/login",
            body.toString()
        )
    }

    /**
     * Existing endpoint:
     * POST /auth/authenticate
     *
     * The backend currently expects master_id.
     */
    fun authenticate(
        masterId: String
    ): ApiResponse {

        val body = JSONObject().apply {
            put("master_id", masterId)
        }

        return ApiClient.post(
            ApiConfig.AUTH_PATH + "/authenticate",
            body.toString()
        )
    }

    /**
     * Existing endpoint:
     * POST /auth/validate
     */
    fun validateToken(
        token: String
    ): ApiResponse {

        val body = JSONObject().apply {
            put("token", token)
        }

        return ApiClient.post(
            ApiConfig.AUTH_PATH + "/validate",
            body.toString()
        )
    }

    /**
     * Existing endpoint:
     * POST /auth/logout
     */
    fun logout(
        token: String? = null,
        sessionId: String? = null
    ): ApiResponse {

        val body = JSONObject().apply {

            if (!token.isNullOrBlank()) {
                put("token", token)
            }

            if (!sessionId.isNullOrBlank()) {
                put("session_id", sessionId)
            }
        }

        return ApiClient.post(
            ApiConfig.AUTH_PATH + "/logout",
            body.toString()
        )
    }
}
