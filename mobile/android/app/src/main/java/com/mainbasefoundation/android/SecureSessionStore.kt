package com.mainbasefoundation.android

import android.content.Context
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import android.util.Base64
import java.nio.charset.StandardCharsets
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec

class SecureSessionStore(context: Context) {

    private val preferences = context.getSharedPreferences(
        "main_base_foundation_secure_session",
        Context.MODE_PRIVATE
    )

    companion object {
        private const val KEY_ALIAS = "main_base_foundation_session_key"
        private const val KEY_TOKEN = "encrypted_access_token"
        private const val KEY_SESSION_ID = "encrypted_session_id"
        private const val KEY_USER_ID = "encrypted_user_id"

        private const val TRANSFORMATION = "AES/GCM/NoPadding"
        private const val IV_SIZE = 12
        private const val TAG_SIZE = 128
    }

    init {
        createKeyIfNeeded()
    }

    private fun createKeyIfNeeded() {

        val keyStore = java.security.KeyStore.getInstance(
            "AndroidKeyStore"
        ).apply {
            load(null)
        }

        if (!keyStore.containsAlias(KEY_ALIAS)) {

            val keyGenerator = KeyGenerator.getInstance(
                KeyProperties.KEY_ALGORITHM_AES,
                "AndroidKeyStore"
            )

            val keySpec = KeyGenParameterSpec.Builder(
                KEY_ALIAS,
                KeyProperties.PURPOSE_ENCRYPT or
                    KeyProperties.PURPOSE_DECRYPT
            )
                .setBlockModes(
                    KeyProperties.BLOCK_MODE_GCM
                )
                .setEncryptionPaddings(
                    KeyProperties.ENCRYPTION_PADDING_NONE
                )
                .setRandomizedEncryptionRequired(true)
                .build()

            keyGenerator.init(keySpec)
            keyGenerator.generateKey()
        }
    }

    private fun getKey(): SecretKey {

        val keyStore = java.security.KeyStore.getInstance(
            "AndroidKeyStore"
        ).apply {
            load(null)
        }

        return keyStore.getKey(
            KEY_ALIAS,
            null
        ) as SecretKey
    }

    private fun encrypt(value: String): String {

        val cipher = Cipher.getInstance(TRANSFORMATION)

        cipher.init(
            Cipher.ENCRYPT_MODE,
            getKey()
        )

        val encrypted = cipher.doFinal(
            value.toByteArray(StandardCharsets.UTF_8)
        )

        val iv = cipher.iv

        val combined = ByteArray(
            iv.size + encrypted.size
        )

        System.arraycopy(
            iv,
            0,
            combined,
            0,
            iv.size
        )

        System.arraycopy(
            encrypted,
            0,
            combined,
            iv.size,
            encrypted.size
        )

        return Base64.encodeToString(
            combined,
            Base64.NO_WRAP
        )
    }

    private fun decrypt(value: String): String? {

        return try {

            val combined = Base64.decode(
                value,
                Base64.NO_WRAP
            )

            if (combined.size <= IV_SIZE) {
                return null
            }

            val iv = combined.copyOfRange(
                0,
                IV_SIZE
            )

            val encrypted = combined.copyOfRange(
                IV_SIZE,
                combined.size
            )

            val cipher = Cipher.getInstance(
                TRANSFORMATION
            )

            cipher.init(
                Cipher.DECRYPT_MODE,
                getKey(),
                GCMParameterSpec(TAG_SIZE, iv)
            )

            String(
                cipher.doFinal(encrypted),
                StandardCharsets.UTF_8
            )

        } catch (_: Exception) {
            null
        }
    }

    fun saveToken(token: String) {
        preferences.edit()
            .putString(KEY_TOKEN, encrypt(token))
            .apply()
    }

    fun getToken(): String? {
        return preferences
            .getString(KEY_TOKEN, null)
            ?.let { decrypt(it) }
    }

    fun saveSessionId(sessionId: String?) {

        val editor = preferences.edit()

        if (sessionId.isNullOrBlank()) {
            editor.remove(KEY_SESSION_ID)
        } else {
            editor.putString(
                KEY_SESSION_ID,
                encrypt(sessionId)
            )
        }

        editor.apply()
    }

    fun getSessionId(): String? {
        return preferences
            .getString(KEY_SESSION_ID, null)
            ?.let { decrypt(it) }
    }

    fun saveUserId(userId: String?) {

        val editor = preferences.edit()

        if (userId.isNullOrBlank()) {
            editor.remove(KEY_USER_ID)
        } else {
            editor.putString(
                KEY_USER_ID,
                encrypt(userId)
            )
        }

        editor.apply()
    }

    fun getUserId(): String? {
        return preferences
            .getString(KEY_USER_ID, null)
            ?.let { decrypt(it) }
    }

    fun clear() {
        preferences.edit()
            .clear()
            .apply()
    }

    fun isLoggedIn(): Boolean {
        return !getToken().isNullOrBlank()
    }
}
