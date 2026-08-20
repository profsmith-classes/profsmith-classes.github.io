# Content Review — Notes-to-Self, Placeholders, and Unwritten Content

**Date:** 2026-08-20
**Scope:** All 34 `.qmd` source files (4,303 lines), `_quarto.yml`, and the rendered `_site/` build.
**Method:** Full read of every source file plus pattern sweeps for placeholder markers, HTML
comments, empty headings, and broken internal links. Findings verified against the rendered
HTML where visibility to students was in question.
**Status:** No edits made. Nothing here has been fixed.

**Start here:** items 1 and 3 are the highest priority — both sit on graded-module pages, and
item 3 blocks a required exercise.

---

## Literal placeholders that are live on the site

### 1. `PUBH_402/module-2-systems-thinking/2.1_Systems_Thinking.qmd:132`

```
# INSERT SYSTEM MAP HERE
```

A note to self rendered as an H1. Also appears in the page's table-of-contents sidebar, so
students see it twice. Line 130 sets it up — "If we took the elements of the urban traffic
system and showed the interconnections, it would make a system map:" — and then delivers
nothing.

Verified in the build:
- `_site/PUBH_402/module-2-systems-thinking/2.1_Systems_Thinking.html:765` → `<h1>INSERT SYSTEM MAP HERE</h1>`
- same file line 484 → TOC entry

### 2. `PUBH_115/pubh115.qmd:4`

```yaml
description: "This is a class"
```

Renders as the visible page subtitle *and* as `<meta name="description">` — so it is what
shows in search results and link previews for the PUBH 115 welcome page.

Verified in the build:
- `_site/PUBH_115/pubh115.html:10` → `<meta name="description" content="This is a class">`
- `_site/PUBH_115/pubh115.html:483` → visible on page

---

## Content referenced as if it exists but was never written

### 3. Module 5 — "Critique Skill Template" does not exist

`PUBH_402/module-5-research-refinement/Module-5---Research-and-System-Refinement-(3-Weeks).qmd`
lines **12** and **121** both link to `../resources/Critique-Skill-Template.qmd`.

There is no such file. This is the **only genuinely broken internal link on the site** —
every other internal link resolves.

Why it matters: it is pointed at from a *required, graded* exercise, described as "a blank,
fill-in-the-blank structure to build it in." Because the target doesn't exist, Quarto left the
raw `.qmd` extension in the href, so students get a 404 on a `.qmd` URL.

Related inconsistency: Module 6 (line 126) sends students to the **AI Explainer** for a
template instead, and the AI Explainer *does* have one (`AI-Explainer.qmd:50-61`, a
deliberately-unrelated workout-plan example). So Modules 5 and 6 currently disagree about
where the template lives.

Two ways to resolve: write `resources/Critique-Skill-Template.qmd` (and add it to
`_quarto.yml`), or repoint Module 5's two links at `AI-Explainer.qmd`.

### 4. `PUBH_402/module-2-systems-thinking/2.1_Systems_Thinking.qmd:278`

```
## Changing the purpose of a system will change the system
```

Heading with no body. Its two siblings each have a full paragraph and a football-team example:
- line 266 `## Changing the elements usually has the least effect on a system.`
- line 272 `## Changing relationships usually changes system behavior`

The third leg of the argument is just the heading.

### 5. `PUBH_402/Syllabus.qmd:107` — a video that isn't there

> "You can view the short video of how the course is structured if you need a refresh,
> [How This Course Fits Together](Welcome.qmd#how-the-course-modules-fit-together)"

The link goes to a *text* section in `Welcome.qmd`. There is no video on that page.

### 6. Module 7 — no point value stated

`PUBH_402/module-7-synthesis-and-final-submission/Module-7---Synthesis-and-Final-Submission-(1-Week).qmd`
lines 47-71. The "How This Will Be Evaluated" section says what earns 0 points but never says
what full credit is worth.

Every other module states it: M3 = 20, M4 = 15, M5 = 20, M6 = 25. M7 = ?

---

## Structural leftovers

### 7. Module 5 — duplicate Format heading

`Module-5---Research-and-System-Refinement-(3-Weeks).qmd:151-153`

```
## Format expectations

## Format:
```

`## Format expectations` is empty and immediately followed by `## Format:`. One of the two is
a leftover.

### 8. `PUBH_115/pubh115_course_modules.qmd` — clearest work-in-progress page

- `draft: true` in frontmatter
- absent from `_quarto.yml`, so unlinked — but still published and reachable by direct URL
  (this was item 8 in the WCAG audit)
- `# Course Introduction` (line 16) and `# Exploring your Values` (line 22) are empty headings
- several topics present in the course calendar are missing from this page entirely

### 9. `PUBH_115/pubh115_other_policy.qmd:42-43` — markdown accident

Missing blank line before the `---`, so the closing sentence becomes a **setext H2**.

Verified in the build: `_site/PUBH_115/pubh115_other_policy.html:542` renders
"Remember: in almost all cases, your writing will only ever be read by exactly two people —
you and me. Is it worth risking a failing grade when you could simply produce your own work?"
as an `<h2>`, and it appears in the page's table of contents (line 473).

The same sentence on `pubh115_grading_policy_assignments.qmd` renders correctly as a paragraph
(`_site/.../pubh115_grading_policy_assignments.html:621`), because that one has the blank line.

Fix: insert a blank line between line 42 and the `---` on line 43.

### 10. `PUBH_115/pubh115_grading_policy_assignments.qmd:115-203` — uncited references

Roughly 17 of the ~40 entries under "AI Policy Sources" are never cited in the policy text
above them:

Al-Sibai; BBC RAI Research; Bender 2024a; Center for Countering Digital Hate; Eichenberger et
al.; HAI; Hao & Seetharaman; Herrman; Joshi et al.; McQuillan; Murakami Wood; Reif et al.;
Salvaggio; Shieh et al.; Speer; Suchak et al.; Vassel et al.

Reads like an accumulating reading pile rather than a citation list. (Not necessarily wrong to
keep — but decide whether it's a bibliography or a further-reading list and label it as such.)

---

## Adjacent drift worth handling in the same pass

- **Module durations conflict with the syllabus.** Module 3's page title says "(3 Weeks)"; the
  syllabus schedules it Sep 7 – Oct 4, which is 4 weeks. Modules 6 and 7 are titled 2 weeks +
  1 week; the syllabus combines them into 2 weeks (Nov 9-22). Titles appear in the sidebar, so
  students see both numbers.

- **`PUBH_115/pubh115_course_calendar.qmd:40`** — the `**11/13/26** Essay 1 due` row sits
  *below* the `11/16/26` row. Out of chronological order in a due-date table.

- **Five full H1 sections duplicate across the two PUBH 115 policy pages**
  (`pubh115_other_policy.qmd` and `pubh115_grading_policy_assignments.qmd`): Technical Issues,
  Class AI Policy, Academic Integrity, Changes to the Course, Other Course Policies. The two
  AI Policy versions already differ — one carries the citations, one doesn't — so they can
  drift further apart. Consider making one canonical and linking to it.

- **`PUBH_402/resources/CSV-Explainer.qmd:12`** — "In this course, CSVs are the default way
  you'll receive and share datasets." Nothing in PUBH 402 actually distributes CSV data; all
  data work is `.gv` files. Possibly a holdover from an earlier design of the course. The
  syllabus repeats the claim at line 338.

- **Typos:**
  - `2.2_System_Maps.qmd:232` — unclosed quotation mark on the Meadows blockquote
  - `Module-4...:65` — "You map must contain" (→ "Your"), and a doubled period ("minimum..")
  - `Module-5...:48` — "the evolution of your amp" (→ "map"), and "in you `.gv` file" (→ "your")
  - `Module-3...:45` — sentence ends without a question mark
  - `Syllabus.qmd:378` — missing period before "For now"

---

## Checked and clean

- **`_quarto.yml` navigation.** The sidebar mislabeling described in `CLAUDE.md` (Module 1
  pointing at `module-2-systems-thinking/`, an entry for a nonexistent
  `module-2-team-formation/`) is **no longer present**. Every nav path resolves to a file on
  disk. That note in `CLAUDE.md` is stale and could be removed.

- **No HTML comments anywhere** in the `.qmd` sources — no hidden `<!-- TODO -->` notes.

- **No TODO / FIXME / TBD / lorem ipsum markers** anywhere in the source.

- **`_internal/` is not published.** Quarto skips underscore-prefixed directories, and
  `_site/_internal` does not exist. However it is **untracked and not listed in
  `.gitignore`** — a `git add -A` would commit these working notes to the public repo.
  Worth adding `/_internal/` to `.gitignore`.

- **Only two pages sit outside `_quarto.yml` nav:** `index.qmd` (expected — it's the site root)
  and `pubh115_course_modules.qmd` (item 8 above).
