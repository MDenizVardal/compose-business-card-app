package com.example.businesscard

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import com.example.businesscard.ui.theme.BusinessCardTheme

private const val TAG = "Lifecycle"

// Screen shown by default. It can also be chosen when the app is started:
// adb shell am start -n com.example.businesscard/.MainActivity --es screen form
const val DEFAULT_SCREEN = "card"

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.d(TAG, "onCreate")
        enableEdgeToEdge()
        val screen = intent.getStringExtra("screen") ?: DEFAULT_SCREEN
        setContent {
            BusinessCardTheme {
                AppScreen(screen)
            }
        }
    }

    override fun onStart() {
        super.onStart()
        Log.d(TAG, "onStart")
    }

    override fun onResume() {
        super.onResume()
        Log.d(TAG, "onResume")
    }

    override fun onPause() {
        super.onPause()
        Log.d(TAG, "onPause")
    }

    override fun onStop() {
        super.onStop()
        Log.d(TAG, "onStop")
    }

    override fun onDestroy() {
        super.onDestroy()
        Log.d(TAG, "onDestroy")
    }
}

@Composable
fun AppScreen(screen: String) {
    if (screen == "card") {
        BusinessCardScreen()                     // tasks 2.1.1-2.1.3, 2.1.5 (has its own Scaffold)
    } else {
        Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
            val m = Modifier.padding(innerPadding)
            when (screen) {
                "quadrants" -> QuadrantScreen(m)                                     // 2.1.4
                "quadrants_swapped" -> QuadrantScreen(m, swapInBoxQuadrant = true)   // 2.1.4
                "broken" -> BrokenCounter(m)                                         // 2.2.1
                "counter" -> Counter(m)                                              // 2.2.1
                "counter_saveable" -> SaveableCounter(m)                             // 2.2.1
                "ratings" -> FilmRatingsScreen(m)                                    // 2.2.2
                "form" -> SignUpForm(m)                                              // 2.2.3
                else -> TaskListScreen(m)                                            // 2.2.4
            }
        }
    }
}
