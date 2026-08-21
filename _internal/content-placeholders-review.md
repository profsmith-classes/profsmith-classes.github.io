# Content Review — Notes-to-Self, Placeholders, and Unwritten Content

**Date:** 2026-08-20 (original review) · **Last updated:** 2026-08-20
**Scope:** All 34 `.qmd` source files (4,303 lines), `_quarto.yml`, and the rendered `_site/` build.
**Method:** Full read of every source file plus pattern sweeps for placeholder markers, HTML
comments, empty headings, and broken internal links. Findings verified against the rendered
HTML where visibility to students was in question.

**Status:** 3 of 10 items resolved — **1, 2, and 5**. All changes are in the working tree and
**not yet committed**. Every remaining finding below was re-verified against current source on
2026-08-20 and still holds.

**Start here:** item 3 — the site's only broken internal link, and it blocks a required,
graded exercise. Item 11 (new) is a one-line decision about what's in the public repo.

### Where things stand

| # | Finding | Status |
|---|---|---|
| 1 | `INSERT SYSTEM MAP HERE` placeholder | ✅ Resolved — map built, WCAG 1.4.1 handled |
| 2 | `description: "This is a class"` | ✅ Resolved |
| 3 | Module 5 → nonexistent Critique Skill Template | ✅ Resolved 2026-08-21 — links removed |
| 4 | Empty "Changing the purpose" heading | ✅ Resolved 2026-08-21 |
| 5 | Syllabus link to a video that isn't there | ✅ Resolved |
| 6 | Module 7 states no point value | ⬜ Open |
| 7 | Module 5 duplicate Format heading | ✅ Resolved 2026-08-21 |
| 8 | `pubh115_course_modules.qmd` work-in-progress | ✅ Closed 2026-08-21 — not a defect |
| 9 | Accidental setext H2 in `pubh115_other_policy.qmd` | ✅ Resolved 2026-08-21 |
| 10 | ~17 uncited entries under AI Policy Sources | ⬜ Open |
| 11 | `_internal/` is committed to the public repo | ✅ Closed 2026-08-21 — tracked by choice |

Uncommitted working-tree changes as of this update:

```
 M PUBH_115/pubh115.qmd                                          (item 2)
 M PUBH_402/Syllabus.qmd                                         (item 5)
 M PUBH_402/module-2-systems-thinking/2.1_Systems_Thinking.qmd    (item 1)
 M _internal/content-placeholders-review.md                       (this file)
```

---

## Literal placeholders that are live on the site

### 1. ~~`PUBH_402/module-2-systems-thinking/2.1_Systems_Thinking.qmd:132`~~ — RESOLVED 2026-08-20

**Fixed:** replaced with a `{dot}` block (`fig-traffic-system`) drawing the urban traffic
system — six elements from the text above, the B1 balancing loop in blue, the R1 induced-demand
loop in red, `cars -> congestion` two-toned as the shared link, and `||` marking the two delays.
Verified rendering: the SVG, figure caption, and legend are all present in the build, and the
placeholder H1 no longer appears on the page or in its TOC.

**1.4.1 Use of Color handled (2026-08-20).** The first version distinguished B1 from R1 by
color alone, with a color-keyed legend that couldn't rescue it — exactly the pattern WCAG audit
item 16 warned about. Now every edge label carries its loop tag (`+ (B1)`, `- (B1)`,
`+ || (R1)`, `+ (B1, R1)` on the shared link) and the three R1 edges are `style=dashed`, so
loop membership is readable from text and line style with color off entirely. The shared
two-tone link stays solid — it can't be both solid and dashed — so its `(B1, R1)` tag is what
identifies it. The legend was rewritten to three lines stating the encoding. Verified in the
build: 3 dashed edges, all 7 tags present, viewbox 435.86×330.40 → 429.86×343.60 (marginally
narrower, slightly taller — no layout bloat).

Pedagogical side benefit: reading `+ (B1)` off each arrow is more direct for students learning
to trace loops than matching arrow colors against a legend, and it makes the shared link
visibly the place where the two loops meet — which is the point of the figure.

**Still carries over into the WCAG audit.** This is now a 10th inline SVG subject to audit
items 10 (no `role="img"` / text alternative) and 11 (fixed 672×480, `max-width: none`,
breaking 1.4.10 Reflow). Both are site-wide fixes that would clear all ten diagrams at once,
not per-diagram ones. Edge-label contrast is fine (royalblue4 9.6:1, firebrick 6.7:1 on the
white SVG canvas).

<details><summary>Original finding</summary>

```
# INSERT SYSTEM MAP HERE
```

A note to self rendered as an H1. Also appeared in the page's table-of-contents sidebar, so
students saw it twice. Line 130 set it up — "If we took the elements of the urban traffic
system and showed the interconnections, it would make a system map:" — and then delivered
nothing.

Verified in the build at the time:
- `_site/PUBH_402/module-2-systems-thinking/2.1_Systems_Thinking.html:765` → `<h1>INSERT SYSTEM MAP HERE</h1>`
- same file line 484 → TOC entry
</details>

### 2. ~~`PUBH_115/pubh115.qmd:4`~~ — RESOLVED 2026-08-20

**Fixed:** the `description:` line was deleted from the frontmatter. The page now emits no
`<meta name="description">`, which matches every other page on the site except the draft
`pubh115_course_modules.qmd`. If you'd rather have a real one for search results and link
previews, add it back with actual course text.

<details><summary>Original finding</summary>

```yaml
description: "This is a class"
```

Rendered as the visible page subtitle *and* as `<meta name="description">` — so it was what
showed in search results and link previews for the PUBH 115 welcome page.

Verified in the build at the time:
- `_site/PUBH_115/pubh115.html:10` → `<meta name="description" content="This is a class">`
- `_site/PUBH_115/pubh115.html:483` → visible on page
</details>

---

## Content referenced as if it exists but was never written

### 3. Module 5 — "Critique Skill Template" does not exist ✅ Resolved 2026-08-21

`PUBH_402/module-5-research-refinement/Module-5---Research-and-System-Refinement-(3-Weeks).qmd`
lines **12** and **121** both linked to `../resources/Critique-Skill-Template.qmd`, which was
never written. Because the target didn't exist, Quarto left the raw `.qmd` extension in the
href, so students got a 404 on a `.qmd` URL — the only genuinely broken internal link on the
site.

**Resolved:** the template is not going to be written, so both references were removed. Each
sentence already named the [AI Explainer](../PUBH_402/resources/AI-Explainer.qmd) alongside it,
and that link remains — which also puts Module 5 in agreement with Module 6 (line 126), which
already sends students to the AI Explainer for a template
(`AI-Explainer.qmd:50-61`, the deliberately-unrelated workout-plan example).

### 4. ~~`2.1_Systems_Thinking.qmd` — empty "Changing the purpose" heading~~ — RESOLVED 2026-08-21

**Fixed:** the heading now has a body (line 320) with a football-team example, matching the
structure of its two siblings — `## Changing the elements usually has the least effect on a
system.` and `## Changing relationships usually changes system behavior`.

<details><summary>Original finding</summary>

> `PUBH_402/module-2-systems-thinking/2.1_Systems_Thinking.qmd:318`
>
> ```
> ## Changing the purpose of a system will change the system
> ```
>
> Heading with no body. Its two siblings each have a full paragraph and a football-team
> example. The third leg of the argument is just the heading — and it's the leg Meadows treats
> as the most powerful, so it's the one most worth writing.
</details>

### 5. ~~`PUBH_402/Syllabus.qmd:107` — a video that isn't there~~ — RESOLVED 2026-08-20

**Fixed:** the sentence and link were removed; the line now reads only "Specific due dates and
exam dates are on Canvas and below."

<details><summary>Original finding</summary>

> "You can view the short video of how the course is structured if you need a refresh,
> [How This Course Fits Together](Welcome.qmd#how-the-course-modules-fit-together)"

The link went to a *text* section in `Welcome.qmd`. There is no video on that page.
</details>

### 6. Module 7 — no point value stated

`PUBH_402/module-7-synthesis-and-final-submission/Module-7---Synthesis-and-Final-Submission-(1-Week).qmd`
lines 47-71. The "How This Will Be Evaluated" section says what earns 0 points — twice, and
emphatically — but never says what full credit is worth.

Every other module states it: M3 = 20, M4 = 15, M5 = 20, M6 = 25. M7 = ?

Sharper than it looks for an async course: this is the *final* deliverable, it's all-or-nothing
on a Format Check, and students can't ask in class what it's worth.

---

## Structural leftovers

### 7. ~~Module 5 — duplicate Format heading~~ — RESOLVED 2026-08-21

**Fixed:** the empty `## Format expectations` heading was removed; `## Format:` (now line 151)
keeps the content and is the only Format H2 on the page.

<details><summary>Original finding</summary>

> `Module-5---Research-and-System-Refinement-(3-Weeks).qmd:151-153`
>
> ```
> ## Format expectations
>
> ## Format:
> ```
>
> `## Format expectations` is empty and immediately followed by `## Format:`, which has the
> actual content. One of the two is a leftover; both appear in the page TOC.
</details>

### 8. ~~`PUBH_115/pubh115_course_modules.qmd` — clearest work-in-progress page~~ — CLOSED 2026-08-21

**Not a defect.** Confirmed by Jason 2026-08-21: the page is complete as written. It is an index
of Leganto reading-list links, and the headings with no link under them (`# Course Introduction`,
`# Exploring your Values`) are modules that have no Leganto list — not unwritten sections. The
original review misread an intentionally sparse index page as a draft.

Two mechanical leftovers on the page are *not* covered by that confirmation and remain open —
raised 2026-08-21, no decision yet:

- `draft: true` in the frontmatter, and the page is absent from `_quarto.yml`. If the page is
  finished and students are meant to use it, it likely wants the draft flag dropped and a nav
  entry added; right now it is reachable only by direct URL.
- `description:` reads "This **pages** contains..." — typo for *page*.

<details><summary>Original finding</summary>

> - `draft: true` in frontmatter
> - absent from `_quarto.yml`, so unlinked — but still published and reachable by direct URL
>   (this was item 8 in the WCAG audit)
> - `# Course Introduction` (line 16) and `# Exploring your Values` (line 22) are empty headings
> - several topics present in the course calendar are missing from this page entirely
> - it is also the only page besides `pubh115.qmd` that carried a `description:` — its one reads
>   "This pages contains..." (typo: *pages* → *page*)
</details>

### 9. ~~`PUBH_115/pubh115_other_policy.qmd:42-43` — markdown accident~~ — RESOLVED 2026-08-21

**Fixed:** a blank line was inserted before the `---`, so the closing sentence is a paragraph
again and the `---` is a horizontal rule. Needs a re-render to clear the stale `<h2>` and TOC
entry from `_site/`.

<details><summary>Original finding</summary>

> Missing blank line before the `---`, so the closing sentence becomes a **setext H2**.
>
> Verified in the build: `_site/PUBH_115/pubh115_other_policy.html:542` renders
> "Remember: in almost all cases, your writing will only ever be read by exactly two people —
> you and me. Is it worth risking a failing grade when you could simply produce your own work?"
> as an `<h2>`, and it appears in the page's table of contents (line 473).
>
> The same sentence on `pubh115_grading_policy_assignments.qmd` renders correctly as a paragraph
> (`_site/.../pubh115_grading_policy_assignments.html:621`), because that one has the blank line.
</details>

### 10. `PUBH_115/pubh115_grading_policy_assignments.qmd:115-203` — uncited references

Roughly 17 of the ~40 entries under "AI Policy Sources" (heading at line 113) are never cited
in the policy text above them:

Al-Sibai; BBC RAI Research; Bender 2024a; Center for Countering Digital Hate; Eichenberger et
al.; HAI; Hao & Seetharaman; Herrman; Joshi et al.; McQuillan; Murakami Wood; Reif et al.;
Salvaggio; Shieh et al.; Speer; Suchak et al.; Vassel et al.

Reads like an accumulating reading pile rather than a citation list. (Not necessarily wrong to
keep — but decide whether it's a bibliography or a further-reading list and label it as such.)

---

## Repo housekeeping

### 11. `_internal/` in the public repo — CLOSED 2026-08-21 (accepted, stays tracked)

**Decision by Jason, 2026-08-21: leave `_internal/` tracked.** It was briefly untracked
(`git rm -r --cached` + a `.gitignore` entry) and then reverted; the repo is back to its
committed state and these files continue to be versioned and pushed with everything else.

What that means going forward:

- **Not published to students.** Quarto skips underscore-prefixed directories, so `_site/_internal`
  is never generated. Nobody using the course site encounters these files.
- **Publicly readable on GitHub.** Anyone browsing the repo can read the WCAG audit, this punch
  list, and the three PDFs — including the running record of what's unfinished.
- **The upside of the choice:** these documents are version-controlled and backed up along with
  the content they describe, which is why keeping them tracked is reasonable.

The standing rule this implies: `_internal/` is a *non-published* directory, not a *private* one.
Don't put anything in it that would be harmful to disclose — unreleased exam keys, student
records, grades, or anything covered by FERPA.

<details><summary>Original finding</summary>

```
# INSERT SYSTEM MAP HERE
```

A note to self rendered as an H1. Also appeared in the page's table-of-contents sidebar, so
students saw it twice. Line 130 set it up — "If we took the elements of the urban traffic
system and showed the interconnections, it would make a system map:" — and then delivered
nothing.

Verified in the build at the time:
- `_site/PUBH_402/module-2-systems-thinking/2.1_Systems_Thinking.html:765` → `<h1>INSERT SYSTEM MAP HERE</h1>`
- same file line 484 → TOC entry
</details>

### 2. ~~`PUBH_115/pubh115.qmd:4`~~ — RESOLVED 2026-08-20

**Fixed:** the `description:` line was deleted from the frontmatter. The page now emits no
`<meta name="description">`, which matches every other page on the site except the draft
`pubh115_course_modules.qmd`. If you'd rather have a real one for search results and link
previews, add it back with actual course text.

<details><summary>Original finding</summary>

```yaml
description: "This is a class"
```

Rendered as the visible page subtitle *and* as `<meta name="description">` — so it was what
showed in search results and link previews for the PUBH 115 welcome page.

Verified in the build at the time:
- `_site/PUBH_115/pubh115.html:10` → `<meta name="description" content="This is a class">`
- `_site/PUBH_115/pubh115.html:483` → visible on page
</details>

---

## Content referenced as if it exists but was never written

### 3. Module 5 — "Critique Skill Template" does not exist ✅ Resolved 2026-08-21

`PUBH_402/module-5-research-refinement/Module-5---Research-and-System-Refinement-(3-Weeks).qmd`
lines **12** and **121** both linked to `../resources/Critique-Skill-Template.qmd`, which was
never written. Because the target didn't exist, Quarto left the raw `.qmd` extension in the
href, so students got a 404 on a `.qmd` URL — the only genuinely broken internal link on the
site.

**Resolved:** the template is not going to be written, so both references were removed. Each
sentence already named the [AI Explainer](../PUBH_402/resources/AI-Explainer.qmd) alongside it,
and that link remains — which also puts Module 5 in agreement with Module 6 (line 126), which
already sends students to the AI Explainer for a template
(`AI-Explainer.qmd:50-61`, the deliberately-unrelated workout-plan example).

### 4. ~~`2.1_Systems_Thinking.qmd` — empty "Changing the purpose" heading~~ — RESOLVED 2026-08-21

**Fixed:** the heading now has a body (line 320) with a football-team example, matching the
structure of its two siblings — `## Changing the elements usually has the least effect on a
system.` and `## Changing relationships usually changes system behavior`.

<details><summary>Original finding</summary>

> `PUBH_402/module-2-systems-thinking/2.1_Systems_Thinking.qmd:318`
>
> ```
> ## Changing the purpose of a system will change the system
> ```
>
> Heading with no body. Its two siblings each have a full paragraph and a football-team
> example. The third leg of the argument is just the heading — and it's the leg Meadows treats
> as the most powerful, so it's the one most worth writing.
</details>

### 5. ~~`PUBH_402/Syllabus.qmd:107` — a video that isn't there~~ — RESOLVED 2026-08-20

**Fixed:** the sentence and link were removed; the line now reads only "Specific due dates and
exam dates are on Canvas and below."

<details><summary>Original finding</summary>

> "You can view the short video of how the course is structured if you need a refresh,
> [How This Course Fits Together](Welcome.qmd#how-the-course-modules-fit-together)"

The link went to a *text* section in `Welcome.qmd`. There is no video on that page.
</details>

### 6. Module 7 — no point value stated

`PUBH_402/module-7-synthesis-and-final-submission/Module-7---Synthesis-and-Final-Submission-(1-Week).qmd`
lines 47-71. The "How This Will Be Evaluated" section says what earns 0 points — twice, and
emphatically — but never says what full credit is worth.

Every other module states it: M3 = 20, M4 = 15, M5 = 20, M6 = 25. M7 = ?

Sharper than it looks for an async course: this is the *final* deliverable, it's all-or-nothing
on a Format Check, and students can't ask in class what it's worth.

---

## Structural leftovers

### 7. ~~Module 5 — duplicate Format heading~~ — RESOLVED 2026-08-21

**Fixed:** the empty `## Format expectations` heading was removed; `## Format:` (now line 151)
keeps the content and is the only Format H2 on the page.

<details><summary>Original finding</summary>

> `Module-5---Research-and-System-Refinement-(3-Weeks).qmd:151-153`
>
> ```
> ## Format expectations
>
> ## Format:
> ```
>
> `## Format expectations` is empty and immediately followed by `## Format:`, which has the
> actual content. One of the two is a leftover; both appear in the page TOC.
</details>

### 8. ~~`PUBH_115/pubh115_course_modules.qmd` — clearest work-in-progress page~~ — CLOSED 2026-08-21

**Not a defect.** Confirmed by Jason 2026-08-21: the page is complete as written. It is an index
of Leganto reading-list links, and the headings with no link under them (`# Course Introduction`,
`# Exploring your Values`) are modules that have no Leganto list — not unwritten sections. The
original review misread an intentionally sparse index page as a draft.

Two mechanical leftovers on the page are *not* covered by that confirmation and remain open —
raised 2026-08-21, no decision yet:

- `draft: true` in the frontmatter, and the page is absent from `_quarto.yml`. If the page is
  finished and students are meant to use it, it likely wants the draft flag dropped and a nav
  entry added; right now it is reachable only by direct URL.
- `description:` reads "This **pages** contains..." — typo for *page*.

<details><summary>Original finding</summary>

> - `draft: true` in frontmatter
> - absent from `_quarto.yml`, so unlinked — but still published and reachable by direct URL
>   (this was item 8 in the WCAG audit)
> - `# Course Introduction` (line 16) and `# Exploring your Values` (line 22) are empty headings
> - several topics present in the course calendar are missing from this page entirely
> - it is also the only page besides `pubh115.qmd` that carried a `description:` — its one reads
>   "This pages contains..." (typo: *pages* → *page*)
</details>

### 9. ~~`PUBH_115/pubh115_other_policy.qmd:42-43` — markdown accident~~ — RESOLVED 2026-08-21

**Fixed:** a blank line was inserted before the `---`, so the closing sentence is a paragraph
again and the `---` is a horizontal rule. Needs a re-render to clear the stale `<h2>` and TOC
entry from `_site/`.

<details><summary>Original finding</summary>

> Missing blank line before the `---`, so the closing sentence becomes a **setext H2**.
>
> Verified in the build: `_site/PUBH_115/pubh115_other_policy.html:542` renders
> "Remember: in almost all cases, your writing will only ever be read by exactly two people —
> you and me. Is it worth risking a failing grade when you could simply produce your own work?"
> as an `<h2>`, and it appears in the page's table of contents (line 473).
>
> The same sentence on `pubh115_grading_policy_assignments.qmd` renders correctly as a paragraph
> (`_site/.../pubh115_grading_policy_assignments.html:621`), because that one has the blank line.
</details>

### 10. `PUBH_115/pubh115_grading_policy_assignments.qmd:115-203` — uncited references

Roughly 17 of the ~40 entries under "AI Policy Sources" (heading at line 113) are never cited
in the policy text above them:

Al-Sibai; BBC RAI Research; Bender 2024a; Center for Countering Digital Hate; Eichenberger et
al.; HAI; Hao & Seetharaman; Herrman; Joshi et al.; McQuillan; Murakami Wood; Reif et al.;
Salvaggio; Shieh et al.; Speer; Suchak et al.; Vassel et al.

Reads like an accumulating reading pile rather than a citation list. (Not necessarily wrong to
keep — but decide whether it's a bibliography or a further-reading list and label it as such.)

---

## Repo housekeeping

### 11. `_internal/` in the public repo — UNTRACKED 2026-08-21 (partially resolved)

**Action taken 2026-08-21:** `git rm -r --cached _internal/` staged the removal of all five
files, and `/_internal/` was added to `.gitignore`. Files remain on disk; git will not pick up
future changes to them.

**Two things still true:**

- The removal is **staged, not committed or pushed.** Until it is pushed, the directory is still
  in the GitHub file listing.
- **Git history retains the files permanently.** Untracking removes them going forward; it does
  not erase commit `3e6a864`. Anyone who knows to look can still retrieve these PDFs and the two
  audit documents from history. Erasing them would require a history rewrite
  (`git filter-repo` + force-push), which was considered and not chosen.

Treat this directory as *unindexed*, not *private*. Don't put anything in it that would be
harmful to disclose.

<details><summary>Original finding</summary>

> The original review listed this under "checked and clean" with the note that `_internal/` was
untracked and worth adding to `.gitignore`. **That is no longer accurate.** Commit `3e6a864`
("Add accessibility audit report and various PDF resources for Fall 2026") added the whole
directory, and `main` is in sync with `origin/main` — so it's already on GitHub.

Now tracked:

```
_internal/FALL 2026 SEMESTER CALENDAR.pdf
_internal/Registration_20Guides_20CSUF_20-_20Office_20of_20the_20Registrar.html.pdf
_internal/UPS 300.004 (1).pdf
_internal/WCAG-2.1-AA-audit.md
_internal/content-placeholders-review.md
```

`.gitignore` still contains only `/.quarto/`, `/_site/`, `**/*.quarto_ipynb`.

Two things are true and worth separating:

- **Not published.** Quarto skips underscore-prefixed directories, and `_site/_internal` does
  not exist. Students following the site will never encounter these files.
- **Publicly readable in the repo.** Anyone browsing the GitHub repo can read the WCAG audit
  and this punch list — including the running inventory of what's broken and unfinished.

Decide which you want:

1. **Leave it.** Defensible — the audit and this list are professional work product, and
   there's a case for accessibility work being visible. Nothing here is confidential.
2. **Untrack it:** `git rm -r --cached _internal/` and add `/_internal/` to `.gitignore`. The
   files stay on disk; they leave future commits. Note this does **not** remove them from
   history already pushed — they'd remain in `3e6a864` unless history is rewritten.
3. **Move it out of the repo entirely** if these notes should never have been near it.

Worth a look either way: the three PDFs (a campus calendar, a registrar guide, and UPS 300.004)
are third-party documents that may not be yours to redistribute.

---

## Adjacent drift worth handling in the same pass

- **Module durations conflict with the syllabus.** Module 3's page title says "(3 Weeks)"; the
  syllabus schedules it Sep 7 – Oct 4 and labels it "(4 weeks)" outright at line 115, with the
  week-by-week table at lines 132-135 counting "Module 3 (1 of 4)" through "(4 of 4)". Modules
  6 and 7 are titled 2 weeks + 1 week; the syllabus combines them into one 2-week block
  (Nov 9-22, line 119). Titles appear in the sidebar, so students see both numbers. The
  syllabus is internally consistent — it's the page titles that are wrong.

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
  syllabus repeats the claim at line 338 ("data are often provided as CSV files"), lists CSV
  skills at 341-344, links the explainer at 347, and puts "I can open a CSV file and explain
  what the rows and columns represent" in the self-check at line 390. So this is four places,
  not two — either restore some CSV work or cut the whole thread.

- **Typos** (all re-verified 2026-08-20):
  - `2.2_System_Maps.qmd:232` — unclosed quotation mark on the Meadows blockquote
  - `Module-4---System-Expansion-and-Early-Evidence-(2-Weeks).qmd:65` — "You map must contain"
    (→ "Your"), and a doubled period ("minimum..")
  - `Module-5---Research-and-System-Refinement-(3-Weeks).qmd:48` — "the evolution of your amp"
    (→ "map"), "in you `.gv` file" (→ "your"), and "it's relationships" (→ "its")
  - `Module-3---System-Framing-and-Initial-Element-Selection-(3-Weeks).qmd:45` — sentence ends
    without a question mark ("...if this problem were solved")
  - `Syllabus.qmd:378` — missing period before "For now"
  - `2.1_Systems_Thinking.qmd:314` — "it's purpose" (→ "its"), in the paragraph above item 4

---

## Checked and clean

- **`_quarto.yml` navigation.** The sidebar mislabeling described in `CLAUDE.md` (Module 1
  pointing at `module-2-systems-thinking/`, an entry for a nonexistent
  `module-2-team-formation/`) is **no longer present**. Every nav path resolves to a file on
  disk. That note in `CLAUDE.md` is stale and could be removed.

- **No HTML comments anywhere** in the `.qmd` sources — no hidden `<!-- TODO -->` notes.

- **No TODO / FIXME / TBD / lorem ipsum markers** anywhere in the source.

- **Only two pages sit outside `_quarto.yml` nav:** `index.qmd` (expected — it's the site root)
  and `pubh115_course_modules.qmd` (item 8 above).

- **Internal links all resolve** except the one in item 3.

> Moved out of this section on 2026-08-20: the `_internal/` note, which is now open item 11 —
> the directory got committed rather than gitignored.

</details>
