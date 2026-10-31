import os
import time

from google import genai
from google.genai import types


MODELS = [
    "gemini-flash-lite-latest",
    "gemini-3.1-flash-lite",
    "gemini-3.8-flash"
]


def get_ai_analysis(prompt):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not configured."
        )

    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=90_000
        )
    )

    last_error = None

    for model_name in MODELS:
        try:
            print(f"Trying model: {model_name}")

            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=800,
                    thinking_config=types.ThinkingConfig(
                        thinking_level="MINIMAL"
                    )
                )
            )

            ai_text = response.text

            if not ai_text:
                raise ValueError(
                    f"{model_name} returned an empty response."
                )

            print(f"Response received from: {model_name}")
            print(f"AI text length: {len(ai_text)} characters")

            return ai_text

        except Exception as error:
            last_error = error

            print(
                f"Model {model_name} failed: "
                f"{type(error).__name__}: {error}"
            )

            time.sleep(2)

    raise RuntimeError(
        f"All Gemini models failed. Last error: {last_error}"
    )