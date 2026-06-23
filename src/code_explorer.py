import json
from dataclasses import dataclass
from datetime import datetime, timedelta
import hashlib
import hmac
import secrets

@dataclass
class Graph:
    id: str
    data: str

class CodeExplorer:
    def __init__(self):
        self.graphs = {}
        self.secret_key = secrets.token_bytes(32)

    def generate_share_link(self, graph_id):
        graph = self.graphs.get(graph_id)
        if not graph:
            raise ValueError("Graph not found")
        token = self._generate_token(graph_id)
        return f"http://example.com/graph/{graph_id}?token={token}"

    def _generate_token(self, graph_id):
        expires_at = int((datetime.now() + timedelta(days=30)).timestamp())
        payload = json.dumps({"graph_id": graph_id, "expires_at": expires_at}).encode()
        signature = hmac.new(self.secret_key, payload, hashlib.sha256).hexdigest()
        return f"{payload.decode()}.{signature}"

    def validate_token(self, token):
        try:
            payload, signature = token.rsplit(".", 1)
            expected_signature = hmac.new(self.secret_key, payload.encode(), hashlib.sha256).hexdigest()
            if signature != expected_signature:
                return False
            data = json.loads(payload)
            if data["expires_at"] < int(datetime.now().timestamp()):
                return False
            return data["graph_id"]
        except (ValueError, json.JSONDecodeError):
            return False

    def add_graph(self, graph):
        self.graphs[graph.id] = graph

    def get_graph(self, graph_id, token):
        if not self.validate_token(token):
            raise ValueError("Invalid or expired token")
        return self.graphs.get(graph_id)
