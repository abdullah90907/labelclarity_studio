# LabelClarity Studio

An interactive privacy label explainer and comparison prototype inspired by research on user acceptance of privacy labels.

## Quick visual preview

See the main outputs first, then scroll for full interpretation and validation.

### Privacy exposure score

![Privacy exposure score gauge](result/newplot%20(9).png)

### Radar risk profile

![Radar profile of privacy factors](result/newplot%20(8).png)

### Data sharing breakdown by purpose

![Data collection and sharing by purpose](result/newplot%20(7).png)

## What this project does

LabelClarity Studio helps users inspect app privacy labels in a more understandable way by adding:

- plain-language explanations for confusing label terms
- a lightweight privacy exposure score
- cross-app comparison views
- user-centered enhancement suggestions
- a short summary that translates dense labels into everyday language

## Why this project exists

Recent research on privacy labels found that users care about transparency, distrust self-reported labels, worry about data-category accuracy, and are influenced by the amount of data practice shown in a label. This prototype turns those findings into a practical decision-support interface.

## Main idea

Instead of showing only the raw label, the prototype answers questions a user actually has:

- How much data does this app collect?
- Is any of that data sensitive?
- Is any of it shared with third parties?
- Does the label rely on self-reporting?
- How does this app compare with others?
- What would make the label easier to trust and understand?

## Features

### 1. Privacy label explainer

The selected app is converted into a short plain-language explanation.

### 2. Lightweight privacy exposure score

The score combines:

- number of data categories
- number of sensitive categories
- number of shared categories
- number of linked categories
- advertising-related use
- self-reported disclosure status

This score is only a prototype design aid and not a legal or compliance judgment.

### 3. Cross-app comparison

Users can compare multiple sample apps and see how data collection practices differ.

### 4. Plain-language term help

The app explains terms such as identifiers, diagnostics, linked, shared, and self-reported.

### 5. Label enhancement suggestions

The app recommends ways a privacy label could be improved for user trust and readability.

## Project structure

```text
labelclarity_studio/
├── app.py
├── requirements.txt
├── README.md
├── result/
│   ├── newplot (7).png
│   ├── newplot (8).png
│   └── newplot (9).png
├── data/
│   └── sample_apps.json
└── src/
    └── privacy_utils.py
```

## Installation

Create and activate a virtual environment.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac or Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

## Run the app

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal.

## Visualization outputs and interpretation

The app produces multiple visual layers to explain privacy-label behavior. The screenshots below represent a valid run for the ChatLoop sample app.

### 1) Data collection and sharing breakdown

![Data collection and sharing by purpose](result/newplot%20(7).png)

What this chart shows:

- each bar is one data-use purpose
- color separates whether that purpose is shared with third parties or not
- in this run: Account management and Find friends are not shared
- in this run: Advertising, Analytics, and Nearby features are shared

Why this matters:

- users can immediately see if sharing is concentrated in specific purposes (especially advertising and analytics)

### 2) Multi-factor radar profile

![Radar profile of privacy factors](result/newplot%20(8).png)

What this chart shows:

- Data categories: 5
- Sensitive data: 3
- Shared data: 3
- Linked data: 4
- Advertising use: 1

Why this matters:

- it explains shape-based risk drivers, not just a single score
- a wide radar in shared/linked dimensions indicates higher exposure tendency

### 3) Privacy exposure score gauge

![Privacy exposure score gauge](result/newplot%20(9).png)

What this chart shows:

- final score displayed: 100 (High)
- gauge range: 0 to 100
- low/moderate/high zones are color-banded for quick interpretation

Why this matters:

- this is the fastest decision-support view for non-technical users

## Validation of the shown result

For ChatLoop (from data/sample_apps.json), the computed factors are:

- total items: 5
- sensitive count: 3
- shared count: 3
- linked count: 4
- advertising count: 1
- analytics count: 1

Current scoring formula in src/privacy_utils.py:

- score = total*10 + sensitive*12 + shared*15 + linked*8 + advertising*18 + analytics*6 + self_reported_bonus(8)
- score is capped at 100

For the shown sample, the raw value is 195, then capped to 100, which is why the gauge reads 100 and level is High.

## Reproduce the same output

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the app:

```bash
streamlit run app.py
```

3. In the UI, select ChatLoop and enable:

- Show raw label table
- Compare all sample apps (optional for extra charts)
- Show term explanations (optional)

4. Capture screenshots from the rendered charts.

## Sample use case

- choose a messaging or productivity app
- inspect its listed data categories
- read the plain-language summary
- check whether the app shares data or uses it for advertising
- compare it against other apps
- review the recommended label improvements

## Suggested research framing

You can describe this prototype like this:

> LabelClarity Studio is a user-centered privacy label analysis prototype that extends standard app privacy labels with plain-language explanations, lightweight risk scoring, and comparison support to reduce confusion and improve decision-making.

## Important note

This project uses a small synthetic dataset for demonstration. It is a research-inspired prototype, not a production privacy auditing system.
