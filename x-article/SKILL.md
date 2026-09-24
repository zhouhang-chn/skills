---
name: x-article
description: Turn existing project work, research, and judgments into a publishable long-form X Article with a clear thesis, evidence boundaries, technical voice, and purposeful visuals.
---

# X Article

## Goal

Compress existing work into a publishable X Article and reusable public knowledge asset.

Prefer material that already exists: project work, decisions, implementation experience, failures, artifacts, benchmarks, diagrams, user feedback, and previously collected evidence. Do not start a new research project merely to produce content.

Use this state model only when tracking article lifecycle:

`Idea -> Selected -> Preparing -> Ready -> Published -> Resurfaced`

Publishing is the first external evidence; drafts and internal artifacts are not.

## Workflow

### 1. Lock the thesis

Write one sentence containing a real, non-generic judgment. Do not draft until the article has a defensible thesis.

### 2. Bound the evidence

For important claims, distinguish:

`verified fact / source claim / direct observation / inference / unknown`

Keep claim -> evidence provenance clear. Prefer existing evidence and research only missing pieces needed to support the thesis.

Use `meta-research` when an uncovered source, entity, relationship, predecessor, or later development could materially change the interpretation.

Stop research when the thesis is supportable with concrete mechanisms, examples, and a relevant boundary or counterpoint.

Never present an engineering analogy or inferred implementation as confirmed fact.

### 3. Choose one structural spine

Organize the article around one dominant progression such as:

`architecture flow / causal chain / lifecycle / before -> after / problem -> mechanism -> evidence -> implication`

Start from a concrete observation or problem and move upward into the model. Cut interesting branches that do not strengthen the thesis, explain a necessary mechanism, establish evidence, or improve the ending.

For architecture-heavy topics, define the overall diagram before drafting the body.

### 4. Plan the visuals

Each visual must answer one reader question and explain one concept.

Typical set:
- one cover
- one overall map when useful
- local mechanism diagrams only where prose is weaker

Use `visual-story` for cover or narrative visuals and `visual-explain` for architecture, process, comparison, state, or evidence diagrams.

Generate figures one by one. Do not combine planned figures into a collage unless a multi-panel figure is intentional.

Keep visual titles independent of section numbering so article sections can move without invalidating the image.

### 5. Draft in a human technical voice

Prefer:
- concrete observation before abstraction
- mechanisms and examples over slogans
- short declarative prose
- precise technical terms, including English when translation loses precision
- uncertainty proportional to evidence

Avoid generic AI/marketing language, ornamental symmetry, empty transitions, repeated conclusions, and background the target reader already knows.

For complex topics, draft section by section and review whether each section advances the thesis with mechanism, evidence, or example.

### 6. Compress

After the full draft exists, remove:
- repeated mechanisms or conclusions
- repeated disclaimers once the evidence boundary is clear
- side branches that are interesting but unnecessary
- sections that exist only for completeness
- English labels that add no precision when natural Chinese is clearer

Prefer one strong concrete example over several abstract explanations.

### 7. End one level up

Do not merely summarize.

End with a reusable principle, architectural implication, higher-order model, new boundary, or next question supported by the article. Returning to the opening observation is useful when it now means something different.

### 8. Prepare the publishing package

Before `Preparing -> Ready`, produce:
- title
- article description
- cover
- body
- body visuals
- visual insertion points
- source links/citations where needed
- optional launch post

Treat X editor UI limits as observed constraints unless officially documented. Current observed constraints:
- cover: design around `5:2`
- description: keep within `256 characters`

Re-check these when publishing because the UI can change. Keep critical cover content inside a central safe area.

If a launch post is needed, use `x-post` after the article is finished; do not let short-post conventions shape the long-form structure.

## Ready contract

An article is ready only if:
- the thesis is specific and defensible
- existing work remains the primary source
- important fact/inference boundaries and provenance are visible
- one structural spine holds the article together
- every section advances the thesis
- every visual has a distinct explanatory job
- unsupported or overly strong claims are removed
- research stopped once sufficient
- a compression pass removed repetition and side branches
- the ending adds a higher-order implication
- title, description, cover, visuals, and insertion points are ready for X

## Output

When preparing a full article, return in this order:

1. `Thesis`
2. `Research Brief / Evidence Map`
3. `Structure`
4. `Visual Plan`
5. `Draft`
6. `Publishing Package`
7. `Ready Check`

If the user asks only for the next step, return only that step.
