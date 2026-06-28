# class VerifierAgent:

#     def verify(self, ranked_evidence):

#         verified_results = []

#         for item in ranked_evidence:

#             confidence = item["confidence"]

#             if confidence >= 8:
#                 status = "Verified"

#             elif confidence >= 6:
#                 status = "Partially Verified"

#             else:
#                 status = "Unverified"

#             item["verification_status"] = status

#             verified_results.append(item)

#         return verified_results

class VerifierAgent:

    def verify(self, ranked_evidence):

        verified_results = []

        for item in ranked_evidence:

            if not isinstance(item, dict):
                continue

            confidence = item.get("confidence", 0)

            if confidence >= 8:

                status = "Verified"

            elif confidence >= 6:

                status = "Partially Verified"

            else:

                status = "Unverified"

            verified_results.append({

                "evidence": item.get("evidence", ""),

                "confidence": confidence,

                "verification_status": status,

                "verifiability": item.get("verifiability", 0),

                "grounding": item.get("grounding", 0),

                "relevance": item.get("relevance", 0),

                "helpfulness": item.get("helpfulness", 0)

            })

        return verified_results