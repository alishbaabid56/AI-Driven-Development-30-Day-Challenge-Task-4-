# import streamlit as st
# from agent import main as run_agent
# import asyncio
# import os
# import tempfile
# import json



# # --- Page Configuration ---
# st.set_page_config(
#     page_title="IntelliNote AI",
#     page_icon="🧠",
#     layout="wide",
# )



# # --- Sidebar ---

# # --- Initialize Session State ---
# if 'quiz_generated' not in st.session_state:
#     st.session_state['quiz_generated'] = False
# if 'quiz_data' not in st.session_state:
#     st.session_state['quiz_data'] = []
# if 'summary_text' not in st.session_state:
#     st.session_state['summary_text'] = ""
# if 'score' not in st.session_state:
#     st.session_state['score'] = 0
# if 'answers' not in st.session_state:
#     st.session_state['answers'] = {}

# # --- Main Application ---
# st.title("🧠 IntelliNote AI: Summarizer & Quiz Generator")

# st.markdown(
#     "Upload your PDF study notes, and let the AI assistant create a summary and a quiz for you."
# )

# # PDF uploader
# uploaded_file = st.file_uploader(
#     "Upload your Study Notes (PDF)",
#     type=["pdf"],
#     help="Please upload a PDF file containing your notes."
# )

# # If a file is uploaded, manage the state
# if uploaded_file:
#     # This block handles the logic for when a quiz has NOT been generated yet.
#     if not st.session_state.quiz_generated:
        
#         # --- Options for Quiz Generation ---
#         st.subheader("Quiz Options")
#         col1, col2 = st.columns(2)
#         with col1:
#             quiz_type = st.selectbox("Quiz Type:", ("Multiple Choice", "True/False"))
#         with col2:
#             num_questions = st.number_input("Number of Questions:", min_value=3, max_value=15, value=5, step=1)
        
#         if st.button("✨ Generate Summary & Quiz", use_container_width=True):
#             with st.spinner("🤖 The AI agent is processing your document... Please wait."):
#                 try:
#                     # Save uploaded file to a temporary path
#                     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
#                         tmp_file.write(uploaded_file.getvalue())
#                         tmp_file_path = tmp_file.name
                    
#                     # Run the agent and get the result, passing all options
#                     result = asyncio.run(run_agent(
#                         file_path=tmp_file_path, 
#                         quiz_type=quiz_type, 
#                         num_questions=num_questions
#                     ))
#                     os.remove(tmp_file_path) # Clean up temp file

#                     if result:
#                         # Parse the agent's response
#                         try:
#                             summary_part, quiz_part = result.split("---QUIZ---")
#                             st.session_state.summary_text = summary_part.replace("---SUMMARY---", "").strip()
#                             json_str = quiz_part.strip().lstrip("```json").rstrip("```").strip()
#                             st.session_state.quiz_data = json.loads(json_str)
#                             st.session_state.quiz_generated = True # Set the flag
#                             # Reset score and answers for the new quiz
#                             st.session_state.score = 0
#                             st.session_state.answers = {}
#                             st.balloons()
#                             st.rerun() # Rerun to enter the display logic below
#                         except (ValueError, json.JSONDecodeError) as e:
#                             st.error(f"Error parsing the agent's response. Please try again. Details: {e}")
#                             st.session_state.summary_text = result
#                     else:
#                         st.error("The agent did not return a result. Please check the console for logs.")

#                 except Exception as e:
#                     st.error(f"An error occurred: {e}")
#                     if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
#                         os.remove(tmp_file_path)


#     # This block handles displaying the quiz AFTER it has been generated
#     if st.session_state.quiz_generated:
#         st.header("Results")
#         summary_tab, quiz_tab = st.tabs(["📝 Summary", "❓ Quiz"])

#         with summary_tab:
#             st.subheader("Generated Summary")
#             st.markdown(st.session_state.summary_text)

#         with quiz_tab:
#             st.subheader("Generated Quiz")
#             if not st.session_state.quiz_data:
#                 st.warning("No quiz data to display.")
#             else:
#                 total_questions = len(st.session_state.quiz_data)
#                 st.metric(label="Your Score", value=f"{st.session_state.score} / {total_questions}")
#                 st.divider()

#                 for i, question_data in enumerate(st.session_state.quiz_data):
#                     st.markdown(f"**Question {i+1}: {question_data['question']}**")
#                     if i in st.session_state.answers:
#                         st.radio("Your selection:", options=question_data['options'], key=f"q_{i}_display",
#                                  index=question_data['options'].index(st.session_state.answers[i]['user_answer']),
#                                  disabled=True, label_visibility="collapsed")
#                         if st.session_state.answers[i]['is_correct']:
#                             st.success("You answered: Correct! 🎉")
#                         else:
#                             st.error(f"You answered: Incorrect. The correct answer was: **{st.session_state.answers[i]['correct_answer']}**")
#                     else:
#                         with st.form(key=f"quiz_form_{i}"):
#                             user_answer = st.radio("Choose your answer:", options=question_data['options'],
#                                                    key=f"q_{i}_option", label_visibility="collapsed")
#                             submitted = st.form_submit_button("Check Answer")
#                             if submitted:
#                                 correct_answer = question_data['answer']
#                                 is_correct = (user_answer.strip() == correct_answer.strip())
#                                 if is_correct:
#                                     st.session_state.score += 1
#                                 st.session_state.answers[i] = {
#                                     'user_answer': user_answer,
#                                     'correct_answer': correct_answer,
#                                     'is_correct': is_correct
#                                 }
#                                 st.rerun()
        
#         if st.button("↩️ Start Over"):
#             st.session_state.quiz_generated = False
#             st.session_state.quiz_data = []
#             st.session_state.summary_text = ""
#             st.session_state.score = 0
#             st.session_state.answers = {}
#             st.rerun()

# else:
#     # If no file is uploaded, reset the state
#     st.session_state.quiz_generated = False
#     st.session_state.quiz_data = []
#     st.session_state.summary_text = ""
#     st.session_state.score = 0
#     st.session_state.answers = {}
#     st.info("Please upload a PDF file to get started.")


import streamlit as st
from agent import main as run_agent
import asyncio
import os
import tempfile
import json

# ------------------------------------------------------------
#                     PAGE CONFIGURATION
# ------------------------------------------------------------
st.set_page_config(page_title="StudySense AI", page_icon="📚", layout="wide")

# --------------------- Modern Custom CSS ---------------------
st.markdown("""
<style>
    .main { background-color: #f4f6fb; }
    .big-card {
        background: white; padding: 30px; border-radius: 18px;
        border: 1px solid #dedede; box-shadow: 0px 4px 18px rgba(0,0,0,0.07);
    }
    .summary-box {
        background: #ffffff; padding: 24px; border-radius: 15px;
        border: 1px solid #e6e6e6; font-size: 17px; line-height: 1.7;
    }
    .score-card {
        padding: 30px; background: #ffffff; border-radius: 14px;
        border-left: 8px solid #4a90e2; box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
#                   SESSION STATE INIT
# ------------------------------------------------------------
required_keys = [
    "quiz_generated", "quiz_data", "summary_text",
    "answers", "quiz_finished", "user_answers"
]
for key in required_keys:
    if key not in st.session_state:
        st.session_state[key] = False if "generated" in key or "finished" in key else (
            [] if "data" in key or "answers" in key else ""
        )
if "user_answers" not in st.session_state:
    st.session_state.user_answers = []

# ------------------------------------------------------------
#                      UTILITIES
# ------------------------------------------------------------
def normalize(text):
    return text.replace("\n", "").replace("\r", "").strip().lower()

# ------------------------------------------------------------
#                      HEADER
# ------------------------------------------------------------
st.title("📚 StudySense AI")
st.caption("Your intelligent study partner — Summaries, Quizzes & Smart Learning ✨🧠")

st.markdown("""
<div class="big-card">
Upload your <b>PDF study notes 📄</b>, and StudySense AI will instantly generate:
<br><br>
<ul>
<li>📝 A structured, clean, easy-to-read summary</li>
<li>🧩 Automatically generated quiz (Multiple Choice or True/False)</li>
</ul>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📤 Upload Your Study Notes (PDF Only)", type=["pdf"])

# ------------------------------------------------------------
#                  FILE PROCESSING & GENERATION
# ------------------------------------------------------------
if uploaded_file and not st.session_state.quiz_generated:
    col1, col2 = st.columns(2)
    with col1:
        quiz_type = st.selectbox("Quiz Type 🧩", ["Multiple Choice", "True/False"])
    with col2:
        num_questions = st.slider("Number of Questions 🎯", 3, 20, 8)

    if st.button("🚀 Generate Summary & Quiz", type="primary"):
        with st.spinner("🤖 StudySense AI is reading your notes and creating quiz..."):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name

                result = asyncio.run(run_agent(
                    document_path=tmp_path,
                    quiz_type=quiz_type,
                    total_questions=num_questions
                ))
                os.unlink(tmp_path)

                if result and "---QUIZ---" in result:
                    summary_part, quiz_part = result.split("---QUIZ---")
                    st.session_state.summary_text = summary_part.replace("---SUMMARY---", "").strip()

                    quiz_json = quiz_part.strip().lstrip("```json").rstrip("```").strip()
                    st.session_state.quiz_data = json.loads(quiz_json)

                    # Clean data
                    for q in st.session_state.quiz_data:
                        q["options"] = [opt.strip() for opt in q["options"]]
                        q["answer"] = q["answer"].strip()

                    st.session_state.quiz_generated = True
                    st.session_state.quiz_finished = False
                    st.session_state.user_answers = [""] * len(st.session_state.quiz_data)
                    st.session_state.answers = {}

                    st.success("🎉 Summary & Quiz Generated Successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("⚠️ Agent returned unexpected format.")
            except Exception as e:
                st.error(f"❌ Error: {e}")

# ------------------------------------------------------------
#                  MAIN QUIZ INTERFACE
# ------------------------------------------------------------
if st.session_state.quiz_generated:
    st.header("🧠 Your Personalized Study Quiz")
    summary_tab, quiz_tab = st.tabs(["📄 Summary", "📝 Quiz"])

    # ==================== SUMMARY TAB ====================
    with summary_tab:
        st.subheader("📄 Generated Summary")
        st.markdown(f"<div class='summary-box'>{st.session_state.summary_text}</div>", 
                    unsafe_allow_html=True)

    # ==================== QUIZ TAB ====================
    with quiz_tab:
        total = len(st.session_state.quiz_data)

        # Initialize user answers
        if len(st.session_state.user_answers) != total:
            st.session_state.user_answers = [""] * total

        # Quiz Form (All questions at once)
        if not st.session_state.quiz_finished:
            with st.form("full_quiz_form"):
                st.write(f"**Answer all {total} questions and click Submit 🏁**")

                for idx, q in enumerate(st.session_state.quiz_data):
                    st.markdown(f"### {idx+1}. {q['question']}")

                    # Create labeled options: A. Text, B. Text, etc.
                    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    labeled = [f"{letters[i]}. {opt}" for i, opt in enumerate(q["options"])]

                    # Pre-select previous answer if exists
                    default_idx = 0
                    if st.session_state.user_answers[idx] in labeled:
                        default_idx = labeled.index(st.session_state.user_answers[idx])

                    choice = st.radio(
                        "Select answer:",
                        labeled,
                        index=default_idx,
                        key=f"radio_{idx}"
                    )
                    st.session_state.user_answers[idx] = choice
                    st.markdown("---")

                submitted = st.form_submit_button("✅ Submit Quiz & See Results", type="primary")

                if submitted:
                    correct_count = 0
                    st.session_state.answers = {}

                    for idx, q in enumerate(st.session_state.quiz_data):
                        user_choice = st.session_state.user_answers[idx]
                        user_letter = user_choice.split(".")[0].upper()
                        correct_raw = q["answer"].strip()

                        # Extract correct letter
                        correct_letter = correct_raw.split(".")[0].strip().upper()
                        if correct_letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                            correct_letter = None

                        # Determine correctness
                        is_correct = False
                        if correct_letter:  # Agent gave letter only (A/B/C/D)
                            is_correct = user_letter == correct_letter
                        else:  # Agent gave full text or "A. Text"
                            expected_text = correct_raw
                            if "." in correct_raw:
                                expected_text = ".".join(correct_raw.split(".")[1:]).strip()
                            is_correct = normalize(user_choice) == normalize(f"{user_letter}. {expected_text}")

                        st.session_state.answers[idx] = {
                            "user_answer": user_choice,
                            "correct_answer": correct_raw,
                            "is_correct": is_correct
                        }
                        if is_correct:
                            correct_count += 1

                    st.session_state.quiz_finished = True
                    st.rerun()

        # ==================== RESULTS ====================
        if st.session_state.quiz_finished:
            score = sum(1 for v in st.session_state.answers.values() if v["is_correct"])

            st.markdown(f"""
            <div class="score-card">
                <h2>🏆 Quiz Completed!</h2>
                <h1 style="color:#4a90e2; font-size:60px; margin:10px;">{score} / {total}</h1>
                <h3>
                    { "🌟 Perfect Score! Outstanding!" if score == total else 
                      "🎯 Well Done! Keep Practicing!" if score >= total*0.7 else 
                      "👍 Good Effort! Review & Try Again!" }
                </h3>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### 📌 Detailed Answers")
            for idx, q in enumerate(st.session_state.quiz_data):
                ans = st.session_state.answers[idx]
                with st.expander(f"Question {idx+1}: {q['question'][:100]}{'...' if len(q['question'])>100 else ''}"):
                    st.write(f"**Your Answer:** {ans['user_answer']}")
                    if ans["is_correct"]:
                        st.success("✔ Correct!")
                    else:
                        st.error(f"✖ Incorrect → Correct: **{ans['correct_answer']}**")

            if st.button("🔄 Start New Quiz", type="primary"):
                keys_to_clear = ["quiz_generated", "quiz_data", "summary_text",
                               "answers", "quiz_finished", "user_answers"]
                for k in keys_to_clear:
                    if k in st.session_state:
                        del st.session_state[k]
                st.rerun()

else:
    st.info("📤 Upload a PDF file above to start your smart study session!")
