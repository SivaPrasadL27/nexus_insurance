class TruthScoreEngine:

    def __init__(self):
        # self.weights = {
        #     "hospital": 0.3,
        #     "expense": 0.4,
        #     "treatment": 0.3
        # }
        self.weights = {
            "hospital": 0.25,
            "expense": 0.30,
            "treatment": 0.25,
            "coverage": 0.20,
            "fraud": 0.20   
        }

    def compute(self, scores):
        total = 0
        evidence = []

        for name, score in scores.items():
            weight = self.weights.get(name, 0.1)
            total += weight * score["value"]
            evidence.append({
                "agent": name,
                "score": score["value"],
                "reason": score["reason"]
            })

        if total >= 0.9:
            level = "high"
            decision = "approve"
        elif total >= 0.6:
            level = "medium"
            decision = "review"
        else:
            level = "low"
            decision = "manual"

        return {
            "decision": decision,
            "confidence": total,
            "level": level,
            "evidence": evidence
        }