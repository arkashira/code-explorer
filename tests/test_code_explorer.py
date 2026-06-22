import pytest
from code_explorer import CodeExplorer, load_components_from_json, Component

def test_get_component_description():
    components = {
        "component1": Component("component1", "This is component 1", ["link1", "link2"]),
        "component2": Component("component2", "This is component 2", ["link3", "link4"])
    }
    explorer = CodeExplorer(components)
    assert explorer.get_component_description("component1") == "This is component 1"
    assert explorer.get_component_description("component3") == "Component not found"

def test_get_contextual_navigation_links():
    components = {
        "component1": Component("component1", "This is component 1", ["link1", "link2"]),
        "component2": Component("component2", "This is component 2", ["link3", "link4"])
    }
    explorer = CodeExplorer(components)
    assert explorer.get_contextual_navigation_links("component1") == ["link1", "link2"]
    assert explorer.get_contextual_navigation_links("component3") == []

def test_get_tooltip():
    components = {
        "component1": Component("component1", "This is component 1", ["link1", "link2"]),
        "component2": Component("component2", "This is component 2", ["link3", "link4"])
    }
    explorer = CodeExplorer(components)
    tooltip = explorer.get_tooltip("component1")
    assert "This is component 1" in tooltip
    assert "link1, link2" in tooltip

def test_load_components_from_json():
    json_data = '[{"name": "component1", "description": "This is component 1", "links": ["link1", "link2"]}, {"name": "component2", "description": "This is component 2", "links": ["link3", "link4"]}]'
    components = load_components_from_json(json_data)
    assert len(components) == 2
    assert components["component1"].description == "This is component 1"
    assert components["component2"].links == ["link3", "link4"]
