#!/usr/bin/env python3
"""Generate topic directory scaffolds under topics/. See scripts/topic_manifest.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_SEGMENT_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def repo_root_from_script(script_path: Path) -> Path | None:
    candidate = script_path.resolve().parent.parent
    topics = candidate / "topics"
    if topics.is_dir():
        return candidate
    return None


def find_repo_root(start: Path) -> Path | None:
    """Walk parents from start looking for ./topics."""
    cur = start.resolve()
    while True:
        if (cur / "topics").is_dir():
            return cur
        parent = cur.parent
        if parent == cur:
            return None
        cur = parent


def resolve_topics_root(repo_root: Path, topics_relative: str) -> Path:
    return (repo_root / topics_relative).resolve()


def validate_rel_path(rel: str) -> str:
    stripped = rel.strip().strip("/")
    if not stripped:
        raise ValueError("relative path must not be empty")
    parts = stripped.split("/")
    for segment in parts:
        if segment in {".", ".."} or "/" in segment or not _SEGMENT_RE.match(segment):
            raise ValueError(f"invalid path segment (use snake_case): {segment!r}")
    canonical = "/".join(parts)
    resolved = canonical
    if ".." in resolved:
        raise ValueError("invalid path")
    return resolved


def slug_to_default_title_en(slug: str) -> str:
    parts = slug.split("_")
    return " ".join(p.capitalize() for p in parts)


DATA_README = """## データについて

この `data/` 以下は **Git で追跡されない**。

- **取得元**（URL / Kaggle データセット名 など）:
- **展開後の構成**（主なファイル名）:
- **`uv run` での準備メモ**（あれば）:
"""


def topic_readme_text(
    *, title_en: str, title_ja: str, rel_path: str, blurb: str
) -> str:
    return (
        f"# {title_en}（{title_ja}）\n\n"
        f"{blurb}\n\n"
        "## データ\n\n"
        "ローカルの `data/` に置く（Git には上げない）。"
        "入手元と前処理メモは [data/README.md](data/README.md) に書く。\n\n"
        "## 実行例\n\n"
        "リポジトリルートで（`uv` 利用時の例）:\n\n"
        f"```bash\ncd topics/{rel_path}\n"
        "# uv run python src/main.py   # 例\n```\n"
    )


def load_manifest(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        payload = json.load(f)
    topics = payload.get("topics")
    if not isinstance(topics, list):
        raise ValueError("manifest root must contain a list 'topics'")
    result: list[dict[str, Any]] = []
    for i, row in enumerate(topics):
        if not isinstance(row, dict):
            raise ValueError(f"topics[{i}] must be an object")
        result.append(row)
    return result


def manifest_entry_for_path(
    manifest_topics: list[dict[str, Any]], rel_path: str
) -> dict[str, Any] | None:
    for row in manifest_topics:
        if row.get("path") == rel_path:
            return row
    return None


class ScaffoldOps:
    def __init__(
        self,
        *,
        topics_root: Path,
        dry_run: bool,
        force: bool,
    ) -> None:
        self.topics_root = topics_root
        self.dry_run = dry_run
        self.force = force

    def _write_text(self, path: Path, body: str) -> None:
        if path.exists() and not self.force:
            print(f"[skip exists] {path}")
            return
        if self.dry_run:
            print(f"[dry-run write] {path}")
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        print(f"[wrote] {path}")

    def _mkdir_only(self, path: Path) -> None:
        if self.dry_run:
            print(f"[dry-run mkdir] {path}")
            return
        path.mkdir(parents=True, exist_ok=True)
        print(f"[mkdir] {path}")

    def _touch_gitkeep(self, path: Path) -> None:
        if path.exists():
            print(f"[skip exists] {path}")
            return
        if self.dry_run:
            print(f"[dry-run gitkeep] {path}")
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")
        print(f"[wrote] {path}")

    def scaffold_topic(
        self,
        *,
        rel_path: str,
        title_ja: str,
        title_en: str,
        blurb: str | None = None,
    ) -> None:
        base = self.topics_root.joinpath(*rel_path.split("/"))
        if blurb is None:
            blurb = f"`{rel_path}` の実験用ディレクトリ。"
        readme = topic_readme_text(
            title_en=title_en,
            title_ja=title_ja,
            rel_path=rel_path,
            blurb=blurb.strip(),
        )
        self._write_text(base / "README.md", readme)
        self._write_text(base / "data" / "README.md", DATA_README)
        self._mkdir_only(base / "outputs")
        self._touch_gitkeep(base / "notebooks" / ".gitkeep")
        self._touch_gitkeep(base / "src" / ".gitkeep")


def cmd_list(script_dir: Path) -> None:
    manifest_path = script_dir / "topic_manifest.json"
    topics_list = load_manifest(manifest_path)
    for row in topics_list:
        path = row.get("path", "")
        tja = row.get("title_ja", "")
        ten = row.get("title_en", "")
        kids = row.get("children") or []
        children_str = ",".join(str(c) for c in kids) if isinstance(kids, list) else ""
        extra = f"  [{children_str}]" if children_str else ""
        print(f"{path}\t{tja}\t{ten}{extra}")


def cmd_create(
    args: argparse.Namespace,
    *,
    repo_root: Path,
    script_dir: Path,
) -> int:
    rel = validate_rel_path(args.rel_path)
    manifest_path = script_dir / "topic_manifest.json"
    manifest_topics = load_manifest(manifest_path)
    entry = manifest_entry_for_path(manifest_topics, rel)

    title_ja = args.title_ja
    title_en = args.title_en
    if entry:
        title_ja = entry.get("title_ja") or title_ja
        title_en = entry.get("title_en") or title_en
    title_ja = title_ja or rel.split("/")[-1].replace("_", " ")
    title_en = title_en or slug_to_default_title_en(rel.split("/")[-1])

    topics_root = resolve_topics_root(repo_root, args.topics_root)
    ops = ScaffoldOps(topics_root=topics_root, dry_run=args.dry_run, force=args.force)
    ops.scaffold_topic(rel_path=rel, title_ja=str(title_ja), title_en=str(title_en))
    return 0


def cmd_create_all(
    args: argparse.Namespace, *, repo_root: Path, script_dir: Path
) -> int:
    manifest_path = script_dir / "topic_manifest.json"
    manifest_topics = load_manifest(manifest_path)
    topics_root = resolve_topics_root(repo_root, args.topics_root)
    ops = ScaffoldOps(topics_root=topics_root, dry_run=args.dry_run, force=args.force)

    for row in manifest_topics:
        path = row.get("path")
        if not isinstance(path, str):
            continue
        rel = validate_rel_path(path)
        title_ja = str(row.get("title_ja") or rel.split("/")[-1])
        title_en = str(
            row.get("title_en") or slug_to_default_title_en(rel.split("/")[-1])
        )
        ops.scaffold_topic(rel_path=rel, title_ja=title_ja, title_en=title_en)

        if not args.with_children:
            continue
        children = row.get("children")
        if not isinstance(children, list):
            continue
        for child in children:
            if not isinstance(child, str):
                continue
            child_rel = validate_rel_path(f"{rel}/{child}")
            child_slug = child.split("/")[-1]
            ops.scaffold_topic(
                rel_path=child_rel,
                title_ja=f"{title_ja} — {child_slug}",
                title_en=f"{title_en} — {slug_to_default_title_en(child_slug)}",
            )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scaffold topic directories under topics/."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without writing files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing README files (use with care).",
    )
    parser.add_argument(
        "--topics-root",
        default="topics",
        help="Directory under repo root (default: topics).",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List paths from manifest.")
    p_list.set_defaults(func=_dispatch_list)

    p_create = sub.add_parser(
        "create",
        help="Scaffold RELPATH relative to topics/ (manifest titles used if matched).",
    )
    p_create.add_argument(
        "rel_path",
        help="e.g. traditional_ml/regression or advanced/nlp/rag_demo",
    )
    p_create.add_argument("--title-ja", default=None)
    p_create.add_argument("--title-en", default=None)
    p_create.set_defaults(func=_dispatch_create)

    p_all = sub.add_parser(
        "create-all",
        help="Scaffold every manifest topic.",
    )
    p_all.add_argument(
        "--children",
        dest="with_children",
        action="store_true",
        help="Also create manifest-listed child topics under parents.",
    )
    p_all.set_defaults(func=_dispatch_create_all)

    return parser


def _dispatch_list(args: argparse.Namespace) -> int:
    script_dir = Path(__file__).resolve().parent
    cmd_list(script_dir)
    return 0


def _dispatch_create(args: argparse.Namespace) -> int:
    script_dir = Path(__file__).resolve().parent
    repo_root = find_repo_root(Path.cwd())
    if repo_root is None:
        repo_root = repo_root_from_script(Path(__file__))
    if repo_root is None:
        print("could not locate repo root (need ./topics/).", file=sys.stderr)
        return 1
    return cmd_create(args, repo_root=repo_root, script_dir=script_dir)


def _dispatch_create_all(args: argparse.Namespace) -> int:
    script_dir = Path(__file__).resolve().parent
    repo_root = find_repo_root(Path.cwd())
    if repo_root is None:
        repo_root = repo_root_from_script(Path(__file__))
    if repo_root is None:
        print("could not locate repo root (need ./topics/).", file=sys.stderr)
        return 1
    return cmd_create_all(args, repo_root=repo_root, script_dir=script_dir)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    func = args.func
    return int(func(args))


if __name__ == "__main__":
    raise SystemExit(main())
