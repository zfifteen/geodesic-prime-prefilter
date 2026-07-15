import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path("research/06-cryptology-rsa/experiments/live-solver/rsa-v3").resolve()))
import pytest

# Mock pytest if it's not installed, we don't strictly need it to run standard asserts
import builtins
class MockPytestRaises:
    def __init__(self, exc):
        self.exc = exc
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and issubclass(exc_type, self.exc):
            return True
        return False
pytest_mock = type('pytest', (), {'raises': MockPytestRaises})
sys.modules['pytest'] = pytest_mock

# Now import the test file
from research._06_cryptology_rsa.tests import test_a1_endpoint_resolver_unit
