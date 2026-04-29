import pytest
from core.clients.api_client import APIClient


@pytest.fixture
def api_client():
    return APIClient()