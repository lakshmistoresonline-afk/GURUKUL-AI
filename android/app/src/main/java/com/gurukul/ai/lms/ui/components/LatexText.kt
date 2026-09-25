package com.gurukul.ai.lms.ui.components

import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView

/**
 * Native KaTeX / LaTeX Math Text Renderer Composable.
 * Renders mathematical equations (e.g. `$\frac{a}{b}$`) inside MCQs and step-by-step explanations cleanly.
 */
@Composable
fun LatexText(
    latexText: String,
    modifier: Modifier = Modifier,
    textColor: Color = Color.White
) {
    val htmlContent = """
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
            <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css"></script>
            <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
            <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"
                onload="renderMathInElement(document.body);"></script>
            <style>
                body {
                    background-color: transparent;
                    color: #${Integer.toHexString(textColor.toArgb()).substring(2)};
                    font-family: sans-serif;
                    font-size: 15px;
                    margin: 0;
                    padding: 0;
                }
            </style>
        </head>
        <body>
            $latexText
        </body>
        </html>
    """.trimIndent()

    AndroidView(
        factory = { context ->
            WebView(context).apply {
                webViewClient = WebViewClient()
                settings.javaScriptEnabled = true
                setBackgroundColor(android.graphics.Color.TRANSPARENT)
                loadDataWithBaseURL(null, htmlContent, "text/html", "UTF-8", null)
            }
        },
        update = { webView ->
            webView.loadDataWithBaseURL(null, htmlContent, "text/html", "UTF-8", null)
        },
        modifier = modifier
            .fillMaxWidth()
            .heightIn(min = 40.dp, max = 200.dp)
    )
}
