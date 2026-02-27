import os
import sys
from crew.research_crew import run_research_crew


def save_report(topic: str, report: str):
    """Save the final report to a markdown file."""
    os.makedirs("outputs", exist_ok=True)
    filename = topic.lower().replace(" ", "_")[:50] + "_report.md"
    filepath = os.path.join("outputs", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n✅ Report saved to: {filepath}")
    return filepath


def main():
    # Get topic from command line or use default
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("Enter a topic to research: ").strip()
        if not topic:
            topic = "Artificial Intelligence trends in 2025"

    print(f"\n📌 Topic: {topic}")

    # Run the crew
    result = run_research_crew(topic)

    if result["status"] == "success":
        print("\n" + "=" * 60)
        print("✅ REPORT GENERATION COMPLETE!")
        print("=" * 60)
        
        # Save report
        filepath = save_report(topic, result["report"])
        
        # Print preview
        print("\n📄 REPORT PREVIEW (first 500 chars):")
        print("-" * 40)
        print(result["report"][:500] + "...")
        print("-" * 40)
        print(f"\n📁 Full report saved at: {filepath}")
    else:
        print("❌ Something went wrong!")


if __name__ == "__main__":
    main()