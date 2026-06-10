def coverage_signal(claim_amount, coverage_amount):

    if claim_amount <= coverage_amount:
        return {
            "value": 0.95,
            "reason": f"Within coverage ({coverage_amount})"
        }

    return {
        "value": 0.2,
        "reason": f"Exceeds coverage limit ({coverage_amount})"
    }