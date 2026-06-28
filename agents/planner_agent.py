# import sys
# import os

# sys.path.append(
#     os.path.dirname(
#         os.path.dirname(
#             os.path.abspath(__file__)
#         )
#     )
# )

# from utils.gemini_client import GeminiClient


# class PlannerAgent:

#     def __init__(self, api_key):
#         self.client = GeminiClient(api_key)

#     def create_plan(self, query):

#         prompt = f"""
# You are an expert Research Planner.

# Your task is to understand the user's intent and generate exactly FIVE research sub-questions that directly answer the user's query.

# User Query:
# {query}

# Instructions:

# - First understand what the user is actually asking.
# - Do NOT always follow the same template.
# - Generate questions that help answer the user's query completely.
# - If the query is about the future, focus on future trends and opportunities.
# - If the query is about comparison, generate comparison questions.
# - If the query is about advantages or disadvantages, focus on those aspects.
# - If the query is a general topic, cover definition, history, concepts, applications and future.
# - Return ONLY numbered questions.
# - Do not include explanations or headings.

# Examples:

# User Query:
# What is Artificial Intelligence?

# 1. What is Artificial Intelligence?
# 2. What is the history of Artificial Intelligence?
# 3. How does Artificial Intelligence work?
# 4. What are the applications of Artificial Intelligence?
# 5. What are the future developments of Artificial Intelligence?

# User Query:
# Is there a future scope in Data Analyst?

# 1. What is the role of a Data Analyst?
# 2. What is the current demand for Data Analysts?
# 3. Which industries are expected to hire more Data Analysts in the future?
# 4. What skills will Data Analysts need in the coming years?
# 5. What is the future career scope and growth of Data Analysts?

# User Query:
# Compare Python and R.

# 1. What are Python and R?
# 2. What are the strengths of Python?
# 3. What are the strengths of R?
# 4. How do Python and R compare for data analysis?
# 5. Which language is better for different use cases?
# """

#         result = self.client.generate(prompt)

#         if (
#             not result
#             or result.startswith("ERROR")
#         ):

#             print("Planner failed. Using fallback plan.")

#             return [
#                 f"What is {query}?",
#                 f"What is the history of {query}?",
#                 f"How does {query} work?",
#                 f"What are the applications of {query}?",
#                 f"What are the advantages, limitations and future of {query}?"
#             ]

#         questions = []

#         for line in result.split("\n"):

#             line = line.strip()

#             if not line:
#                 continue

#             if "." in line:

#                 try:
#                     line = line.split(".", 1)[1].strip()
#                 except Exception:
#                     pass

#             if line:
#                 questions.append(line)

#         if len(questions) < 5:

#             questions = [
#                 f"What is {query}?",
#                 f"What is the history of {query}?",
#                 f"How does {query} work?",
#                 f"What are the applications of {query}?",
#                 f"What are the advantages, limitations and future of {query}?"
#             ]

#         return questions[:5]




import os
from utils.gemini_client import GeminiClient


class PlannerAgent:

    def __init__(self, api_key):

        self.client = GeminiClient(api_key)

    def create_plan(self, query):

        prompt = f"""
You are an expert Research Planner.

The user asked:

{query}

Create ONLY 5 research questions.

Rules:

- Cover different aspects.
- No overlapping questions.
- Make questions specific.
- Keep them short.
- Do NOT repeat the user's words unnecessarily.

Use this structure:

1. Definition / Overview
2. Working / Process
3. Features or Types
4. Applications / Use Cases
5. Advantages, Limitations and Future

Return ONLY the questions.
"""

        answer = self.client.generate(prompt)

        if not answer:

            return [

                f"What is {query}?",

                f"How does {query} work?",

                f"What are the main features of {query}?",

                f"What are the applications of {query}?",

                f"What are the advantages, limitations and future of {query}?"

            ]

        questions = []

        for line in answer.split("\n"):

            line = line.strip()

            if not line:
                continue

            if line[0].isdigit():

                line = line.split(".", 1)[1].strip()

            questions.append(line)

        return questions[:5]
