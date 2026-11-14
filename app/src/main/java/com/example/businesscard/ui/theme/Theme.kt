package com.example.businesscard.ui.theme

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext

private val DarkColorScheme = darkColorScheme(
    primary = Purple80,
    secondary = PurpleGrey80,
    tertiary = Pink80
)

// Task 2.1.5: own colours instead of the template's Purple40 / PurpleGrey40
private val LightColorScheme = lightColorScheme(
    primary = Teal40,
    secondary = Orange40,
    tertiary = Pink40,
    primaryContainer = Teal90,
    secondaryContainer = Orange90
)

@Composable
fun BusinessCardTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    // Task 2.1.5: false, otherwise Android 12+ takes the colours from the wallpaper
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
