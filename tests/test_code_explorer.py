import pytest
from code_explorer import analyze_code, upload_code, CodeAnalysis

def test_analyze_code():
    codebase = "example_code"
    analysis = analyze_code(codebase)
    assert analysis.structure == "The codebase has a simple structure."
    assert analysis.purpose == "The codebase is designed to perform a specific task."

def test_upload_code():
    codebase = "example_code"
    analysis = upload_code(codebase)
    assert analysis.structure == "The codebase has a simple structure."
    assert analysis.purpose == "The codebase is designed to perform a specific task."

def test_upload_code_empty():
    codebase = ""
    analysis = upload_code(codebase)
    assert analysis.structure == "The codebase has a simple structure."
    assert analysis.purpose == "The codebase is designed to perform a specific task."

def test_analyze_code_edge_case():
    codebase = None
    with pytest.raises(AttributeError):
        analyze_code(codebase)
