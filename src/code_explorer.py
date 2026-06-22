import json
from dataclasses import dataclass
from collections import defaultdict
from typing import List, Dict

@dataclass
class Function:
    name: str
    usage_count: int
    related_functions: List[str]

class CodeExplorer:
    def __init__(self):
        self.functions = {}
        self.function_usage = defaultdict(int)

    def add_function(self, name: str, related_functions: List[str]):
        self.functions[name] = Function(name, 0, related_functions)

    def update_usage(self, function_name: str):
        if function_name in self.functions:
            self.functions[function_name].usage_count += 1
            self.function_usage[function_name] += 1

    def get_related_functions(self, function_name: str) -> List[str]:
        if function_name in self.functions:
            return self.functions[function_name].related_functions
        return []

    def search_functions(self, query: str) -> List[str]:
        results = []
        for function in self.functions.values():
            if query.lower() in function.name.lower():
                results.append(function.name)
        return results

    def rank_functions(self, function_name: str) -> List[str]:
        related_functions = self.get_related_functions(function_name)
        ranked_functions = sorted(related_functions, key=lambda x: self.function_usage[x], reverse=True)
        return ranked_functions

    def navigate(self, function_name: str) -> str:
        related_functions = self.rank_functions(function_name)
        return related_functions[0] if related_functions else None
