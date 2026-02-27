from crewai import LLM

from config.settings import settings


def build_groq_llm(temperature: float) -> LLM:
    model_name = settings.GROQ_MODEL
    if not model_name.startswith("groq/"):
        model_name = f"groq/{model_name}"

    return LLM(
        model=model_name,
        api_key=settings.GROQ_API_KEY,
        temperature=temperature,
        max_retries=3,
        timeout=120,
    )
