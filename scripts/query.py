#!/usr/bin/env python3
"""Interactive Query Interface.

Provides an interactive REPL for querying the Knowledge Graph using SPARQL.

Usage:
    python scripts/query.py
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))


def main():
    """Interactive query interface."""
    print("\nSemanticRAG Query Interface")
    print("=" * 50)
    print("Enter SPARQL queries interactively.")
    print("Type 'help' for commands, 'exit' to quit.\n")

    # TODO: Implement interactive REPL
    #   - Load Knowledge Graph from RDF files
    #   - Provide SPARQL query interface
    #   - Format and display results
    #   - Support for both local and GraphDB queries


if __name__ == "__main__":
    main()
