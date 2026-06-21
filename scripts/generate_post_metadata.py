#!/usr/bin/env python3
"""Generate Hugo post summaries from article content."""

from __future__ import annotations

import argparse
import math
import re
from collections import Counter
from pathlib import Path


STOPWORDS = {
    "the",
    "and",
    "with",
    "from",
    "this",
    "that",
    "into",
    "your",
    "you",
    "are",
    "for",
    "http",
    "https",
    "com",
    "www",
    "一个",
    "一些",
    "可以",
    "这个",
    "这些",
    "因为",
    "所以",
    "如果",
    "但是",
    "就是",
    "还是",
    "没有",
    "我们",
    "他们",
    "进行",
    "使用",
    "通过",
    "问题",
    "文章",
    "原文",
    "本文",
    "介绍",
    "代码",
}


def split_front_matter(text: str) -> tuple[list[str], str]:
    text = text.lstrip()
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return [], text
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index], "\n".join(lines[index + 1 :]).strip()
    return [], text


def title_from_body(path: Path, body: str) -> str:
    for line in body.splitlines():
        match = re.match(r"^\s*#{1,3}\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return path.stem.replace("-", " ").replace("_", " ").strip().title()


def get_scalar(front: list[str], key: str, fallback: str = "") -> str:
    pattern = re.compile(rf"^\s*{re.escape(key)}\s*:\s*(.*)\s*$")
    for line in front:
        match = pattern.match(line)
        if match:
            return match.group(1).strip().strip("'\"")
    return fallback


def get_list(front: list[str], key: str) -> list[str]:
    raw = get_scalar(front, key)
    if not raw:
        return []
    if raw.startswith("[") and raw.endswith("]"):
        raw = raw[1:-1]
    return [item.strip().strip("'\"") for item in raw.split(",") if item.strip()]


def clean_inline(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"[*_#>`]+", "", text)
    text = re.sub(r"https?://\S+", "", text)
    return re.sub(r"\s+", " ", text).strip(" ，,。；;:：-")


def strip_markdown(body: str) -> str:
    body = re.sub(r"```.*?```", " ", body, flags=re.S)
    body = re.sub(r"~~~.*?~~~", " ", body, flags=re.S)
    body = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", body)
    body = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"`([^`]+)`", r"\1", body)
    body = re.sub(r"[*_]{1,3}([^*_]+)[*_]{1,3}", r"\1", body)
    body = re.sub(r"^>\s?", "", body, flags=re.M)
    body = re.sub(r"^#{1,6}\s*", "", body, flags=re.M)
    body = re.sub(r"^\s*[-*+]\s+", "", body, flags=re.M)
    body = re.sub(r"\|", " ", body)
    body = re.sub(r"https?://\S+", " ", body)
    return re.sub(r"\s+", " ", body).strip()


def extract_headings(body: str) -> list[str]:
    headings: list[str] = []
    for line in body.splitlines():
        match = re.match(r"^\s*#{2,4}\s+(.+?)\s*$", line)
        if not match:
            continue
        heading = clean_inline(match.group(1))
        if not heading or re.search(r"^(参考|reference|license|译者|原文)$", heading, re.I):
            continue
        if heading not in headings:
            headings.append(heading)
    return headings


def fit_items(items: list[str], limit: int) -> list[str]:
    selected: list[str] = []
    seen: set[str] = set()
    total = 0
    for item in items:
        item = clean_inline(item)
        key = item.lower()
        if not item or key in seen:
            continue
        projected = total + len(item) + (1 if selected else 0)
        if projected > limit:
            break
        selected.append(item)
        seen.add(key)
        total = projected
    return selected


def natural_join(items: list[str]) -> str:
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return "、".join(items[:-1]) + "和" + items[-1]


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[。！？!?；;])\s+|(?<=[。！？!?；;])|(?<=[a-zA-Z0-9][.])\s+", text)
    sentences: list[str] = []
    for part in parts:
        sentence = re.sub(r"\s+", " ", part).strip(" \t\r\n,，")
        if 18 <= len(sentence) <= 180:
            sentences.append(sentence)
    return sentences


def tokens(text: str) -> list[str]:
    latin = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{2,}", text.lower())
    chinese = re.findall(r"[\u4e00-\u9fff]{2,}", text)
    grams: list[str] = []
    for chunk in chinese:
        grams.extend(chunk[index : index + 2] for index in range(0, max(len(chunk) - 1, 0)))
        grams.extend(chunk[index : index + 3] for index in range(0, max(len(chunk) - 2, 0), 2))
    return [token for token in latin + grams if token not in STOPWORDS]


def build_summary(title: str, tags: list[str], categories: list[str], body: str) -> str:
    headings = fit_items(extract_headings(body), 46)
    if headings:
        return f"本文围绕《{title}》展开，重点梳理{natural_join(headings[:3])}等内容，提炼背景、思路与实践注意点。"

    labels = fit_items(categories + tags, 24)
    label_text = natural_join(labels)
    if label_text:
        return f"本文围绕《{title}》梳理{label_text}相关的背景、方法和实践细节，可作为排查与学习记录。"

    clean = strip_markdown(body)
    sentences = split_sentences(clean)
    if not sentences:
        return f"本文围绕《{title}》展开，梳理核心概念、实践步骤与作者在处理过程中的经验判断。"

    title_terms = set(tokens(title + " " + " ".join(tags + categories)))
    frequencies = Counter(tokens(clean))
    scored: list[tuple[float, int, str]] = []
    for index, sentence in enumerate(sentences[:80]):
        sentence_tokens = tokens(sentence)
        if not sentence_tokens:
            continue
        score = sum(math.log(frequencies[token] + 1.0) for token in sentence_tokens)
        score += 3.0 * len(title_terms.intersection(sentence_tokens))
        score += max(0.0, 4.0 - index * 0.18)
        if "总结" in sentence or "关键" in sentence or "核心" in sentence:
            score += 1.2
        if re.search(r"(原文|译者|LICENSE|welcome to star)", sentence, re.I):
            score -= 5.0
        score /= max(1.0, len(sentence_tokens) ** 0.45)
        scored.append((score, index, sentence))

    picked = [item for item in sorted(scored, reverse=True) if 24 <= len(clean_inline(item[2])) <= 96][:2]
    summary = " ".join(clean_inline(item[2]) for item in sorted(picked, key=lambda item: item[1]))
    if not summary or len(summary) > 150:
        topic = label_text or title
        return f"本文围绕《{title}》梳理{topic}相关的背景、方法和实践细节，可作为排查与学习记录。"
    return summary.rstrip("，,；;:：") + ("。" if not re.search(r"[。！？.!?]$", summary) else "")


def quote_yaml(value: str) -> str:
    value = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    return f'"{value}"'


def rewrite_front_matter(front: list[str], summary: str) -> list[str]:
    rewritten = [line for line in front if not re.match(r"^\s*summary\s*:", line)]
    insert_at = 0
    for index, line in enumerate(rewritten):
        if re.match(r"^\s*author\s*:", line):
            insert_at = index + 1
            break
        if re.match(r"^\s*title\s*:", line):
            insert_at = index + 1
    return rewritten[:insert_at] + [f"summary: {quote_yaml(summary)}"] + rewritten[insert_at:]


def process(content_dir: Path) -> tuple[int, int]:
    posts = sorted(content_dir.rglob("*.md"))
    updated = 0

    for post in posts:
        text = post.read_text(encoding="utf-8")
        front, body = split_front_matter(text)
        if not front:
            title = title_from_body(post, body)
            front = [f"title: {quote_yaml(title)}", "author: Neal"]
        else:
            title = get_scalar(front, "title", post.stem)
        tags = get_list(front, "tags")
        categories = get_list(front, "categories")
        summary = build_summary(title, tags, categories, body)
        new_front = rewrite_front_matter(front, summary)
        new_text = "---\n" + "\n".join(new_front).rstrip() + "\n---\n\n" + body.strip() + "\n"
        if new_text != text:
            post.write_text(new_text, encoding="utf-8")
            updated += 1

    return updated, len(posts)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-dir", default="content", type=Path)
    args = parser.parse_args()
    updated, posts = process(args.content_dir)
    print(f"Updated {updated} posts with generated summaries out of {posts}.")


if __name__ == "__main__":
    main()
