from app.core.neo4j_db import driver


class GraphService:

    @staticmethod
    def create_claim_graph(
        customer_id,
        policy_id,
        claim_id,
        hospital,
        amount
    ):

        query = """
        MERGE (c:Customer {id: $customer_id})
        MERGE (p:Policy {id: $policy_id})
        MERGE (cl:Claim {id: $claim_id})
        MERGE (h:Hospital {name: $hospital})

        MERGE (c)-[:OWNS]->(p)
        MERGE (p)-[:HAS_CLAIM]->(cl)
        MERGE (cl)-[:TREATED_AT]->(h)

        SET cl.amount = $amount
        """

        with driver.session() as session:
            session.run(
                query,
                customer_id=customer_id,
                policy_id=policy_id,
                claim_id=claim_id,
                hospital=hospital,
                amount=amount
            )
    
    @staticmethod
    def hospital_risk_score(hospital_name):

        query = """
        MATCH (h:Hospital {name: $hospital})<-[:TREATED_AT]-(c:Claim)

        RETURN count(c) as claim_count,
               avg(c.amount) as avg_amount
        """

        with driver.session() as session:

            result = session.run(
                query,
                hospital=hospital_name
            )

            record = result.single()

            if not record:
                return {
                    "score": 0.9,
                    "reason": "No suspicious graph activity"
                }

            count = record["claim_count"] or 0
            avg_amount = record["avg_amount"] or 0

            # ✅ Basic anomaly logic

            if count > 20 and avg_amount > 5000:
                return {
                    "score": 0.2,
                    "reason": "Hospital linked to unusually high claim activity"
                }

            if count > 10:
                return {
                    "score": 0.5,
                    "reason": "Elevated hospital claim frequency"
                }

            return {
                "score": 0.9,
                "reason": "Normal graph behavior"
            }

