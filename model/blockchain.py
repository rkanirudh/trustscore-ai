import hashlib
import time

def generate_transaction_hash(amount, risk_score):
    payload = f"{amount}-{risk_score}-{time.time()}"
    return hashlib.sha256(payload.encode()).hexdigest()

def create_block(transaction):
    return {
        "timestamp": time.time(),
        "amount": transaction["Amount"],
        "risk_score": transaction["risk_score"],
        "trust_score": transaction["trust_score"],
        "hash": generate_transaction_hash(
            transaction["Amount"], transaction["risk_score"]
        )
    }
