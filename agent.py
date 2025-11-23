# from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
# import os
# import asyncio
# from dotenv import load_dotenv

# # Import the tools from tools.py
# from tools import extract_text_from_pdf, read_user_profile, update_user_profile

# # Load environment
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise ValueError("GEMINI_API_KEY environment variable not set")

# # External Gemini Client
# external_client = AsyncOpenAI(
#     api_key=GEMINI_API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta", # Corrected base_url
#     timeout=60.0, # Added timeout
# )

# # Model Configuration
# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash", # Corrected model name
#     openai_client=external_client,
# )

# # Runner configuration
# config = RunConfig(
#     model=model,
#     model_provider=external_client,
#     tracing_disabled=True  # As per instructions
# )

# # --- Main function to run the agent ---
# async def main(file_path: str, quiz_type: str, num_questions: int):
#     """
#     Runs the StudyNotesAgent to process the PDF and returns the result.
#     """
#     print(f"Agent main function called with file_path: {file_path}, quiz_type: {quiz_type}, num_questions: {num_questions}")

#     # --- Dynamic Instructions based on Quiz Type and Number of Questions ---
#     base_instructions = (
#         "You are an expert AI assistant for students. Your goal is to help users study more effectively. "
#         "1. First, use the `extract_text_from_pdf` tool to read the content of the PDF file specified by the user. "
#         "2. After extracting the text, create a concise, easy-to-understand summary of the key points. "
#         f"3. Following the summary, generate a quiz with exactly {num_questions} questions based on the content. "
#     )

#     if quiz_type == "True/False":
#         quiz_instructions = (
#             "4. The quiz must be a 'True/False' quiz. **Crucially, format your final output *exactly* as follows:**\n"
#             "---SUMMARY---\n\n<Your summary here>\n\n"
#             "---QUIZ---\n\n"
#             "```json\n"
#             "[\n"
#             "  {\n"
#             '    "question": "Is the sky blue?",\n'
#             '    "options": ["True", "False"],\n'
#             '    "answer": "True"\n'
#             "  }\n"
#             "]\n"
#             "```"
#         )
#     else: # Default to Multiple Choice
#         quiz_instructions = (
#             "4. The quiz must be a 'Multiple Choice' quiz with 4 options per question. **Crucially, format your final output *exactly* as follows:**\n"
#             "---SUMMARY---\n\n<Your summary here>\n\n"
#             "---QUIZ---\n\n"
#             "```json\n"
#             "[\n"
#             "  {\n"
#             '    "question": "What is the capital of France?",\n'
#             '    "options": ["London", "Berlin", "Paris", "Madrid"],\n'
#             '    "answer": "Paris"\n'
#             "  }\n"
#             "]\n"
#             "```"
#         )

#     full_instructions = base_instructions + quiz_instructions
    
#     # --- Define Agent with Dynamic Instructions ---
#     study_agent = Agent(
#         name="StudyNotesAgent",
#         instructions=full_instructions,
#         model=model,
#         tools=[extract_text_from_pdf, read_user_profile, update_user_profile],
#     )
    
#     # The prompt given to the agent, including the path to the file
#     prompt = f"Please process the document located at the following path: {file_path}"
#     print(f"Agent prompt: {prompt}")

#     print("Calling Runner.run...")
#     # Run the agent
#     result = await Runner.run(study_agent, prompt, run_config=config)
#     print("Runner.run completed.")

#     # Return the final output to be displayed in the UI
#     if result and result.final_output:
#         print("Agent returned a final output.")
#         return result.final_output
    
#     print("Agent did not return a final output or result was None.")
#     return None

# if __name__ == "__main__":
#     # This part is for local testing of the agent, e.g., from the command line.
#     # You would need to provide a sample file path and quiz type.
#     # Example: asyncio.run(main("path/to/your/test.pdf", "Multiple Choice", 5))
#     # The primary execution is now through app.py
#     print("Agent module run directly. This should typically be called from app.py.")
#     pass


from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
import os
import asyncio
from dotenv import load_dotenv

# Import tools from the updated tools.py
from tools import pdf_text_extractor, fetch_user_profile, modify_user_profile


# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing! Add it to your .env file.")


# Gemini Client
client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta",
    timeout=60.0,
)

# Model setup
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

# Runner settings
config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)


# -------------------------------------------------------
#  Main AI Agent Logic
# -------------------------------------------------------
async def main(document_path: str, quiz_type: str, total_questions: int):
    """
    Handles PDF extraction, summary creation, and quiz generation.
    """

    print(f"[AGENT] Started with: file={document_path}, quiz={quiz_type}, questions={total_questions}")

    # Base instruction for agent
    instructions = (
        "You are an advanced academic assistant designed to help users understand study material. "
        "Your tasks are:\n"
        "1️⃣ Use the `pdf_text_extractor` tool to read the contents of the uploaded PDF.\n"
        "2️⃣ Produce a clean, easy-to-read summary.\n"
        f"3️⃣ After the summary, create *exactly {total_questions}* quiz questions based on the content.\n"
    )

    # Different quiz format instructions
    if quiz_type == "True/False":
        quiz_format = (
            "4️⃣ The quiz type must strictly be **True/False**.\n"
            "5️⃣ Format your response *exactly* like this:\n\n"
            "---SUMMARY---\n"
            "<Write your summary here>\n\n"
            "---QUIZ---\n"
            "```json\n"
            "[\n"
            "  {\n"
            '    \"question\": \"Example question?\",\n'
            '    \"options\": [\"True\", \"False\"],\n'
            '    \"answer\": \"True\"\n'
            "  }\n"
            "]\n"
            "```"
        )
    else:
        quiz_format = (
            "4️⃣ The quiz type must be **Multiple Choice (4 options)**.\n"
            "5️⃣ Format your output *exactly* like this:\n\n"
            "---SUMMARY---\n"
            "<Write your summary here>\n\n"
            "---QUIZ---\n"
            "```json\n"
            "[\n"
            "  {\n"
            '    \"question\": \"Sample question?\",\n'
            '    \"options\": [\"A\", \"B\", \"C\", \"D\"],\n'
            '    \"answer\": \"C\"\n'
            "  }\n"
            "]\n"
            "```"
        )

    agent_instructions = instructions + quiz_format

    # Create Agent
    study_agent = Agent(
        name="SmartStudyAgent",
        instructions=agent_instructions,
        model=model,
        tools=[pdf_text_extractor, fetch_user_profile, modify_user_profile],
    )

    # Prompt to pass to agent
    prompt = f"Process the file located at: {document_path}"
    print(f"[AGENT] Sending prompt: {prompt}")

    result = await Runner.run(study_agent, prompt, run_config=config)

    if result and result.final_output:
        print("[AGENT] Output successfully generated.")
        return result.final_output

    print("[AGENT] No output returned!")
    return None


# Local testing trigger
if __name__ == "__main__":
    print("⚠ This module should be executed through app.py, not directly.")
