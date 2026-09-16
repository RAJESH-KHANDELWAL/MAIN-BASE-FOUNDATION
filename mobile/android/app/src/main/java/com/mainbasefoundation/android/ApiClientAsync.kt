package com.mainbasefoundation.android

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * Asynchronous API wrapper for MAIN-BASE-FOUNDATION.
 *
 * All network operations are executed on Dispatchers.IO
 * so the Android main/UI thread is never blocked.
 */
object ApiClientAsync {

    /**
     * Perform an asynchronous GET request.
     */
    suspend fun get(
        path: String,
        bearerToken: String? = null
    ): ApiResponse {

        return withContext(Dispatchers.IO) {
            ApiClient.get(
                path = path,
                bearerToken = bearerToken
            )
        }
    }

    /**
     * Perform an asynchronous POST request.
     */
    suspend fun post(
        path: String,
        jsonBody: String,
        bearerToken: String? = null
    ): ApiResponse {

        return withContext(Dispatchers.IO) {
            ApiClient.post(
                path = path,
                jsonBody = jsonBody,
                bearerToken = bearerToken
            )
        }
    }
}
