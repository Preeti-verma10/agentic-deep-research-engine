from utils.web_search import search_sources
from utils.document_parser import fetch_document
from utils.document_parser import parse_document

from utils.retriever import (
    chunk_text,
    retrieve_relevant_chunks,
    extract_evidence
)

from agents.planner_agent import PlannerAgent
from agents.ranking_agent import RankingAgent
from agents.verifier_agent import VerifierAgent
from agents.answer_agent import AnswerAgent

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

        for i, question in enumerate(sub_questions, start=1):
            print(f"{i}. {question}")

        ranking_agent = RankingAgent()
        verifier_agent = VerifierAgent()
        answer_agent = AnswerAgent()

        total_documents = []
        report_sections = []

        total_sources = 0

        # ==========================================
        # Research Every Question
        # ==========================================

        for index, question in enumerate(sub_questions, start=1):

            print("\n" + "=" * 70)
            print(f"Researching Question {index}")
            print(question)
            print("=" * 70)

            sources = search_sources(question)

            total_sources += len(sources)

            documents = []

            all_verified = []

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

                    # Keep only verified evidence
                    verified = [
                        item
                        for item in verified
                        if item["verification_status"] != "Unverified"
                    ]

                    # Keep only top 5 evidence from each page
                    verified = verified[:5]

                    documents.append({

                        "source": url,

                        "content": text[:2500],

                        "chunks": relevant_chunks,

                        "evidence": verified

                    })

                    total_documents.append({

                        "source": url,

                        "content": text[:2500]

                    })

                    all_verified.extend(verified)

                except Exception as e:

                    print(f"Failed: {url}")

                    print(e)

            # ==========================================
            # Remove duplicate evidence
            # ==========================================

            unique = []

            seen = set()

            for item in all_verified:

                text = item["evidence"].strip()

                key = text.lower()

                if key in seen:
                    continue

                seen.add(key)

                unique.append(item)

            # ==========================================
            # Sort by confidence
            # ==========================================

            unique.sort(

                key=lambda x: x["confidence"],

                reverse=True

            )

            # ==========================================
            # Send only best evidence to Gemini
            # ==========================================

            best_evidence = unique[:8]

            answer = answer_agent.generate_answer(

                question,

                best_evidence

            )

            report_sections.append({

                "question": question,

                "answer": answer,

                "documents": documents

            })

        # ==========================================
        # Final User Answer
        # ==========================================

        final_answer = answer_agent.generate_final_answer(

            query,

            report_sections

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

            "sections": report_sections,

            "final_answer": final_answer

        }