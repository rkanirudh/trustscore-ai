import hashlib
import json
import time

class SimpleBlockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        self.chain.append({
            "index": 0,
            "timestamp": time.time(),
            "data": "Genesis Block",
            "previous_hash": "0",
            "hash": self.hash_block("Genesis Block")
        })

    def hash_block(self, data):
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def add_block(self, data):
        previous_hash = self.chain[-1]["hash"]
        block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "data": data,
            "previous_hash": previous_hash,
            "hash": self.hash_block(data)
        }
        self.chain.append(block)

    def get_chain(self):
        return self.chain
