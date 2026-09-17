package com.mainbasefoundation.android

import android.annotation.SuppressLint
import android.graphics.Color
import android.os.Bundle
import android.view.ViewGroup
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity
import androidx.webkit.WebSettingsCompat
import androidx.webkit.WebViewFeature

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView

    /*
     * IMPORTANT:
     * Replace this URL with the HTTPS URL where the
     * MAIN-BASE-FOUNDATION frontend/API gateway is deployed.
     *
     * Example:
     * https://your-production-domain.com
     */
    private val appUrl = "https://YOUR-PRODUCTION-DOMAIN.com"

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        webView = WebView(this)

        webView.layoutParams = ViewGroup.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.MATCH_PARENT
        )

        webView.setBackgroundColor(Color.WHITE)

        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            databaseEnabled = true

            allowFileAccess = false
            allowContentAccess = false

            builtInZoomControls = false
            displayZoomControls = false

            javaScriptCanOpenWindowsAutomatically = false
            setSupportMultipleWindows(false)
        }

        if (WebViewFeature.isFeatureSupported(
                WebViewFeature.FORCE_DARK
            )
        ) {
            WebSettingsCompat.setForceDark(
                webView.settings,
                WebSettingsCompat.FORCE_DARK_OFF
            )
        }

        webView.webViewClient = object : WebViewClient() {

            override fun shouldOverrideUrlLoading(
                view: WebView?,
                request: WebResourceRequest?
            ): Boolean {
                return false
            }
        }

        webView.webChromeClient = WebChromeClient()

        setContentView(webView)

        webView.loadUrl(appUrl)

        onBackPressedDispatcher.addCallback(
            this,
            object : OnBackPressedCallback(true) {

                override fun handleOnBackPressed() {
                    if (webView.canGoBack()) {
                        webView.goBack()
                    } else {
                        finish()
                    }
                }
            }
        )
    }

    override fun onDestroy() {
        webView.apply {
            stopLoading()
            webChromeClient = null
            webViewClient = null
            destroy()
        }

        super.onDestroy()
    }
}
