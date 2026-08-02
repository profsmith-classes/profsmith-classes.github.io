# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This is a Quarto website for Professor Smith's undergraduate courses, published to GitHub Pages. The repo produces static course sites for two classes: **PUBH 115** (Introduction to Environmental Health and Safety) and **PUBH 402** (Introduction to the US Health Care System). Content is authored as `.qmd` (Quarto Markdown) files.

## Background Information

- PUBH 402 is an upper-level undergraduate course in a public health program using problem-based learning as the pedagological approach. 
- PUBH 115 is an introductry general education course.
- Both courses are online asynchronous classes. Students never meet together or with professor for online course sessions. The website must thus be extremely clear and supportive of self-guided learning. 

## Commands

- Preview locally with live reload: `quarto preview`
- Build the static site (outputs to `_site/`, gitignored): `quarto render`
- Publish to GitHub Pages: `quarto publish gh-pages` — this renders the site and pushes the output to the `gh-pages` branch, which is what GitHub Pages actually serves. There is no CI workflow for this; publishing is a manual, local step.

There is no linter or test suite in this repo — it's course content, not application code.

## Architecture

- `_quarto.yml` is the single source of truth for site structure: navbar, sidebar navigation tree, and HTML format/theme (sandstone theme, `styles.css`). Every new `.qmd` page must be added here to appear in navigation — a page existing on disk does not make it reachable in the site.
- Each course lives in its own top-level directory (`PUBH_115/`, `PUBH_402/`), with page files prefixed/named per course (e.g. `pubh115_*.qmd`). PUBH_402 further splits weekly content into `module-N-<topic>/` subdirectories, plus a `resources/` subdirectory for shared reference material (CSV/DOT/graphviz explainers, research resources).
- `.qmd` files use YAML frontmatter with fields like `title`, `date`, `draft`, `class` (course number as a string, e.g. `"402"`), and sometimes `sidebar`/`categories`. Follow the existing frontmatter shape when adding a new page.
- `saveit.yml` is a leftover/draft nav config not referenced by `_quarto.yml` — don't treat it as active configuration.
- Known drift to be aware of: the `_quarto.yml` sidebar for PUBH_402 currently mislabels/misroutes some module entries (e.g. "Module 1: Systems Thinking" points at the `module-2-systems-thinking/` directory, and one sidebar entry points at a `module-2-team-formation/` directory that doesn't exist). When editing navigation, verify `contents:` paths actually match the module directory names on disk.
- `_site/` and `.quarto/` are build artifacts (gitignored) — never hand-edit or commit into these; regenerate via `quarto render`/`quarto preview` instead.


## Specific Goals
1. Ensure the site remains easy to navigate and workign for students. 