import os
from dotenv import load_dotenv

from utils.gemini_client import GeminiClient

load_dotenv()


class AnswerAgent:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        self.client = GeminiClient(api_key)

    # --------------------------------------------------
    # Generate answer for one research question
    # --------------------------------------------------

    def generate_answer(
        self,
        question,
        evidence_list
    ):

        if not evidence_list:

            return (
                "No sufficient evidence was found "
                "to answer this research question."
            )

        evidence_text = ""

        for i, item in enumerate(
            evidence_list,
            start=1
        ):

            if isinstance(item, dict):
                evidence = item.get(
                    "evidence",
                    ""
                )
            else:
                evidence = str(item)

            evidence_text += (
                f"{i}. {evidence}\n"
            )

        prompt = f"""
You are an expert research assistant.

Use ONLY the evidence provided.

Research Question:
{question}

Evidence:
{evidence_text}

Instructions:

- Write naturally.
- Explain in simple English.
- Merge repeated information.
- Do not copy every sentence.
- Do not invent facts.
- Mention if evidence is incomplete.
- Keep the answer between 100 and 150 words.
- Answer like ChatGPT.

Final Answer:
"""

        answer = self.client.generate(prompt)

        if (
            not answer
            or answer.startswith("ERROR")
        ):

            if isinstance(evidence_list[0], dict):

                return "\n".join(
                    item["evidence"]
                    for item in evidence_list[:5]
                )

            return "\n".join(
                evidence_list[:5]
            )

        return answer.strip()

    # --------------------------------------------------
    # Final answer for ORIGINAL USER QUESTION
    # --------------------------------------------------

    def generate_final_answer(
        self,
        user_query,
        section_answers
    ):

        combined = ""

        for section in section_answers:

            if isinstance(section, dict):

                combined += (
                    f"Question: {section['question']}\n"
                )

                combined += (
                    f"Answer:\n"
                    f"{section['answer']}\n\n"
                )

            else:

                combined += (
                    str(section) + "\n\n"
                )

        prompt = f"""
You are an expert AI Research Assistant.

The user asked:

{user_query}

Below are answers generated from research.

Research Findings:

{combined}

Instructions:

- Answer ONLY the user's original question.
- Combine all findings into one answer.
- Do NOT mention Question 1, Question 2, etc.
- Remove repetition.
- Write naturally like ChatGPT.
- Use short paragraphs.
- Keep the answer between 120 and 180 words.
- Be concise and informative.
- Stay grounded in the research findings.
- Do not invent facts.

Final Answer:
"""

        final_answer = self.client.generate(prompt)

        if (
            not final_answer
            or final_answer.startswith("ERROR")
        ):

            return combined.strip()

        return final_answer.strip()

    # --------------------------------------------------
    # Follow-up Chat
    # --------------------------------------------------

    def answer_followup(
        self,
        chat_history,
        followup_question
    ):

        history = ""

        for chat in chat_history:

            history += (
                f"User: {chat['question']}\n"
            )

            history += (
                f"Assistant: {chat['answer']}\n\n"
            )

        prompt = f"""
You are an AI Research Assistant.

Conversation History:

{history}

User Follow-up Question:

{followup_question}

Instructions:

- Use the conversation as context.
- Resolve references like "it", "they", "this".
- Answer naturally.
- Keep the answer under 150 words.
- Do not invent unsupported facts.

Answer:
"""

        answer = self.client.generate(prompt)

        if (
            not answer
            or answer.startswith("ERROR")
        ):

            return (
                "Unable to generate a follow-up answer."
            )

        return answer.strip()