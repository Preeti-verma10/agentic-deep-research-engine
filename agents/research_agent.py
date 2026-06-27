# from utils.web_search import search_sources
# from utils.document_parser import fetch_document
# from utils.document_parser import parse_document

# from utils.retriever import (
#     chunk_text,
#     retrieve_relevant_chunks,
#     extract_evidence
# )

# from agents.planner_agent import PlannerAgent
# from agents.ranking_agent import RankingAgent
# from agents.verifier_agent import VerifierAgent
# from agents.answer_agent import AnswerAgent

# import os
# from dotenv import load_dotenv

# load_dotenv()


# class ResearchAgent:

#     def research(self, query):

#         print("\nGenerating Research Plan...\n")

#         api_key = os.getenv("GEMINI_API_KEY")

#         planner = PlannerAgent(api_key)

#         sub_questions = planner.create_plan(query)

#         print("\nResearch Plan:\n")

#         for i, question in enumerate(
#             sub_questions,
#             start=1
#         ):
#             print(f"{i}. {question}")

#         ranking_agent = RankingAgent()
#         verifier_agent = VerifierAgent()
#         answer_agent = AnswerAgent()

#         total_documents = []
#         report_sections = []

#         total_sources = 0

#         for index, question in enumerate(
#             sub_questions,
#             start=1
#         ):

#             print("\n" + "=" * 60)
#             print(f"Researching Question {index}")
#             print(question)
#             print("=" * 60)

#             sources = search_sources(question)

#             total_sources += len(sources)

#             documents = []

#             all_verified_evidence = []

#             for url in sources:

#                 try:

#                     print(f"Reading: {url}")

#                     html = fetch_document(url)

#                     if not html:
#                         continue

#                     text = parse_document(html)

#                     if not text:
#                         continue

#                     chunks = chunk_text(text)

#                     relevant_chunks = retrieve_relevant_chunks(
#                         question,
#                         chunks
#                     )

#                     evidence = extract_evidence(
#                         relevant_chunks
#                     )

#                     if not evidence:
#                         continue

#                     ranked = ranking_agent.score_evidence(
#                         evidence,
#                         question
#                     )

#                     verified = verifier_agent.verify(
#                         ranked
#                     )

#                     doc = {

#                         "source": url,

#                         "content": text[:3000],

#                         "chunks": relevant_chunks,

#                         "evidence": verified

#                     }

#                     documents.append(doc)

#                     total_documents.append(doc)

#                     all_verified_evidence.extend(
#                         verified
#                     )

#                 except Exception as e:

#                     print(f"Failed: {url}")
#                     print(e)

#             answer = answer_agent.generate_answer(
#                 question,
#                 all_verified_evidence
#             )

#             report_sections.append(

#                 {

#                     "question": question,

#                     "answer": answer,

#                     "documents": documents

#                 }

#             )

#         print("\nResearch Completed.")

#         plan = {

#             "original_query": query,

#             "sources_found": total_sources,

#             "sub_questions": sub_questions

#         }

#         return {

#             "documents": total_documents,

#             "plan": plan,

#             "sections": report_sections

#         }




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

        for i, question in enumerate(
            sub_questions,
            start=1
        ):
            print(f"{i}. {question}")

        ranking_agent = RankingAgent()
        verifier_agent = VerifierAgent()
        answer_agent = AnswerAgent()

        total_documents = []
        report_sections = []

        total_sources = 0

        # -----------------------------------
        # Research each sub-question
        # -----------------------------------

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

            all_verified_evidence = []

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

                    all_verified_evidence.extend(
                        verified
                    )

                except Exception as e:

                    print(f"Failed: {url}")
                    print(e)

            # -----------------------------------
            # AI Answer for this sub-question
            # -----------------------------------

            answer = answer_agent.generate_answer(
                question,
                all_verified_evidence
            )

            report_sections.append(

                {

                    "question": question,

                    "answer": answer,

                    "documents": documents

                }

            )

        # -----------------------------------
        # FINAL ANSWER FOR USER QUERY
        # -----------------------------------

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