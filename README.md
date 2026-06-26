# Agentic Deep Research Engine

## Requirements

* Python 3.10 or above
* Gemini API Key

## Installation

1. Clone or download the project.

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment.

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the project root:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

6. Run the project:

```bash
python main.py
```

## How to Use

1. Enter a research query.
2. The Planner Agent generates research sub-questions.
3. The system searches Wikipedia.
4. Documents are fetched and parsed.
5. Relevant evidence is extracted and ranked.
6. A final research report is generated automatically.

## Generated Report

After execution, the report is saved in:

```
reports/final_report.md
```

Open the report using:

* VS Code (recommended)
* Any Markdown Viewer
* Notepad (plain text)
* Typora (best formatting)

## Project Structure

```
deep_research_engine/
│
├── agents/
├── utils/
├── reports/
├── main.py
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```
