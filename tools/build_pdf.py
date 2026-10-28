#!/usr/bin/env python3
"""
Render a branded LoopFound guide PDF from a carousel folder's guide.json.

Adapted from build_pdfs.py in github.com/piyushxt43/posts- (layout code only):
same cover, numbered section tabs, callouts and panels, restyled to the
LoopFound palette and driven by JSON instead of a Python content file.

    python tools/build_pdf.py carousels/2026-10-29-reviews-ai-reads

guide.json keys: title, kicker, subtitle, intro, callout {title, text},
sections [{title, body [..], bullets [[lead, text]..]}], playbook [..],
mistakes [..], sources [[label, url]..]; optional faq [[q, a]..], filename.
The keyword comes from the folder's brief.md ("Keyword: WORD").
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

HANDLE = "@teamloopfound"

# ---- Brand palette (style/style-dna.md) -----------------------------------
PAPER = HexColor("#F4F1EA")
CARD = HexColor("#FBFAF6")
INK = HexColor("#1A1A1A")
MUTED = HexColor("#5E5B55")
ORANGE = HexColor("#FF5A1F")
ORANGE_SOFT = HexColor("#FFE3D6")
LINE = HexColor("#D9D4C8")

PAGE_W, PAGE_H = letter
MARGIN = 0.72 * inch
CONTENT_W = PAGE_W - 2 * MARGIN

# ---- Paragraph styles ------------------------------------------------------
STY_INTRO = ParagraphStyle("intro", fontName="Helvetica", fontSize=11.5, leading=17, textColor=INK, spaceAfter=4)
STY_BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=10.5, leading=15.5, textColor=INK, spaceAfter=6)
STY_BULLET = ParagraphStyle("bullet", fontName="Helvetica", fontSize=10.5, leading=15, textColor=INK)
STY_PANEL_TITLE = ParagraphStyle("ptitle", fontName="Helvetica-Bold", fontSize=12.5, leading=15, textColor=INK)
STY_PANEL_ITEM = ParagraphStyle("pitem", fontName="Helvetica", fontSize=10, leading=14.5, textColor=INK,
                                leftIndent=18, firstLineIndent=-18, spaceBefore=2, spaceAfter=2)
STY_CALLOUT_TITLE = ParagraphStyle("ctitle", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=ORANGE)
STY_CALLOUT = ParagraphStyle("callout", fontName="Helvetica", fontSize=10.5, leading=15.5, textColor=INK)
STY_SOURCE = ParagraphStyle("source", fontName="Helvetica", fontSize=9, leading=13, textColor=MUTED)
STY_EYEBROW = ParagraphStyle("eyebrow", fontName="Helvetica-Bold", fontSize=10.5, leading=13, textColor=ORANGE,
                             spaceAfter=10)


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap_words(text: str, max_chars: int) -> list[str]:
    lines, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---- Page painters -----------------------------------------------------------
def paint_background(canvas):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canvas.restoreState()


def make_footer(cta: str):
    def on_content_page(canvas, doc):
        paint_background(canvas)
        canvas.saveState()
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.8)
        canvas.line(MARGIN, 0.55 * inch, PAGE_W - MARGIN, 0.55 * inch)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica-Bold", 8.5)
        canvas.drawString(MARGIN, 0.4 * inch, HANDLE)
        canvas.drawCentredString(PAGE_W / 2, 0.4 * inch, str(doc.page))
        canvas.setFont("Helvetica", 8.5)
        canvas.drawRightString(PAGE_W - MARGIN, 0.4 * inch, cta)
        canvas.restoreState()
    return on_content_page


# ---- Flowables -----------------------------------------------------------------
class SectionHeader(Flowable):
    """An orange numbered tab + heading + underline rule."""

    def __init__(self, number: str, title: str):
        super().__init__()
        self.number, self.title = number, title
        self.width, self.height = CONTENT_W, 30

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return availWidth, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(ORANGE)
        c.roundRect(0, 6, 26, 20, 4, stroke=0, fill=1)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(13, 11.5, self.number)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 15)
        c.drawString(38, 11, self.title)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.8)
        c.line(0, 1, self.width, 1)


class Cover(Flowable):
    def __init__(self, kicker: str, title: str, subtitle: str, cta: str):
        super().__init__()
        self.kicker, self.title, self.subtitle, self.cta = kicker, title, subtitle, cta

    def wrap(self, availWidth, availHeight):
        return availWidth, availHeight

    def draw(self):
        c = self.canv
        c.saveState()
        c.translate(-MARGIN, -0.75 * inch)
        left = MARGIN
        c.setFont("Helvetica-Bold", 10)
        tab_w = c.stringWidth(self.kicker, "Helvetica-Bold", 10) + 20
        c.setFillColor(ORANGE)
        c.roundRect(left, PAGE_H - 1.45 * inch, tab_w, 22, 5, stroke=0, fill=1)
        c.setFillColor(white)
        c.drawString(left + 10, PAGE_H - 1.45 * inch + 7, self.kicker)

        y = PAGE_H - 2.5 * inch
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 40)
        for ln in wrap_words(self.title, 17):
            c.drawString(left, y, ln)
            y -= 44
        c.setFillColor(ORANGE)
        c.rect(left, y + 18, 2.2 * inch, 6, stroke=0, fill=1)
        y -= 18
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 13.5)
        for ln in wrap_words(self.subtitle, 56):
            c.drawString(left, y, ln)
            y -= 19

        c.setStrokeColor(LINE)
        c.setLineWidth(0.8)
        c.line(left, 1.25 * inch, PAGE_W - MARGIN, 1.25 * inch)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left, 0.95 * inch, HANDLE)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 10)
        c.drawString(left, 0.78 * inch, "get found online  -  " + self.cta)
        c.restoreState()


def bullets_table(bullets) -> Table:
    rows = [[Paragraph('<font color="#FF5A1F">&#9632;</font>', STY_BULLET),
             Paragraph(f"<b>{esc(lead)}.</b> {esc(text)}", STY_BULLET)] for lead, text in bullets]
    t = Table(rows, colWidths=[16, CONTENT_W - 16])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def callout_box(title: str, text: str) -> Table:
    t = Table([[Paragraph(esc(title).upper(), STY_CALLOUT_TITLE)], [Paragraph(esc(text), STY_CALLOUT)]],
              colWidths=[CONTENT_W - 24])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ORANGE_SOFT),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (0, 0), 12),
        ("BOTTOMPADDING", (0, 0), (0, 0), 2),
        ("TOPPADDING", (0, 1), (0, 1), 0),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 12),
        ("LINEBEFORE", (0, 0), (0, -1), 3, ORANGE),
    ]))
    return t


def panel(title: str, items, marker) -> Table:
    rows = [[Paragraph(esc(title).upper(), STY_PANEL_TITLE)]]
    for i, item in enumerate(items, start=1):
        rows.append([Paragraph(f'<font color="#FF5A1F"><b>{marker(i)}</b></font>&nbsp;&nbsp;{esc(item)}',
                               STY_PANEL_ITEM)])
    t = Table(rows, colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CARD),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
        ("TOPPADDING", (0, 1), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 2),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 12),
        ("LINEABOVE", (0, 0), (-1, 0), 2, ORANGE),
        ("BOX", (0, 0), (-1, -1), 0.8, LINE),
    ]))
    return t


def faq_table(items) -> Table:
    rows = [[Paragraph(f"<b>{esc(q)}</b><br/>{esc(a)}", STY_BODY)] for q, a in items]
    t = Table(rows, colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, LINE),
    ]))
    return t


# ---- Build -----------------------------------------------------------------------
def read_keyword(folder: Path) -> str:
    brief = folder / "brief.md"
    m = re.search(r"^Keyword:\s*(\S+)", brief.read_text(encoding="utf-8"), re.M) if brief.exists() else None
    if not m:
        raise SystemExit(f"No 'Keyword: WORD' line in {brief}")
    return m.group(1).upper()


def build_pdf(folder: Path) -> Path:
    data = json.loads((folder / "guide.json").read_text(encoding="utf-8"))
    keyword = read_keyword(folder)
    cta = f"Comment {keyword} for a free website consultation"
    out = folder / data.get("filename", "guide.pdf")

    doc = BaseDocTemplate(str(out), pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN,
                          topMargin=MARGIN, bottomMargin=0.75 * inch, title=data["title"], author=HANDLE)
    frame = Frame(MARGIN, 0.75 * inch, CONTENT_W, PAGE_H - MARGIN - 0.75 * inch, id="main")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame], onPage=lambda c, d: paint_background(c)),
        PageTemplate(id="content", frames=[frame], onPage=make_footer(cta)),
    ])

    story = [NextPageTemplate("content"), Cover(data["kicker"], data["title"], data["subtitle"], cta), PageBreak()]

    story += [Paragraph("THE BIG IDEA", STY_EYEBROW), Paragraph(esc(data["intro"]), STY_INTRO), Spacer(1, 10),
              callout_box(data["callout"]["title"], data["callout"]["text"]), Spacer(1, 18)]

    for i, sec in enumerate(data["sections"], start=1):
        story += [SectionHeader(str(i), sec["title"]), Spacer(1, 8)]
        story += [Paragraph(esc(p), STY_BODY) for p in sec.get("body", [])]
        if sec.get("bullets"):
            story += [Spacer(1, 2), bullets_table(sec["bullets"])]
        story.append(Spacer(1, 14))

    story += [PageBreak(), Paragraph("DO IT THIS WEEK", STY_EYEBROW),
              panel("Your checklist", data["playbook"], lambda i: f"{i}."), Spacer(1, 14),
              panel("Mistakes to avoid", data["mistakes"], lambda i: "&#10007;"), Spacer(1, 14)]

    if data.get("faq"):
        story += [Paragraph("QUESTIONS OWNERS ASK", STY_EYEBROW), faq_table(data["faq"]), Spacer(1, 14)]

    story += [callout_box("Want a website that brings in customers?",
                          f"Comment {keyword} on the post and we'll set up a free website consultation. "
                          f"Follow {HANDLE} for more plain-English tips.")]

    if data.get("sources"):
        story += [Spacer(1, 18), Paragraph("SOURCES", STY_EYEBROW)]
        story += [Paragraph(f'{esc(label)}: <link href="{esc(url)}">{esc(url)}</link>', STY_SOURCE)
                  for label, url in data["sources"]]

    doc.build(story)
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    folder = Path(sys.argv[1]).resolve()
    out = build_pdf(folder)
    print(f"OK  {out} ({out.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
