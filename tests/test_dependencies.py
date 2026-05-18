from __future__ import annotations


def test_runtime_dependencies_are_importable() -> None:
    import lunar_python
    import streamlit
    import streamlit_js_eval

    assert lunar_python is not None
    assert streamlit is not None
    assert streamlit_js_eval is not None
