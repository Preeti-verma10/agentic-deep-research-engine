import os


class ReportAgent:

    def generate_report(
        self,
        query,
        documents,
        plan
    ):

        report = "# Research Report\n\n"

        report += f"## Research Query\n\n{query}\n\n"

        # -----------------------
        # Research Plan
        # -----------------------

        report += "## Research Plan\n\n"

        report += (
            f"Original Query: "
            f"{plan['original_query']}\n\n"
        )

        report += (
            f"Clean Query: "
            f"{plan['clean_query']}\n\n"
        )

        report += (
            f"Sources Found: "
            f"{plan['sources_found']}\n\n"
        )

        report += "Research Steps:\n\n"

        for step in plan["steps"]:
            report += f"- {step}\n"

        report += "\n"

        # -----------------------
        # Executive Summary
        # -----------------------

        report += "## Executive Summary\n\n"

        report += (
            f"This report investigates "
            f"'{query}'. "
            f"{len(documents)} relevant documents "
            f"were collected and analyzed.\n\n"
        )

        # -----------------------
        # Findings
        # -----------------------

        report += "## Key Findings\n\n"

        all_evidence = []

        for i, doc in enumerate(
            documents,
            start=1
        ):

            report += (
                f"### Source {i}\n\n"
            )

            report += (
                f"URL: {doc['source']}\n\n"
            )

            for item in doc["evidence"]:

                evidence_text = (
                    item["evidence"]
                )

                all_evidence.append(
                    evidence_text
                )

                report += (
                    f"- {evidence_text}\n"
                )

            report += "\n"

        # -----------------------
        # Combined Analysis
        # -----------------------

        report += (
            "## Combined Analysis\n\n"
        )

        report += (
            f"The evidence gathered for "
            f"'{query}' indicates:\n\n"
        )

        for evidence in all_evidence[:10]:

            report += (
                f"- {evidence[:300]}\n"
            )

        report += "\n"

        # -----------------------
        # Conclusion
        # -----------------------

        report += "## Conclusion\n\n"

        report += (
            f"Based on the collected "
            f"information, the topic "
            f"'{query}' was successfully "
            f"researched using multiple "
            f"sources.\n"
        )

        os.makedirs(
            "reports",
            exist_ok=True
        )

        report_path = (
            "reports/final_report.md"
        )

        with open(
            report_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(report)

        return report_path