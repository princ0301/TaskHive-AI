from crewai import Crew, Process

from agents import (
    create_researcher_agent,
    create_writer_agent,
    create_critic_agent,
    create_formatter_agent,
)
from crew.tasks import (
    create_research_task,
    create_writing_task,
    create_critic_task,
    create_formatting_task,
)


def run_research_crew(topic: str) -> dict:
    """
    Run the full multi-agent research pipeline.

    Args:
        topic: The topic to research and write a report on

    Returns:
        dict with status and final report content
    """
    print(f"\nStarting Multi-Agent Research Pipeline for: {topic}\n")
    print("=" * 60)

    print("Initializing agents...")
    researcher = create_researcher_agent()
    writer = create_writer_agent()
    critic = create_critic_agent()
    formatter = create_formatter_agent()

    print("Creating tasks...")
    research_task = create_research_task(researcher, topic)
    writing_task = create_writing_task(writer, topic)
    critic_task = create_critic_task(critic, topic)
    formatting_task = create_formatting_task(formatter, topic)

    crew = Crew(
        agents=[researcher, writer, critic, formatter],
        tasks=[research_task, writing_task, critic_task, formatting_task],
        process=Process.sequential,
        verbose=True,
    )

    print("\nRunning crew pipeline...\n")
    result = crew.kickoff()

    return {
        "status": "success",
        "topic": topic,
        "report": str(result),
    }
