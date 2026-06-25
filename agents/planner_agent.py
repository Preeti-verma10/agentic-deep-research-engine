import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from utils.gemini_client import GeminiClient


class PlannerAgent:

    def __init__(self, api_key):
        self.client = GeminiClient(api_key)

    def create_plan(self, query):

        prompt = f"""
You are a Planner Agent.

Break the user query into 5 research sub-questions.

Query:
{query}

Return only numbered questions.

Example:

1. What is AI?
2. How does AI work?
3. What are AI applications?
"""

        result = self.client.generate(prompt)

        if (
            not result
            or result.startswith("ERROR")
        ):
            print(
                "Planner failed. Using fallback plan."
            )

            return f"""
1. Definition of {query}
2. History of {query}
3. Key concepts of {query}
4. Applications of {query}
5. Advantages and limitations of {query}
"""

        return result