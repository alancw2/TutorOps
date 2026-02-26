from pathlib import Path
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure backend/ is on PYTHONPATH so `import app...` works
BACKEND_DIR = Path(__file__).resolve().parents[1]  # .../backend
sys.path.insert(0, str(BACKEND_DIR))

from app.main import app
from app import storage


@pytest.fixture(autouse=True)
def reset_storage():
    storage.reset_db()
    yield


@pytest.fixture()
def client():
    return TestClient(app)
