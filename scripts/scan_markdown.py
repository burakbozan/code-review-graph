from pathlib import Path
from textwrap import indent

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE = {"node_modules", "dist", ".git", ".venv", "__pycache__"}

CATEGORY_PATTERNS = [
    ("User docs", lambda p: p.parts[1:] and p.parts[1] == "docs"),
    ("Localized README", lambda p: p.name.startswith("README.") and p.parent == ROOT),
    ("Project landing", lambda p: p.name == "README.md" and p.parent == ROOT),
    ("Governance", lambda p: p.name in {"CHANGELOG.md", "SECURITY.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md"}),
    ("Extension docs", lambda p: p.parts[1:] and p.parts[1] == "code-review-graph-vscode"),
    ("Skills/docs", lambda p: p.parts[1:] and p.parts[1] == "skills"),
    ("Internal/other", lambda p: True),
]


def categorize(path: Path) -> str:
    for label, matcher in CATEGORY_PATTERNS:
        if matcher(path):
            return label
    return "Uncategorized"


def scan_markdown(root: Path) -> dict[str, list[Path]]:
    files = []
    for path in root.rglob("*.md"):
        if any(part in EXCLUDE for part in path.parts):
            continue
        if path.is_file():
            files.append(path.relative_to(root))
    categories: dict[str, list[Path]] = {}
    for path in sorted(files):
        category = categorize(path)
        categories.setdefault(category, []).append(path)
    return categories


def print_categories(categories: dict[str, list[Path]]) -> None:
    for category, paths in categories.items():
        print(f"{category} ({len(paths)})")
        print(indent("\n".join(str(p) for p in paths), "  "))
        print()


if __name__ == "__main__":
    categories = scan_markdown(ROOT)
    print_categories(categories)
