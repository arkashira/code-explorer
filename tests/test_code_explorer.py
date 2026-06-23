import json
import hmac
import hashlib
from code_explorer import CodeExplorer, Graph
import pytest

def test_generate_share_link():
    explorer = CodeExplorer()
    graph = Graph("1", "example data")
    explorer.add_graph(graph)
    link = explorer.generate_share_link("1")
    assert link.startswith("http://example.com/graph/1?token=")

def test_validate_token():
    explorer = CodeExplorer()
    graph = Graph("1", "example data")
    explorer.add_graph(graph)
    token = explorer._generate_token("1")
    assert explorer.validate_token(token) == "1"

def test_validate_token_expired():
    explorer = CodeExplorer()
    graph = Graph("1", "example data")
    explorer.add_graph(graph)
    payload = json.dumps({"graph_id": "1", "expires_at": 0}).encode()
    signature = hmac.new(explorer.secret_key, payload, hashlib.sha256).hexdigest()
    token = f"{payload.decode()}.{signature}"
    assert not explorer.validate_token(token)

def test_get_graph():
    explorer = CodeExplorer()
    graph = Graph("1", "example data")
    explorer.add_graph(graph)
    token = explorer._generate_token("1")
    retrieved_graph = explorer.get_graph("1", token)
    assert retrieved_graph == graph

def test_get_graph_invalid_token():
    explorer = CodeExplorer()
    graph = Graph("1", "example data")
    explorer.add_graph(graph)
    with pytest.raises(ValueError):
        explorer.get_graph("1", "invalid token")
