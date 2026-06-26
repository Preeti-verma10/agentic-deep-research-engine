from utils.web_search import search_sources
from utils.document_parser import fetch_document
from utils.document_parser import parse_document

from utils.retriever import (
    chunk_text,
    retrieve_relevant_chunks,
    extract_evidence
)

from agents.ranking_agent import RankingAgent
from agents.verifier_agent import VerifierAgent
from agents.planner_agent import PlannerAgent

import os
from dotenv import load_dotenv

load_dotenv()


class ResearchAgent:

    def research(self, query):

        print("\nGenerating Research Plan...\n")

        api_key = os.getenv("GEMINI_API_KEY")

        planner = PlannerAgent(api_key)

        sub_questions = planner.create_plan(query)

        print("\nResearch Plan:\n")

        for i, q in enumerate(sub_questions, start=1):
            print(f"{i}. {q}")

        ranking_agent = RankingAgent()
        verifier_agent = VerifierAgent()

        total_documents = []
        report_sections = []

        total_sources = 0

        for index, question in enumerate(
            sub_questions,
            start=1
        ):

            print("\n" + "=" * 60)
            print(f"Researching Question {index}")
            print(question)
            print("=" * 60)

            sources = search_sources(question)

            total_sources += len(sources)

            documents = []

            answer = ""

            for url in sources:

                try:

                    print(f"Reading: {url}")

                    html = fetch_document(url)

                    if not html:
                        continue

                    text = parse_document(html)

                    if not text:
                        continue

                    chunks = chunk_text(text)

                    relevant_chunks = retrieve_relevant_chunks(
                        question,
                        chunks
                    )

                    evidence = extract_evidence(
                        relevant_chunks
                    )

                    if not evidence:
                        continue

                    ranked = ranking_agent.score_evidence(
                        evidence,
                        question
                    )

                    verified = verifier_agent.verify(
                        ranked
                    )

                    doc = {
                        "source": url,
                        "content": text[:3000],
                        "chunks": relevant_chunks,
                        "evidence": verified
                    }

                    documents.append(doc)
                    total_documents.append(doc)

                    for item in verified[:3]:
                        answer += item["evidence"] + "\n\n"

                except Exception as e:

                    print(f"Failed: {url}")
                    print(e)

            if answer.strip() == "":
                answer = "No sufficient evidence found."

            report_sections.append(
                {
                    "question": question,
                    "answer": answer,
                    "documents": documents
                }
            )

        print("\nResearch Completed.")

        plan = {

            "original_query": query,

            "sources_found": total_sources,

            "sub_questions": sub_questions

        }

        return {

            "documents": total_documents,

            "plan": plan,

            "sections": report_sections

        }