import pytest
from code_explorer import CodeExplorer, Node

@pytest.fixture
def nodes():
    return [
        Node(1, "Summary 1", "https://example.com/doc1"),
        Node(2, "Summary 2", "https://example.com/doc2"),
    ]

def test_get_node_tooltip(nodes):
    explorer = CodeExplorer(nodes)
    assert explorer.get_node_tooltip(1) == "Summary 1 (https://example.com/doc1)"

def test_get_node_tooltip_missing_node(nodes):
    explorer = CodeExplorer(nodes)
    assert explorer.get_node_tooltip(3) == ""

def test_get_accessible_tooltip(nodes):
    explorer = CodeExplorer(nodes)
    assert explorer.get_accessible_tooltip(1) == "<div role='tooltip' aria-label='Summary 1 (https://example.com/doc1)'>Summary 1 (https://example.com/doc1)</div>"

def test_get_accessible_tooltip_missing_node(nodes):
    explorer = CodeExplorer(nodes)
    assert explorer.get_accessible_tooltip(3) == ""
