package com.example.businesscard

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Checkbox
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp

@Composable
fun SignUpForm(modifier: Modifier = Modifier) {
    var email by rememberSaveable { mutableStateOf("") }
    var age by rememberSaveable { mutableStateOf("") }
    var password by rememberSaveable { mutableStateOf("") }
    var confirmPassword by rememberSaveable { mutableStateOf("") }
    var acceptTerms by rememberSaveable { mutableStateOf(false) }
    var newsletter by rememberSaveable { mutableStateOf(false) }
    var message by rememberSaveable { mutableStateOf("") }

    // derived values - not state, computed again in every recomposition
    val emailValid = email.contains("@") && email.contains(".")
    val ageValue = age.toIntOrNull()
    val ageValid = ageValue != null && ageValue in 16..120
    val passwordValid = password.length >= 8 && password.any { it.isDigit() }
    val confirmValid = confirmPassword == password
    val formValid = emailValid && ageValid && passwordValid &&
        confirmPassword.isNotEmpty() && confirmValid && acceptTerms

    Column(
        modifier = modifier
            .padding(16.dp)
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        OutlinedTextField(
            value = email,
            onValueChange = { email = it.trim() },
            label = { Text("E-mail") },
            singleLine = true,
            isError = email.isNotEmpty() && !emailValid,
            supportingText = {
                if (email.isNotEmpty() && !emailValid) Text("Enter a valid e-mail address")
            },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
            modifier = Modifier.fillMaxWidth()
        )
        OutlinedTextField(
            value = age,
            onValueChange = { new -> if (new.all { it.isDigit() }) age = new },
            label = { Text("Age") },
            singleLine = true,
            isError = age.isNotEmpty() && !ageValid,
            supportingText = {
                if (age.isNotEmpty() && !ageValid) Text("Age must be between 16 and 120")
            },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
            modifier = Modifier.fillMaxWidth()
        )
        // Task 2.2.3: password - at least 8 characters with at least one digit
        OutlinedTextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("Password") },
            singleLine = true,
            visualTransformation = PasswordVisualTransformation(),
            isError = password.isNotEmpty() && !passwordValid,
            supportingText = {
                if (password.isNotEmpty() && !passwordValid) {
                    Text("At least 8 characters, including a digit")
                }
            },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
            modifier = Modifier.fillMaxWidth()
        )
        // Task 2.2.3: confirmation - must be equal to the password
        OutlinedTextField(
            value = confirmPassword,
            onValueChange = { confirmPassword = it },
            label = { Text("Confirm password") },
            singleLine = true,
            visualTransformation = PasswordVisualTransformation(),
            isError = confirmPassword.isNotEmpty() && !confirmValid,
            supportingText = {
                if (confirmPassword.isNotEmpty() && !confirmValid) Text("Passwords do not match")
            },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
            modifier = Modifier.fillMaxWidth()
        )
        Row(verticalAlignment = Alignment.CenterVertically) {
            Checkbox(checked = acceptTerms, onCheckedChange = { acceptTerms = it })
            Text("I accept the terms")
        }
        // Task 2.2.3: Switch "Newsletter"
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Newsletter", modifier = Modifier.weight(1f))
            Switch(checked = newsletter, onCheckedChange = { newsletter = it })
        }
        Spacer(Modifier.padding(4.dp))
        Button(
            onClick = {
                message = "Account created for $email" +
                    if (newsletter) " (newsletter: yes)" else " (newsletter: no)"
                // Task 2.2.3: clear the form after a successful sign-up
                email = ""
                age = ""
                password = ""
                confirmPassword = ""
                acceptTerms = false
                newsletter = false
            },
            enabled = formValid,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Sign up")
        }
        if (message.isNotEmpty()) {
            Text(message, color = MaterialTheme.colorScheme.primary)
        }
    }
}
