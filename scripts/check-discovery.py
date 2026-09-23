#!/usr/bin/env python3
"""Validate public discovery files and per-page metadata."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://imdennie.com/"
PAGES = [ROOT / "index.html", ROOT / "story.html", ROOT / "approach.html", ROOT / "resume.html"]
PAGES += sorted((ROOT / "case").glob("*.html"))
PAGES += sorted((ROOT / "blog").glob("*.html"))


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.refs, self.metas, self.links = set(), [], [], []
        self.title = ""
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.refs.append(attrs[key])
        if tag == "meta":
            self.metas.append(attrs)
        elif tag == "link":
            self.links.append(attrs)
        elif tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def canonical(path):
    rel = path.relative_to(ROOT).as_posix()
    return BASE + ("" if rel == "index.html" else "blog/" if rel == "blog/index.html" else rel)


def page_ids(path):
    parser = Page()
    parser.feed(path.read_text())
    return parser.ids


parsed = {}
for file in PAGES:
    page = Page()
    text = file.read_text()
    page.feed(text)
    parsed[file] = page
    expected = canonical(file)
    canonical_links = [x.get("href") for x in page.links if x.get("rel") == "canonical"]
    markdown_links = [x.get("href") for x in page.links if x.get("rel") == "alternate" and x.get("type") == "text/markdown"]
    described = [x.get("href") for x in page.links if x.get("rel") == "describedby"]
    assert canonical_links == [expected], (file, canonical_links)
    assert markdown_links == ["/" + file.relative_to(ROOT).as_posix() + ".md"], (file, markdown_links)
    assert described == ["/llms.txt"], (file, described)
    assert (ROOT / (file.relative_to(ROOT).as_posix() + ".md")).exists(), file
    meta = {x.get("property", x.get("name")): x.get("content") for x in page.metas}
    for key in ("description", "robots", "og:title", "og:description", "og:url", "og:image", "og:image:alt",
                "twitter:card", "twitter:title", "twitter:description", "twitter:image", "twitter:image:alt"):
        assert meta.get(key), (file, key)
    assert meta["og:url"] == expected, (file, meta["og:url"])
    schemas = [json.loads(x) for x in re.findall(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', text, re.S)]
    assert len(schemas) == 1, (file, len(schemas))
    graph = schemas[0].get("@graph", [])
    assert any(x.get("@id") == BASE + "#person" for x in graph), file
    assert any(x.get("@id") == expected + "#webpage" for x in graph), file
    assert text.count('rel="icon"') == 1, file
    assert text.count("gtag('config'") <= 1, file

for file, page in parsed.items():
    for ref in page.refs:
        split = urlsplit(ref)
        if split.scheme or split.netloc or ref.startswith(("data:", "mailto:")):
            continue
        target = ROOT / split.path.lstrip("/") if split.path.startswith("/") else file.parent / split.path if split.path else file
        if target.is_dir():
            target = target / "index.html"
        assert target.exists(), (file, ref)
        if split.fragment and target.suffix == ".html":
            ids = parsed[target].ids if target in parsed else page_ids(target)
            assert unquote(split.fragment) in ids, (file, ref)


sitemap = ET.parse(ROOT / "sitemap.xml")
urls = [node.text for node in sitemap.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
expected_urls = [canonical(file) for file in PAGES]
assert sorted(urls) == sorted(expected_urls), (len(urls), len(expected_urls))
assert "Sitemap: https://imdennie.com/sitemap.xml" in (ROOT / "robots.txt").read_text()
llms = (ROOT / "llms.txt").read_text()
assert "Numi is released on the App Store" in llms
assert all("/" + file.relative_to(ROOT).as_posix() + ".md" in llms for file in PAGES)
assert (ROOT / "llms-full.txt").stat().st_size > 10_000
numi = (ROOT / "case/numi.html").read_text()
expected_numi_images = [
    "simulator-meal-history.webp",
    "simulator-home.webp",
    "simulator-progress.webp",
    "simulator-fasting.webp",
]
numi_decisions = numi.split("Where the product thinking became pixels.", 1)[1].split("<!-- DESIGN SYSTEM", 1)[0]
assert re.findall(r'simulator-[^"/]+\.webp', numi_decisions) == expected_numi_images
assert "/dist/open-studio/pages.css?v=20260923-numi-screens" in numi
print(f"Discovery checks passed for {len(PAGES)} pages and {len(urls)} sitemap URLs.")
