from utils.web_search import search_sources
from utils.document_parser import fetch_document
from utils.document_parser import parse_document

from utils.retriever import chunk_text
from utils.retriever import retrieve_relevant_chunks
from utils.retriever import extract_evidence

from agents.ranking_agent import RankingAgent
from agents.verifier_agent import VerifierAgent

import os
from dotenv import load_dotenv

load_dotenv()

class ResearchAgent:

 def research(self, query):

    print("\nSearching sources...\n")

    clean_query = (
        query
        .replace("What is", "")
        .replace("?", "")
        .strip()
    )

    print(f"Searching Wikipedia for: {clean_query}")

    sources = search_sources(clean_query)

    print(f"Sources Found: {len(sources)}")

    documents = []

    ranking_agent = RankingAgent()
    verifier_agent = VerifierAgent()

    # ✅ FIX: CREATE PLAN HERE
    plan = {
        "original_query": query,
        "clean_query": clean_query,
        "sources_found": len(sources),
        "steps": [
            "search_sources",
            "fetch_documents",
            "parse_html",
            "chunk_text",
            "retrieve_relevant_chunks",
            "extract_evidence",
            "rank_evidence",
            "verify_evidence"
        ]
    }

    for url in sources:

        try:

            print(f"\nReading: {url}")

            html = fetch_document(url)

            if not html:
                continue

            text = parse_document(html)

            if not text:
                continue

            chunks = chunk_text(text)

            relevant_chunks = retrieve_relevant_chunks(
                clean_query,
                chunks
            )

            evidence = extract_evidence(relevant_chunks)

            if not evidence:
                continue

            ranked = ranking_agent.score_evidence(
                evidence,
                clean_query
            )

            verified = verifier_agent.verify(ranked)

            documents.append({
                "source": url,
                "content": text[:3000],
                "chunks": relevant_chunks,
                "evidence": verified
            })

            print("Document Added")

        except Exception as e:

            print(f"Failed: {url}")
            print(e)

    print(f"\nDocuments Collected: {len(documents)}")

    return {
        "documents": documents,
        "plan": plan   # ✅ FIXED
    }