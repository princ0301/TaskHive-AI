from crewai import Agent
from agents.llm_factory import build_llm


def create_critic_agent() -> Agent:
    llm = build_llm(temperature=0.1)

    return Agent(
        role="Critical Fact Checker & Editor",
        goal="Review reports for accuracy, clarity, completeness, and logical consistency.",
        backstory="""You are a meticulous fact-checker and editor with an eye for detail.
        You review content critically, identify any unsupported claims, logical gaps,
        or areas that need improvement. You provide constructive feedback and 
        suggest specific improvements to make the report more accurate and credible.
        You are honest and thorough in your reviews.""",
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )