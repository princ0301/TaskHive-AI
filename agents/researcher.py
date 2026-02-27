from crewai import Agent
from tools.search_tool import SearchTool
from agents.llm_factory import build_llm


def create_researcher_agent() -> Agent:
    llm = build_llm(temperature=0.3)
    search_tool = SearchTool()

    return Agent(
        role="Senior Research Analyst",
        goal="Find comprehensive, accurate, and up-to-date information on the given topic.",
        backstory="""You are an expert research analyst with years of experience 
        in gathering and synthesizing information from various sources. 
        You are thorough, detail-oriented, and always verify facts before reporting them.
        You know how to find the most relevant and credible sources.""",
        tools=[search_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=5
    )