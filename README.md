# StudyMate AI 📚

An AI-powered study assistant that transforms PDF notes into summaries, interactive quizzes, flashcards, and question-answering support.

## ✨ Features

- **PDF Upload:** Extract text from PDF study materials.
- **AI Summaries:** Generate concise summaries of your notes.
- **Interactive Quizzes:** Generate multiple-choice questions, check answers, and view scores with explanations.
- **Flashcards:** Create flashcards to revise important concepts.
- **Ask Your Notes:** Ask questions based on your uploaded study material.

## 🛠️ Tech Stack

- Python
- Streamlit
- Groq API
- PyMuPDF
- python-dotenv

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Amit-0045/studymate-ai.git
cd studymate-ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project folder:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

Replace the placeholder with your own API key. Never upload your real API key to GitHub.

### 5. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## 🔐 Security

Keep your API key private. The `.env` file and virtual environment should not be committed to version control.

## 👨‍💻 Author

Built as an AI/ML learning and portfolio project.
