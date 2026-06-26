import os


class ReportAgent:

    def generate_report(
        self,
        query,
        documents,
        plan,
        sections
    ):

        report = "# Research Report\n\n"

        # -----------------------------------------
        # Research Query
        # -----------------------------------------

        report += "## Research Query\n\n"
        report += f"{query}\n\n"

        # -----------------------------------------
        # Research Plan
        # -----------------------------------------

        report += "## Research Plan\n\n"

        report += (
            f"Original Query: {plan['original_query']}\n\n"
        )

        report += (
            f"Total Sources Found: {plan['sources_found']}\n\n"
        )

        report += "### Research Sub-Questions\n\n"

        for i, question in enumerate(
            plan["sub_questions"],
            start=1
        ):
            report += f"{i}. {question}\n"

        report += "\n"

        # -----------------------------------------
        # Executive Summary
        # -----------------------------------------

        report += "## Executive Summary\n\n"

        report += (
            f"This report investigates **{query}**. "
            f"The topic was divided into "
            f"{len(plan['sub_questions'])} research "
            f"sub-questions. Information was collected "
            f"from multiple sources and processed using "
            f"retrieval, ranking and verification agents.\n\n"
        )

        # -----------------------------------------
        # Detailed Research
        # -----------------------------------------

        report += "## Detailed Research\n\n"

        for i, section in enumerate(
            sections,
            start=1
        ):

            report += f"### Question {i}\n\n"

            report += (
                f"**{section['question']}**\n\n"
            )

            report += "#### Answer\n\n"

            answer = section["answer"].strip()

            if answer == "":
                answer = "No sufficient evidence found."

            report += answer + "\n\n"

            report += "#### Sources\n\n"

            if len(section["documents"]) == 0:

                report += "No sources found.\n\n"

            else:

                for doc in section["documents"]:

                    report += (
                        f"- {doc['source']}\n"
                    )

                report += "\n"

            report += "#### Top Evidence\n\n"

            count = 1

            for doc in section["documents"]:

                for item in doc["evidence"][:3]:

                    report += (
                        f"{count}. {item['evidence']}\n\n"
                    )

                    count += 1

        # -----------------------------------------
        # Combined Analysis
        # -----------------------------------------

        report += "## Combined Analysis\n\n"

        combined = ""

        for section in sections:

            combined += section["answer"] + "\n"

        report += combined[:3500]

        report += "\n\n"

        # -----------------------------------------
        # Conclusion
        # -----------------------------------------

        report += "## Conclusion\n\n"

        report += (
            f"The research indicates that **{query}** "
            f"can be understood through multiple perspectives "
            f"including definition, history, concepts, "
            f"applications and future developments. "
            f"The collected evidence provides a comprehensive "
            f"overview of the topic.\n"
        )

        os.makedirs(
            "reports",
            exist_ok=True
        )

        report_path = "reports/final_report.md"

        with open(
            report_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(report)

        return report_path