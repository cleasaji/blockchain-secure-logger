# Blockchain Secure Decision Logger

A tamper-proof security audit logging system built using a SHA-256 chained block structure. Each security event is hashed together with the previous block's hash, making any retroactive modification immediately detectable.

## What it does

- Logs security events (login attempts, access decisions, policy changes) as immutable blocks
- Each block contains: timestamp, event data, previous block hash, and its own hash
- Any tampering with a past record breaks the entire chain — detectable instantly
- REST API for log ingestion and chain verification
- Simple web dashboard to view and verify the chain

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Hashing | SHA-256 (hashlib) |
| Database | SQLite |
| API | REST (JSON) |
| Frontend | HTML, CSS, JS |

## Project Structure

```
blockchain-secure-logger/
├── app.py               # Flask app and REST API routes
├── blockchain.py        # Core block chain logic
├── models.py            # SQLite database models
├── templates/
│   └── dashboard.html   # Web UI to view the chain
├── static/
│   └── style.css
├── requirements.txt
└── README.md
```

## How to Run

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/blockchain-secure-logger.git
cd blockchain-secure-logger

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py

# 4. Open in browser
# http://localhost:5000
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/log` | Add a new security event |
| GET | `/chain` | Get the full chain |
| GET | `/verify` | Verify chain integrity |

### Example — Log an event
```bash
curl -X POST http://localhost:5000/log \
  -H "Content-Type: application/json" \
  -d '{"event": "Failed login attempt", "user": "admin", "ip": "192.168.1.10"}'
```

### Example — Verify chain
```bash
curl http://localhost:5000/verify
# Returns: {"valid": true, "blocks": 42}
```

## How the Chaining Works

```
Block 0 (Genesis)         Block 1                    Block 2
┌─────────────────┐       ┌─────────────────┐        ┌─────────────────┐
│ data: "genesis" │       │ data: "event1"  │        │ data: "event2"  │
│ prev: "0000..." │──────▶│ prev: hash(B0)  │───────▶│ prev: hash(B1)  │
│ hash: abc123... │       │ hash: def456... │        │ hash: ghi789... │
└─────────────────┘       └─────────────────┘        └─────────────────┘
```

If anyone modifies Block 1, its hash changes — which breaks Block 2's `prev` field — which breaks every block after it. The chain is invalid.

## Use Case

Designed for security operations environments where audit log integrity is critical — e.g. SOC incident logs, access control decisions, or compliance records that must not be altered after the fact.

## Requirements

```
flask==3.0.0
hashlib (built-in)
sqlite3 (built-in)
```
