from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def test_path() -> Path:
    return Path(__file__).parent


@pytest.fixture(scope="session")
def template_path(test_path) -> Path:
    return test_path.parent / 'templates'
