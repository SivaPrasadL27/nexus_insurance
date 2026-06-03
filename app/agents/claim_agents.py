async def hospital_agent(hospital_name):
    valid = hospital_name.lower() in ["austin medical center"]
    return {
        "value": 1.0 if valid else 0.3,
        "reason": "Verified hospital" if valid else "Unknown hospital"
    }

async def expense_agent(amount):
    if amount < 1500:
        return {"value": 0.9, "reason": "Within normal range"}
    return {"value": 0.4, "reason": "Too high"}

async def treatment_agent(code):
    valid = code in ["M17"]
    return {
        "value": 0.9 if valid else 0.5,
        "reason": "Valid treatment" if valid else "Unclear mapping"
    }