"""
resume_tailor.py

Uses LangChain's new `create_agent` API to send a parsed resume
and a filtered job posting to GPT-5-mini for specific tailoring suggestions.
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver


# ---------- ENVIRONMENT ----------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ---------- SYSTEM PROMPT ----------
SYSTEM_PROMPT = """
You are an expert career coach and resume advisor.

Do NOT rewrite the resume entirely. Instead:
1. Analyze each line of the candidate's resume.
2. Identify lines that could be improved, clarified, or tailored.
3. Suggest specific edits to wording, detail, or emphasis.
4. Tie suggestions to the job posting and the company's values, ideals, or focus areas.
5. Provide 3–4 line-specific recommendations across the resume.
6. Provide 2–3 big-picture edits about structure, tone, or sections to emphasize.

Your tone should be natural, conversational, and confident — not overly formal.
When giving praise, weave it in casually at the end (for example:
"Overall, this already reads like a strong candidate for Apple — just a few tweaks to make it pop even more.").

Output format:
- Start with **line-specific suggestions** (with line numbers if possible).
- Then provide **big-picture edits** if any.
- End with a friendly, natural compliment — no need for a header.
"""


# ---------- CONTEXT ----------
@dataclass
class Context:
    """Runtime context (optional)."""
    user_id: str


# ---------- TOOL ----------
@tool
def get_resume_context(runtime: ToolRuntime[Context], resume: str, job: str) -> str:
    """Combine the resume and job posting into a single contextual block."""
    return f"Job Description:\n{job}\n\nCandidate Resume:\n{resume}"


# ---------- MODEL CONFIG ----------
model = init_chat_model(
    "openai:gpt-5-mini",
    temperature=0.4,
    api_key=OPENAI_API_KEY
)


# ---------- RESPONSE FORMAT ----------
@dataclass
class ResponseFormat:
    """Structured response for tailoring suggestions."""
    line_suggestions: str 
    big_picture_edits: str 
    compliment: str


# ---------- MEMORY ----------
checkpointer = InMemorySaver()


# ---------- AGENT CREATION ----------
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_resume_context],
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer
)


# ---------- MAIN FUNCTION ----------
def tailor_resume(resume_text: str, job_text: str, user_id: str = "1") -> str:
    """
    Sends resume + job description to GPT-5-mini via LangChain agent.

    Returns:
        str: Formatted tailoring suggestions.
    """
    try:
        context = Context(user_id=user_id)
        config = {"configurable": {"thread_id": user_id}}

        print("Sending info to agent...")

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            "Please tailor this resume for the given job posting.\n\n"
                            f"Job Description:\n{job_text}\n\nResume:\n{resume_text}"
                        )
                    }
                ]
            },
            config=config,
            context=context
        )

        structured = response.get("structured_response")
        if not structured:
            return "⚠️ No suggestions returned. Please verify API connection."

        # Build sections conditionally
        sections = []
        if structured.line_suggestions and structured.line_suggestions.strip().lower() != "none":
            sections.append(f"=== Line-Specific Suggestions ===\n{structured.line_suggestions.strip()}")

        if structured.big_picture_edits and structured.big_picture_edits.strip().lower() != "none":
            sections.append(f"=== Big-Picture Edits ===\n{structured.big_picture_edits.strip()}")

        # Compliment should always appear, no header
        compliment = (
            f"\n\n{structured.compliment.strip()}"
            if structured.compliment and structured.compliment.strip().lower() != "none"
            else "\n\nOverall, this resume already looks strong — just refine it with these details to make it stand out even more."
        )

        return "\n\n".join(sections) + compliment

    except Exception as e:
        print("Error generating tailoring suggestions:", e)
        return ""