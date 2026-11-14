"""Builds report.html from the project sources, logs and screenshots,
then prints it to AMAD_Report02_Vardal_Deniz.pdf with headless Edge."""
import html
import tempfile
import subprocess
from pathlib import Path

REPORT = Path(__file__).resolve().parent
PROJECT = REPORT.parent
SRC = PROJECT / "app/src/main/java/com/example/businesscard"
RES = PROJECT / "app/src/main/res"
LOGS = REPORT / "logs"
OUT_HTML = REPORT / "report.html"
OUT_PDF = REPORT / "AMAD_Report02_Vardal_Deniz.pdf"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def code(path: Path, title: str | None = None) -> str:
    text = path.read_text(encoding="utf-8").rstrip()
    name = title or str(path.relative_to(PROJECT)).replace("\\", "/")
    return f'<div class="file">{html.escape(name)}</div><pre>{html.escape(text)}</pre>'


def log(name: str, caption: str) -> str:
    text = (LOGS / f"{name}.txt").read_text(encoding="utf-8").rstrip()
    return f'<div class="file">{html.escape(caption)}</div><pre class="log">{html.escape(text)}</pre>'


def figs(*items, landscape=False) -> str:
    cls = "fig land" if landscape else "fig"
    cells = "".join(
        f'<figure class="{cls}"><img src="img/{f}.png"><figcaption>{c}</figcaption></figure>'
        for f, c in items
    )
    return f'<div class="figs">{cells}</div>'


def comment(text: str) -> str:
    return f'<div class="comment"><b>Comment.</b> {text}</div>'


CSS = """
@page { size: A4; margin: 16mm 15mm 16mm 15mm; }
body { font-family: 'Segoe UI', Calibri, Arial, sans-serif; font-size: 10.5pt; line-height: 1.42; color: #111; }
h1 { font-size: 20pt; margin: 0 0 4px 0; color: #0b4f6c; }
h2 { font-size: 15pt; color: #0b4f6c; border-bottom: 2px solid #0b4f6c; padding-bottom: 3px; margin-top: 26px; break-after: avoid; }
h3 { font-size: 12.5pt; margin: 22px 0 6px 0; color: #00696b; break-after: avoid; }
h4 { font-size: 10.5pt; margin: 12px 0 4px 0; break-after: avoid; }
p { margin: 5px 0; text-align: justify; }
code { font-family: Consolas, 'Cascadia Mono', 'Courier New', monospace; font-size: 9.2pt; background: #f1f3f4; padding: 0 2px; border-radius: 2px; }
pre { font-family: Consolas, 'Cascadia Mono', 'Courier New', monospace; font-size: 8.1pt; line-height: 1.32;
      background: #f7f8fa; border: 1px solid #d5d9de; border-left: 3px solid #00696b; padding: 6px 8px; margin: 0 0 10px 0;
      white-space: pre-wrap; word-break: break-word; }
pre.log { background: #1e1e1e; color: #e6e6e6; border-left-color: #f0a030; }
.file { font-family: Consolas, monospace; font-size: 8.4pt; font-weight: bold; color: #444; margin-top: 8px; padding: 2px 8px;
        background: #e3e7eb; border: 1px solid #d5d9de; border-bottom: none; display: inline-block; }
.figs { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin: 8px 0 10px 0; break-inside: avoid; }
figure { margin: 0; text-align: center; break-inside: avoid; }
figure.fig img { width: 52mm; border: 1px solid #bbb; }
figure.land img { width: 118mm; border: 1px solid #bbb; }
figcaption { font-size: 8.6pt; color: #444; max-width: 56mm; margin: 3px auto 0 auto; }
figure.land figcaption { max-width: 118mm; }
.comment { background: #fff8e6; border-left: 3px solid #f0a030; padding: 6px 9px; margin: 8px 0; break-inside: avoid; }
.meta td { padding: 1px 12px 1px 0; vertical-align: top; }
table.t { border-collapse: collapse; margin: 6px 0; font-size: 9.6pt; }
table.t td, table.t th { border: 1px solid #c8ccd0; padding: 3px 7px; text-align: left; vertical-align: top; }
table.t th { background: #e9f4f4; }
.q { font-weight: 600; margin-top: 10px; break-after: avoid; }
.pb { break-before: page; }
"""

parts: list[str] = []
add = parts.append

# ---------------------------------------------------------------- title page
add("""
<h1>Lab Report 02</h1>
<div style="font-size:12pt;color:#333;margin-bottom:10px">Advanced Mobile Application Development &middot; 2026/2027</div>
<table class="meta">
<tr><td><b>Student</b></td><td>Deniz Vardal</td></tr>
<tr><td><b>Instructions</b></td><td>02.1 &ndash; Anatomy of an Android application, resources, layouts and Material 3<br>
02.2 &ndash; State, state hoisting, forms and lists</td></tr>
<tr><td><b>Tasks</b></td><td>2.1.1&ndash;2.1.5, 2.2.1&ndash;2.2.4, control questions of both parts</td></tr>
<tr><td><b>Date</b></td><td>14.11.2026</td></tr>
</table>

<h2>Environment and project structure</h2>
<table class="t">
<tr><th>Item</th><th>Value</th></tr>
<tr><td>Project</td><td><code>BusinessCard</code> (Empty Activity template structure), package <code>com.example.businesscard</code></td></tr>
<tr><td>Build</td><td>Gradle 8.7, Android Gradle Plugin 8.5.2, Kotlin 2.0.21 with the Compose compiler plugin, Compose BOM 2024.09.03, JDK 17</td></tr>
<tr><td>SDK</td><td><code>compileSdk = 34</code>, <code>targetSdk = 34</code>, <code>minSdk = 24</code></td></tr>
<tr><td>Device</td><td>Android Emulator, Android 14 (API 34, Google APIs x86_64), 1080&times;2400 px</td></tr>
</table>
<p>Both instructions were done in <b>one project</b>, as allowed in 02.2 (&ldquo;switch between the screens by changing the
call in <code>setContent</code>&rdquo;). <code>MainActivity</code> keeps the lifecycle logs from task 2.1.1 and shows one
screen chosen in a <code>when</code> expression. Instead of editing a constant before every run, the name of the screen can
also be passed when the Activity is started (<code>--es screen form</code>), so each screen could be opened directly from the
command line while taking screenshots. All screenshots come from the emulator and show the final version of the code below.</p>
""")
add(comment("Listing 3 of 02.1 uses <code>compileSdk</code>/<code>targetSdk</code> 37. On my machine only the API 34 SDK platform "
            "and API 34 system image are installed, so I used 34. Nothing in the tasks needs a newer API."))
add(code(PROJECT / "app/build.gradle.kts"))
add(code(PROJECT / "gradle/libs.versions.toml"))

# ---------------------------------------------------------------- 2.1.1
add('<h2 class="pb">Part 02.1</h2>')
add("<h3>Task 2.1.1 &ndash; Activity lifecycle in Logcat</h3>")
add("<p>The lifecycle methods from listing 2 were added to <code>MainActivity</code>. Every overridden method first calls "
    "its version from the superclass and then writes a message with the tag <code>Lifecycle</code>. "
    "Logcat was filtered with <code>tag:Lifecycle</code>.</p>")
add(code(SRC / "MainActivity.kt"))
add("<h4>Logcat output</h4>")
add(log("a_start", "(a) after starting the application from the launcher"))
add(log("b_home_return", "(b) after pressing Home and returning to the application"))
add(log("c_rotate", "(c) after rotating the emulator to landscape"))
add(log("d_back", "(d) after pressing Back"))
add("""
<table class="t">
<tr><th>Case</th><th>Order of calls</th><th>Meaning</th></tr>
<tr><td>(a) start</td><td>onCreate &rarr; onStart &rarr; onResume</td><td>the Activity is created, becomes visible, then gets focus</td></tr>
<tr><td>(b) Home + return</td><td>onPause &rarr; onStop &nbsp;|&nbsp; onStart &rarr; onResume</td><td>the Activity is only hidden, <b>not</b> destroyed; when we return, <code>onCreate</code> is not called again &ndash; the same object is reused</td></tr>
<tr><td>(c) rotation</td><td>onPause &rarr; onStop &rarr; onDestroy &rarr; onCreate &rarr; onStart &rarr; onResume</td><td>configuration change: the old Activity is destroyed and a new one is created</td></tr>
<tr><td>(d) Back</td><td>onPause &rarr; onStop &rarr; onDestroy</td><td>the user leaves the screen, the Activity is finished</td></tr>
</table>
<p><b>What happened during the rotation.</b> Rotating the screen is a <i>configuration change</i> (the orientation and the
screen size change). The system did not try to adapt the existing screen &ndash; it destroyed the whole Activity
(<code>onPause</code>, <code>onStop</code>, <code>onDestroy</code>) and immediately created a new instance
(<code>onCreate</code>, <code>onStart</code>, <code>onResume</code>), so that resources for the new configuration (e.g. a
<code>layout-land</code> variant) can be loaded. The process number in the log (5052) did not change: the application process
lives on, only the Activity object is new. Therefore everything kept only in fields of the old Activity or in a plain
<code>remember</code> is lost &ndash; this is exactly what is observed again in task 2.2.1.</p>
""")
add(figs(("2_1_1_rotated_landscape", "Business card after rotating to landscape &ndash; the contact card does not fit on the screen"), landscape=True))
add(comment("The emulator was rotated with <code>adb shell settings put system user_rotation 1</code> (auto-rotation off), "
            "which has the same effect as the rotation button on the toolbar. In landscape the <code>Card</code> with the "
            "contacts is cut off, the same as in Figure 1 of the instruction, because the <code>Column</code> is not "
            "scrollable. It would be fixed by adding <code>Modifier.verticalScroll(rememberScrollState())</code>; I left "
            "the screen as in listing 6. In (b) <code>onRestart</code> is not visible only because it is not overridden."))

# ---------------------------------------------------------------- 2.1.2
add("<h3>Task 2.1.2 &ndash; Business card with my own data</h3>")
add("<p>The screen uses <code>ContactRow</code>, <code>ProfileHeader</code> and <code>BusinessCardScreen</code> from "
    "listings 5 and 6. All texts on the screen come from <code>strings.xml</code> via <code>stringResource</code>. "
    "A third contact row (GitHub) was added.</p>")
add(code(RES / "values/strings.xml"))
add(code(SRC / "BusinessCard.kt"))
add(figs(("2_1_2_card_light", "Business card on the emulator, three contact rows")))
add(comment("The phone number and the e-mail address are example values (the domain <code>example.com</code> is reserved "
            "for examples), so no real personal data is published in the report. The application worked on the first "
            "run. When importing <code>Alignment</code> Android Studio may propose <code>android.text.Layout.Alignment</code>; "
            "the correct one is <code>androidx.compose.ui.Alignment</code>."))

# ---------------------------------------------------------------- 2.1.3
add("<h3>Task 2.1.3 &ndash; Polish translation</h3>")
add("<p>First the labels <code>\"Phone\"</code> and <code>\"E-mail\"</code> (and the new <code>\"GitHub\"</code>) were "
    "moved from the code to <code>strings.xml</code> as <code>label_phone</code>, <code>label_email</code>, "
    "<code>label_github</code> (see the default <code>strings.xml</code> and <code>BusinessCardScreen</code> in task 2.1.2). "
    "Then the file <code>res/values-pl/strings.xml</code> was created with the qualifier <i>Locale: pl</i>:</p>")
add(code(RES / "values-pl/strings.xml"))
add("<p>Only translated strings are listed in <code>values-pl</code>. The other ones (name, phone, e-mail, GitHub address) "
    "are missing there on purpose &ndash; for a missing key Android falls back to the default "
    "<code>values/strings.xml</code>.</p>")
add(figs(("2_1_3_settings_polish", "Emulator system language: Polski (Polska)"),
         ("2_1_3_card_polish", "Business card with the language set to Polish: title, job title and labels are translated")))
add(comment("The language of the emulator was switched to Polish with <code>adb root</code> and "
            "<code>setprop persist.sys.locale pl-PL</code> (the same as Settings &rarr; System &rarr; Languages). Changing the "
            "language is also a configuration change, so the Activity is recreated and the texts are loaded again from "
            "<code>values-pl</code> without any change in the Kotlin code. The clock also switched to the 24-hour format."))

# ---------------------------------------------------------------- 2.1.4
add("<h3>Task 2.1.4 &ndash; Four quadrants and the order of modifiers</h3>")
add("<p>The screen is a <code>Column</code> with two <code>Row</code>s; each <code>Row</code> and each quadrant gets "
    "<code>Modifier.weight(1f)</code>, so the four parts are equal. Each quadrant has its own background colour, a bold "
    "centred title and a one-sentence description. The parameter <code>paddingBeforeBackground</code> swaps the order of "
    "<code>padding</code> and <code>background</code> in one quadrant (Box).</p>")
add(code(SRC / "Quadrants.kt"))
add(figs(("2_1_4_quadrants", "Before: <code>background(color).padding(16.dp)</code> in all quadrants"),
         ("2_1_4_quadrants_swapped", "After: <code>padding(16.dp).background(color)</code> in the Box quadrant")))
add("""
<p><b>Difference.</b> Modifiers are applied from left to right, each one wraps everything that follows it.</p>
<ul>
<li><code>background(color).padding(16.dp)</code> &ndash; the background is drawn for the full size of the quadrant first,
then 16&nbsp;dp of space is added <i>inside</i> it. The colour fills the whole quadrant, the text is 16&nbsp;dp away from the edge.</li>
<li><code>padding(16.dp).background(color)</code> &ndash; the 16&nbsp;dp is taken off first, so it lies <i>outside</i> the
coloured area. The blue rectangle is smaller and is surrounded by a frame of the screen background (it works like a margin),
and the text now has no inner space &ndash; e.g. &ldquo;e.g.&rdquo; reaches the edge of the blue area.</li>
</ul>
""")
add(comment("Without <code>color = Color.Black</code> the text would take <code>onSurface</code> from the theme and become "
            "white on the pastel colours in dark mode, so I set the text colour explicitly for these fixed backgrounds."))

# ---------------------------------------------------------------- 2.1.5
add("<h3>Task 2.1.5 &ndash; Own Material 3 colours</h3>")
add("<p>In <code>Color.kt</code> four own colours were defined (teal and orange). In <code>Theme.kt</code> the light colour "
    "scheme uses them for <code>primary</code>, <code>secondary</code>, <code>primaryContainer</code> and "
    "<code>secondaryContainer</code>, and <code>dynamicColor</code> is now <code>false</code> by default.</p>")
add(code(SRC / "ui/theme/Color.kt"))
add(code(SRC / "ui/theme/Theme.kt"))
add(figs(("2_1_5_card_light", "Light theme: own teal colours"),
         ("2_1_5_card_dark", "Dark theme: template's dark scheme")))
add("""
<p><b>Comparison of light and dark.</b> In the light theme the top bar and the circle behind the image use
<code>primaryContainer</code> (light teal <code>#9CF1F2</code>) and the job title uses <code>primary</code>
(dark teal <code>#00696B</code>). In the dark theme the same composables read the same roles, but the values come from
<code>DarkColorScheme</code>, which I did not change: <code>primary</code> is <code>Purple80</code> and
<code>primaryContainer</code> is the default dark baseline purple. The background becomes almost black, the texts switch to light
<code>onSurface</code>/<code>onBackground</code>, and the card uses a dark <code>surfaceVariant</code>. Nothing in the
composables had to change &ndash; they use only colour <i>roles</i>. The comparison also shows a weakness: the two themes now
look like two different brands (teal vs. purple). In a real application the dark scheme should get matching tones of the same
colours, e.g. a light teal <code>primary</code> and a dark teal <code>primaryContainer</code>.</p>
""")
add(comment("<code>dynamicColor = false</code> is required: with the template default <code>true</code>, on Android 12+ "
            "(the emulator has Android 14) the colours would be taken from the wallpaper and mine would be ignored. The screenshots were taken on the emulator with the system "
            "dark mode switched on and off (<code>adb shell cmd uimode night yes/no</code>); this renders the same as the "
            "&ldquo;Light&rdquo; and &ldquo;Dark&rdquo; <code>@Preview</code>s from listing 6, which are still in "
            "<code>BusinessCard.kt</code>. Switching to dark mode is again a configuration change &ndash; the Activity was recreated."))

# ---------------------------------------------------------------- 2.2.1
add('<h2 class="pb">Part 02.2</h2>')
add("<h3>Task 2.2.1 &ndash; remember vs rememberSaveable</h3>")
add("<p>Three versions of the counter: the broken one from listing 1, the working one with <code>remember</code> from "
    "listing 2, and the same counter with <code>rememberSaveable</code> (listing 3). Each was opened, the button was clicked "
    "five times (three times for the broken one) and the emulator was rotated.</p>")
add(code(SRC / "Counters.kt"))
add(figs(("2_2_1_broken_after_3_clicks", "Listing 1 after three clicks: still &ldquo;Clicked 0 times&rdquo;"),
         ("2_2_1_remember_before_rotation", "<code>remember</code>: 5 clicks, portrait"),
         ("2_2_1_saveable_before_rotation", "<code>rememberSaveable</code>: 5 clicks, portrait")))
add(figs(("2_2_1_remember_after_rotation", "<code>remember</code> after rotation &ndash; the counter is back at 0, Reset is disabled"), landscape=True))
add(figs(("2_2_1_saveable_after_rotation", "<code>rememberSaveable</code> after rotation &ndash; the counter still shows 5"), landscape=True))
add("""
<p><b>Difference between remember and rememberSaveable.</b> <code>remember</code> stores the state object in the
<i>composition</i>. It survives recompositions (every click redraws the text and the value stays), but it lives only as long as
the composition. In task 2.1.1 we saw that rotation calls <code>onDestroy</code> and then <code>onCreate</code> of a
<b>new</b> Activity. The old composition is thrown away together with the old Activity, <code>setContent</code> builds a new one,
and <code>remember { mutableIntStateOf(0) }</code> runs its initializer again &ndash; the counter starts from 0.
<code>rememberSaveable</code> additionally writes the value into the Activity's saved instance state (a <code>Bundle</code>)
when the old Activity is being destroyed. The new Activity receives this <code>Bundle</code> in
<code>onCreate(savedInstanceState)</code>, and <code>rememberSaveable</code> restores the value from it instead of
running the initializer, so the counter still shows 5.</p>
<p><b>Why listing 1 does not work.</b> <code>var count = 0</code> is an ordinary local variable. Clicking increases it,
but Compose does not observe ordinary variables: no state was read through the snapshot system, so no recomposition is
scheduled and the text keeps showing the old value. Even if something else triggered a recomposition, the function would run
from the beginning and execute <code>var count = 0</code> again, so the value would be lost anyway. It needs both
<code>mutableStateOf</code> (observable value) and <code>remember</code> (keep it between calls).</p>
""")
add(comment("Listing 1 compiles and runs &ndash; the mistake is not visible to the compiler, the button just does not react. "
            "<code>mutableIntStateOf</code> needs the imports <code>getValue</code>/<code>setValue</code> for the "
            "<code>by</code> delegate; without them the code does not compile."))

# ---------------------------------------------------------------- 2.2.2
add("<h3>Task 2.2.2 &ndash; Stateless RatingBar</h3>")
add("<p><code>RatingBar(rating, onRatingChange)</code> is stateless: it shows five buttons, filled (<code>Button</code>) "
    "up to the current rating and outlined (<code>OutlinedButton</code>) after it, and only reports the click. The three "
    "ratings are hoisted to <code>FilmRatingsScreen</code>, the lowest common ancestor of the three bars and the average, "
    "so the screen can compute the average &ndash; three stateful bars could not do that.</p>")
add(code(SRC / "Ratings.kt"))
add(figs(("2_2_2_ratings", "Ratings 5, 4 and 2 &rarr; average (5+4+2)/3 = 3.67")))
add(comment("A Material 3 <code>Button</code> has a minimum width and 24&nbsp;dp horizontal content padding, so five buttons "
            "with &ldquo;*&rdquo; did not fit nicely in one row. I set <code>Modifier.size(48.dp)</code> and "
            "<code>contentPadding = PaddingValues(0.dp)</code>. The value 0 means &ldquo;not rated yet&rdquo;, so the average "
            "is computed only from rated films; it is a derived value, not a separate state."))

# ---------------------------------------------------------------- 2.2.3
add("<h3>Task 2.2.3 &ndash; Extended sign-up form</h3>")
add("<p>The form from listing 5 got a password field (<code>PasswordVisualTransformation</code>, at least 8 characters with "
    "at least one digit), a confirmation field that must be equal to the password, and a <code>Switch</code> "
    "&ldquo;Newsletter&rdquo;. Every incorrect field shows its own message in <code>supportingText</code> (the age field "
    "too). After a successful sign-up all fields are cleared and the confirmation message stays below the button.</p>")
add(code(SRC / "SignUpForm.kt"))
add(figs(("2_2_3_form_errors", "Incorrect data: each field shows its error, Sign up is disabled"),
         ("2_2_3_form_valid", "Correct data, terms accepted, newsletter on: Sign up is enabled"),
         ("2_2_3_form_after_signup", "After Sign up: the form is cleared and the message is shown")))
add(comment("<code>formValid</code> also checks <code>confirmPassword.isNotEmpty()</code> &ndash; without it an empty "
            "confirmation would count as &ldquo;equal&rdquo; to an empty password. Errors are shown only after the user typed something, "
            "so an empty form is not red. With six fields the form is taller than a phone in landscape, so I added "
            "<code>verticalScroll</code> to the <code>Column</code> (this is allowed &ndash; there is no "
            "<code>LazyColumn</code> inside). The password is not stored anywhere; only the e-mail is used in the message."))

# ---------------------------------------------------------------- 2.2.4
add("<h3>Task 2.2.4 &ndash; Task list with priorities and filters</h3>")
add("<p><code>Task</code> got a <code>priority</code> of type <code>enum class Priority { LOW, NORMAL, HIGH }</code>, "
    "chosen with three <code>RadioButton</code>s before adding. The shown list is sorted with "
    "<code>sortedByDescending { it.priority }</code> (enums compare by their declaration order, so HIGH comes first). "
    "Three buttons All / Active / Done select a filter. Sorting and filtering produce a new derived list "
    "<code>visibleTasks</code>; the state <code>tasks</code> itself is never changed by the filter.</p>")
add(code(SRC / "TaskList.kt"))
add(figs(("2_2_4_tasks_all", "All: HIGH tasks at the top, then NORMAL, then LOW"),
         ("2_2_4_tasks_active", "Active: only not finished tasks (3 of 5)"),
         ("2_2_4_tasks_done", "Done: only finished tasks (2 of 5)")))
add(comment("The counter &ldquo;Done: 2 / 5&rdquo; is the same for every filter, which proves that the filter changes only "
            "what is shown. The sort is stable, so tasks with the same priority keep the order in which they were added. "
            "<code>Priority.entries</code> requires Kotlin 1.9 or newer (older code uses <code>values()</code>). "
            "The filter and the chosen priority are kept with <code>rememberSaveable</code> (an enum can be put into a "
            "<code>Bundle</code>), while the list itself is kept with <code>remember</code> as in listing 6, so &ndash; as the "
            "instruction says &ndash; the added tasks are lost after a rotation."))

# ---------------------------------------------------------------- questions 02.1
add('<h2 class="pb">Control questions &ndash; 02.1</h2>')
QA_21 = [
    ("1. What are the four kinds of components of an Android application? Which of them has a user interface?",
     "Activity, Service, Broadcast receiver and Content provider. Only the <b>Activity</b> has a user interface &ndash; it is "
     "a single screen and the entry point for the user. A Service works in the background, a Broadcast receiver reacts to "
     "system-wide events, and a Content provider shares data with other applications."),
    ("2. In what order are the lifecycle methods called when the user rotates the screen? Why is this a problem for the data of the Activity?",
     "<code>onPause &rarr; onStop &rarr; onDestroy &rarr; onCreate &rarr; onStart &rarr; onResume</code> (observed in task "
     "2.1.1, case c). The old Activity object is destroyed and a new one is created, so all data kept only in its fields, "
     "local variables or in plain <code>remember</code> is lost (e.g. the counter in task 2.2.1 went back to 0). Such data "
     "has to be saved in the saved instance state (<code>rememberSaveable</code>) or kept in a <code>ViewModel</code>."),
    ("3. What is the difference between the declarative and the imperative approach to building the user interface?",
     "In the <b>imperative</b> approach the screen is built once (e.g. from XML) and the code changes it step by step: it finds "
     "views and calls methods like <code>textView.setText(...)</code>; the programmer must remember to update every view, "
     "which easily leads to an inconsistent screen. In the <b>declarative</b> approach (Compose) the code describes "
     "<i>what</i> the screen should look like for the current data; when the data changes, the framework calls the "
     "functions again (recomposition) and updates the screen itself. The UI is a function of the state."),
    ("4. Why should texts be kept in strings.xml instead of being written directly in the code?",
     "So that the application can be translated without changing the code: the system chooses <code>values-pl/strings.xml</code> "
     "for a Polish phone automatically (task 2.1.3). All texts are in one place, they are easy to change and reuse, "
     "translators can work on XML files only, and the tools can check for missing translations."),
    ("5. Why does the order of modifiers matter? Give an example in which swapping two modifiers changes the result.",
     "Modifiers are applied from left to right and each one wraps the rest of the chain, so every modifier works on the size "
     "and position left by the previous ones. Example from task 2.1.4: <code>background(c).padding(16.dp)</code> paints the "
     "whole area and adds space inside the colour, while <code>padding(16.dp).background(c)</code> leaves a 16&nbsp;dp "
     "uncoloured margin around a smaller coloured area. Similarly, <code>clickable().padding()</code> makes the padding "
     "part of the touch area, but <code>padding().clickable()</code> does not."),
    ("6. What is a colour role in Material 3 and why is it better to use MaterialTheme.colorScheme.primary than a fixed colour?",
     "A colour role is a semantic name of a colour in the colour scheme &ndash; <code>primary</code>, <code>onPrimary</code>, "
     "<code>primaryContainer</code>, <code>surface</code>, <code>error</code> &hellip; &ndash; which describes <i>what the "
     "colour is used for</i>, not its value. The actual value comes from the current theme. Using "
     "<code>MaterialTheme.colorScheme.primary</code> means that the component changes automatically with the light/dark "
     "theme, dynamic colour or a new brand colour (task 2.1.5 &ndash; no composable had to be changed), and that matching "
     "pairs like <code>primary</code>/<code>onPrimary</code> keep good contrast. A fixed <code>Color(0xFF...)</code> would stay "
     "the same in dark mode and could become unreadable."),
]
for q, a in QA_21:
    add(f'<p class="q">{q}</p><p>{a}</p>')

# ---------------------------------------------------------------- questions 02.2
add("<h2>Control questions &ndash; 02.2</h2>")
QA_22 = [
    ("1. What is recomposition? Why does the change of an ordinary var not redraw the screen?",
     "Recomposition is calling composable functions again after the state they read has changed, so that the interface shows "
     "the new data; Compose re-runs only the functions that read the changed state. Compose knows about a change only for "
     "<b>observable</b> state created with <code>mutableStateOf</code>: reading it subscribes the function, writing it "
     "schedules a recomposition. An ordinary <code>var</code> is not observed, so its change schedules nothing (listing 1 in "
     "task 2.2.1), and in a new call it would be initialised again anyway."),
    ("2. What is the role of remember and of mutableStateOf? What happens when one of them is missing?",
     "<code>mutableStateOf</code> creates an observable value &ndash; changes cause recomposition. <code>remember</code> keeps an "
     "object between recompositions. Without <code>mutableStateOf</code> the value is kept but its change does not redraw "
     "the screen (the UI shows an old value). Without <code>remember</code> a new state object with the initial value is "
     "created in every recomposition, so the click triggers a recomposition which immediately resets the value &ndash; the "
     "counter would always show 0 (Android Studio warns about creating state without <code>remember</code>)."),
    ("3. What is the difference between remember and rememberSaveable? Which situations does each of them survive?",
     "<code>remember</code> survives only recompositions; the value is lost when the composable leaves the composition, on "
     "configuration changes (rotation, language, dark mode) and when the process is killed. <code>rememberSaveable</code> also "
     "saves the value in the saved instance state <code>Bundle</code>, so it survives configuration changes and the system "
     "killing the process in the background. Neither survives the user finishing the Activity with Back. "
     "<code>rememberSaveable</code> can store only <code>Bundle</code>-compatible values (numbers, String, Boolean, enums, "
     "Parcelable&hellip;) or values with a <code>Saver</code>."),
    ("4. What is state hoisting? What are the advantages of a stateless composable?",
     "State hoisting is moving the state up to the caller: the composable gets the current value and an event lambda "
     "(e.g. <code>rating: Int</code>, <code>onRatingChange: (Int) -&gt; Unit</code>) instead of owning the state. Data flows "
     "down, events flow up. A stateless composable is reusable (the same <code>RatingBar</code> is used three times), easy to "
     "preview and test with any value, has a single source of truth, and its state can be shared and combined by the caller "
     "(the average in task 2.2.2, the sum of two counters in listing 4)."),
    ("5. Why is a value such as formValid in listing 5 not kept in a separate state?",
     "Because it is <b>derived</b> &ndash; it can always be computed from the state that already exists (email, age, "
     "acceptTerms). Storing it separately would create a second source of truth that would have to be updated by hand after "
     "every change and could get out of sync with the fields. Computing it in every recomposition is cheap and is always "
     "correct."),
    ("6. Why does LazyColumn need the parameter key? What could go wrong without it when an item is deleted?",
     "Without <code>key</code> items are identified by their <b>position</b>. When an item is deleted, all items below it "
     "move up one position, so Compose thinks that the items changed their content: state remembered inside an item "
     "(e.g. a checkbox animation, text typed in a field, an expanded section) stays at the old position and is shown at the "
     "wrong task, more items are recomposed than needed, and animations of removal/reordering do not work correctly. "
     "<code>key = { it.id }</code> gives each item a stable identity, so its state moves together with it."),
]
for q, a in QA_22:
    add(f'<p class="q">{q}</p><p>{a}</p>')

page = f"<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><title>AMAD Report 02 - Deniz Vardal</title><style>{CSS}</style></head><body>{''.join(parts)}</body></html>"
OUT_HTML.write_text(page, encoding="utf-8")
print("HTML written:", OUT_HTML)

subprocess.run([
    EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--no-first-run",
    "--user-data-dir=" + str(Path(tempfile.gettempdir()) / "edge-report-profile"),
    f"--print-to-pdf={OUT_PDF}", OUT_HTML.as_uri(),
], check=True, timeout=180)
print("PDF written:", OUT_PDF, OUT_PDF.stat().st_size, "bytes")
