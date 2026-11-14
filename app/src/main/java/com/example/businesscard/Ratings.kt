package com.example.businesscard

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.businesscard.ui.theme.BusinessCardTheme

// Task 2.2.2: stateless - gets the value and reports the change as an event
@Composable
fun RatingBar(rating: Int, onRatingChange: (Int) -> Unit, modifier: Modifier = Modifier) {
    Row(modifier = modifier, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
        for (star in 1..5) {
            val buttonModifier = Modifier.size(48.dp)
            val padding = PaddingValues(0.dp)
            if (star <= rating) {
                Button(
                    onClick = { onRatingChange(star) },
                    modifier = buttonModifier,
                    contentPadding = padding
                ) { Text("*") }
            } else {
                OutlinedButton(
                    onClick = { onRatingChange(star) },
                    modifier = buttonModifier,
                    contentPadding = padding
                ) { Text("*") }
            }
        }
    }
}

// The state is hoisted here - the lowest common ancestor of the three bars and the average
@Composable
fun FilmRatingsScreen(modifier: Modifier = Modifier) {
    var inception by rememberSaveable { mutableIntStateOf(0) }
    var interstellar by rememberSaveable { mutableIntStateOf(0) }
    var matrix by rememberSaveable { mutableIntStateOf(0) }

    // derived value, computed again in every recomposition
    val given = listOf(inception, interstellar, matrix).filter { it > 0 }
    val averageText = if (given.isEmpty()) {
        "No ratings yet"
    } else {
        "Average rating: %.2f (%d of 3 films rated)".format(given.average(), given.size)
    }

    Column(modifier = modifier.padding(16.dp)) {
        Text("Rate the films", style = MaterialTheme.typography.headlineSmall)
        Spacer(Modifier.height(16.dp))
        Text("Inception")
        RatingBar(rating = inception, onRatingChange = { inception = it })
        Spacer(Modifier.height(12.dp))
        Text("Interstellar")
        RatingBar(rating = interstellar, onRatingChange = { interstellar = it })
        Spacer(Modifier.height(12.dp))
        Text("The Matrix")
        RatingBar(rating = matrix, onRatingChange = { matrix = it })
        Spacer(Modifier.height(24.dp))
        Text(
            averageText,
            style = MaterialTheme.typography.titleMedium,
            color = MaterialTheme.colorScheme.primary
        )
    }
}

@Preview(showBackground = true)
@Composable
fun RatingBarPreview() {
    BusinessCardTheme { RatingBar(rating = 3, onRatingChange = {}) }
}
