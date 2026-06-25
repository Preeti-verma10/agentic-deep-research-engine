class RankingAgent:

    def score_evidence(self, evidence, query):

        ranked_evidence = []

        query_words = query.lower().split()

        for item in evidence:

            # V = Verifiability
            verifiability = 8 if len(item) > 50 else 5

            # G = Grounding
            grounding = 8

            # R = Relevance
            relevance = 0

            for word in query_words:
                if word in item.lower():
                    relevance += 2

            relevance = min(relevance, 10)

            # H = Helpfulness
            helpfulness = 8 if len(item) > 80 else 6

            confidence = round(
                (
                    verifiability +
                    grounding +
                    relevance +
                    helpfulness
                ) / 4,
                2
            )

            ranked_evidence.append({
                "evidence": item,
                "verifiability": verifiability,
                "grounding": grounding,
                "relevance": relevance,
                "helpfulness": helpfulness,
                "confidence": confidence
            })

        ranked_evidence.sort(
            key=lambda x: x["confidence"],
            reverse=True
        )

        return ranked_evidence