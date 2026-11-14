package com.example.businesscard

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.Checkbox
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.RadioButton
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableLongStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.unit.dp

// Task 2.2.4: the declaration order gives the order used for sorting (LOW < NORMAL < HIGH)
enum class Priority { LOW, NORMAL, HIGH }

enum class TaskFilter(val label: String) { ALL("All"), ACTIVE("Active"), DONE("Done") }

data class Task(
    val id: Long,
    val title: String,
    val done: Boolean = false,
    val priority: Priority = Priority.NORMAL
)

@Composable
fun TaskListScreen(modifier: Modifier = Modifier) {
    var tasks by remember {
        mutableStateOf(
            listOf(
                Task(1, "Install Android Studio", done = true, priority = Priority.LOW),
                Task(2, "Learn Compose")
            )
        )
    }
    var newTitle by rememberSaveable { mutableStateOf("") }
    var nextId by rememberSaveable { mutableLongStateOf(3L) }
    var newPriority by rememberSaveable { mutableStateOf(Priority.NORMAL) }
    var filter by rememberSaveable { mutableStateOf(TaskFilter.ALL) }

    // Derived from the state: sorted (HIGH first) and filtered copy.
    // The list "tasks" itself is not changed by the filter.
    val visibleTasks = tasks
        .sortedByDescending { it.priority }
        .filter {
            when (filter) {
                TaskFilter.ALL -> true
                TaskFilter.ACTIVE -> !it.done
                TaskFilter.DONE -> it.done
            }
        }

    Column(modifier = modifier.padding(16.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            OutlinedTextField(
                value = newTitle,
                onValueChange = { newTitle = it },
                label = { Text("New task") },
                singleLine = true,
                modifier = Modifier.weight(1f)
            )
            Spacer(Modifier.width(8.dp))
            Button(
                onClick = {
                    tasks = tasks + Task(nextId, newTitle.trim(), priority = newPriority)
                    nextId++
                    newTitle = ""
                    newPriority = Priority.NORMAL
                },
                enabled = newTitle.isNotBlank()
            ) { Text("Add") }
        }
        // priority of the new task: three RadioButtons
        Row(verticalAlignment = Alignment.CenterVertically) {
            Priority.entries.forEach { p ->
                RadioButton(selected = newPriority == p, onClick = { newPriority = p })
                Text(p.name, modifier = Modifier.padding(end = 8.dp))
            }
        }
        // filter buttons: the selected one is filled, the others outlined
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            TaskFilter.entries.forEach { f ->
                if (f == filter) {
                    Button(onClick = { filter = f }) { Text(f.label) }
                } else {
                    OutlinedButton(onClick = { filter = f }) { Text(f.label) }
                }
            }
        }
        Text(
            "Done: ${tasks.count { it.done }} / ${tasks.size}   (shown: ${visibleTasks.size})",
            modifier = Modifier.padding(vertical = 8.dp)
        )
        LazyColumn(modifier = Modifier.fillMaxSize()) {
            items(visibleTasks, key = { it.id }) { task ->
                TaskRow(
                    task = task,
                    onToggle = {
                        tasks = tasks.map { if (it.id == task.id) it.copy(done = !it.done) else it }
                    },
                    onDelete = { tasks = tasks.filter { it.id != task.id } }
                )
            }
        }
    }
}

@Composable
fun TaskRow(task: Task, onToggle: () -> Unit, onDelete: () -> Unit, modifier: Modifier = Modifier) {
    Row(modifier = modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
        Checkbox(checked = task.done, onCheckedChange = { onToggle() })
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = task.title,
                textDecoration = if (task.done) TextDecoration.LineThrough else null
            )
            Text(
                text = task.priority.name,
                style = MaterialTheme.typography.labelSmall,
                color = if (task.priority == Priority.HIGH) {
                    MaterialTheme.colorScheme.error
                } else {
                    MaterialTheme.colorScheme.secondary
                }
            )
        }
        TextButton(onClick = onDelete) { Text("Delete") }
    }
}
