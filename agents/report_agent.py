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

        # --------------------------------------------------
        # User Question
        # --------------------------------------------------

        report += "## Question\n\n"
        report += f"{query}\n\n"

        # --------------------------------------------------
        # Final Answer
        # --------------------------------------------------

        report += "## Answer\n\n"

        combined_answers = []

        for section in sections:
            combined_answers.append(section["answer"])

        report += "\n\n".join(combined_answers)

        report += "\n"

        # --------------------------------------------------
        # Save Report
        # --------------------------------------------------

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