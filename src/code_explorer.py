import json
from dataclasses import dataclass
from typing import List

@dataclass
class Node:
    id: int
    summary: str
    doc_link: str

class CodeExplorer:
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes

    def get_node_tooltip(self, node_id: int) -> str:
        node = next((n for n in self.nodes if n.id == node_id), None)
        if node:
            return f"{node.summary} ({node.doc_link})"
        return ""

    def get_accessible_tooltip(self, node_id: int) -> str:
        tooltip = self.get_node_tooltip(node_id)
        if tooltip:
            return f"<div role='tooltip' aria-label='{tooltip}'>{tooltip}</div>"
        return ""
