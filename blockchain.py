import hashlib
import json
from datetime import datetime


class Block:
    def __init__(self, index, event, previous_hash):
        self.index = index
        self.timestamp = datetime.utcnow().isoformat()
        self.event = event
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_data = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "event": self.event,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_data.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "event": self.event,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }


class Blockchain:
    def __init__(self):
        self.chain = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        genesis = Block(0, "Genesis Block", "0" * 64)
        self.chain.append(genesis)

    def get_last_block(self):
        return self.chain[-1]

    def add_event(self, event_data):
        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            event=event_data,
            previous_hash=last_block.hash
        )
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.compute_hash():
                return False, f"Block {i} hash is invalid (tampered)"

            if current.previous_hash != previous.hash:
                return False, f"Block {i} previous_hash does not match Block {i-1} hash"

        return True, "Chain is valid"

    def to_list(self):
        return [block.to_dict() for block in self.chain]
