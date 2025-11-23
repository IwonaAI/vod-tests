import sys
import pathlib
import pytest

# Ensure project root is on sys.path for module imports like `utils` and `pages`
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.driver_factory import create_driver

@pytest.fixture
def driver():
    try:
        drv = create_driver()
    except Exception as e:
        pytest.skip(f"Skipping test - driver initialization failed: {e}")
    yield drv
    try:
        drv.quit()
    except Exception:
        pass
