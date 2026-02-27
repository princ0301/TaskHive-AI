from crewai import Agent
from agents.llm_factory import build_llm


def create_writer_agent() -> Agent:
    llm = build_llm(temperature=0.7)

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