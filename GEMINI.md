Generate a complete Python project called "StudySense AI" with the following specifications:

1. The project should be modular with three files:
   - app.py : Streamlit application handling UI, PDF upload, quiz display, score calculation, and session state.
   - agent.py : AI agent responsible for extracting text from PDF, generating summaries, and generating quizzes (Multiple Choice and True/False).
   - tools.py : Utility functions for text normalization, PDF parsing, and helper functions for the agent.

2. Features for the Streamlit app (app.py):
   - Upload PDF study notes
   - Generate a clean, structured summary from the PDF
   - Generate a quiz automatically (MCQ or True/False)
   - Track user answers
   - Calculate and display score correctly
   - Handle options with letters (A, B, C, etc.) and text
   - Display a final result with emojis/icons
   - Ability to start a new quiz

3. Features for agent.py:
   - Extract text from PDF
   - Generate summary
   - Generate quiz in JSON format with questions, options, and correct answer
   - Return output in a format compatible with the Streamlit app:
       ---SUMMARY---
       <summary text>
       ---QUIZ---
       JSON array of questions

4. Features for tools.py:
   - Normalize text for comparison
   - Any additional helper functions needed by agent.py

5. Create a requirements.txt file with all necessary dependencies (Streamlit, PyPDF2, openai, asyncio, etc.)

6. Make the UI modern and friendly using Streamlit with custom CSS (cards, score display, buttons, summary box, emojis/icons)

7. Ensure quiz answers are evaluated correctly and score calculation is accurate

8. Project structure should be ready-to-run, modular, and maintainable

9. No code snippets in this prompt; Gemini should generate all code files based on these requirements.


