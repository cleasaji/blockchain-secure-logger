from flask import Flask, request, jsonify, render_template_string
from blockchain import Blockchain

app = Flask(__name__)
bc = Blockchain()

DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
  <title>Secure Decision Logger</title>
  <style>
    body { font-family: Calibri, sans-serif; background: #f1f5f9; margin: 0; padding: 20px; }
    h1 { color: #1A3C5E; }
    .block { background: white; border-left: 4px solid #2563EB; padding: 14px 18px;
             margin-bottom: 12px; border-radius: 6px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
    .block h3 { margin: 0 0 6px; color: #1A3C5E; }
    .hash { font-family: monospace; font-size: 12px; color: #6b7280; word-break: break-all; }
    .valid { color: #16a34a; font-weight: bold; }
    .invalid { color: #dc2626; font-weight: bold; }
    form { background: white; padding: 16px; border-radius: 8px; margin-bottom: 20px; }
    input[type=text] { width: 60%; padding: 8px; border: 1px solid #d1d5db; border-radius: 4px; }
    button { padding: 8px 18px; background: #2563EB; color: white; border: none;
             border-radius: 4px; cursor: pointer; }
  </style>
</head>
<body>
  <h1>🔒 Blockchain Secure Decision Logger</h1>
  <form method="POST" action="/log-form">
    <input type="text" name="event" placeholder="Enter security event e.g. Failed login from 192.168.1.10" required>
    <button type="submit">Log Event</button>
  </form>
  <p>Chain status: <span class="{{ 'valid' if valid else 'invalid' }}">{{ status }}</span></p>
  {% for block in chain %}
  <div class="block">
    <h3>Block #{{ block.index }} — {{ block.timestamp }}</h3>
    <p>{{ block.event }}</p>
    <p class="hash">Hash: {{ block.hash }}</p>
    <p class="hash">Prev: {{ block.previous_hash }}</p>
  </div>
  {% endfor %}
</body>
</html>
"""

@app.route("/")
def dashboard():
    valid, status = bc.is_chain_valid()
    return render_template_string(DASHBOARD, chain=bc.to_list(), valid=valid, status=status)

@app.route("/log-form", methods=["POST"])
def log_form():
    event = request.form.get("event", "")
    if event:
        bc.add_event(event)
    from flask import redirect
    return redirect("/")

@app.route("/log", methods=["POST"])
def log_event():
    data = request.get_json()
    if not data or "event" not in data:
        return jsonify({"error": "Missing 'event' field"}), 400
    block = bc.add_event(data["event"])
    return jsonify({"message": "Event logged", "block": block.to_dict()}), 201

@app.route("/chain", methods=["GET"])
def get_chain():
    return jsonify({"length": len(bc.chain), "chain": bc.to_list()})

@app.route("/verify", methods=["GET"])
def verify():
    valid, message = bc.is_chain_valid()
    return jsonify({"valid": valid, "message": message, "blocks": len(bc.chain)})


if __name__ == "__main__":
    app.run(debug=True)
