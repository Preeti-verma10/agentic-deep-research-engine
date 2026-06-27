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

Answer the question ONLY using the evidence below.

Question:
{question}

Evidence:
{evidence_text}

Instructions:

- Give ONE direct answer.
- Merge repeated information.
- Ignore duplicate evidence.
- Do not copy sentences exactly.
- Explain naturally like ChatGPT.
- Use simple English.
- Keep the answer between 80 and 120 words.
- Never mention "Evidence says..." or "According to the evidence..."
- If information is incomplete, mention that briefly.
- Do not invent facts.

Answer:
"""

        answer = self.client.generate(prompt)

        if (
            not answer
            or answer.startswith("ERROR")
        ):

            if isinstance(evidence_list[0], dict):

                return "\n".join(
                    item["evidence"]
                    for item in evidence_list[:3]
                )

            return "\n".join(
                evidence_list[:3]
            )

        return answer.strip()

    # --------------------------------------------------
    # Final Answer for Original User Query
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
                    f"{section['answer']}\n\n"
                )

            else:

                combined += (
                    str(section) + "\n\n"
                )

        prompt = f"""
You are ChatGPT.

The user asked:

{user_query}

Below are research findings collected from reliable sources.

Research Findings:

{combined}

Your task is to answer ONLY the user's original question.

Requirements:

- DO NOT mention Question 1, Question 2 or research findings.
- DO NOT repeat information.
- Give only ONE final answer.
- Write naturally like ChatGPT.
- Use Markdown formatting.

Structure:

## Short Introduction

2-3 sentences.

## Key Points

- Bullet Point
- Bullet Point
- Bullet Point
- Bullet Point

## Conclusion

1-2 sentences.

Keep the total answer between 150 and 220 words.

Do not invent facts outside the research findings.

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
You are ChatGPT.

Conversation:

{history}

User:

{followup_question}

Instructions:

- Answer using the previous conversation.
- Resolve references like "it", "they", or "this".
- Be conversational.
- Keep the answer below 120 words.
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