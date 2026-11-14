package com.example.businesscard

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

// Listing 1 - does NOT work: an ordinary variable is not observed by Compose
@Composable
fun BrokenCounter(modifier: Modifier = Modifier) {
    var count = 0
    Column(
        modifier = modifier.fillMaxWidth().padding(top = 32.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("BrokenCounter (ordinary var)", style = MaterialTheme.typography.titleMedium)
        Button(onClick = { count++ }) {
            Text("Clicked $count times")
        }
    }
}

// Listing 2 - state kept with remember: survives recomposition, NOT rotation
@Composable
fun Counter(modifier: Modifier = Modifier) {
    var count by remember { mutableIntStateOf(0) }

    Column(
        modifier = modifier.fillMaxWidth().padding(top = 32.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("Counter with remember", style = MaterialTheme.typography.titleMedium)
        Text("Clicked $count times", style = MaterialTheme.typography.headlineSmall)
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(onClick = { count++ }) { Text("+1") }
            OutlinedButton(onClick = { count = 0 }, enabled = count > 0) {
                Text("Reset")
            }
        }
    }
}

// Listing 3 - state kept with rememberSaveable: also survives rotation
@Composable
fun SaveableCounter(modifier: Modifier = Modifier) {
    var count by rememberSaveable { mutableIntStateOf(0) }

    Column(
        modifier = modifier.fillMaxWidth().padding(top = 32.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("Counter with rememberSaveable", style = MaterialTheme.typography.titleMedium)
        Text("Clicked $count times", style = MaterialTheme.typography.headlineSmall)
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(onClick = { count++ }) { Text("+1") }
            OutlinedButton(onClick = { count = 0 }, enabled = count > 0) {
                Text("Reset")
            }
        }
    }
}
