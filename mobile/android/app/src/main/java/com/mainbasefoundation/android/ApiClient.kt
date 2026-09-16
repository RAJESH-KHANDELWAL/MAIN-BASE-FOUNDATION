package com.mainbasefoundation.android

import java.io.IOException
import java.net.HttpURLConnection
import java.net.URL

object ApiClient {

```
private const val CONNECT_TIMEOUT = 15000
private const val READ_TIMEOUT = 30000

/**
 * Perform a GET request against the MAIN-BASE-FOUNDATION API.
 *
 * The BASE_URL must be HTTPS and configured in ApiConfig.kt.
 */
fun get(
    path: String,
    bearerToken: String? = null
): ApiResponse {

    return request(
        method = "GET",
        path = path,
        bearerToken = bearerToken
    )
}

/**
 * Perform a POST request with a JSON body.
 */
fun post(
    path: String,
    jsonBody: String,
    bearerToken: String? = null
): ApiResponse {

    return request(
        method = "POST",
        path = path,
        jsonBody = jsonBody,
        bearerToken = bearerToken
    )
}

private fun request(
    method: String,
    path: String,
    jsonBody: String? = null,
    bearerToken: String? = null
): ApiResponse {

    if (!ApiConfig.BASE_URL.startsWith("https://")) {
        return ApiResponse(
            success = false,
            statusCode = -1,
            body = "",
            error = "Production API must use HTTPS."
        )
    }

    val endpoint = ApiConfig.BASE_URL.trimEnd('/') +
            "/" +
            path.trimStart('/')

    var connection: HttpURLConnection? = null

    return try {

        connection = (URL(endpoint).openConnection() as HttpURLConnection).apply {

            requestMethod = method
            connectTimeout = CONNECT_TIMEOUT
            readTimeout = READ_TIMEOUT

            setRequestProperty(
                "Accept",
                "application/json"
            )

            setRequestProperty(
                "Content-Type",
                "application/json"
            )

            setRequestProperty(
                "X-Client",
                "MAIN-BASE-FOUNDATION-ANDROID"
            )

            if (!bearerToken.isNullOrBlank()) {
                setRequestProperty(
                    "Authorization",
                    "Bearer $bearerToken"
                )
            }

            if (method == "POST") {
                doOutput = true

                jsonBody?.let { body ->
                    outputStream.use { stream ->
                        stream.write(
                            body.toByteArray(Charsets.UTF_8)
                        )
                    }
                }
            }
        }

        val statusCode = connection.responseCode

        val responseStream =
            if (statusCode in 200..399) {
                connection.inputStream
            } else {
                connection.errorStream
            }

        val responseBody =
            responseStream?.bufferedReader()?.use {
                it.readText()
            } ?: ""

        ApiResponse(
            success = statusCode in 200..299,
            statusCode = statusCode,
            body = responseBody,
            error = if (statusCode !in 200..299) {
                responseBody
            } else {
                null
            }
        )

    } catch (exception: IOException) {

        ApiResponse(
            success = false,
            statusCode = -1,
            body = "",
            error = exception.message
                ?: "Network request failed."
        )

    } finally {
        connection?.disconnect()
    }
}
```

}

data class ApiResponse(
val success: Boolean,
val statusCode: Int,
val body: String,
val error: String?
)
