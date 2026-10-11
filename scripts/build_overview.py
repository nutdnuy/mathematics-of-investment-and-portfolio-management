import html
import json
import shutil
from pathlib import Path
from urllib.parse import urlparse
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'
E = html.escape
book = json.loads((ROOT / 'content.json').read_text())
library = json.loads((ROOT / 'collection.json').read_text())
assert len(library) == 10 and len({b['slug'] for b in library}) == 10
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
shutil.copytree(ROOT / 'web', OUT / 'assets')
(OUT / '.nojekyll').touch()

def layout(page, title, body):
    nav = ''.join(f'<a href="{p}"' + (' aria-current="page"' if p == page else '') + f'>{label}</a>' for p,label in [('index.html','Overview'),('topics.html','Learning themes'),('library.html','Library · 10')])
    return f'''<!doctype html>
<html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{E(title)} · Lecture Notes</title><meta name="description" content="{E(book['summary'])}"><meta name="color-scheme" content="light dark"><link rel="stylesheet" href="assets/style.css"><script src="assets/site.js" defer></script></head>
<body><a class="skip" href="#main">Skip to content</a><header><div class="top"><a class="wordmark" href="library.html">Lecture Notes <span>Quantitative finance collection</span></a><button id="theme" type="button" aria-pressed="false">Dark theme</button></div><nav aria-label="Main navigation">{nav}</nav></header>
<main id="main">{body}</main><footer><p>Book overview · เนื้อหาแนะนำเรียบเรียงสำหรับเว็บไซต์นี้</p><p lang="th">ฉบับอ่านเต็มยังอยู่ระหว่างตรวจทานและเตรียมการเผยแพร่</p><a href="https://github.com/nutdnuy/{E(book['slug'])}">Website source on GitHub</a><a href="assets/fonts/roboto-LICENSE.txt">Roboto license</a><a href="assets/fonts/noto-sans-thai-LICENSE.txt">Noto Sans Thai license</a></footer></body></html>'''

meta = f'<dl class="facts"><div><dt>Source chapters</dt><dd>{book["chapters"]}</dd></div><div><dt>Source PDF pages</dt><dd>{book["pages"]}</dd></div><div><dt>Source edition</dt><dd>{E(book["edition"])}</dd></div></dl>'
isbn = f'<p>ISBN {E(book["isbn"])}</p>' if book['isbn'] else ''
home = f'''<section class="hero"><p class="eyebrow">{E(book['subject'])}</p><p class="status">Book overview</p><h1 lang="en">{E(book['title'])}</h1><p class="thai-title">{E(book['thai'])}</p><p class="lead">{E(book['summary'])}</p><div class="actions"><a class="button primary" href="topics.html">Explore learning themes</a><a class="button" href="library.html">Browse all 10 projects</a></div>{meta}</section>
<section class="reading"><p class="eyebrow">THE LEARNING QUESTION</p><h2>{E(book['question'])}</h2><p>พื้นฐานที่ช่วยในการอ่าน: {E(book['prerequisites'])}</p></section>
<section class="source"><div><h2>About the book</h2><p>{E(book['thai'])}</p><p>ผู้เขียน: รองศาสตราจารย์ ดร.วิชัย วิทยาเกียรติเลิศ</p>{isbn}</div><div><h2>Publication status</h2><p>หน้าแนะนำและหัวข้อการเรียนรู้เปิดอ่านได้แล้ว เนื้อหาฉบับอ่านเต็มยังตรวจทานกับต้นฉบับและตรวจสิทธิ์การเผยแพร่ จึงยังไม่มีปุ่มอ่านทั้งเล่มหรือดาวน์โหลด PDF</p><p class="small">จำนวนบทและหน้าในตารางอ้างอิงจากไฟล์ต้นฉบับ ไม่ใช่จำนวนบทที่เผยแพร่บนเว็บไซต์นี้</p></div></section>'''
(OUT / 'index.html').write_text(layout('index.html',book['title'],home))

items = ''.join(f'<details class="topic" id="theme-{i}"><summary><span class="number">{i:02d}</span><span><strong lang="en">{E(t)}</strong><span class="topic-thai">{E(th)}</span></span></summary><p>{E(d)}</p></details>' for i,(t,th,d) in enumerate(book['themes'],1))
topics = f'<section class="page-head"><p class="eyebrow">LEARNING THEMES</p><h1>Questions to explore</h1><p class="lead">{E(book["thai"])}</p><p>ภาพรวมประเด็นสำหรับวางแผนการเรียน เรียบเรียงใหม่สำหรับหน้าแนะนำนี้ คลิกหัวข้อเพื่ออ่านคำถามและขอบเขตการศึกษา</p></section><section aria-label="Learning themes">{items}</section><section class="reading"><h2>Continue exploring</h2><p>ระหว่างเตรียมฉบับอ่านเต็ม สามารถเลือกเว็บไซต์ในคอลเลกชันที่เปิดเผยแพร่แล้วได้จากหน้ารวม</p><a class="button primary" href="library.html">Open the library</a></section>'
(OUT / 'topics.html').write_text(layout('topics.html','Learning themes',topics))

rows = ''.join(f'<li class="book-row" data-search="{E(b["title"]+" "+b["description"])}"><span class="number">{i:02d}</span><div><a class="book-link" href="https://nutdnuy.github.io/{E(b["slug"])}/">{E(b["title"])}</a><p>{E(b["description"])}</p></div><span class="badge">{E(b["status"])}</span></li>' for i,b in enumerate(library,1))
lib = f'<section class="page-head"><p class="eyebrow">THE COLLECTION</p><h1>Ten projects. One library.</h1><p class="lead">เจ็ดเว็บไซต์เดิม พร้อมหน้าแนะนำหนังสือใหม่อีกสามเล่ม</p><p>Existing site = เว็บไซต์เดิม · Book overview = หน้าแนะนำหนังสือที่กำลังเตรียมฉบับอ่านเต็ม</p><label for="search">Find a project</label><input id="search" type="search" placeholder="Search title or topic…" aria-describedby="result-count"><p id="result-count" class="small" aria-live="polite">10 projects</p></section><ol class="library">{rows}</ol><p id="empty" hidden>ไม่พบโปรเจ็กต์ ลองค้นหาด้วยคำอื่น</p>'
(OUT / 'library.html').write_text(layout('library.html','Library',lib))

# Validate local references against the independently built public artifact.
class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('href', 'src') and value:
                u = urlparse(value)
                if not u.scheme and u.path:
                    assert (OUT / u.path).is_file(), value
for p in OUT.glob('*.html'):
    Links().feed(p.read_text())
allowed = {'.html', '.css', '.js', '.woff2', '.txt'}
assert all(p.suffix in allowed or p.name == '.nojekyll' for p in OUT.rglob('*') if p.is_file())
assert not any(p.suffix.lower() in {'.pdf','.png','.jpg','.webp'} for p in OUT.rglob('*'))
print(f'Built 3 public overview pages for {book["slug"]}; 10 unique projects; local references valid; no PDF or transcript assets.')
