# from google import genai
# import time


# class GeminiClient:

#     def __init__(self, api_key: str):
#         self.client = genai.Client(api_key=api_key)

#     def generate(self, prompt: str):

#         for attempt in range(3):

#             try:

#                 response = self.client.models.generate_content(
#                     model="gemini-2.5-flash",
#                     contents=prompt
#                 )

#                 if hasattr(response, "text"):
#                     return response.text

#                 return str(response)

#             except Exception as e:

#                 print(f"Gemini Error (Attempt {attempt + 1}): {e}")

#                 if attempt < 2:
#                     time.sleep(5)

#         return "ERROR: Gemini API failed after 3 attempts."


from google import genai
import time


class GeminiClient:
    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.5-flash",
        max_retries: int = 3,
        retry_delay: int = 5,
    ):
        """
        Initialize Gemini client.

        Args:
            api_key: Gemini API key.
            model: Gemini model name.
            max_retries: Number of retry attempts.
            retry_delay: Delay (seconds) between retries.
        """
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def generate(self, prompt: str) -> str:
        """
        Generate a response from Gemini.

        Args:
            prompt: Input prompt.

        Returns:
            Generated text or an error message.
        """

        for attempt in range(self.max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )

                if hasattr(response, "text") and response.text:
                    return response.text.strip()

                return str(response)

            except Exception as e:
                print(
                    f"Gemini Error (Attempt {attempt + 1}/{self.max_retries}): {e}"
                )

                if attempt < self.max_retries - 1:
                    print(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)

        return "ERROR: Gemini API failed after all retry attempts."