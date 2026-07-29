#!/usr/bin/env python3
"""Sync a chart's README version table and changelog annotation from Chart.yaml.

Usage: sync_chart_metadata.py <chart-dir> [<chart-dir> ...]
Exits non-zero (and prints changed files) if any file was rewritten.
"""
import re
import sys
from pathlib import Path


def read_chart_versions(chart_yaml: Path) -> tuple[str, str]:
    text = chart_yaml.read_text()
    version = re.search(r'^version:\s*(\S+)\s*$', text, re.MULTILINE).group(1)
    app_version = re.search(r'^appVersion:\s*"?([^"\s]+)"?\s*$', text, re.MULTILINE).group(1)
    return version, app_version


def sync_readme(readme: Path, version: str, app_version: str) -> bool:
    if not readme.exists():
        return False
    text = readme.read_text()
    pattern = re.compile(
        r'(\| Chart version \| App version \|\n\| -+ \| -+ \|\n)\| [^\n]+ \|\n'
    )
    new_row = f"| {version:<13} | {app_version:<11} |\n"
    new_text, count = pattern.subn(r'\1' + new_row, text, count=1)
    if count and new_text != text:
        readme.write_text(new_text)
        return True
    return False


def sync_changelog_annotation(chart_yaml: Path, app_version: str) -> bool:
    text = chart_yaml.read_text()
    pattern = re.compile(
        r'(  artifacthub\.io/changes: \|\n)(?:    .*\n)*'
    )
    new_block = f"  artifacthub.io/changes: |\n    - Bump n8n appVersion to {app_version}\n"
    new_text, count = pattern.subn(new_block, text, count=1)
    if count and new_text != text:
        chart_yaml.write_text(new_text)
        return True
    return False


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1

    changed = []
    for chart_dir in argv[1:]:
        chart_dir = Path(chart_dir)
        chart_yaml = chart_dir / "Chart.yaml"
        readme = chart_dir / "README.md"
        version, app_version = read_chart_versions(chart_yaml)

        if sync_readme(readme, version, app_version):
            changed.append(str(readme))
        if sync_changelog_annotation(chart_yaml, app_version):
            changed.append(str(chart_yaml))

    if changed:
        print("Updated:", ", ".join(changed))
    else:
        print("Nothing to sync.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
