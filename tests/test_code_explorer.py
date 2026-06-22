import pytest
from code_explorer import CodeExplorer

def test_add_function():
    explorer = CodeExplorer()
    explorer.add_function("auth_login", ["auth_register", "auth_logout"])
    assert "auth_login" in explorer.functions

def test_update_usage():
    explorer = CodeExplorer()
    explorer.add_function("auth_login", ["auth_register", "auth_logout"])
    explorer.update_usage("auth_login")
    assert explorer.functions["auth_login"].usage_count == 1

def test_get_related_functions():
    explorer = CodeExplorer()
    explorer.add_function("auth_login", ["auth_register", "auth_logout"])
    related_functions = explorer.get_related_functions("auth_login")
    assert related_functions == ["auth_register", "auth_logout"]

def test_search_functions():
    explorer = CodeExplorer()
    explorer.add_function("auth_login", ["auth_register", "auth_logout"])
    explorer.add_function("user_register", ["user_login", "user_logout"])
    results = explorer.search_functions("auth")
    assert "auth_login" in results

def test_rank_functions():
    explorer = CodeExplorer()
    explorer.add_function("auth_login", ["auth_register", "auth_logout"])
    explorer.update_usage("auth_register")
    explorer.update_usage("auth_register")
    ranked_functions = explorer.rank_functions("auth_login")
    assert ranked_functions == ["auth_register", "auth_logout"]

def test_navigate():
    explorer = CodeExplorer()
    explorer.add_function("auth_login", ["auth_register", "auth_logout"])
    explorer.update_usage("auth_register")
    explorer.update_usage("auth_register")
    next_function = explorer.navigate("auth_login")
    assert next_function == "auth_register"
