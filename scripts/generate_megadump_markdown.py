from __future__ import annotations

from datetime import datetime
import hashlib
from pathlib import Path
from typing import Iterable

import nbformat

try:
    from docx import Document  # type: ignore
except Exception:
    Document = None


ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "reports" / "CE310_MEGA_CONTEXT_DUMP_FOR_GPT_PRO.md"

EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".ipynb_checkpoints",
}


def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def write_line(f, line: str = "") -> None:
    f.write(line + "\n")


def iter_files(root: Path) -> list[Path]:
    files = [p for p in root.rglob("*") if p.is_file() and not is_excluded(p)]
    # Avoid self-including output file while generating.
    files = [p for p in files if p.resolve() != OUT_PATH.resolve()]
    return sorted(files)


def write_header(f, files: list[Path]) -> None:
    write_line(f, "# CE310 Mega Context Dump For GPT Pro")
    write_line(f)
    write_line(f, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    write_line(f, f"Root: `{ROOT.as_posix()}`")
    write_line(f, f"Total files scanned: **{len(files)}**")
    write_line(f)
    write_line(f, "This document is intentionally very large and exhaustive.")
    write_line(f, "It includes code, notebook source, documents, tables/data files,")
    write_line(f, "image catalogs, and full-file manifest/checksums for deep downstream analysis.")
    write_line(f)


def write_repository_overview(f, files: list[Path]) -> None:
    write_line(f, "## 1. Repository File Manifest (All Files)")
    write_line(f)
    write_line(f, "| Relative Path | Size (bytes) | SHA256 |")
    write_line(f, "|---|---:|---|")
    for p in files:
        write_line(f, f"| `{rel(p)}` | {p.stat().st_size} | `{sha256_file(p)}` |")
    write_line(f)


def write_requirements_sources(f, files: list[Path]) -> None:
    write_line(f, "## 2. Requirements And Course Sources")
    write_line(f)
    src_candidates = sorted(
        [
            p
            for p in files
            if p.suffix.lower() in {".txt", ".md"}
            and (
                "coursework" in p.name.lower()
                or "requirements" in p.name.lower()
                or "lecture" in p.name.lower()
            )
        ]
    )
    for p in src_candidates:
        write_line(f, f"### `{rel(p)}`")
        write_line(f)
        content = read_text(p).rstrip()
        write_line(f, "```text")
        write_line(f, content)
        write_line(f, "```")
        write_line(f)


def write_python_code(f, files: list[Path]) -> None:
    write_line(f, "## 3. Full Python Code (`.py`)")
    write_line(f)
    py_files = [p for p in files if p.suffix.lower() == ".py"]
    for p in py_files:
        write_line(f, f"### `{rel(p)}`")
        write_line(f)
        write_line(f, "```python")
        write_line(f, read_text(p).rstrip())
        write_line(f, "```")
        write_line(f)


def summarize_outputs(cell) -> list[str]:
    out_lines: list[str] = []
    outputs = cell.get("outputs", [])
    if not outputs:
        return out_lines
    out_lines.append(f"- output_count: {len(outputs)}")
    for i, out in enumerate(outputs, 1):
        otype = out.get("output_type", "")
        out_lines.append(f"- output_{i}_type: {otype}")
        if otype == "stream":
            text = out.get("text", "")
            if isinstance(text, list):
                text = "".join(text)
            text = str(text).strip()
            if text:
                out_lines.append("  - stream_text:")
                for ln in text.splitlines()[:30]:
                    out_lines.append(f"    - {ln}")
        elif otype in {"execute_result", "display_data"}:
            data = out.get("data", {})
            if "text/plain" in data:
                txt = data["text/plain"]
                if isinstance(txt, list):
                    txt = "".join(txt)
                txt = str(txt).strip()
                if txt:
                    out_lines.append("  - text_plain:")
                    for ln in txt.splitlines()[:30]:
                        out_lines.append(f"    - {ln}")
            mime_keys = sorted(list(data.keys()))
            out_lines.append(f"  - data_keys: {', '.join(mime_keys)}")
        elif otype == "error":
            ename = out.get("ename", "")
            evalue = out.get("evalue", "")
            out_lines.append(f"  - error: {ename}: {evalue}")
    return out_lines


def write_notebooks(f, files: list[Path]) -> None:
    write_line(f, "## 4. Full Notebook Source (`.ipynb` as cells)")
    write_line(f)
    nb_files = [p for p in files if p.suffix.lower() == ".ipynb"]
    for p in nb_files:
        write_line(f, f"### Notebook: `{rel(p)}`")
        write_line(f)
        try:
            nb = nbformat.read(str(p), as_version=4)
        except Exception as e:
            write_line(f, f"- [ERROR] Could not parse notebook JSON: `{e}`")
            raw = read_text(p).strip()
            if raw:
                write_line(f)
                write_line(f, "```text")
                write_line(f, raw[:20000])
                write_line(f, "```")
            write_line(f)
            continue
        code_cells = sum(1 for c in nb.cells if c.get("cell_type") == "code")
        md_cells = sum(1 for c in nb.cells if c.get("cell_type") == "markdown")
        write_line(f, f"- total_cells: {len(nb.cells)}")
        write_line(f, f"- code_cells: {code_cells}")
        write_line(f, f"- markdown_cells: {md_cells}")
        write_line(f)
        for idx, cell in enumerate(nb.cells, 1):
            ctype = cell.get("cell_type", "unknown")
            write_line(f, f"#### Cell {idx} [{ctype}]")
            write_line(f)
            src = str(cell.get("source", "")).rstrip()
            if ctype == "markdown":
                write_line(f, src if src else "_(empty markdown)_")
            elif ctype == "code":
                write_line(f, "```python")
                write_line(f, src)
                write_line(f, "```")
                out_lines = summarize_outputs(cell)
                if out_lines:
                    write_line(f)
                    write_line(f, "**Output summary**")
                    for ln in out_lines:
                        write_line(f, ln)
            else:
                write_line(f, "```text")
                write_line(f, src)
                write_line(f, "```")
            write_line(f)


def write_markdown_docs(f, files: list[Path]) -> None:
    write_line(f, "## 5. Full Markdown Documents (`.md`)")
    write_line(f)
    md_files = [p for p in files if p.suffix.lower() == ".md"]
    for p in md_files:
        write_line(f, f"### `{rel(p)}`")
        write_line(f)
        write_line(f, "```markdown")
        write_line(f, read_text(p).rstrip())
        write_line(f, "```")
        write_line(f)


def write_text_docs(f, files: list[Path]) -> None:
    write_line(f, "## 6. Full Text Documents (`.txt`)")
    write_line(f)
    txt_files = [p for p in files if p.suffix.lower() == ".txt"]
    for p in txt_files:
        write_line(f, f"### `{rel(p)}`")
        write_line(f)
        write_line(f, "```text")
        write_line(f, read_text(p).rstrip())
        write_line(f, "```")
        write_line(f)


def write_csv_data(f, files: list[Path]) -> None:
    write_line(f, "## 7. Full CSV Data (`.csv`) - Exhaustive")
    write_line(f)
    csv_files = [p for p in files if p.suffix.lower() == ".csv"]
    for p in csv_files:
        write_line(f, f"### `{rel(p)}`")
        write_line(f)
        write_line(f, "```csv")
        write_line(f, read_text(p).rstrip())
        write_line(f, "```")
        write_line(f)


def write_json_data(f, files: list[Path]) -> None:
    write_line(f, "## 8. Full JSON Data (`.json`) - Exhaustive")
    write_line(f)
    json_files = [p for p in files if p.suffix.lower() == ".json"]
    for p in json_files:
        write_line(f, f"### `{rel(p)}`")
        write_line(f)
        write_line(f, "```json")
        write_line(f, read_text(p).rstrip())
        write_line(f, "```")
        write_line(f)


def write_docx_extracts(f, files: list[Path]) -> None:
    write_line(f, "## 9. DOCX Extracted Text (`.docx`)")
    write_line(f)
    docx_files = [p for p in files if p.suffix.lower() == ".docx"]
    if Document is None:
        write_line(f, "python-docx not available; DOCX extraction skipped.")
        write_line(f)
        return
    for p in docx_files:
        write_line(f, f"### `{rel(p)}`")
        write_line(f)
        try:
            doc = Document(str(p))
            text = "\n".join(par.text for par in doc.paragraphs if par.text.strip()).rstrip()
        except Exception as e:
            text = f"[ERROR reading DOCX: {e}]"
        write_line(f, "```text")
        write_line(f, text)
        write_line(f, "```")
        write_line(f)


def write_image_catalog(f, files: list[Path]) -> None:
    write_line(f, "## 10. Image Catalog (`.png`) - Exhaustive")
    write_line(f)
    png_files = [p for p in files if p.suffix.lower() == ".png"]
    for p in png_files:
        rp = rel(p)
        size = p.stat().st_size
        write_line(f, f"### `{rp}`")
        write_line(f)
        write_line(f, f"- size_bytes: {size}")
        write_line(f, f"- preview:")
        write_line(f, f"![{rp}]({rp})")
        write_line(f)


def write_other_binaries(f, files: list[Path]) -> None:
    write_line(f, "## 11. Other Binary Artifacts")
    write_line(f)
    text_like = {".py", ".ipynb", ".md", ".txt", ".csv", ".json", ".docx", ".png"}
    others = [p for p in files if p.suffix.lower() not in text_like]
    write_line(f, "| File | Size (bytes) | SHA256 |")
    write_line(f, "|---|---:|---|")
    for p in others:
        write_line(f, f"| `{rel(p)}` | {p.stat().st_size} | `{sha256_file(p)}` |")
    write_line(f)


def main() -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    files = iter_files(ROOT)
    with OUT_PATH.open("w", encoding="utf-8") as f:
        write_header(f, files)
        write_repository_overview(f, files)
        write_requirements_sources(f, files)
        write_python_code(f, files)
        write_notebooks(f, files)
        write_markdown_docs(f, files)
        write_text_docs(f, files)
        write_csv_data(f, files)
        write_json_data(f, files)
        write_docx_extracts(f, files)
        write_image_catalog(f, files)
        write_other_binaries(f, files)
    print(f"Wrote mega dump: {OUT_PATH}")
    print(f"Size bytes: {OUT_PATH.stat().st_size}")


if __name__ == "__main__":
    main()
