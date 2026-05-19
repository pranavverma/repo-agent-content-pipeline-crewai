#!/usr/bin/env python3
"""
CLI for the CrewAI content pipeline.

Usage
-----
    python scripts/generate.py "Topic here" [--tone professional] [--audience general] [--words 800]

Examples
--------
    python scripts/generate.py "The rise of edge computing in IoT" --tone technical --words 1000
    python scripts/generate.py "Why remote work is here to stay" --audience executive
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import yaml
from dotenv import load_dotenv

from src.crews.content_crew import ContentCrew


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Generate an SEO-optimised article via CrewAI.")
    parser.add_argument("topic", help="Topic for the article")
    parser.add_argument("--tone", default="professional", choices=["professional", "conversational", "technical"])
    parser.add_argument("--audience", default="general", choices=["general", "technical", "executive"])
    parser.add_argument("--words", type=int, default=800)
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()

    with open(args.config) as f:
        cfg = yaml.safe_load(f)

    print(f"\n{'='*60}")
    print("  CrewAI Content Pipeline")
    print(f"{'='*60}")
    print(f"  Topic    : {args.topic}")
    print(f"  Tone     : {args.tone}")
    print(f"  Audience : {args.audience}")
    print(f"  Words    : {args.words}")
    print(f"{'='*60}\n")

    crew = ContentCrew(cfg)
    result = crew.run(args.topic, args.tone, args.audience, args.words)

    print(f"\n{'='*60}")
    print("  Pipeline Complete")
    print(f"{'='*60}")
    print(f"  Output saved → {result['output_file']}\n")
    print(result["content"])


if __name__ == "__main__":
    main()
