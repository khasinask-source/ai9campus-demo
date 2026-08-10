```python
import streamlit as st
import ollama


# ═══════════════════════════════════════════════════════════════
# 1. OLLAMA CONFIGURATION
# ═══════════════════════════════════════════════════════════════

OLLAMA_MODEL = "qwen3:8b"

# Change this if Ollama is running on another server.
# Example:
# OLLAMA_HOST = "http://192.168.1.100:11434"
OLLAMA_HOST = "http://localhost:11434"

ollama_client = ollama.Client(host=OLLAMA_HOST)


# ═══════════════════════════════════════════════════════════════
# 2. PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="AI9Campus Smart Tutor - Telangana State Board",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded"
)


# ═══════════════════════════════════════════════════════════════
# 3. CUSTOM CSS FOR BETTER UI
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<style>

.main-header {
    text-align: center;
    color: #1E88E5;
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.sub-header {
    text-align: center;
    color: #43A047;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.info-box {
    background-color: #E3F2FD;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #1E88E5;
    margin-bottom: 1rem;
}

.warning-box {
    background-color: #FFF3E0;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #FF9800;
    margin-bottom: 1rem;
}

</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 4. HEADER SECTION
# ═══════════════════════════════════════════════════════════════

st.markdown(
    '<div class="main-header">🎓 School-Name Smart Tutor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-header">Telangana State Board (SCERT) - Classes 1 to 10</div>',
    unsafe_allow_html=True
)


# ═══════════════════════════════════════════════════════════════
# 5. SIDEBAR - CURRICULUM INFO & SETTINGS
# ═══════════════════════════════════════════════════════════════

with st.sidebar:

    st.header("📚 Curriculum Information")

    st.markdown("""
    **Official Source:**  
    SCERT Telangana e-Textbooks  

    **Academic Year:** 2024-25

    **Coverage:**
    - 📖 **Classes:** 1 to 10
    - 🗣️ **Mediums:** English, Telugu, Urdu
    - 📝 **Subjects:** All SCERT subjects

    **Support:**
    - Primary (1-5)
    - Upper Primary (6-7)
    - High School (8-10)
    - SSC Exam Preparation
    """)

    st.divider()

    st.header("⚙️ Settings")

    student_class = st.selectbox(
        "Your Class",
        options=[
            "Select", "1", "2", "3", "4", "5",
            "6", "7", "8", "9", "10"
        ],
        index=0
    )

    medium = st.selectbox(
        "Medium of Instruction",
        options=["Select", "English", "Telugu", "Urdu"],
        index=0
    )

    st.divider()

    # Optional Ollama model display
    st.caption(f"🤖 Local AI Model: {OLLAMA_MODEL}")

    st.markdown("""
    **⚠️ Important Notes:**
    - Always verify chapter numbers with your textbook
    - Report any curriculum mismatches
    - This bot covers only TS Board syllabus

    **Need Help?**
    Press 👎 below any response to provide feedback.
    """)

    if st.button("🔄 Reset Chat", use_container_width=True):
        st.session_state.clear()
        st.rerun()


# ═══════════════════════════════════════════════════════════════
# 6. OLLAMA CONNECTION CHECK
# ═══════════════════════════════════════════════════════════════

@st.cache_resource
def check_ollama_connection():

    try:
        models_response = ollama_client.list()

        model_names = []

        # Compatible with different Ollama Python client versions
        if hasattr(models_response, "models"):
            for model in models_response.models:
                if hasattr(model, "model"):
                    model_names.append(model.model)
                elif hasattr(model, "name"):
                    model_names.append(model.name)

        elif isinstance(models_response, dict):
            for model in models_response.get("models", []):
                model_names.append(
                    model.get("model") or model.get("name")
                )

        model_exists = any(
            name == OLLAMA_MODEL
            or name.startswith(OLLAMA_MODEL.split(":")[0] + ":")
            for name in model_names
        )

        return True, model_exists, model_names

    except Exception as e:
        return False, False, str(e)


ollama_running, model_available, ollama_info = check_ollama_connection()

if not ollama_running:

    st.error("⚠️ **Ollama is not running or cannot be reached.**")

    st.markdown(f"""
    ### Please follow these steps:

    1. Make sure Ollama is installed.
    2. Open PowerShell or Command Prompt.
    3. Run:

    `ollama serve`

    4. In another terminal, make sure the model is downloaded:

    `ollama pull {OLLAMA_MODEL}`

    5. Restart this Streamlit application.
    """)

    with st.expander("Technical details"):
        st.code(str(ollama_info))

    st.stop()


if not model_available:

    st.error(f"⚠️ **The Ollama model `{OLLAMA_MODEL}` is not available.**")

    st.markdown(f"""
    Open PowerShell or Command Prompt and run:

    `ollama pull {OLLAMA_MODEL}`

    After the download completes, refresh this application.
    """)

    with st.expander("Available Ollama models"):
        if isinstance(ollama_info, list):
            st.write(ollama_info)

    st.stop()


# ═══════════════════════════════════════════════════════════════
# 7. CURRICULUM DATABASE
# ═══════════════════════════════════════════════════════════════

CURRICULUM_DB = {

    10: {

        "Social Studies": {

            "English": {

                1: "India: Relief Features",
                2: "Ideas of Development",
                3: "Production and Employment",
                4: "Climate of India",
                5: "Indian Rivers and Water Resources",
                6: "The Population",
                7: "Settlements - Migrations",
                8: "Rampur: A Village Economy",
                9: "Globalisation",
                10: "Food Security",
                11: "Sustainable Development with Equity",
                12: "World Between the World Wars (1914-1945)",
                13: "National Liberation Movements in the Colonies",
                14: "National Movement in India–Partition & Independence: 1939-1947",
                15: "The Making of Independent India's Constitution",
                16: "Election Process in India",
                17: "Independent India (The First 30 years: 1947-77)",
                18: "Emerging Political Trends 1977 to 2000",
                19: "Post - War World and India",
                20: "Social Movements in Our Times",
                21: "The Movement for the Formation of Telangana State"

            },

            "Telugu": {

                1: "భారతదేశం – మతాలు, తాత్విక దృక్పథం"

                # Add more Telugu chapters here

            }

        }

    }

    # Add more classes and subjects here

}


def verify_chapter_title(
    class_num,
    subject,
    chapter_num,
    medium="English"
):
    """Verify if chapter title matches curriculum database."""

    try:

        expected_title = (
            CURRICULUM_DB
            .get(int(class_num), {})
            .get(subject, {})
            .get(medium, {})
            .get(chapter_num)
        )

        return expected_title

    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════
# 8. OPTIMIZED SYSTEM PROMPT
# ═══════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """
You are an **AI School Tutor specialized in Telangana State Board (SCERT) Curriculum**.

═══════════════════════════════════════════════════════════════
📚 KNOWLEDGE BASE & SCOPE
═══════════════════════════════════════════════════════════════

**1. OFFICIAL SOURCE:**
- Primary Reference: SCERT Telangana e-Textbooks
- Academic Year: 2024-25 (Always verify with latest syllabus)
- Coverage: Classes 1-10
- Primary: Classes 1-5
- Upper Primary: Classes 6-7
- High School: Classes 8-10

**2. SUBJECTS COVERED:**
- Languages: Telugu, Hindi, English, Urdu, Sanskrit
- Mathematics: Arithmetic, Algebra, Geometry, Mensuration, Statistics
- Sciences: Physical Science, Biological Science, Environmental Science
- Social Studies: History, Geography, Civics, Economics
- Other: Computer Science, General Knowledge, Life Skills

**3. MEDIUM OF INSTRUCTION:**
Support ALL three mediums with equal expertise:
- English Medium
- Telugu Medium (తెలుగు మాధ్యమం)
- Urdu Medium (اردو میڈیم)

═══════════════════════════════════════════════════════════════
🎯 CURRICULUM STRUCTURE AWARENESS
═══════════════════════════════════════════════════════════════

IMPORTANT - Chapter Verification Protocol:

Before answering ANY chapter-specific question:

1. Ask for exact chapter number and subject if not provided.
2. Verify chapter title matches the curriculum information available.
3. Cross-reference page numbers if the student provides them.
4. If there is uncertainty or a mismatch, clearly say that the
   chapter structure may have been updated and ask the student to
   confirm the exact chapter title from their textbook.
5. Never invent an exact chapter title or page number when uncertain.

═══════════════════════════════════════════════════════════════
🎓 TEACHING METHODOLOGY BY CLASS LEVEL
═══════════════════════════════════════════════════════════════

PRIMARY (Classes 1-5):
- Use simple language and everyday examples.
- Incorporate storytelling and visual descriptions.
- Relate concepts to Telangana culture where appropriate.
- Use repetition and reinforcement.
- Encourage curiosity.
- Use a friendly tone and emojis when appropriate.

UPPER PRIMARY (Classes 6-7):
- Introduce structured learning with definitions.
- Use real-world Telangana examples where helpful.
- Build foundations for analytical thinking.
- Include simple diagram or flowchart descriptions.
- Connect concepts to practical applications.

HIGH SCHOOL (Classes 8-10):
- Provide detailed, exam-oriented explanations.
- Include key definitions, formulas and theorems when appropriate.
- Do not invent textbook page numbers.
- Explain answer patterns for 1-mark, 2-mark, 4-mark and 8-mark questions.
- Provide memory techniques where helpful.
- Highlight exam relevance without inventing official weightage.

═══════════════════════════════════════════════════════════════
📝 EXAM-ORIENTED SUPPORT
═══════════════════════════════════════════════════════════════

For numerical problems:

1. Read the question carefully.
2. Identify what is given.
3. Identify what must be found.
4. Write the correct formula.
5. Substitute the values.
6. Show calculations step by step.
7. Give the final answer with the correct unit.

For essay-type answers:

- Introduction
- Main explanation using clear points
- Examples where relevant
- Conclusion

Marking awareness:

- 1-mark: Direct and concise.
- 2-mark: Key points with a brief explanation.
- 4-mark: Structured explanation with sufficient points.
- 8-mark: Introduction, detailed points, examples and conclusion.

═══════════════════════════════════════════════════════════════
🚫 STRICT BOUNDARIES
═══════════════════════════════════════════════════════════════

Do not pretend that information is directly from an SCERT textbook
unless the exact information is available to you.

Never fabricate:
- Chapter numbers
- Chapter titles
- Page numbers
- Official weightage
- Official exam patterns
- Textbook quotations

If uncertain, clearly ask the student to provide the exact question,
chapter title, textbook page or image.

Always teach and explain. Do not merely provide a homework answer
without explanation.

═══════════════════════════════════════════════════════════════
🌐 MULTILINGUAL SUPPORT
═══════════════════════════════════════════════════════════════

If the student asks in Telugu:
- Respond primarily in Telugu.
- Include English terms in parentheses where useful.

If the student asks in Urdu:
- Respond primarily in Urdu.
- Include English terms in parentheses where useful.

If the student asks in English:
- Respond in English.

Support natural code-mixing such as Hinglish or Tenglish when the
student uses that style.

═══════════════════════════════════════════════════════════════
🔄 ADAPTIVE LEARNING
═══════════════════════════════════════════════════════════════

If the student struggles:
- Simplify the explanation.
- Give more examples.
- Break the topic into smaller steps.
- Ask which part is confusing.
- Explain prerequisite concepts if needed.

If the student understands quickly:
- Provide deeper insights within the school-level scope.
- Ask conceptual practice questions.
- Connect the concept with related topics.

═══════════════════════════════════════════════════════════════
🎯 RESPONSE QUALITY CHECK
═══════════════════════════════════════════════════════════════

Before every response, check:

- Is the explanation appropriate for the student's class?
- Is the language appropriate?
- Is the chapter/topic correctly identified?
- Is the answer understandable?
- Are formulas shown clearly?
- Are units included where necessary?
- Have you avoided inventing official textbook details?
- Is the tone encouraging and patient?

═══════════════════════════════════════════════════════════════
🎯 YOUR MISSION
═══════════════════════════════════════════════════════════════

Empower every Telangana student with:

- Accurate educational explanations
- Accessible multilingual learning
- Engaging examples
- Exam preparation support
- Confidence to learn

Be a trusted study companion: patient, clear, honest and encouraging.

Every student learns differently.
Adapt, explain and inspire! 🎓✨
"""


# ═══════════════════════════════════════════════════════════════
# 9. INITIALIZE CHAT HISTORY
# ═══════════════════════════════════════════════════════════════

if "message" not in st.session_state:

    st.session_state["message"] = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    st.session_state["user_info_collected"] = False


# ═══════════════════════════════════════════════════════════════
# 10. WELCOME MESSAGE
# ═══════════════════════════════════════════════════════════════

if not st.session_state.get("user_info_collected", False):

    with st.chat_message("assistant"):

        st.markdown("""
### Welcome to AI9Campus Smart Tutor! 👋

I'm your personal learning assistant for
**Telangana State Board (SCERT)** curriculum.

📚 **I can help you with:**

- Explaining concepts from your textbooks (Classes 1-10)
- Solving numerical problems step-by-step
- Exam preparation and answer writing techniques
- Clarifying doubts in English, Telugu, or Urdu medium

**Let's get started!** Ask me anything from your syllabus.

You can try:

- "Explain 10th class Social Studies Chapter 1"
- "How do I solve quadratic equations?"
- "What is photosynthesis in simple terms?"
- "తెలుగు మాధ్యమంలో వివరించు"
- "اردو میں آسانی سے سمجھائیں"
""")


# ═══════════════════════════════════════════════════════════════
# 11. DISPLAY CHAT HISTORY
# ═══════════════════════════════════════════════════════════════

for msg in st.session_state.message:

    if msg["role"] != "system":

        with st.chat_message(msg["role"]):

            st.markdown(msg["content"])


# ═══════════════════════════════════════════════════════════════
# 12. HANDLE USER INPUT
# ═══════════════════════════════════════════════════════════════

prompt = st.chat_input(
    "Ask your question here... (Type in English, Telugu, or Urdu)"
)


if prompt:

    st.session_state["user_info_collected"] = True

    # Add user message to history
    st.session_state.message.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):

        placeholder = st.empty()

        full_response = ""

        try:

            # Create streaming request using LOCAL OLLAMA
            stream = ollama_client.chat(

                model=OLLAMA_MODEL,

                messages=st.session_state.message,

                stream=True,

                options={

                    "temperature": 0.6,

                    "top_p": 0.9,

                    "num_predict": 4096

                }

            )


            # Process Ollama streaming response
            for chunk in stream:

                token = ""

                if hasattr(chunk, "message"):

                    if hasattr(chunk.message, "content"):
                        token = chunk.message.content or ""

                elif isinstance(chunk, dict):

                    token = (
                        chunk
                        .get("message", {})
                        .get("content", "")
                    )

                if token:

                    full_response += token

                    placeholder.markdown(
                        full_response + "▌"
                    )


            # Final response without cursor
            if full_response:

                placeholder.markdown(full_response)

                # Save assistant response
                st.session_state.message.append(
                    {
                        "role": "assistant",
                        "content": full_response
                    }
                )

            else:

                st.warning(
                    "⚠️ The local model returned an empty response. "
                    "Please try rephrasing your question."
                )


        except Exception as e:

            error_message = (
                f"❌ **An error occurred:** {str(e)}\n\n"
            )

            error_message += (
                "**Possible solutions:**\n\n"
            )

            error_message += (
                f"- Make sure Ollama is running at `{OLLAMA_HOST}`\n"
            )

            error_message += (
                f"- Make sure the model `{OLLAMA_MODEL}` is installed\n"
            )

            error_message += (
                f"- Run: `ollama pull {OLLAMA_MODEL}`\n"
            )

            error_message += (
                "- Check that your computer has enough RAM\n"
            )

            error_message += (
                "- Try asking your question in a different way\n"
            )

            st.error(error_message)


# ═══════════════════════════════════════════════════════════════
# 13. FOOTER & QUICK ACTIONS
# ═══════════════════════════════════════════════════════════════

st.divider()


col1, col2, col3 = st.columns(3)


with col1:

    if st.button(
        "📝 Sample Questions",
        use_container_width=True
    ):

        st.info("""
**Try asking:**

- Explain the water cycle (Class 6 Science)
- What is democracy? (Class 9 Social)
- Solve: x² + 5x + 6 = 0 (Class 10 Maths)
- రుతువులు ఎలా వస్తాయి? (Telugu)
""")


with col2:

    if st.button(
        "🎯 Exam Tips",
        use_container_width=True
    ):

        st.info("""
**SSC Exam Strategies:**

- Read questions carefully
- Attempt easy questions first
- Show all steps in numericals
- Use diagrams where required
- Review answers before submitting
""")


with col3:

    if st.button(
        "📞 Need Help?",
        use_container_width=True
    ):

        st.info("""
**Support:**

- Check your textbook for chapter numbers
- Verify important content with your teacher
- Report curriculum or answer issues to your school
- Refer to official SCERT Telangana materials
""")


st.caption(
    "🎓 Powered by AI9Campus | "
    "Telangana State Board (SCERT) Curriculum"
)

st.caption(
    f"🤖 Running locally with Ollama model: {OLLAMA_MODEL}"
)

st.caption(
    "⚠️ Always cross-verify important information "
    "with your textbook and teacher"
)
```
