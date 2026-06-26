from agents.research_agent import ResearchAgent
from agents.report_agent import ReportAgent


def main():

    query = input("Enter Research Query: ")

    researcher = ResearchAgent()

    research_result = researcher.research(query)

    documents = research_result["documents"]

    plan = research_result["plan"]

    sections = research_result["sections"]

    report_agent = ReportAgent()

    report_path = report_agent.generate_report(
        query,
        documents,
        plan,
        sections
    )

    print(f"\nReport Saved: {report_path}")

    print("\n==============================")
    print("RESEARCH SUMMARY")
    print("==============================")

    print("\nResearch Query:")
    print(query)

    print("\nResearch Plan:\n")

    for i, question in enumerate(
        plan["sub_questions"],
        start=1
    ):
        print(f"{i}. {question}")

    print("\n==============================")

    for i, section in enumerate(
        sections,
        start=1
    ):

        print(f"\nQuestion {i}")
        print("-" * 60)

        print(section["question"])

        print("\nAnswer:\n")

        if section["answer"]:
            print(section["answer"][:700])
        else:
            print("No answer generated.")

        print("\nSources:")

        if len(section["documents"]) == 0:
            print("No sources.")

        else:

            for doc in section["documents"]:

                print(doc["source"])

    print("\n==============================")
    print("Evidence Details")
    print("==============================")

    for i, doc in enumerate(
        documents,
        start=1
    ):

        print(f"\nSource {i}")
        print(doc["source"])

        print("\nEvidence:\n")

        for item in doc["evidence"]:

            print(item["evidence"][:200])

            print(
                f"Confidence : {item['confidence']}"
            )

            print(
                f"Verification : {item['verification_status']}"
            )

            print(
                f"V:{item['verifiability']} "
                f"G:{item['grounding']} "
                f"R:{item['relevance']} "
                f"H:{item['helpfulness']}"
            )

            print()

        print("-" * 60)


if __name__ == "__main__":
    main()