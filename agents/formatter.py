from crewai import Agent
from agents.llm_factory import build_llm


def create_formatter_agent() -> Agent:
    llm = build_llm(temperature=0.2)

    return Agent(
        role="Report Formatter & Finalizer",
        goal="Format the reviewed report into a clean, professional, well-structured markdown document.",
        backstory="""You are an expert in document formatting and presentation.
        You take reviewed content and transform it into beautifully structured 
        markdown reports with proper headings, sections, bullet points, 
        summaries, and key takeaways. Your reports are always professional,
        easy to read, and visually well-organized.""",
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )