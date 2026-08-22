#!/usr/bin/env python3
"""Build the accessible PUBH 402 Word syllabus from its Markdown source.

    python3 _internal/build-402-syllabus-docx.py

Reads PUBH-402-Syllabus-Fall-2026.md, converts it with pandoc (bundled with
Quarto) using the PUBH 115 syllabus as the style reference, then repairs the
two things pandoc's docx writer cannot express:

  - table alt text: Word stores a table's title and description in tblPr as
    w:tblCaption and w:tblDescription, which is what a screen reader announces
    before reading the cells. Pandoc has no syntax for them, so they live in
    the TABLES list below, matched to tables in document order.
  - header rows: w:tblHeader on the first row so it repeats across page breaks
    and is exposed as a header row.
  - paragraph styles: pandoc tags body text Compact/FirstParagraph and quotes
    BlockText, none of which the reference document defines any more - Word
    dropped them as unused when the 115 syllabus was last edited. Paragraphs
    pointing at a missing style silently fall back to Normal, so they are
    remapped onto styles that do exist: BodyText, ListBullet, ListNumber, Quote.
    The list paragraphs keep pandoc's own numPr, which is what makes them a real
    list to Word and to a screen reader, and which numbers each list from 1
    rather than continuing the previous one.

It also writes docProps/core.xml, since a document title in the file
properties is what assistive technology reads instead of the filename.

Requirements: quarto (for its bundled pandoc). No Python packages needed.
"""

import datetime
import pathlib
import re
import shutil
import subprocess
import sys
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
SOURCE = HERE / "PUBH-402-Syllabus-Fall-2026.md"
REFERENCE = HERE / "PUBH-115-Syllabus-Fall-2026.docx"
DOCX = HERE / "PUBH-402-Syllabus-Fall-2026.docx"

TITLE = "PUBH 402 Introduction to the U.S. Health Care System - Syllabus, Fall 2026"
AUTHOR = "Jason A. Smith"
DESCRIPTION = ("Accessible course syllabus prepared in accordance with CSUF UPS 300.004, "
               "Policy on Syllabi (effective November 5, 2025).")

# Table title and alt-text description, in document order.
TABLES = [
    ("Course Information",
     "Two-column table listing basic course facts: title, number, section, class number, "
     "units, term, modality, meeting times, prerequisites, General Education status, "
     "learning management system, and course website."),
    ("Instructor Information",
     "Two-column table listing the instructor's name, office location, telephone number, "
     "email address, office hours, and email response time."),
    ("Assessment Guide",
     "Two-column table mapping each of the eight course student learning outcomes to the "
     "assignment that primarily assesses it, either the Final Exam or the Systems Analysis "
     "Project."),
    ("Course Calendar, Fall 2026",
     "Four-column table covering all fifteen instructional weeks, the Fall Recess week, and "
     "final examination week. Columns are week number, date range, module and topic, and key "
     "dates and what is due that week."),
    ("Required Assignments, Type, and Due Dates",
     "Four-column table listing every graded deliverable in the course. Columns are the "
     "module it belongs to, the assignment name, whether it is individual or group work, and "
     "its due date."),
    ("Team Check-In Scoring",
     "Two-column table giving the five check-in tiers, from clear understanding to "
     "non-submission, and the percentage of the team score each tier earns."),
    ("Grade Breakdown, Undergraduate Students",
     "Two-column table listing the three graded components for undergraduates and their "
     "weights: Exam 1 at 22 percent, Systems Analysis Project at 40 percent, and Final Exam "
     "at 38 percent, totaling 100 percent."),
    ("Grade Breakdown, Graduate Students",
     "Two-column table listing the four graded components for graduate students and their "
     "weights: Exam 1 at 22 percent, Systems Analysis Project at 40 percent, Final Exam at 23 "
     "percent, and Secondary System Analysis at 15 percent, totaling 100 percent."),
]

CORE_XML = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"\
 xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"\
 xmlns:dcmitype="http://purl.org/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\
<dc:title>{title}</dc:title><dc:subject>Course syllabus</dc:subject><dc:creator>{author}</dc:creator>\
<cp:keywords>PUBH 402, syllabus, Fall 2026, health care system, CSUF</cp:keywords>\
<dc:description>{description}</dc:description><cp:lastModifiedBy>{author}</cp:lastModifiedBy>\
<cp:revision>1</cp:revision><dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>\
<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified><cp:category>Syllabus</cp:category>\
<dc:language>en-US</dc:language></cp:coreProperties>"""


def run_pandoc(target):
    subprocess.run(
        ["quarto", "pandoc", str(SOURCE), "-f", "markdown", "-t", "docx",
         "--reference-doc", str(REFERENCE), "-o", str(target)],
        check=True,
    )


def add_table_metadata(document):
    """Give every table its alt text and mark its first row as a header row."""
    tables = list(re.finditer(r'<w:tbl>.*?</w:tbl>', document, flags=re.S))
    if len(tables) != len(TABLES):
        raise SystemExit('Expected %d tables, found %d. Update TABLES to match the source.'
                         % (len(TABLES), len(tables)))

    for (caption, description), match in reversed(list(zip(TABLES, tables))):
        table = match.group(0)

        if 'w:tblCaption' in table:
            raise SystemExit('Table %r already carries a caption.' % caption)
        alt_text = ('<w:tblCaption w:val="%s"/><w:tblDescription w:val="%s"/>'
                    % (escape(caption), escape(description)))
        table = table.replace('</w:tblPr>', alt_text + '</w:tblPr>', 1)

        # First row repeats across pages and is announced as the header row.
        first_row = re.search(r'<w:tr\b[^>]*>', table)
        if not first_row:
            raise SystemExit('Table %r has no rows.' % caption)
        head = table[first_row.end():]
        if head.lstrip().startswith('<w:trPr>'):
            table = table[:first_row.end()] + re.sub(
                r'<w:trPr>', '<w:trPr><w:tblHeader/>', head, count=1)
        else:
            table = table[:first_row.end()] + '<w:trPr><w:tblHeader/></w:trPr>' + head

        document = document[:match.start()] + table + document[match.end():]

    return document


def restyle(document, numbering):
    """Point paragraphs at styles the reference document actually defines."""
    bullet_ids = bullet_num_ids(numbering)

    def fix(match):
        paragraph = match.group(0)
        style = re.search(r'<w:pStyle w:val="(Compact|FirstParagraph|BlockText)"\s*/>', paragraph)
        if not style:
            return paragraph
        if style.group(1) == 'BlockText':
            replacement = 'Quote'
        else:
            num_id = re.search(r'<w:numId w:val="(\d+)"\s*/>', paragraph)
            if not num_id:
                replacement = 'BodyText'
            elif num_id.group(1) in bullet_ids:
                replacement = 'ListBullet'
            else:
                replacement = 'ListNumber'
        return paragraph[:style.start()] + '<w:pStyle w:val="%s" />' % replacement + \
            paragraph[style.end():]

    return re.sub(r'<w:p\b(?:(?!</w:p>).)*?</w:p>', fix, document, flags=re.S)


def bullet_num_ids(numbering):
    """numIds whose level-0 format is a bullet rather than a number."""
    abstract_format = {}
    for match in re.finditer(r'<w:abstractNum w:abstractNumId="(\d+)".*?</w:abstractNum>',
                             numbering, flags=re.S):
        level = re.search(r'<w:lvl w:ilvl="0".*?</w:lvl>', match.group(0), flags=re.S)
        fmt = re.search(r'<w:numFmt w:val="([^"]+)"', level.group(0)) if level else None
        abstract_format[match.group(1)] = fmt.group(1) if fmt else 'decimal'
    bullets = set()
    for match in re.finditer(r'<w:num w:numId="(\d+)".*?</w:num>', numbering, flags=re.S):
        abstract = re.search(r'<w:abstractNumId w:val="(\d+)"', match.group(0))
        if abstract and abstract_format.get(abstract.group(1)) == 'bullet':
            bullets.add(match.group(1))
    return bullets


def escape(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;')
                .replace('>', '&gt;').replace('"', '&quot;'))


def rewrite(source_docx, target_docx):
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    core = CORE_XML.format(title=escape(TITLE), author=escape(AUTHOR),
                           description=escape(DESCRIPTION), now=now)
    with zipfile.ZipFile(source_docx) as original:
        names = original.namelist()
        numbering = original.read('word/numbering.xml').decode('utf-8')
        with zipfile.ZipFile(target_docx, 'w', zipfile.ZIP_DEFLATED) as rebuilt:
            for name in names:
                data = original.read(name)
                if name == 'word/document.xml':
                    document = restyle(data.decode('utf-8'), numbering)
                    data = add_table_metadata(document).encode('utf-8')
                elif name == 'docProps/core.xml':
                    data = core.encode('utf-8')
                rebuilt.writestr(name, data)
            if 'docProps/core.xml' not in names:
                raise SystemExit('Reference document has no docProps/core.xml to replace.')


def list_styles(document):
    """Style of every paragraph that is part of a numbered or bulleted list."""
    out = []
    for match in re.finditer(r'<w:p\b(?:(?!</w:p>).)*?</w:p>', document, flags=re.S):
        if '<w:numPr>' in match.group(0):
            style = re.search(r'<w:pStyle w:val="([^"]+)"', match.group(0))
            out.append(style.group(1) if style else '(none)')
    return out


def defined_styles(path):
    with zipfile.ZipFile(path) as document:
        styles = document.read('word/styles.xml').decode('utf-8')
    return set(re.findall(r'<w:style [^>]*w:styleId="([^"]+)"', styles))


def verify(path):
    """Check the accessibility structure of the finished document."""
    with zipfile.ZipFile(path) as document:
        xml = document.read('word/document.xml').decode('utf-8')
        core = document.read('docProps/core.xml').decode('utf-8')

    results = []

    def check(label, ok, detail=''):
        results.append((ok, label, detail))

    styles = re.findall(r'w:pStyle w:val="([^"]+)"', xml)
    headings = [int(s[-1]) for s in styles if re.fullmatch(r'Heading[1-9]', s)]
    check('Exactly one Title paragraph', styles.count('Title') == 1,
          '%d found' % styles.count('Title'))
    check('Headings use real Word heading styles', bool(headings),
          '%d headings' % len(headings))
    skips = [(a, b) for a, b in zip(headings, headings[1:]) if b > a + 1]
    check('No skipped heading levels', not skips, str(skips[:3]))

    tables = re.findall(r'<w:tbl>.*?</w:tbl>', xml, flags=re.S)
    check('Every table has a title (w:tblCaption)',
          all('w:tblCaption' in t for t in tables), '%d tables' % len(tables))
    check('Every table has alt text (w:tblDescription)',
          all('w:tblDescription' in t for t in tables))
    check('Every table has a repeating header row (w:tblHeader)',
          all('<w:tblHeader/>' in t for t in tables))

    check('Document title set in file properties', '<dc:title>' in core and TITLE in core)
    check('Author set in file properties', AUTHOR in core)
    check('Document language set', '<dc:language>en-US</dc:language>' in core)
    check('Lists are real Word lists, not typed bullets', xml.count('<w:numPr>') > 0,
          '%d list paragraphs' % xml.count('<w:numPr>'))
    check('List paragraphs carry a list style',
          all(s.startswith('List') for s in list_styles(xml)),
          'styles: %s' % sorted(set(list_styles(xml))))
    undefined = sorted(set(styles) - defined_styles(path))
    check('Every referenced paragraph style is defined', not undefined, str(undefined))
    check('No literal placeholder text left in the document',
          not re.search(r'TBD|TODO|\[insert|XXXX', xml, re.I))

    print()
    print('Accessibility checks (%d headings, %d tables):' % (len(headings), len(tables)))
    for ok, label, detail in results:
        print('  %s %s%s' % ('PASS' if ok else 'FAIL', label,
                             '  [%s]' % detail if detail and not ok else ''))
    if any(not ok for ok, _, _ in results):
        raise SystemExit('Accessibility checks failed.')


def main():
    if not shutil.which('quarto'):
        raise SystemExit('quarto not found; it provides the pandoc used here.')
    staged = DOCX.with_suffix('.pandoc.docx')
    try:
        run_pandoc(staged)
        rewrite(staged, DOCX)
    finally:
        staged.unlink(missing_ok=True)
    print('Wrote %s' % DOCX)
    verify(DOCX)


if __name__ == '__main__':
    main()
