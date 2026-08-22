#!/usr/bin/env python3
"""Build a tagged, PDF/UA-1 accessible PDF from the Word syllabus.

    python3 _internal/build-syllabus-pdf.py

Reads PUBH-115-Syllabus-Fall-2026.docx, converts it to accessible HTML with
pandoc (bundled with Quarto), and renders that to PDF with WeasyPrint.

The Word file is already structured for accessibility - real heading styles, a
Title paragraph, table captions and table descriptions - so this script's job is
to carry that structure through to the PDF's tag tree rather than to invent it.

Requirements:
  - quarto (for its bundled pandoc)
  - weasyprint, installed against a Python that can load the system libpango.
    Anaconda's Python cannot: its bundled libglib is older than the system
    pango and dlopen fails on g_once_init_leave_pointer. Use /usr/bin/python3:
      /usr/bin/python3 -m pip install --target=<dir> weasyprint pypdf
      PYTHONPATH=<dir> /usr/bin/python3 _internal/build-syllabus-pdf.py
  - pypdf, optional: it powers the accessibility checks printed after the
    render. Without it the PDF still builds, unverified.
"""

import collections
import html
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
DOCX = HERE / "PUBH-115-Syllabus-Fall-2026.docx"
PDF = HERE / "PUBH-115-Syllabus-Fall-2026.pdf"
HTML_OUT = HERE / "PUBH-115-Syllabus-Fall-2026.html"

# Metadata, matching docProps/core.xml in the Word file.
DOC_TITLE = "PUBH 115 Introduction to Environmental Health and Safety - Syllabus, Fall 2026"
H1 = "PUBH 115: Introduction to Environmental Health and Safety"
SUBTITLE = "Course Syllabus &#124; Fall 2026 &#124; California State University, Fullerton"
AUTHOR = "Jason A. Smith"
DESCRIPTION = (
    "Accessible course syllabus for PUBH 115, Introduction to Environmental Health and "
    "Safety, Fall 2026, California State University, Fullerton. Prepared in accordance "
    "with CSUF University Policy Statement 300.004, Policy on Syllabi."
)
KEYWORDS = "PUBH 115, syllabus, Fall 2026, environmental health, CSUF"

# w:tblCaption values from the Word file, in document order. Pandoc concatenates
# each one with its w:tblDescription; these let us split them apart again.
CAPTIONS = [
    "Course Information",
    "Instructor Information",
    "Course Calendar, Fall 2026",
    "Assignments, Due Dates, and Weights",
    "Grade Breakdown",
]
TABLE_CLASSES = ["kv", "kv", "calendar", "assignments", "kv"]

CSS = """
@page {
  size: Letter;
  margin: 20mm 18mm 18mm 18mm;
  @top-left { content: "PUBH 115 Syllabus — Fall 2026"; font-size: 8.5pt; color: #444; }
  @bottom-right { content: "Page " counter(page) " of " counter(pages); font-size: 8.5pt; color: #444; }
}
@page :first { @top-left { content: none; } }

html { font-family: "DejaVu Sans", "Ubuntu Sans", sans-serif; font-size: 11pt; line-height: 1.5; color: #14171c; }
body { margin: 0; hyphens: none; }

h1, h2, h3 { font-weight: bold; line-height: 1.25; break-after: avoid; }
h1 { font-size: 21pt; margin: 0 0 0.15em; color: #0b2a4a; }
h2 { font-size: 15pt; margin: 1.5em 0 0.45em; color: #0b2a4a;
     border-bottom: 1.5pt solid #0b2a4a; padding-bottom: 0.15em; }
h3 { font-size: 12pt; margin: 1.15em 0 0.3em; color: #22405e; }
p, li { orphans: 2; widows: 2; }
p { margin: 0 0 0.7em; }
ul, ol { margin: 0 0 0.8em; padding-left: 1.35em; }
li { margin-bottom: 0.35em; }
strong { font-weight: bold; }
em { font-style: italic; }

a { color: #0b3f7a; text-decoration: underline; }

.docheader { border-bottom: 3pt solid #0b2a4a; padding-bottom: 0.7em; margin-bottom: 1.2em; }
.subtitle { font-size: 12pt; color: #33445a; margin: 0; }

.toc { break-after: page; }
.toc h2 { margin-top: 0.6em; }
.toc ul { list-style: none; padding-left: 0; }
/* The page number is a flex sibling and the rule is a border, so neither adds
   text a screen reader has to wade through. A leader(". ") would: it emits one
   marked-content span per dot pair, ~600 of them across this contents list.
   The rule is solid, not dotted: WeasyPrint draws a dotted border as one path
   per dot, which cost 2.4MB of page-one content stream. */
.toc li { border-bottom: 0.5pt solid #c3ccd8; margin-bottom: 0.35em; padding-bottom: 0.2em; }
.toc a { display: flex; justify-content: space-between; gap: 1.5em;
         text-decoration: none; color: #14171c; }
.toc a::after { content: target-counter(attr(href), page); color: #444; }

table { border-collapse: collapse; width: 100%; margin: 0.4em 0 1.3em; font-size: 10pt; }
caption { caption-side: top; text-align: left; margin-bottom: 0.4em; break-after: avoid; }
.cap-title { display: block; font-weight: bold; font-size: 10.5pt; color: #0b2a4a; }
.cap-desc { display: block; font-size: 8.5pt; color: #4a5568; line-height: 1.35; margin-top: 0.15em; }
th, td { border: 0.75pt solid #6b7684; padding: 5pt 7pt; text-align: left; vertical-align: top; }
thead th { background: #dfe6ee; color: #14171c; font-weight: bold; }
tbody th { background: #f2f5f8; font-weight: bold; }
tr { break-inside: avoid; }
thead { display: table-header-group; }
.keep { break-inside: avoid; }

table.kv th[scope="row"] { width: 27%; }
table.calendar th[scope="row"] { width: 7%; }
table.calendar td:nth-of-type(1) { width: 15%; }
table.calendar td:nth-of-type(3) { width: 26%; }
table.assignments th[scope="row"] { width: 27%; }
table.assignments td:nth-of-type(3) { width: 14%; }
"""

# WeasyPrint 69 raises "Table wrapper without a table" while building the tag
# tree if a table's caption lands at the bottom of a page and the table body
# moves to the next. Wrapping the short tables in .keep prevents that for them;
# the calendar is too long to keep whole, so if the crash shows up we retry with
# the calendar forced onto a fresh page. That wastes part of a page, hence the
# retry rather than doing it unconditionally.
CALENDAR_PAGE_BREAK = "table.calendar { break-before: page; }"


def to_html_fragment():
    result = subprocess.run(
        ["quarto", "pandoc", "-f", "docx", "-t", "html5", "--wrap=none", str(DOCX)],
        capture_output=True, text=True, check=True,
    )
    return result.stdout


def build_html(body):
    # Drop the plain-bold subtitle paragraph; it is re-added as a styled header.
    body = re.sub(
        r'^<p><strong>Course Syllabus \| Fall 2026 \| '
        r'California State University, Fullerton</strong></p>\n',
        '', body, count=1)

    # Demote headings by one level so the document has exactly one h1.
    body = re.sub(r'<(/?)h2(\s|>)', r'<\1h3\2', body)
    body = re.sub(r'<(/?)h1(\s|>)', r'<\1h2\2', body)

    # Drop pandoc's pixel-derived column widths; the CSS above handles layout.
    body = re.sub(r'<colgroup>.*?</colgroup>\n?', '', body, flags=re.S)
    body = body.replace('<table style="width:100%;">', '<table>')

    # <u> carries no meaning; links are underlined via CSS instead.
    body = body.replace('<u>', '').replace('</u>', '')

    # Column headers get scope; bold markup inside a th is redundant.
    def fix_thead(match):
        inner = re.sub(r'<th><strong>(.*?)</strong></th>', r'<th scope="col">\1</th>', match.group(1))
        return '<thead>' + inner.replace('<th>', '<th scope="col">') + '</thead>'
    body = re.sub(r'<thead>(.*?)</thead>', fix_thead, body, flags=re.S)

    # Split the merged caption + table description into two lines.
    def fix_caption(match):
        text = match.group(1)
        for number, caption in enumerate(CAPTIONS, start=1):
            if text.startswith(caption):
                return ('<caption><span class="cap-title">Table %d. %s</span>'
                        '<span class="cap-desc">%s</span></caption>'
                        % (number, caption, text[len(caption):].strip()))
        raise SystemExit('Unrecognised table caption: %r' % text[:80])
    body = re.sub(r'<caption>(.*?)</caption>', fix_caption, body, flags=re.S)

    # First cell of every body row becomes a row header.
    tables = list(re.finditer(r'<table>.*?</table>', body, flags=re.S))
    if len(tables) != len(TABLE_CLASSES):
        raise SystemExit('Expected %d tables, found %d' % (len(TABLE_CLASSES), len(tables)))
    for index, match in reversed(list(enumerate(tables))):
        def row_header(row):
            return re.sub(r'<td>(.*?)</td>', r'<th scope="row">\1</th>',
                          row.group(0), count=1, flags=re.S)
        table = re.sub(r'<tr>.*?</tr>', row_header, match.group(0), flags=re.S)
        table = table.replace('<table>', '<table class="%s">' % TABLE_CLASSES[index], 1)
        if TABLE_CLASSES[index] != 'calendar':
            table = '<div class="keep">%s</div>' % table
        body = body[:match.start()] + table + body[match.end():]

    # Contents list, built from the top-level sections.
    entries = ['<li><a href="#%s">%s</a></li>' % (m.group(1), m.group(2).strip())
               for m in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', body, flags=re.S)]
    toc = ('<nav class="toc" aria-labelledby="toc-heading" role="doc-toc">\n'
           '<h2 id="toc-heading">Contents</h2>\n<ul>\n' + "\n".join(entries) + '\n</ul>\n</nav>')

    return """<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="author" content="{author}">
<meta name="description" content="{description}">
<meta name="keywords" content="{keywords}">
<meta name="dcterms.language" content="en-US">
<style>{css}</style>
</head>
<body>
<header class="docheader">
<h1>{h1}</h1>
<p class="subtitle">{subtitle}</p>
</header>
{toc}
<main>
{body}
</main>
</body>
</html>
""".format(title=html.escape(DOC_TITLE), author=html.escape(AUTHOR),
           description=html.escape(DESCRIPTION), keywords=html.escape(KEYWORDS),
           css=CSS, h1=html.escape(H1), subtitle=SUBTITLE, toc=toc, body=body)


def verify(path):
    """Re-open the finished PDF and check the accessibility claims it makes.

    Automated checks catch the mechanical half of PDF/UA - tagging, metadata,
    reading order plumbing, table header association. Judgement calls (are the
    table descriptions accurate? is the reading order the order a reader wants?)
    still need a human or a tool like PAC.
    """
    try:
        from pypdf import PdfReader
        from pypdf.generic import IndirectObject
    except ImportError:
        print('pypdf not installed; skipping verification.', file=sys.stderr)
        return

    reader = PdfReader(str(path))
    catalog = reader.trailer['/Root']
    results = []

    def check(label, ok, detail=''):
        results.append((ok, label, detail))

    check('Tagged (MarkInfo /Marked true)',
          bool(catalog.get('/MarkInfo', {}).get('/Marked')))
    check('Structure tree present', '/StructTreeRoot' in catalog)
    check('Document language set', catalog.get('/Lang') == 'en-US',
          str(catalog.get('/Lang')))
    check('Window title shows document title, not filename',
          bool(catalog.get('/ViewerPreferences', {}).get('/DisplayDocTitle')))
    check('Title in document properties', bool(reader.metadata.get('/Title')))
    xmp = catalog['/Metadata'].get_data().decode('utf-8', 'replace')
    check('XMP declares PDF/UA-1', 'pdfuaid:part="1"' in xmp)
    check('XMP carries dc:title', 'dc:title' in xmp)

    # Walk the tag tree.
    counts = collections.Counter()
    headings = []
    header_ids = set()
    cells_without_headers = 0
    figures_without_alt = 0

    def walk(node):
        nonlocal cells_without_headers, figures_without_alt
        if isinstance(node, IndirectObject):
            node = node.get_object()
        if isinstance(node, list):
            for child in node:
                walk(child)
            return
        if not hasattr(node, 'get'):
            return
        structure_type = str(node.get('/S') or '')
        if structure_type:
            counts[structure_type] += 1
        if re.fullmatch(r'/H[1-6]', structure_type):
            headings.append(int(structure_type[2]))
        if structure_type == '/TH' and node.get('/ID'):
            header_ids.add(str(node['/ID']))
        if structure_type == '/TD':
            attributes = node.get('/A')
            if isinstance(attributes, IndirectObject):
                attributes = attributes.get_object()
            attributes = (attributes if isinstance(attributes, list)
                          else [attributes] if attributes else [])
            if not any(a.get_object().get('/Headers') for a in attributes):
                cells_without_headers += 1
        if structure_type == '/Figure' and not node.get('/Alt'):
            figures_without_alt += 1
        walk(node.get('/K'))

    walk(catalog['/StructTreeRoot'].get('/K'))

    check('Exactly one H1', counts['/H1'] == 1, 'found %d' % counts['/H1'])
    skips = [(a, b) for a, b in zip(headings, headings[1:]) if b > a + 1]
    check('No skipped heading levels', not skips, str(skips))
    check('Tables tagged with header and body rows',
          counts['/Table'] and counts['/TH'] and counts['/TD'])
    check('Every data cell names its headers', cells_without_headers == 0,
          '%d cells without /Headers' % cells_without_headers)
    check('Every referenced header id exists', bool(header_ids))
    check('Every figure has alternative text', figures_without_alt == 0)

    # Page content: every text block marked, running head kept out of the tree.
    parent_tree = catalog['/StructTreeRoot']['/ParentTree'].get_object()['/Nums']
    mapped = {parent_tree[i]: parent_tree[i + 1].get_object()
              for i in range(0, len(parent_tree), 2)}
    untagged_text = 0
    unmapped_mcids = 0
    artifact_text = 0
    for number, page in enumerate(reader.pages):
        content = page.get_contents().get_data().decode('latin-1')
        open_tags = []
        for token in re.finditer(r'^(?:/(\w+)[^\n]*\n)?(BDC|BMC|EMC|BT)$',
                                 content, flags=re.M):
            name, operator = token.group(1), token.group(2)
            if operator in ('BDC', 'BMC'):
                open_tags.append(name)
            elif operator == 'EMC':
                open_tags and open_tags.pop()
            elif not open_tags:
                untagged_text += 1
            elif 'Artifact' in open_tags:
                artifact_text += 1
        mcids = {int(m) for m in re.findall(r'/MCID (\d+)', content)}
        if len(mapped.get(number, [])) != len(mcids):
            unmapped_mcids += 1
    check('All page text is tagged or artifacted', untagged_text == 0,
          '%d text blocks outside marked content' % untagged_text)
    check('Marked content ids all resolve to tags', unmapped_mcids == 0,
          '%d pages with a mismatch' % unmapped_mcids)

    # A footer on every page, a running header on all but the title page.
    expected_running = 2 * len(reader.pages) - 1
    check('Running header and footer are artifacts, not read as content',
          artifact_text == expected_running,
          '%d artifacted text blocks, expected %d' % (artifact_text, expected_running))

    # Links and fonts.
    missing_description = sum(
        1 for page in reader.pages for annotation in (page.get('/Annots') or [])
        if annotation.get_object().get('/Subtype') == '/Link'
        and not annotation.get_object().get('/Contents'))
    check('Every link annotation has a description', missing_description == 0,
          '%d without /Contents' % missing_description)
    unembedded = set()
    for page in reader.pages:
        fonts = page.get('/Resources', {}).get_object().get('/Font', {}) or {}
        for font in fonts.values():
            font = font.get_object()
            if not (font.get('/FontDescriptor') or font.get('/DescendantFonts')):
                unembedded.add(str(font.get('/BaseFont')))
    check('All fonts embedded', not unembedded, str(unembedded))

    print()
    print('Accessibility checks (%d pages, %d tagged elements):'
          % (len(reader.pages), sum(counts.values())))
    for ok, label, detail in results:
        print('  %s %s%s' % ('PASS' if ok else 'FAIL', label,
                             '  [%s]' % detail if detail and not ok else ''))
    failures = [label for ok, label, _ in results if not ok]
    if failures:
        raise SystemExit('%d accessibility check(s) failed.' % len(failures))


def artifact_margin_boxes():
    """Mark the running header and footer as artifacts instead of tagging them.

    WeasyPrint gives margin-box text a marked-content id and hangs it off the
    document root as a NonStruct span, so assistive technology reads "PUBH 115
    Syllabus - Fall 2026. Page 4 of 15." between every page's content. Running
    heads are decoration, and PDF/UA wants them artifacted - but PDF 1.7 has no
    Artifact structure type, so the fix has to happen where the content is
    marked, not in the tag tree. Margin-box text is the only text WeasyPrint
    draws with no originating HTML element, which is what identifies it here.
    """
    from contextlib import contextmanager

    import weasyprint
    from weasyprint.formatting_structure import boxes
    from weasyprint.pdf import tags as pdf_tags
    from weasyprint.pdf.stream import Stream

    if not weasyprint.__version__.startswith('69.'):
        print('Warning: margin-box artifact patch was written against WeasyPrint 69, '
              'found %s. Check the tag tree in the verification report below.'
              % weasyprint.__version__, file=sys.stderr)

    marked = Stream.marked

    @contextmanager
    def marked_or_artifact(self, box, tag):
        if getattr(box, 'element', None) is None:
            with self.artifact():
                yield
        else:
            with marked(self, box, tag):
                yield

    build_box_tree = pdf_tags._build_box_tree

    def skip_margin_boxes(box, *args, **kwargs):
        # The margin box's content carries no marked-content ids now, so the
        # original walk - which pops one per text box - has nothing to pop.
        if isinstance(box, boxes.MarginBox):
            return iter(())
        return build_box_tree(box, *args, **kwargs)

    Stream.marked = marked_or_artifact
    pdf_tags._build_box_tree = skip_margin_boxes


def main():
    artifact_margin_boxes()
    from weasyprint import HTML

    document = build_html(to_html_fragment())
    try:
        HTML(string=document).write_pdf(PDF, pdf_variant='pdf/ua-1')
    except ValueError as error:
        if 'Table wrapper without a table' not in str(error):
            raise
        print('Caption orphaned from a table; retrying with the calendar on its own page.',
              file=sys.stderr)
        document = document.replace('.keep { break-inside: avoid; }',
                                    '.keep { break-inside: avoid; }\n' + CALENDAR_PAGE_BREAK)
        HTML(string=document).write_pdf(PDF, pdf_variant='pdf/ua-1')

    HTML_OUT.write_text(document, encoding='utf-8')
    print('Wrote %s' % PDF)
    print('Wrote %s' % HTML_OUT)
    verify(PDF)


if __name__ == '__main__':
    main()
