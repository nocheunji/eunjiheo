#!/usr/bin/env python3
"""
포트폴리오 사이트 빌더 (추가 설치 필요 없음, 파이썬 표준 라이브러리만 사용)

  python3 build.py           → _site/ 폴더에 사이트 생성
  python3 build.py --serve   → 생성 후 http://localhost:8000 에서 미리보기

  works/<폴더>/info.md  → 작품 페이지   /works/<폴더>/
  pages/<이름>.md       → 일반 페이지   /<이름>/   (About, Contact 등. 왼쪽 목록 위쪽에 표시)
  site.md               → 이름, SNS 등 사이트 전체 설정
작성 규칙은 AGENTS.md 를 참고하세요.
"""
import html
import hashlib
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKS = ROOT / "works"
OUT = ROOT / "_site"

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif"}
VIDEO_EXT = {".mp4", ".webm", ".mov"}
CSS_VERSION = hashlib.sha256((ROOT / "assets" / "style.css").read_bytes()).hexdigest()[:12]


# ---------- 파싱 ----------

def parse_front_matter(text):
    """'---' 사이의 key: value 를 읽고, (정보 dict, 본문) 을 돌려준다."""
    meta, body = {}, text
    m = re.match(r"^﻿?---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.strip().startswith("#"):
                k, v = line.split(":", 1)
                v = v.strip().strip('"').strip("'")
                meta[k.strip().lower()] = v
        body = m.group(2)
    return meta, body


def inline(text):
    """텍스트 한 덩어리를 HTML로: 이스케이프, **굵게**, [링크](url), 자동 링크, 줄바꿈."""
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
               r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    t = re.sub(r'(?<!href=")(?<!">)(https?://[^\s<]+)',
               r'<a href="\1" target="_blank" rel="noopener">\1</a>', t)
    return t.replace("\n", "<br>\n")


def youtube_id(v):
    m = re.search(r"(?:youtu\.be/|v=|embed/|shorts/)([\w-]{6,})", v)
    return m.group(1) if m else v.strip()


def vimeo_id(v):
    m = re.search(r"(\d{5,})", v)
    return m.group(1) if m else v.strip()


def render_block(block, folder):
    """본문의 한 덩어리(빈 줄로 구분)를 사진/영상/텍스트 중 하나로 변환."""
    s = block.strip()
    low = s.lower()

    # 사진: ![설명](파일) 또는 파일 이름만
    m = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", s)
    if m or (Path(s).suffix.lower() in IMAGE_EXT and "\n" not in s and " " not in s):
        alt, src = (m.group(1), m.group(2)) if m else ("", s)
        if Path(src).suffix.lower() in VIDEO_EXT:
            return render_block(src, folder)
        check_file(folder, src)
        return (f'<figure class="b-img"><img src="{html.escape(src)}" '
                f'alt="{html.escape(alt)}" loading="lazy"></figure>')

    # 유튜브 / 비메오
    if low.startswith("youtube:"):
        vid = youtube_id(s.split(":", 1)[1])
        return ('<div class="b-video"><iframe src="https://www.youtube-nocookie.com/embed/'
                f'{html.escape(vid)}" title="YouTube video" allow="autoplay; encrypted-media; '
                'picture-in-picture; fullscreen" allowfullscreen loading="lazy"></iframe></div>')
    if low.startswith("vimeo:"):
        vid = vimeo_id(s.split(":", 1)[1])
        return (f'<div class="b-video"><iframe src="https://player.vimeo.com/video/{html.escape(vid)}" '
                'title="Vimeo video" allow="autoplay; fullscreen; picture-in-picture" '
                'allowfullscreen loading="lazy"></iframe></div>')

    # 영상 파일: video: 파일.mp4  또는 파일.mp4  (loop: 를 쓰면 소리 없이 자동 반복)
    m = re.fullmatch(r"(?:(video|loop):\s*)?(\S+)", s, re.I)
    if m and Path(m.group(2)).suffix.lower() in VIDEO_EXT:
        src = m.group(2)
        check_file(folder, src)
        if (m.group(1) or "").lower() == "loop":
            return (f'<figure class="b-img"><video src="{html.escape(src)}" autoplay muted loop '
                    'playsinline preload="metadata"></video></figure>')
        return (f'<figure class="b-img"><video src="{html.escape(src)}" controls playsinline '
                'preload="metadata"></video></figure>')

    # 그 외는 텍스트
    return f'<p class="b-text">{inline(s)}</p>'


WARNINGS = []


def check_file(folder, src):
    if not src.startswith("http") and not (folder / src).exists():
        WARNINGS.append(f"  ! {folder.name}/info.md : '{src}' 파일이 폴더에 없어요")


def load_works():
    works = []
    if not WORKS.exists():
        return works
    for folder in sorted(p for p in WORKS.iterdir() if p.is_dir()):
        info = folder / "info.md"
        if not info.exists():
            WARNINGS.append(f"  ! works/{folder.name} 에 info.md 가 없어서 건너뜀")
            continue
        meta, body = parse_front_matter(info.read_text(encoding="utf-8"))
        if meta.get("hidden", "").lower() in ("true", "yes", "1"):
            continue
        images = sorted(f.name for f in folder.iterdir() if f.suffix.lower() in IMAGE_EXT)
        thumb = meta.get("thumbnail") or next(
            (n for n in images if n.lower().startswith("thumb")), images[0] if images else "")
        if thumb:
            check_file(folder, thumb)
        blocks = [b for b in re.split(r"\n\s*\n", body.strip()) if b.strip()]
        works.append({
            "slug": folder.name,
            "folder": folder,
            "title": meta.get("title") or folder.name.replace("-", " "),
            "meta": " · ".join(x for x in (meta.get("category", ""), meta.get("year", "")) if x),
            "date": meta.get("date") or meta.get("year", ""),
            "order": float(meta["order"]) if re.fullmatch(r"-?\d+(\.\d+)?", meta.get("order", "")) else None,
            "thumb": thumb,
            "html": "\n".join(render_block(b, folder) for b in blocks),
        })
    # order 가 있으면 작은 숫자가 먼저, 없으면 날짜 최신순
    works.sort(key=lambda w: w["date"], reverse=True)
    works.sort(key=lambda w: (w["order"] is None, w["order"] or 0))
    return works


# ---------- 화면 ----------

def page(site, works, current, root, title, main, body_class):
    name = html.escape(site.get("name", "Portfolio"))
    items = "\n".join(
        f'<li><a href="{root}works/{w["slug"]}/"{" aria-current=page" if w["slug"] == current else ""}>'
        f'{html.escape(w["title"])}</a></li>' for w in works)
    page_items = "\n".join(
        f'<li><a href="{root}{p["slug"]}/" class="muted"{" aria-current=page" if "page:" + p["slug"] == current else ""}>'
        f'{html.escape(p["title"])}</a></li>' for p in PAGES if p["menu"])
    extra = []
    if site.get("email"):
        extra.append(f'<li><a href="mailto:{html.escape(site["email"])}">Contact</a></li>')
    work_group = (
        '<li class="work-group"><details class="works-index" open>'
        '<summary>Works</summary>'
        f'<ul class="work-list">{items}</ul>'
        '</details></li>'
    ) if items else ""
    desc = html.escape(site.get("description", name))
    og = f'<meta property="og:image" content="{site["url"].rstrip("/")}/{current_thumb(works, current)}">' \
        if site.get("url") and current_thumb(works, current) else ""
    return f"""<!doctype html>
<html lang="{html.escape(site.get('lang', 'ko'))}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{desc}">
{og}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/style.css?v={CSS_VERSION}">
</head>
<body class="{body_class}">
<div class="wrap">
  <aside class="side">
    <a class="name" href="{root}">{name}</a>
    <details class="index" open>
      <summary>Index</summary>
      <ul class="list">
        {page_items}
        {work_group}
        {"".join(extra)}
      </ul>
    </details>
  </aside>
  <main class="main">
{main}
  </main>
</div>
<script>
  // 모바일에서는 목록을 접어서 시작
  if (matchMedia('(max-width: 760px)').matches) document.querySelector('.index').removeAttribute('open');
</script>
</body>
</html>
"""


def current_thumb(works, slug):
    for w in works:
        if w["slug"] == slug and w["thumb"]:
            return f'works/{w["slug"]}/{w["thumb"]}'
    return works[0]["thumb"] and f'works/{works[0]["slug"]}/{works[0]["thumb"]}' if works else ""


def grid(works, root):
    cards = []
    for w in works:
        img = (f'<img src="{root}works/{w["slug"]}/{html.escape(w["thumb"])}" alt="" loading="lazy">'
               if w["thumb"] else '<span class="noimg"></span>')
        cards.append(f'<a class="card" href="{root}works/{w["slug"]}/">'
                     f'<div class="thumb">{img}</div>'
                     f'<div class="cap">{html.escape(w["title"])}</div></a>')
    return '<div class="grid">\n' + "\n".join(cards) + "\n</div>"


PAGES = []
RESERVED = {"works", "assets", "404"}  # 이 이름들은 페이지 주소로 쓸 수 없음


def load_pages():
    """pages/<slug>.md 하나 = 페이지 하나. 같은 이름의 폴더(pages/<slug>/)가 있으면 그 안 파일을 함께 복사."""
    pages = []
    folder = ROOT / "pages"
    if not folder.exists():
        return pages
    for f in sorted(folder.glob("*.md")):
        slug = f.stem
        if slug in RESERVED:
            WARNINGS.append(f"  ! pages/{f.name} : '{slug}' 는 쓸 수 없는 이름이에요")
            continue
        meta, body = parse_front_matter(f.read_text(encoding="utf-8"))
        if meta.get("hidden", "").lower() in ("true", "yes", "1"):
            continue
        assets = folder / slug
        blocks = [b for b in re.split(r"\n\s*\n", body.strip()) if b.strip()]
        pages.append({
            "slug": slug,
            "title": meta.get("title") or slug.replace("-", " ").title(),
            "order": float(meta["order"]) if re.fullmatch(r"-?\d+(\.\d+)?", meta.get("order", "")) else 99,
            "menu": meta.get("menu", "true").lower() not in ("false", "no", "0"),
            "assets": assets,
            "html": "\n".join(render_block(b, assets) for b in blocks),
        })
    pages.sort(key=lambda p: (p["order"], p["slug"]))
    return pages


def build():
    site_meta, _ = parse_front_matter((ROOT / "site.md").read_text(encoding="utf-8"))
    PAGES[:] = load_pages()
    works = load_works()
    name = site_meta.get("name", "Portfolio")

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")
    (OUT / ".nojekyll").write_text("")

    # 메인
    (OUT / "index.html").write_text(
        page(site_meta, works, "", "", name, grid(works, ""), "home"), encoding="utf-8")

    # 일반 페이지 (pages/*.md → /<파일이름>/)
    for p in PAGES:
        dest = OUT / p["slug"]
        dest.mkdir(parents=True, exist_ok=True)
        if p["assets"].exists():
            shutil.copytree(p["assets"], dest, dirs_exist_ok=True)
        (dest / "index.html").write_text(
            page(site_meta, works, "page:" + p["slug"], "../", f'{p["title"]} — {name}',
                 f'<article class="work">\n<h1 class="title">{html.escape(p["title"])}</h1>\n{p["html"]}\n</article>',
                 "about"),
            encoding="utf-8")

    # 작품 페이지
    for i, w in enumerate(works):
        dest = OUT / "works" / w["slug"]
        shutil.copytree(w["folder"], dest, ignore=shutil.ignore_patterns("info.md", ".*"))
        prev_w = works[i - 1] if i > 0 else None
        next_w = works[i + 1] if i < len(works) - 1 else None
        nav = '<nav class="pager">'
        nav += f'<a href="../{prev_w["slug"]}/">← {html.escape(prev_w["title"])}</a>' if prev_w else "<span></span>"
        nav += '<a href="../../">Index</a>'
        nav += f'<a href="../{next_w["slug"]}/">{html.escape(next_w["title"])} →</a>' if next_w else "<span></span>"
        nav += "</nav>"
        meta = f'<p class="meta">{html.escape(w["meta"])}</p>' if w["meta"] else ""
        main = (f'<article class="work">\n<h1 class="title">{html.escape(w["title"])}</h1>\n{meta}\n'
                f'{w["html"]}\n</article>\n{nav}\n'
                f'<div class="more">{grid([x for x in works if x is not w], "../../")}</div>')
        (dest / "index.html").write_text(
            page(site_meta, works, w["slug"], "../../", f'{w["title"]} — {name}', main, "detail"),
            encoding="utf-8")

    # 404 (어느 주소에서든 열리므로 site.md 의 url 경로를 기준으로 링크)
    from urllib.parse import urlparse
    root404 = (urlparse(site_meta.get("url", "")).path.rstrip("/") + "/") if site_meta.get("url") else "/"
    (OUT / "404.html").write_text(
        page(site_meta, works, "", root404, f"Not found — {name}",
             '<article class="work"><h1 class="title">페이지를 찾을 수 없어요</h1></article>', "about"),
        encoding="utf-8")

    print(f"완료: 작품 {len(works)}개, 페이지 {len(PAGES)}개 → _site/")
    for w in WARNINGS:
        print(w)
    return 1 if WARNINGS and "--strict" in sys.argv else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # 윈도우 터미널 한글 깨짐 방지
    except Exception:
        pass
    code = build()
    if "--serve" in sys.argv:
        import functools
        import http.server
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
        print("미리보기: http://localhost:8000  (끄려면 Ctrl+C)")
        http.server.ThreadingHTTPServer(("", 8000), handler).serve_forever()
    sys.exit(code)
