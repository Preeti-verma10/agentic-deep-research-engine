# import os
# import time
# from google import genai


# class GeminiClient:

#     def __init__(
#         self,
#         api_key,
#         model="gemini-2.5-flash",
#         max_retries=3,
#         retry_delay=5
#     ):

#         if not api_key:
#             raise ValueError(
#                 "GEMINI_API_KEY not found."
#             )

#         self.client = genai.Client(
#             api_key=api_key
#         )

#         self.model = model
#         self.max_retries = max_retries
#         self.retry_delay = retry_delay

#     def generate(self, prompt):

#         for attempt in range(self.max_retries):

#             try:

#                 response = self.client.models.generate_content(
#                     model=self.model,
#                     contents=prompt
#                 )

#                 return response.text.strip()

#             except Exception as e:

#                 print(f"Gemini Error: {e}")

#                 if attempt < self.max_retries - 1:
#                     time.sleep(self.retry_delay)

#         return None



from google import genai
import time


class GeminiClient:

    def __init__(
        self,
        api_key,
        model="gemini-2.5-flash",
        max_retries=3,
        retry_delay=3,
    ):

        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def generate(self, prompt):

        for attempt in range(self.max_retries):

            try:

                response = self.client.models.generate_content(

                    model=self.model,

                    contents=prompt,

                    config={

                        "temperature": 0.3,

                        "top_p": 0.9,

                        "top_k": 40,

                        "candidate_count": 1,

                        "max_output_tokens": 1200,

                    }

                )

                if (
                    hasattr(response, "text")
                    and response.text
                ):

                    return response.text.strip()

                return None

            except Exception as e:

                print(
                    f"Gemini Error ({attempt + 1}/{self.max_retries}) : {e}"
                )

                if attempt < self.max_retries - 1:

                    time.sleep(self.retry_delay)

        return None