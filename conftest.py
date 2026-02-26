"""
Root conftest — sets environment variables before any src.* imports.

This must live at the project root so pytest loads it before test files
trigger the import of src.core.config.Settings().
"""
import os

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault(
    "SECRET_KEY", "test-secret-key-minimum-32-characters-long-for-tests-only"
)
os.environ.setdefault("ALLOWED_ORIGINS", '["http://localhost:3000"]')
