
import os
import fitz
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
import json

# -------------------- CONFIGURATION --------------------

load_dotenv()

st.set_page_config(
    page_title="StudyMate AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# -------------------- DESIGN --------------------

st.markdown("""
<style>
    .stApp {
        background: #0b1020;
        color: #edf2ff;
    }

    .block-container {
        max-width: 1600px;
        width: 100%;
        padding: 2rem 3rem 3rem;
        margin: auto;
    }

    [data-testid="stSidebar"] {
        background: #111a30;
        border-right: 1px solid #273653;
    }

    h1, h2, h3 {
        color: #f4f7ff !important;
        letter-spacing: -0.4px;
    }

    h1 {
        font-size: 2.4rem !important;
    }

    h2 {
        font-size: 1.75rem !important;
    }

    h3 {
        font-size: 1.3rem !important;
    }

    p, li, label, .stMarkdown {
        font-size: 16px;
        line-height: 1.7;
    }

    .hero {
        background: linear-gradient(120deg, #172e59, #39245f);
        border: 1px solid #465b8a;
        border-radius: 18px;
        padding: 32px;
        margin-bottom: 28px;
    }

    .eyebrow {
        color: #b9caff;
        text-transform: uppercase;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
    }

    .hero h1 {
        margin-top: 12px;
        font-size: 2.3rem !important;
    }

    .hero p {
        color: #dce5ff;
        margin-bottom: 0;
    }

    .metric-card {
        background: #141f35;
        border: 1px solid #2d4163;
        border-radius: 14px;
        padding: 20px;
        min-height: 125px;
    }

    .metric-label {
        color: #aebfdf;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .metric-value {
        color: #ffffff;
        font-size: 28px;
        font-weight: 750;
        margin-top: 8px;
    }

    .metric-detail {
        color: #9eb2d8;
        font-size: 13px;
        margin-top: 4px;
    }

    .section-intro {
        color: #aebfdf;
        margin-top: -8px;
        margin-bottom: 20px;
    }

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 10px;
        min-height: 44px;
        font-weight: 650;
    }

    .stTextInput input,
    .stTextArea textarea {
        border-radius: 10px;
    }

    [data-testid="stFileUploader"] {
        background: #121d32;
        border: 1px dashed #506895;
        border-radius: 14px;
        padding: 12px;
    }

    [data-testid="stMetric"] {
        background: #141f35;
        border: 1px solid #2d4163;
        padding: 16px;
        border-radius: 12px;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
    }

    hr {
        border-color: #293854;
        margin: 28px 0;
    }

    .small-note {
        color: #9eafd0;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- AI FUNCTIONS --------------------

def get_client():
    if not API_KEY:
        raise ValueError(
            "Groq API key not found. Check that GROQ_API_KEY "
            "is correctly set in your .env file."
        )
    return Groq(api_key=API_KEY)


def ask_ai(instructions, notes, question=None):
    client = get_client()

    user_message = (
        f"LECTURE NOTES:\n{notes}\n\n"
        f"INSTRUCTIONS:\n{instructions}"
    )

    if question:
        user_message += f"\n\nSTUDENT QUESTION:\n{question}"

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are StudyMate AI, a helpful college study assistant. "
                    "Use the supplied lecture notes as your primary source. "
                    "Be accurate, clear, well-structured, and useful for exams. "
                    "Do not invent facts from the notes. If information is "
                    "missing, say so. Use Markdown formatting."
                ),
            },
            {"role": "user", "content": user_message},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content


def extract_pdf(uploaded_file):
    pdf_bytes = uploaded_file.getvalue()
    text_parts = []

    with fitz.open(stream=pdf_bytes, filetype="pdf") as pdf:
        page_count = len(pdf)

        for page_number, page in enumerate(pdf, start=1):
            page_text = page.get_text("text").strip()

            if page_text:
                text_parts.append(
                    f"\n--- Page {page_number} ---\n{page_text}"
                )

    return page_count, "\n".join(text_parts).strip()


def show_ai_result(title, content, filename):
    st.markdown(f"### {title}")
    st.markdown(content)

    st.download_button(
        label="⬇️ Download as Markdown",
        data=content,
        file_name=filename,
        mime="text/markdown",
        key=f"download_{filename}",
    )


# -------------------- SIDEBAR --------------------

with st.sidebar:
    st.markdown("## 📚 StudyMate AI")
    st.caption("YOUR PERSONAL STUDY COMPANION")

    st.divider()

    st.markdown("### 🧭 Navigation")
    st.markdown(
        "- 🏠 Dashboard\n"
        "- 📝 AI Summary\n"
        "- 🎯 Quiz Generator\n"
        "- 🗂️ Flashcards\n"
        "- 💬 Ask Your Notes"
    )

    st.divider()

    st.markdown("### ✨ Your study toolkit")
    st.markdown(
        "- PDF text extraction\n"
        "- AI-powered summaries\n"
        "- Practice questions\n"
        "- Revision flashcards\n"
        "- Context-based Q&A"
    )

    st.divider()

    st.caption("Built with Python · Streamlit · Groq")


# -------------------- HEADER --------------------

st.markdown("""
<div class="hero">
    <div class="eyebrow">Learn smarter, not longer</div>
    <h1>Welcome to StudyMate AI 👋</h1>
    <p>
        Turn your lecture notes into clear summaries, practice quizzes,
        revision flashcards, and helpful answers.
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------- DOCUMENT UPLOAD --------------------

st.markdown("## 📂 Your study workspace")
st.markdown(
    '<p class="section-intro">'
    'Upload your lecture notes to begin your revision session.'
    '</p>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Upload your lecture notes (PDF)",
    type=["pdf"],
    help="Choose a text-based PDF containing your lecture notes.",
)

if uploaded_file:
    try:
        page_count, extracted_text = extract_pdf(uploaded_file)

        if not extracted_text:
            st.error(
                "No readable text was found. This may be a scanned PDF. "
                "OCR support can be added later."
            )
            st.stop()

        # Limit text sent to the AI to help manage request size.
        notes = extracted_text[:12000]

        st.success("✅ PDF uploaded and text extracted successfully!")

        word_count = len(extracted_text.split())
        char_count = len(extracted_text)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📄 PDF pages</div>
                <div class="metric-value">{page_count}</div>
                <div class="metric-detail">Pages detected</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📝 Word count</div>
                <div class="metric-value">{word_count:,}</div>
                <div class="metric-detail">{char_count:,} characters</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">✨ AI status</div>
                <div class="metric-value">Ready</div>
                <div class="metric-detail">Choose a study tool below</div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("👀 Preview extracted lecture notes"):
            st.text_area(
                "Extracted text",
                value=extracted_text[:12000],
                height=260,
                disabled=True,
                label_visibility="collapsed",
            )

        st.divider()

        # -------------------- STUDY TOOLS --------------------

        st.markdown("## ✨ AI study assistant")
        st.markdown(
            '<p class="section-intro">'
            'Choose a tool to turn your notes into useful study material.'
            '</p>',
            unsafe_allow_html=True,
        )

        summary_tab, quiz_tab, flashcard_tab, ask_tab = st.tabs([
            "📝 Summary",
            "🎯 Quiz Generator",
            "🗂️ Flashcards",
            "💬 Ask Your Notes",
        ])

        with summary_tab:
            st.markdown("### 📝 Create your revision summary")
            st.write(
                "Get organized notes with definitions, key concepts, "
                "examples, and exam-focused takeaways."
            )

            if st.button(
                "✨ Generate AI Summary",
                type="primary",
                key="generate_summary",
                use_container_width=False,
            ):
                with st.spinner("Creating your summary..."):
                    try:
                        result = ask_ai(
                            instructions=(
                                "Create a detailed but readable college "
                                "revision summary from these lecture notes. "
                                "Use a suitable title, clear headings, bullet "
                                "points, important definitions, examples, "
                                "and exam tips. Preserve important formulas "
                                "and technical terms. Do not add unsupported "
                                "facts. Clearly flag any unclear content."
                            ),
                            notes=notes,
                        )
                        st.session_state["summary_result"] = result
                    except Exception as error:
                        st.error(f"Could not generate summary: {error}")

            if st.session_state.get("summary_result"):
                show_ai_result(
                    "📑 Your AI-generated summary",
                    st.session_state["summary_result"],
                    "studymate_summary.md",
                )

        
        with quiz_tab:
            st.markdown("### 🎯 Test your understanding")
            st.write("Answer the questions and submit to see your score.")

            question_count = st.selectbox(
                "Number of questions",
                [5, 10, 15],
                index=0,
                key="quiz_count",
            )

            if st.button(
                "🚀 Generate Interactive Quiz",
                type="primary",
                key="generate_quiz",
            ):
                with st.spinner("Preparing your quiz..."):
                    try:
                        result = ask_ai(
                            instructions=(
                                f"Create exactly {question_count} multiple-choice "
                                "questions using only the lecture notes. Return "
                                "ONLY valid JSON, without Markdown code fences, "
                                "in this format: "
                                '{"questions":[{"question":"Question text",'
                                '"options":{"A":"Option A","B":"Option B",'
                                '"C":"Option C","D":"Option D"},'
                                '"answer":"A","explanation":"Why A is correct"}]}. '
                                "Each answer must be A, B, C, or D. Include four "
                                "options and a short explanation per question. "
                                "Avoid repeated questions and unsupported facts."
                            ),
                            notes=notes,
                        )

                        cleaned = result.strip()
                        if cleaned.startswith("```"):
                            cleaned = cleaned.split("\n", 1)[1]
                            if cleaned.rstrip().endswith("```"):
                                cleaned = cleaned.rstrip()[:-3]
                            cleaned = cleaned.strip()

                        data = json.loads(cleaned)
                        questions = data.get("questions", [])

                        if not questions:
                            raise ValueError("No questions were returned.")

                        for item in questions:
                            if (
                                not all(k in item for k in [
                                    "question", "options", "answer"
                                ])
                                or item["answer"] not in ["A", "B", "C", "D"]
                                or not all(k in item["options"] for k in [
                                    "A", "B", "C", "D"
                                ])
                            ):
                                raise ValueError(
                                    "The quiz format was invalid. Please try again."
                                )

                        st.session_state["interactive_quiz"] = data
                        st.session_state["quiz_submitted"] = False
                        st.session_state.pop("quiz_score", None)

                        for i in range(len(questions)):
                            st.session_state.pop(f"interactive_answer_{i}", None)

                    except Exception as error:
                        st.error(f"Could not generate quiz: {error}")

            quiz_data = st.session_state.get("interactive_quiz")

            if quiz_data:
                questions = quiz_data["questions"]
                st.markdown("---")
                st.markdown("### 📝 Your quiz")
                st.caption(
                    f"{len(questions)} questions · 1 point per correct answer"
                )

                for i, item in enumerate(questions):
                    st.markdown(f"**Q{i + 1}. {item['question']}**")

                    st.radio(
                        "Choose your answer",
                        options=["A", "B", "C", "D"],
                        format_func=lambda key, opts=item["options"]: (
                            f"{key}. {opts[key]}"
                        ),
                        key=f"interactive_answer_{i}",
                        disabled=st.session_state.get(
                            "quiz_submitted", False
                        ),
                        label_visibility="collapsed",
                    )

                    if st.session_state.get("quiz_submitted", False):
                        chosen = st.session_state.get(
                            f"interactive_answer_{i}"
                        )
                        correct = item["answer"]

                        if chosen == correct:
                            st.success("Correct!")
                        else:
                            st.error(
                                f"Correct answer: {correct}. "
                                f"{item['options'][correct]}"
                            )

                        st.info(
                            item.get("explanation", "No explanation provided.")
                        )

                    st.divider()

                if not st.session_state.get("quiz_submitted", False):
                    if st.button(
                        "✅ Submit Answers",
                        type="primary",
                        key="submit_interactive_quiz",
                    ):
                        score = sum(
                            1 for i, item in enumerate(questions)
                            if st.session_state.get(
                                f"interactive_answer_{i}"
                            ) == item["answer"]
                        )
                        st.session_state["quiz_score"] = score
                        st.session_state["quiz_submitted"] = True
                        st.rerun()

                else:
                    score = st.session_state.get("quiz_score", 0)
                    total = len(questions)
                    percentage = round(score / total * 100)

                    st.markdown("### 🏆 Your results")
                    st.metric("Final score", f"{score} / {total}", f"{percentage}%")
                    st.progress(percentage / 100)

                    if percentage == 100:
                        st.success("Perfect score! Excellent work!")
                    elif percentage >= 60:
                        st.success("Good job! Review your mistakes to improve.")
                    else:
                        st.warning("Keep practising and review the explanations.")

                    if st.button("🔄 Generate Another Quiz", key="reset_interactive_quiz"):
                        st.session_state.pop("interactive_quiz", None)
                        st.session_state.pop("quiz_submitted", None)
                        st.session_state.pop("quiz_score", None)
                        for i in range(len(questions)):
                            st.session_state.pop(f"interactive_answer_{i}", None)
                        st.rerun()

        with flashcard_tab:
            st.markdown("### 🗂️ Revise with flashcards")
            card_count = st.selectbox(
                "Number of flashcards",
                [5, 10, 15],
                index=0,
                key="card_count",
            )

            if st.button(
                "✨ Create Flashcards",
                type="primary",
                key="generate_flashcards",
            ):
                with st.spinner("Creating your flashcards..."):
                    try:
                        result = ask_ai(
                            instructions=(
                                f"Create {card_count} useful study "
                                "flashcards from the lecture notes. Format "
                                "each card with a numbered heading, a "
                                "**Question / Front** section, and an "
                                "**Answer / Back** section. Keep questions "
                                "focused on one concept each. Include key "
                                "definitions, formulas, and comparisons "
                                "where relevant. Use only supported content."
                            ),
                            notes=notes,
                        )
                        st.session_state["flashcards_result"] = result
                    except Exception as error:
                        st.error(f"Could not create flashcards: {error}")

            if st.session_state.get("flashcards_result"):
                show_ai_result(
                    "🧠 Your flashcards",
                    st.session_state["flashcards_result"],
                    "studymate_flashcards.md",
                )

        with ask_tab:
            st.markdown("### 💬 Ask a question about your notes")
            st.write(
                "Ask about a concept, definition, formula, or example "
                "from the uploaded lecture notes."
            )

            question = st.text_area(
                "Your question",
                placeholder="For example: Explain the difference between ML and deep learning.",
                height=100,
                key="student_question",
            )

            if st.button(
                "💡 Get Answer",
                type="primary",
                key="ask_question",
            ):
                if not question.strip():
                    st.warning("Please enter a question first.")
                else:
                    with st.spinner("Finding an answer in your notes..."):
                        try:
                            result = ask_ai(
                                instructions=(
                                    "Answer the student's question using "
                                    "the lecture notes as your primary source. "
                                    "Explain the idea in simple language, "
                                    "then give a short example if supported. "
                                    "If the notes do not contain enough "
                                    "information, clearly say so rather "
                                    "than guessing."
                                ),
                                notes=notes,
                                question=question.strip(),
                            )
                            st.session_state["answer_result"] = result
                        except Exception as error:
                            st.error(f"Could not answer your question: {error}")

            if st.session_state.get("answer_result"):
                show_ai_result(
                    "💬 Answer from your study assistant",
                    st.session_state["answer_result"],
                    "studymate_answer.md",
                )

    except Exception as error:
        st.error(f"Could not read this PDF: {error}")

else:
    st.info(
        "👆 Upload a PDF above to unlock summaries, quizzes, flashcards, "
        "and question answering."
    )

    st.markdown("### What you can do with StudyMate AI")

    feature1, feature2, feature3, feature4 = st.columns(4)

    with feature1:
        st.markdown("#### 📝 Summarize")
        st.write("Convert lengthy lecture notes into revision material.")

    with feature2:
        st.markdown("#### 🎯 Practice")
        st.write("Generate multiple choice questions from your notes.")

    with feature3:
        st.markdown("#### 🗂️ Memorize")
        st.write("Create question-and-answer flashcards.")

    with feature4:
        st.markdown("#### 💬 Understand")
        st.write("Ask questions about the material you upload.")

st.divider()

st.markdown(
    '<p class="small-note">'
    'StudyMate AI · Built with Python, Streamlit, PyMuPDF and Groq. '
    'Always verify important academic information against your original notes.'
    '</p>',
    unsafe_allow_html=True,
)
