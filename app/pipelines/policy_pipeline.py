class PolicyPipeline:

    def calculate_premium(self, age, salary):
        base = 500
        return base + age * 10 + salary * 0.01

    def run(self, data):

        premium = self.calculate_premium(
            data["age"], data["salary"]
        )

        if premium < 2000:
            decision = "approve"
        else:
            decision = "review"

        return {
            "premium": premium,
            "decision": decision
        }