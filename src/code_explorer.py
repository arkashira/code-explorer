import json
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Component:
    name: str
    description: str
    links: List[str]

class CodeExplorer:
    def __init__(self, components: Dict[str, Component]):
        self.components = components

    def get_component_description(self, component_name: str) -> str:
        component = self.components.get(component_name)
        if component:
            return component.description
        return "Component not found"

    def get_contextual_navigation_links(self, component_name: str) -> List[str]:
        component = self.components.get(component_name)
        if component:
            return component.links
        return []

    def get_tooltip(self, component_name: str) -> str:
        description = self.get_component_description(component_name)
        links = self.get_contextual_navigation_links(component_name)
        tooltip = f"{description}\nLinks: {', '.join(links)}"
        return tooltip

def load_components_from_json(json_data: str) -> Dict[str, Component]:
    components = {}
    data = json.loads(json_data)
    for component_data in data:
        component = Component(
            name=component_data["name"],
            description=component_data["description"],
            links=component_data["links"]
        )
        components[component.name] = component
    return components
