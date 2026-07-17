import json
import groq
from groq import Groq
from app.config import get_settings

settings = get_settings()
_client = Groq(api_key=settings.GROQ_API_KEY)

# Llama 3.3 70B on Groq — free tier, fast, strong at structured JSON output.
MODEL = "llama-3.3-70b-versatile"


class GroqServiceError(Exception):
    """Raised for any Groq API failure, with a user-friendly message attached."""
    def __init__(self, message: str, is_rate_limit: bool = False):
        self.message = message
        self.is_rate_limit = is_rate_limit
        super().__init__(message)


def chat_completion(system_prompt: str, user_prompt: str, json_mode: bool = False, temperature: float = 0.4) -> str:
    """Single call to Groq's chat completion endpoint. Returns raw text content."""
    kwargs = {}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    try:
        response = _client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=8000,
            timeout=60,
            **kwargs,
        )
    except groq.RateLimitError:
        raise GroqServiceError(
            "The AI service has hit its free-tier rate limit. Please wait a minute and try again.",
            is_rate_limit=True,
        )
    except groq.APITimeoutError:
        raise GroqServiceError("The AI took too long to respond. Please try again.")
    except groq.APIConnectionError:
        raise GroqServiceError("Couldn't reach the AI service. Check your connection and try again.")
    except groq.APIStatusError as e:
        raise GroqServiceError(f"The AI service returned an error ({e.status_code}). Please try again.")

    return response.choices[0].message.content


def chat_completion_json(system_prompt: str, user_prompt: str, temperature: float = 0.4) -> dict:
    """Calls Groq in JSON mode and parses the result. Raises ValueError on bad JSON."""
    raw = chat_completion(system_prompt, user_prompt, json_mode=True, temperature=temperature)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Groq did not return valid JSON: {e}\nRaw output:\n{raw[:2000]}")
