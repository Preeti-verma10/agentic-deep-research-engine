from agents.research_agent import ResearchAgent
from agents.report_agent import ReportAgent


def main():

    query = input("Enter Research Query: ")

    researcher = ResearchAgent()

    research_result = researcher.research(query)

    documents = research_result["documents"]
    plan = research_result["plan"]

    report_agent = ReportAgent()

    report_path = report_agent.generate_report(
        query,
        documents,
        plan
    )

    print(f"\nReport Saved: {report_path}\n")

    print("\n===== RESULTS =====\n")

    for i, doc in enumerate(documents, start=1):

        print(f"\nSource {i}:")
        print(doc["source"])

        print("\nContent Preview:\n")
        print(doc["content"][:500])

        print("\nEvidence:\n")

        for item in doc["evidence"]:

            print("\nEvidence:")
            print(item["evidence"][:200])

            print(
                f"Confidence: {item['confidence']}"
            )

            print(
                f"Verification: {item['verification_status']}"
            )

            print(
                f"V:{item['verifiability']} "
                f"G:{item['grounding']} "
                f"R:{item['relevance']} "
                f"H:{item['helpfulness']}"
            )

        print("-" * 50)


if __name__ == "__main__":
    main()