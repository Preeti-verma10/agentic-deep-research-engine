class VerifierAgent:

    def verify(self, ranked_evidence):

        verified_results = []

        for item in ranked_evidence:

            confidence = item["confidence"]

            if confidence >= 8:
                status = "Verified"

            elif confidence >= 6:
                status = "Partially Verified"

            else:
                status = "Unverified"

            item["verification_status"] = status

            verified_results.append(item)

        return verified_results