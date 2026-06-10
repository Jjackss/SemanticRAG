#!/usr/bin/env python3
"""SemanticRAG - Main Build Script.

Main entry point for Knowledge Graph construction from technical manuals.

Usage:
    python scripts/build.py --manual-id my_manual --mode resume-compatible
    python scripts/build.py --source-chunks data/input/manual.txt --manual-id my_manual
"""

import argparse
import logging
import sys
from pathlib import Path

from config.settings import settings

# Add repo root to path
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))


def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(settings.log_file),
            logging.StreamHandler(),
        ],
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Build Knowledge Graph from technical manuals"
    )
    parser.add_argument(
        "--manual-id",
        required=True,
        help="Unique identifier for the manual (e.g., my_manual)",
    )
    parser.add_argument(
        "--source-chunks",
        type=Path,
        help="Path to chunks file (data/input/manual.txt)",
    )
    parser.add_argument(
        "--mode",
        choices=["resume-compatible", "force-stale", "force-all"],
        default="resume-compatible",
        help="Execution mode: resume from previous, force recalculation",
    )
    parser.add_argument(
        "--skip-publish",
        action="store_true",
        help="Skip GraphDB publication",
    )
    parser.add_argument(
        "--skip-cache",
        action="store_true",
        help="Skip cache and rebuild from scratch",
    )
    parser.add_argument(
        "--eval-dataset",
        type=Path,
        help="Path to golden set for evaluation (optional)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output",
    )
    return parser.parse_args()


def main():
    """Main entry point"""
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        args = parse_args()

        logger.info(f"SemanticRAG Build Pipeline Starting")
        logger.info(f"Manual ID: {args.manual_id}")
        logger.info(f"Mode: {args.mode}")
        logger.info(f"API Model: {settings.llm_model}")

        # TODO: Implement build pipeline
        #   1. Ingestion (core.ingestion)
        #   2. Extraction (core.extraction)
        #   3. Consolidation (canonicalization)
        #   4. Enrichment
        #   5. Evaluation (if golden set provided)
        #   6. Publication (if enabled)

        logger.info("Build Pipeline Complete ✓")
        return 0

    except Exception as e:
        logger.error(f"Build failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
