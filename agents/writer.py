from crewai import Agent, LLM
from config.settings import settings


def create_writer_agent() -> Agent:
    llm = LLM(
        model=f"groq/{settings.GROQ_MODEL}",
        api_key=settings.GROQ_API_KEY,
        temperature=0.7
    )

    return Agent(
        role="Expert Content Writer",
        goal="Write clear, engaging, and well-structured reports based on research findings.",
        backstory="""You are a skilled content writer with expertise in transforming 
        complex research into clear, readable, and engaging reports. 
        You have a talent for structuring information logically, 
        using proper headings, and making technical content accessible to all audiences.
        You always write in a professional yet approachable tone.""",
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )