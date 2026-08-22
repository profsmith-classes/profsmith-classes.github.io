# WCAG 2.1 Level AA Audit — profsmith-classes.github.io

**Date:** 2026-08-19
**Scope:** 34 `.qmd` source pages and the corresponding local `_site/` build (Quarto website, `superhero` Bootswatch theme).
**Method:** static analysis of source, rendered HTML, and the shipped CSS cascade; contrast ratios computed from actual resolved color values.

**Not covered:** no browser or assistive technology was available in this environment, so runtime behavior (search overlay, sidebar toggles, footnote tooltips, the Vimeo player UI) was assessed statically, and caption/transcript availability on Vimeo and YouTube could not be checked directly.

---

## Critical

### 1. Code blocks are invisible — 1.4.3 Contrast (Minimum), AA
Contrast **1.00:1**. Required 4.5:1.

The cascade resolves to light-gray text on a light-gray box:

- `pre { background-color: #ebebeb; color: inherit }`
- `pre code { background-color: transparent; color: inherit }`
- body color is `#ebebeb`

So the text color and the background are the same value. Quarto ships an override for inline code (`p code, li code, td code`) that swaps in a dark background, but nothing corrects `<pre>`.

Affected — 8 blocks, all core PUBH 402 technical instruction:

| Page | Blocks |
|---|---|
| `PUBH_402/resources/DOT-Explainer.qmd` | 5 |
| `PUBH_402/resources/CSV-Explainer.qmd` | 2 |
| `PUBH_402/resources/Coffee-Shop-Example-Graphviz.qmd` | 1 |

These are the pages that teach students to write `.gv` files. The example code is currently unreadable for everyone, not only users with low vision.

### 2. Inline `code` inside headings is invisible — 1.4.3, AA
Contrast **1.00:1**.

The Quarto override only covers `code` inside `<p>`, `<li>`, and `<td>`. Inline code in a heading falls back to `background-color: #ebebeb` with `color: inherit`, and `--bs-heading-color: inherit` resolves to `#ebebeb`.

8 instances (1 × `h1`, 5 × `h2`, 2 × `h3`), including the DOT Explainer's own page heading, which begins with an invisible `.gv`:

- `<h1><code>.gv</code> Files and Graphviz: An Overview and Resources`
- `<h2>What a <code>.gv</code> File Is`
- `<h2>Why This Course Uses <code>.gv</code> files`
- `<h2><code>.gv</code> File Notation: Comments, Labels, and Formatting`
- `<h2>Tools for Working with <code>.gv</code> Files`
- `<h2>2. Graphviz <code>.gv</code> file`
- `<h3>Positive Polarity (<code>+</code>)`
- `<h3>Negative Polarity (<code>-</code>)`

The last two are worth singling out: the `+` and `-` polarity notation is the whole point of that section, and both symbols are invisible.

### 3. Focus indicator is effectively invisible — 2.4.7 Focus Visible (AA) and 1.4.11 Non-text Contrast (AA)
Bootstrap suppresses the native outline (`outline: 0`) and substitutes a 25%-opacity orange glow, `box-shadow: 0 0 0 .25rem rgba(223,105,25,.25)`.

| Context | Ratio vs. adjacent color | Required |
|---|---|---|
| Focus ring on page background `#0f2537` | 1.35:1 | 3:1 |
| Focus ring on navbar background `#df6919` | 1.00:1 | 3:1 |

On the navbar the ring color is the navbar background color, so keyboard focus on the three primary course links produces no visible change at all. For fully asynchronous courses where the site is the only navigation surface, keyboard-only students have no way to tell where they are.

### 4. Navbar text fails contrast — 1.4.3, AA
`#fffefd` on `#df6919` = **3.38:1**. Required 4.5:1.

This affects the site brand and all three top-level course links. Note the brand is set to `1.1rem` (17.6px) in `styles.css`, just under the 18.66px threshold for large text, so it does not qualify for the relaxed 3:1 ratio either.

### 5. Six video iframes have no accessible name — 4.1.2 Name, Role, Value, A
The `{{< video >}}` shortcodes in `PUBH_402/module-2-systems-thinking/2.1_Systems_Thinking.qmd` (lines 103, 110, 117, 140, 154, 264) render as `<iframe ... title="">`. An empty `title` gives screen reader users nothing to identify the embed.

The one hand-written iframe on the same page (line 13) does have a real title, `"2026 01 05 System Thinking Overview"` — so the fix is to supply a title on the shortcodes too.

### 6. Video captions and transcripts unverified — 1.2.2 Captions (A), 1.2.5 Audio Description (AA)
Seven Vimeo embeds on `2.1_Systems_Thinking.qmd`, plus video and film references in `PUBH_115/pubh115_course_materials.qmd` (Vimeo, YouTube, Kanopy, 60 Minutes).

Nothing in the source provides a transcript, caption track, or text alternative alongside any of them. Whether captions exist on the Vimeo side could not be checked from here — **this needs manual confirmation** and is the highest-stakes item on this list for a CSU course, given Section 508 and CSU accessible-technology policy.

### 7. A published page has no title and no content — 2.4.2 Page Titled, A
`_site/PUBH_115/pubh115_course_modules.html` renders as an empty document: `<html lang="en"></html>` — no `<title>`, no body.

Cause: `draft: true` in the frontmatter. The page is absent from `_quarto.yml` navigation, so it is not linked, but it is still published and reachable by direct URL.

---

## Moderate

### 8. Heading levels are skipped — 1.3.1 Info and Relationships, A

| Page | Skip |
|---|---|
| `PUBH_402/module-2-systems-thinking/2.1_Systems_Thinking.qmd` | h1 → h3 |
| `PUBH_402/module-4-system-expansion/Module-4---System-Expansion-and-Early-Evidence-(2-Weeks).qmd` | h1 → h3 (×3) |
| `PUBH_402/module-6-interpretation-leverage/Module-6---Interpretation-and-Leverage-(2-Weeks).qmd` | h2 → h4 (×2) |
| `PUBH_402/resources/Research-Resources.qmd` | h1 → h3 |

### 9. Flat heading outline — 1.3.1, A (structural weakness)
Every page uses `#` for its top-level sections, which renders as `<h1>` in addition to the title `<h1>`. Result: 5–15 `<h1>` elements per page (Syllabus and Tips both have 15).

Not a hard failure on its own, but it removes the document hierarchy that screen reader users rely on to skim a long page by heading level. On a 15-section syllabus in an asynchronous course, that matters.

### 10. Graphviz diagrams have no programmatic text alternative — 1.1.1 Non-text Content, A
The 9 inline SVGs on `2.2_System_Maps.qmd` carry no `role="img"`, no `aria-label`, and no `<title>` child element.

Substantially mitigated: each is wrapped in `<figure>` with a genuinely descriptive `<figcaption>`, which is good practice and carries most of the meaning. Two gaps remain:

- Without `role="img"`, assistive technology walks into the SVG and reads its loose internal text nodes — "Content Visibility", "User Engagement", "+" — in DOM order, with no indication of which element points at which.
- Figures 8 and 9 ("A thermostat balancing loop", "A surveillance reinforcing loop") have captions that state the loop *type* but never name the elements or the links, so the actual diagram content is unavailable in text.

### 11. Diagrams force horizontal scrolling — 1.4.10 Reflow, AA
All 9 SVGs are emitted at `width="672" height="480"` with inline `style="max-width: none; max-height: none"`, and no stylesheet constrains them. At a 320 CSS px viewport — or at 400% zoom, which is what the success criterion actually tests — the page scrolls in two dimensions.

### 12. Red edge label fails contrast — 1.4.3, AA
In `fig-connection-highlight` (`2.2_System_Maps.qmd:77`), the `+` label is drawn in `red` at 14px on the white diagram canvas: **4.00:1**, required 4.5:1.

The red *arrow* itself is fine — as a graphical object it needs only 3:1, and it reaches 4.00:1.

### 13. Sidebar and TOC contrast, marginal failures — 1.4.3, AA
Computed against the resolved sidebar background `rgb(24,42,57)`:

| Element | Ratio | Required | |
|---|---|---|---|
| TOC active / hover link `#df6919` | 4.32:1 | 4.5:1 | fail |
| Disabled sidebar item (75% `#ebebeb`) | 4.46:1 | 4.5:1 | fail |
| Sidebar footer `#6c757d` | 3.13:1 | 4.5:1 | fail |
| `--bs-tertiary-color` (50% `#ebebeb`) | 4.33:1 | 4.5:1 | fail |
| Sidebar nav items `rgb(169,177,183)` | 6.76:1 | 4.5:1 | pass |
| Sidebar active item `#ea9c67` | 6.61:1 | 4.5:1 | pass |

The TOC one is the practical concern: the active table-of-contents entry is the page-position cue, and it is the one that fails.

---

## Advisory

### 14. Non-descriptive link text — 2.4.4 Link Purpose (In Context), A
Three links whose text does not convey destination out of context:

- `PUBH_402/resources/DOT-Explainer.qmd:141` — "example"
- `PUBH_402/resources/DOT-Explainer.qmd:188` — "overview"
- `PUBH_115/pubh115_grading_policy_assignments.qmd:109` — "policy"

Each is understandable from the surrounding sentence, so this likely passes as written; it fails the stricter 2.4.9 (AAA). Worth fixing anyway, since screen reader users often pull up a links list stripped of context.

### 15. No skip link — 2.4.1 Bypass Blocks, A
There is no "skip to content" link. This **passes** via the ARIA landmark technique — Quarto emits `<header>`, `<nav>`, and `<main id="quarto-document-content">`.

Still worth adding: the sidebar carries 40+ links and repeats on all 34 pages, so keyboard users tab through the entire course tree before reaching content on every single page.

### 16. Color as a highlight cue — 1.4.1 Use of Color, A
`fig-connection-highlight` uses red as the sole visual means of marking the highlighted edge. The caption explains what is being shown, so this passes, but the pattern is fragile if reused without an equally explicit caption.

---

## Conforming

Verified as passing, worth recording so they are not disturbed by later edits:

- **3.1.1 Language of Page** — `lang="en"` present on all 34 rendered pages.
- **1.4.3 body text** — `#ebebeb` on `#0f2537` = 13.14:1.
- **1.4.3 body links** — `#eca575` on `#0f2537` = 7.62:1; hover 8.87:1.
- **1.4.1 links** — underlined by default, not distinguished by color alone.
- **1.1.1 images** — the site uses no `<img>` elements at all, so there are no missing `alt` attributes.
- **1.3.1 tables** — all 8 pipe tables include header rows and render real `<th>` cells.
- **2.4.2 page titles** — unique and descriptive on all pages except the draft noted in item 7.
- **1.3.1 landmarks** — `<header>`, `<nav>`, `<main>` present; breadcrumb nav is `aria-label`ed.
- **1.4.3 diagram internals** — black on `lightblue` nodes = 13.74:1; black on white canvas = 21.00:1.
- **1.4.10 tables** — wide data tables may scroll horizontally, which the success criterion explicitly permits for two-dimensional content.

---

## Suggested order of work

1. **Items 1 and 2** — one small block of CSS in `styles.css` fixes both, and they are outright blockers on the pages that teach the course's core technical skill.
2. **Item 6** — confirm captions on all seven Vimeo videos and both PUBH 115 video sets. Highest legal exposure; longest lead time if captions turn out to be missing.
3. **Items 3 and 4** — theme-level contrast. Both trace to the `superhero` palette; a handful of CSS overrides addresses them without changing themes.
4. **Item 5** — add `title` to the six video shortcodes.
5. **Items 8, 10, 11** — content and figure fixes, page by page.
6. **Item 7** — decide whether the draft page should be excluded from render entirely.

Items 1, 2, 3, 4, and 13 are all fixable from `styles.css` alone, without touching any `.qmd` content.

---

## Status — updated 2026-08-20

Items **1, 2, 3, 4, and 13** were addressed in `styles.css`. No `.qmd` content was touched.

**Correction to item 1.** The finding is withdrawn. This audit resolved `pre` to Bootstrap's
`pre{color:inherit;background-color:#ebebeb}` (offset 9113 of the theme bundle) and missed a later
top-level Quarto rule, `pre{background-color:initial;padding:initial;border:initial}` (offset 443540),
which is equal specificity, sits in no at-rule context, and therefore wins. `pre` background resolves
to `transparent`, so code-block text is #ebebeb on #0f2537 = **13.14:1 — passing**, not 1.00:1.
Re-verified against a fresh `quarto render`; the `_site/` build this audit read was partly stale.

That rule does strip `padding` and `border` from `pre`, so the examples had no visual container.
`styles.css` restores one (#ebebeb on rgb(35,55,71) = 10.31:1). That is a readability change, not a
conformance fix.

**Item 2** — confirmed and fixed. `code` is now styled globally to the same chip Quarto already
applied inside `<p>`/`<li>`/`<td>`, with `pre code` handing colour back to the block.
#ebebeb on rgb(44,63,78) = 9.14:1. Covers all 8 heading instances.

**Item 3** — fixed. The 25%-opacity glow is replaced by a 3px white outline plus an `#0b1b28` halo,
so one ring always contrasts: white is 15.67:1 on the page and 5.67:1 on the navbar; the halo is
17.48:1 against the white ring and 3.08:1 on the navbar. Applied via `:root :focus-visible` (0,2,0),
which outscores `.nav-link:focus-visible`, plus a higher-specificity rule for the search widget,
which suppressed focus styling at (1,4,0).

**Item 4** — fixed by darkening the bar to `#a84c0d` rather than changing text colour; #fffefd on it
is **5.63:1**. Jason chose this over keeping #df6919 with dark text. `--bs-navbar-hover-color` was
80%-opacity white, which would have landed at 4.19:1 on the darker bar, so hover is now fully opaque
(5.67:1) and underlined.

**Item 13** — all four fixed, measured on #0f2537:

| Element | Was | Now |
|---|---|---|
| TOC active / hover | #df6919, 4.32:1 | #f0a878, 7.89:1 |
| Disabled sidebar item | 75% opacity, 4.45:1 | 85% opacity, 5.58:1 |
| Sidebar footer | #6c757d, 3.13:1 | #a0aab2, 6.63:1 |
| `--bs-tertiary-color` | 50% opacity, 4.33:1 | 70% opacity, 7.11:1 |

Every override was confirmed to win the cascade by resolving all competing rules across the syntax
highlighting sheet, the theme bundle, and `styles.css` in load order.

**Still open:** items 7, 8, 9, 10, 12, 14, 15, 16. Item 6 is largely closed — see the item 6
update below. Items 5 and 11 were fixed on 2026-08-21 — see the update below that.

**Noticed while fixing, not previously listed:** the breadcrumb separator on the mobile secondary nav
(`.breadcrumb-item::before`, hsl(207,9%,49%) ≈ #74818b) is 1.42:1 on the darkened bar and was 1.63:1
on the original orange. It is decorative punctuation between breadcrumb links, so it is arguably
exempt under 1.4.1, but it is effectively invisible either way.

### Item 6 update — 2026-08-20

Jason confirmed **all videos are captioned**. That satisfies **1.2.2 Captions (Prerecorded), Level A**
for the seven Vimeo embeds on `2.1_Systems_Thinking.qmd` and the PUBH 115 media list. This was the
highest-exposure finding in the audit and it is now closed.

Captions do not by themselves close the other two criteria the original item bundled together:

- **1.2.3 Audio Description *or* Media Alternative (Prerecorded), Level A** — needs audio description
  **or** a full text alternative. Captions cover dialogue, not visual-only content, so this is
  satisfied only where a transcript exists or nothing meaningful is shown that the narration does not
  also say.
- **1.2.5 Audio Description (Prerecorded), Level AA** — strictly requires audio description, and only
  bites where the video carries information visually that the audio never states.

Practically, for narrated lecture video this is usually satisfied trivially. The exception worth a
spot check is the four loop-drawing videos at lines 103, 110, 117 and 264, which demonstrate *how to
draw* balancing loops, reinforcing loops, delays and system change. If the narration says aloud what
is being drawn ("an arrow from congestion back to number of cars, negative polarity"), both criteria
are met. If the drawing is silent or narrated only as "like this", the visual content is unavailable
to a student who cannot see it, and a short transcript or written walkthrough would close the gap.
Note that `2.2_System_Maps.qmd` already provides written diagram walkthroughs those videos link to,
which may serve as the media alternative.

Item 6 is therefore reduced from a blocking finding to a targeted question about four videos.

### Items 5 and 11 update — 2026-08-21

**Item 5 — fixed.** The six `{{< video >}}` shortcodes on `2.1_Systems_Thinking.qmd` now carry a
`title` naming what the video covers: balancing feedback / congestion, reinforcing feedback /
induced demand, delays and structural change, institutions and power as structure, analytic vs.
systems thinking, and systems change. Verified in a fresh render — zero iframes sitewide are left
with an empty or missing `title`, counting the seventh hand-written embed that always had one.

**Item 11 — fixed.** `styles.css` now constrains figure SVGs:

```css
.cell-output-display svg,
figure svg { max-width: 100% !important; height: auto !important; }
```

`!important` is required because the override target is an inline `style="max-width: none"`, which
outranks any selector but not an author `!important` declaration. `height: auto` lets the `viewBox`
scale the drawing rather than distorting it. Scope checked against the build: the site contains
exactly 10 inline SVGs, all of them Graphviz figures on `2.1_Systems_Thinking` and `2.2_System_Maps`,
and all 10 sit inside a wrapper the selector matches. No UI chrome is affected.

This does not touch item 10 — the same figures still have no `role="img"`, `aria-label`, or `<title>`,
and figures 8 and 9 still need descriptions written.
