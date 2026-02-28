from crewai import LLM
from config.settings import settings


def _normalize_ollama_base_url(url: str) -> str:
    
    base = (url or "").rstrip("/")
    if base.endswith("/api"):
        return base[: -len("/api")]
    return base


def build_llm(temperature: float = 0.3) -> LLM:
    """
    Build LLM based on the configured provider.
    
    Args:
        temperature: Temperature setting for the LLM
        
    Returns:
        Configured LLM instance
    """
    provider = settings.LLM_PROVIDER.lower()
    
    if provider == "ollama":
        return build_ollama_llm(temperature)
    elif provider == "groq":
        return build_groq_llm(temperature)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")


def build_ollama_llm(temperature: float) -> LLM:
    """Build Ollama LLM configuration."""
    llm_kwargs = {
        "model": f"ollama/{settings.OLLAMA_MODEL}",
        "base_url": _normalize_ollama_base_url(settings.OLLAMA_BASE_URL),
        "temperature": temperature,
    }

    # Some hosted Ollama-compatible endpoints require auth.
    if settings.OLLAMA_API_KEY:
        llm_kwargs["api_key"] = settings.OLLAMA_API_KEY

    return LLM(
        **llm_kwargs,
    )


def build_groq_llm(temperature: float) -> LLM:
    """Build Groq LLM configuration."""
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
