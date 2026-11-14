# Compose Business Card App

AMAD Lab 02 – Jetpack Compose. Android app for Lab Report 02 of Advanced Mobile Application Development (2026/2027). It covers both instructions of the lab in one project: 02.1 (Activity lifecycle, resources, layouts, Material 3) and 02.2 (state, state hoisting, forms and lists).

| Task | Screen | What it shows |
|---|---|---|
| 2.1.1 | `card` | Lifecycle methods logged to Logcat (start, Home, rotation, Back) |
| 2.1.2 | `card` | Business card built from `strings.xml`, three contact rows |
| 2.1.3 | `card` | Polish translation in `values-pl/strings.xml` |
| 2.1.4 | `quadrants`, `quadrants_swapped` | Four equal quadrants; order of `padding` and `background` swapped in one |
| 2.1.5 | `card` | Own light colour scheme, `dynamicColor = false` |
| 2.2.1 | `broken`, `counter`, `counter_saveable` | Ordinary `var` vs `remember` vs `rememberSaveable` across rotation |
| 2.2.2 | `ratings` | Stateless `RatingBar` used three times, average of the ratings |
| 2.2.3 | `form` | Sign-up form with password, confirmation, newsletter switch and validation |
| 2.2.4 | `tasks` | `LazyColumn` task list with priorities, sorting and All / Active / Done filters |

## How it works

1. **One Activity.** `MainActivity` logs every lifecycle call with the tag `Lifecycle` and shows one screen chosen in a `when` expression.
2. **Choosing a screen.** The default is the business card. Any other screen is opened by passing its name when the Activity starts (`--es screen <name>`).
3. **Report.** `docs/build_report.py` reads the source files, the Logcat logs and the screenshots and prints the report to PDF with Edge, so the code in the PDF is always the code in the repository.

## Getting started

Requires JDK 17 and the Android SDK (API 34). Open the folder in Android Studio, or build from the command line:

```bash
./gradlew assembleDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

Open a specific screen:

```bash
adb shell am start -n com.example.businesscard/.MainActivity --es screen form
```

Screen names: `card`, `quadrants`, `quadrants_swapped`, `broken`, `counter`, `counter_saveable`, `ratings`, `form`, `tasks`.

Rebuild the report after changing the code or the screenshots:

```bash
python docs/build_report.py
```

## Project structure

```
├── app/src/main/java/com/example/businesscard/
│   ├── MainActivity.kt      lifecycle logging and screen selection
│   ├── BusinessCard.kt      ContactRow, ProfileHeader, BusinessCardScreen, light/dark previews
│   ├── Quadrants.kt         four-quadrant layout (Column, Row, Box, Spacer)
│   ├── Counters.kt          broken, remember and rememberSaveable counters
│   ├── Ratings.kt           stateless RatingBar and film ratings screen
│   ├── SignUpForm.kt        sign-up form with validation
│   ├── TaskList.kt          task list with priorities and filters
│   └── ui/theme/            colours, typography and BusinessCardTheme
├── app/src/main/res/        strings (English and Polish), launcher icon
└── docs/
    ├── AMAD_Report02_Vardal_Deniz.pdf   the submitted report
    ├── img/                 emulator screenshots used in the report
    ├── logs/                Logcat output for task 2.1.1
    └── build_report.py      report generator
```

Built with Kotlin, Jetpack Compose, Material 3 and Gradle.
