from google import genai
import time


class GeminiClient:

    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str):

        for attempt in range(3):

            try:

                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                if hasattr(response, "text"):
                    return response.text

                return str(response)

            except Exception as e:

                print(f"Gemini Error (Attempt {attempt + 1}): {e}")

                if attempt < 2:
                    time.sleep(5)

        return "ERROR: Gemini API failed after 3 attempts."