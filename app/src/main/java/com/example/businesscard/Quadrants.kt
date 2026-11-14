package com.example.businesscard

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.businesscard.ui.theme.BusinessCardTheme

@Composable
fun QuadrantScreen(modifier: Modifier = Modifier, swapInBoxQuadrant: Boolean = false) {
    Column(modifier = modifier.fillMaxSize()) {
        Row(modifier = Modifier.weight(1f)) {
            Quadrant(
                title = stringResource(R.string.quadrant_column_title),
                description = stringResource(R.string.quadrant_column_desc),
                backgroundColor = Color(0xFFFFE0B2),
                modifier = Modifier.weight(1f)
            )
            Quadrant(
                title = stringResource(R.string.quadrant_row_title),
                description = stringResource(R.string.quadrant_row_desc),
                backgroundColor = Color(0xFFC8E6C9),
                modifier = Modifier.weight(1f)
            )
        }
        Row(modifier = Modifier.weight(1f)) {
            Quadrant(
                title = stringResource(R.string.quadrant_box_title),
                description = stringResource(R.string.quadrant_box_desc),
                backgroundColor = Color(0xFFBBDEFB),
                paddingBeforeBackground = swapInBoxQuadrant,
                modifier = Modifier.weight(1f)
            )
            Quadrant(
                title = stringResource(R.string.quadrant_spacer_title),
                description = stringResource(R.string.quadrant_spacer_desc),
                backgroundColor = Color(0xFFF8BBD0),
                modifier = Modifier.weight(1f)
            )
        }
    }
}

@Composable
fun Quadrant(
    title: String,
    description: String,
    backgroundColor: Color,
    modifier: Modifier = Modifier,
    paddingBeforeBackground: Boolean = false
) {
    // The order of modifiers matters:
    //   background -> padding : the colour fills the whole quadrant, the padding is inside it
    //   padding -> background : the padding is outside, the colour is drawn only in the smaller area
    val decorated = if (paddingBeforeBackground) {
        modifier.padding(16.dp).background(backgroundColor)
    } else {
        modifier.background(backgroundColor).padding(16.dp)
    }
    Column(
        modifier = decorated.fillMaxSize(),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = title,
            fontWeight = FontWeight.Bold,
            color = Color.Black,
            modifier = Modifier.padding(bottom = 16.dp)
        )
        Text(
            text = description,
            textAlign = TextAlign.Center,
            color = Color.Black,
            modifier = Modifier.fillMaxWidth()
        )
    }
}

@Preview(showBackground = true, name = "Quadrants")
@Composable
fun QuadrantPreview() {
    BusinessCardTheme { QuadrantScreen() }
}

@Preview(showBackground = true, name = "Quadrants - padding before background")
@Composable
fun QuadrantSwappedPreview() {
    BusinessCardTheme { QuadrantScreen(swapInBoxQuadrant = true) }
}
