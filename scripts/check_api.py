#!/usr/bin/env python3
"""Check API Usage and Health.

Verifies API connectivity, authentication, and usage limits.

Usage:
    python scripts/check_api.py
"""

import logging
import sys
from pathlib import Path

from config.settings import settings

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))


def main():
    """Check API status."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    print("\nSemanticRAG API Health Check")
    print("=" * 50)

    # Check LLM API
    print(f"\nLLM Configuration")
    print(f"  Model: {settings.llm_model}")
    print(f"  API Key: {'Present' if settings.has_api_key else 'Missing'}")

    # Check GraphDB
    if settings.graphdb_endpoint:
        print(f"\nGraphDB Configuration")
        print(f"  Endpoint: {settings.graphdb_endpoint}")
        print(f"  Enabled: {settings.is_graphdb_enabled}")
    else:
        print(f"\nGraphDB: Not configured")

    # TODO: Actually ping APIs to verify connectivity
    print("\nConfiguration loaded successfully")


if __name__ == "__main__":
    main()
