import os
from dotenv import load_dotenv
from utils.gemini_client import GeminiClient

load_dotenv()


class AnswerAgent:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        self.client = GeminiClient(api_key)

    # --------------------------------------------------
    # Generate answer for ONE research question
    # --------------------------------------------------

    def generate_answer(
        self,
        question,
        evidence_list
    ):

        if not evidence_list:

            return (
                "No reliable information was found for this research question."
            )

        evidence = ""

        for i, item in enumerate(
            evidence_list,
            start=1
        ):

            if isinstance(item, dict):

                evidence += (
                    f"{i}. {item.get('evidence','')}\n"
                )

            else:

                evidence += (
                    f"{i}. {item}\n"
                )

        prompt = f"""
You are an expert AI Research Assistant.

Answer ONLY the question below.

Question:

{question}

Reliable Evidence:

{evidence}

Instructions:

- Read ALL evidence carefully.
- Ignore duplicated facts.
- Merge similar information.
- Explain naturally like ChatGPT.
- Use ONLY the provided evidence.
- Do NOT copy sentences exactly.
- Do NOT mention "According to the evidence".
- If information is missing, say so briefly.
- Answer ONLY this question.
- Ignore information unrelated to this question.

Write between 200 and 400 words.

Use Markdown.

Good Answer Example:

Machine Learning (ML) is a branch of Artificial Intelligence that enables computers to learn patterns from data without being explicitly programmed. Instead of following fixed rules, ML models improve their performance by analyzing examples and making predictions. It is widely used in recommendation systems, fraud detection, image recognition, and language processing.

Answer:
"""

        answer = self.client.generate(prompt)

        if (
            answer is None
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
    # Generate Final Answer for User Query
    # --------------------------------------------------

    def generate_final_answer(
        self,
        user_query,
        section_answers
    ):

        findings = ""

        for section in section_answers:

            findings += f"""

Question:
{section['question']}

Answer:
{section['answer']}

"""

        prompt = f"""
You are ChatGPT.

The user originally asked:

{user_query}

Below are answers collected from multiple research tasks.

Research:

{findings}

Your job is to answer ONLY the user's original question.

Rules:

- Do NOT mention Question 1, Question 2, Topic 1 or research tasks.
- Merge all information naturally.
- Remove duplicate information.
- Remove unnecessary details.
- Write like ChatGPT.
- Use simple English.
- Do NOT copy the research answers.
- Rewrite everything naturally.
- Stay factual.
- Do NOT invent facts.
- If some information is unavailable, simply omit it.

Use this format exactly.

# Introduction

Write 2–3 sentences introducing the topic.

# Key Points

• Use 5–8 bullet points.

• Each bullet should be 1–3 sentences.

# Conclusion

Summarize everything in 2–3 sentences.

Keep the total answer around 250–500 words.

Return ONLY the final answer.
"""

        final_answer = self.client.generate(prompt)

        if (
            final_answer is None
            or final_answer.startswith("ERROR")
        ):

            return "\n\n".join(

                section["answer"]

                for section in section_answers

            )

        return final_answer.strip()
            # --------------------------------------------------
    # Follow-up Conversation
    # --------------------------------------------------

    def answer_followup(
        self,
        chat_history,
        followup_question
    ):

        history = ""

        for chat in chat_history:

            history += f"""
User:
{chat['question']}

Assistant:
{chat['answer']}

"""

        prompt = f"""
You are ChatGPT.

Below is the previous conversation.

Conversation:

{history}

The user now asks:

{followup_question}

Instructions:

- Use the previous conversation as context.
- Resolve references like "it", "they", "that", "this", etc.
- If the answer exists in the conversation, answer using it.
- If more explanation is helpful, expand naturally.
- If the answer is not fully available in the conversation, use your general knowledge.
- Be conversational and helpful.
- Keep the answer between 80 and 150 words.
- Use simple English.
- Do not mention "conversation history" or "context".

Answer:
"""

        answer = self.client.generate(prompt)

        if (
            answer is None
            or answer.startswith("ERROR")
        ):

            return (
                "Sorry, I couldn't generate a follow-up answer."
            )

        return answer.strip()