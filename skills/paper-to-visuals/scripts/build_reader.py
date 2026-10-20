#!/usr/bin/env python3
"""Package authored paper chapters as a self-contained HTML reader and Markdown."""
import argparse
import base64
import copy
import html
import json
from pathlib import Path
import re
from urllib.parse import urlsplit


IMAGE_MIMES = {".svg": "image/svg+xml", ".png": "image/png",
               ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}


def image_data(figure, base):
    path = (base / figure["path"]).resolve()
    mime = IMAGE_MIMES.get(path.suffix.lower())
    if not mime:
        raise ValueError(f"Unsupported image type: {path.name}")
    if not figure.get("alt", "").strip():
        raise ValueError(f"Missing image description: {path.name}")
    content = path.read_bytes()
    if mime == "image/svg+xml":
        source = content.decode("utf-8")
        if re.search(r"<\s*(script|foreignObject)\b", source, re.I):
            raise ValueError(f"SVG must be an image without scripts/embedded HTML: {path.name}")
        for target in re.findall(r"(?:href|src)\s*=\s*['\"]([^'\"]+)", source):
            if not target.startswith(("#", "data:")):
                raise ValueError(f"SVG depends on an external resource: {path.name}")
    return {key: value for key, value in figure.items() if key != "path"} | {
        "src": f"data:{mime};base64," + base64.b64encode(content).decode("ascii")
    }


def validate(data):
    for field in ("title", "summary", "scope"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f"Missing {field}")
    chapters = data.get("chapters")
    if not isinstance(chapters, list) or not chapters:
        raise ValueError("At least one chapter is required")
    for i, chapter in enumerate(chapters, 1):
        if chapter.get("id") != f"{i:02d}":
            raise ValueError(f"Chapter IDs must be consecutive, expected {i:02d}")
        for field in ("title", "category", "summary"):
            if not isinstance(chapter.get(field), str) or not chapter[field].strip():
                raise ValueError(f"Chapter {i:02d} missing {field}")
        if not chapter.get("explanation"):
            raise ValueError(f"Chapter {i:02d} needs a readable explanation")
        if not chapter.get("overview") and not chapter.get("status"):
            raise ValueError(f"Chapter {i:02d} needs a visual or an explicit missing-data state")
        if not chapter.get("figures") and not chapter.get("status"):
            raise ValueError(f"Chapter {i:02d} needs a detailed visual or explicit missing-data state")
        for source in chapter.get("sources", []):
            if urlsplit(source["url"]).scheme not in ("https", "http"):
                raise ValueError(f"Source must use an HTTP(S) URL: {source['url']}")


def markdown(data, html_name):
    lines = [f"# {data['title']}", "", data.get("subtitle", ""), "",
             f"阅读范围：{data['scope']}", "", f"> {data['summary']}", "", "## 章节索引", ""]
    for c in data["chapters"]:
        lines.append(f"- [{c['id']} {c['title']}]({html_name}#chapter-{c['id']})")
    for c in data["chapters"]:
        lines += ["", f"## {c['id']} {c['title']}", "", f"所属内容：{c['category']}", ""]
        for paragraph in c["explanation"]:
            lines += [paragraph, ""]
        for section in c.get("sections", []):
            lines += [f"### {section['heading']}", ""]
            for paragraph in section.get("paragraphs", []):
                lines += [paragraph, ""]
            if section.get("items"):
                lines += [f"- {item}" for item in section["items"]] + [""]
        if c.get("figures"):
            lines += [f"[查看本章详细图解]({html_name}#chapter-{c['id']})", ""]
            for f in c["figures"]:
                if f.get("caption"):
                    lines += [f"图解说明：{f['caption']}", ""]
        if c.get("sources"):
            lines += ["来源：" + "；".join(f"[{s['label']}]({s['url']})" for s in c["sources"]), ""]
    return "\n".join(lines).rstrip() + "\n"


def build(content_path, output_dir, replace=False):
    content_path = Path(content_path).resolve()
    data = json.loads(content_path.read_text(encoding="utf-8"))
    validate(data)
    html_name, md_name = "论文导览.html", "论文讲解.md"
    output_dir = Path(output_dir).resolve()
    for name in (html_name, md_name):
        if (output_dir / name).exists() and not replace:
            raise FileExistsError(f"Preserving existing output; use --replace to update: {name}")
    md = markdown(data, html_name)
    packed = copy.deepcopy(data)
    for c in packed["chapters"]:
        if c.get("overview"):
            c["overview"] = image_data(c["overview"], content_path.parent)
        c["figures"] = [image_data(f, content_path.parent) for f in c.get("figures", [])]
    packed["markdown"], packed["markdown_name"] = md, md_name
    template_path = Path(__file__).resolve().parent.parent / "assets" / "reader.html"
    template = template_path.read_text(encoding="utf-8")
    if template.count("__READER_DATA__") != 1 or template.count("__PAGE_TITLE__") != 1:
        raise ValueError("Reader template must contain one data slot and one title slot")
    serialized = json.dumps(packed, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    page = template.replace("__PAGE_TITLE__", html.escape(data["title"])).replace("__READER_DATA__", serialized)
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, content in ((html_name, page), (md_name, md)):
        target = output_dir / name
        temporary = target.with_name(target.name + ".tmp")
        temporary.write_text(content, encoding="utf-8")
        temporary.replace(target)
    return {"html": str(output_dir / html_name), "markdown": str(output_dir / md_name),
            "chapters": len(data["chapters"])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content", help="Authored chapter JSON")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--replace", action="store_true", help="Update the two generated deliverables")
    args = parser.parse_args()
    print(json.dumps(build(args.content, args.output_dir, args.replace), ensure_ascii=False))


if __name__ == "__main__":
    main()
