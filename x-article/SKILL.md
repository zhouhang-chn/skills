---
name: x-article
description: Turn existing project work, research, and judgments into a structured X Article. Use when preparing a serious long-form X article from material that already exists. Optimize for a clear thesis, evidence-backed structure, human voice, and visual explanation rather than generic AI prose.
---

# X Article

## Goal

Turn existing work into a publishable X Article.

Do not create a new research project just to produce content. Prefer material that already exists in:
- current projects
- recent decisions
- validated judgments
- implementation experience
- real failures
- external evidence already collected
- diagrams, artifacts, skills, workflows, benchmarks, or user feedback

The article should compress existing work into a reusable public knowledge asset.

## State

Use only:

`Idea -> Selected -> Preparing -> Ready -> Published -> Resurfaced`

Publishing is the first external evidence.
Drafts, diagrams, research, and outlines are internal outputs only.

## Inputs

Minimum:
- topic
- why it matters now
- existing source material

Useful optional inputs:
- project artifacts
- previous chats
- code / git history
- external references
- diagrams
- examples / counterexamples
- desired audience
- tone reference

## Workflow

### 1. Lock the thesis

Write one sentence that contains an actual judgment.

Good:
- `X-to-Skill is better understood as the input side of a Capability Compiler.`
- `The important boundary in agent systems is not model vs tool, but capability authoring vs capability consumption.`

Weak:
- `This article explores X-to-Skill.`
- `AI agents are changing software development.`

If the thesis is still generic, do not draft the article yet.

### 2. Build the evidence map

Before writing, list:
- what is already known
- what is directly observed
- what is externally verified
- what is inference
- what is still missing

For research-heavy technical articles, make this an explicit research brief with four labels:

`verified fact / source claim / inference / unknown`

Keep claim -> evidence provenance explicit.

Prefer existing evidence.
Research only the missing pieces required to support the thesis.

Use `meta-research` when missing a highly relevant source, entity, relationship, predecessor, or later development could materially change the interpretation.

Stop research when the thesis can be defended with concrete mechanisms, examples, and at least one counterpoint or boundary condition.

Do not silently turn an inference into an implementation claim. If an engineering abstraction such as `event sourcing`, `compiler`, `materialized view`, or `retrieval` is useful but not confirmed by the source, label it as an analogy or model.

### 3. Find the article's structural spine

Choose one dominant structure.

Preferred structures:
- architecture flow
- causal chain
- lifecycle
- before -> after
- source -> compiler -> runtime
- problem -> mechanism -> evidence -> implication

For architecture-heavy topics, create the overall diagram before writing the full body.

The article should then walk through that structure in order.

Example:

`Source -> Adapter -> Evidence -> Capability IR -> Validation -> Registry -> Runtime -> Execution Evidence -> Recompile`

Avoid a collection of loosely related sections.

### 4. Design the section sequence

Default to 5-7 sections, but let the argument determine the count.

Each section should answer at least three of these:
- What is this?
- Why is it needed?
- What mechanism makes it work?
- What evidence supports it?
- What changes because of it?
- What remains unresolved?

Start from the concrete problem or observation, then move upward into the model.

Do not begin with a long abstract introduction.

Keep interesting but non-essential extrapolations out of the main line. If a section does not strengthen the thesis, explain a necessary mechanism, establish evidence, or improve the ending, cut it.

### 5. Write in a human technical voice

Preferred style:
- start from a concrete observation
- use short declarative sentences
- mix Chinese with precise English technical terms naturally
- make judgments, but leave room where evidence is incomplete
- prefer mechanisms over slogans
- prefer examples over abstract praise
- prefer "I noticed / the interesting part is / the real boundary is..." over polished report language when appropriate

Avoid:
- "随着..."
- "赋能..."
- "全面提升..."
- "智能化升级..."
- generic "first, second, finally" scaffolding
- excessive rhetorical symmetry
- repeated conclusions
- paragraphs that sound complete but add no new mechanism or evidence

Use assertions over narration.

Bad:
`This approach can greatly improve the efficiency and intelligence of enterprise agents.`

Better:
`The important change is that validation moves out of model judgment and into the capability lifecycle.`

### 6. Use diagrams as part of the argument

Plan visuals before generating them.

For each visual, write:
- the reader question it answers
- the one concept it must explain
- where it belongs in the article
- whether it is a cover, overall map, or local mechanism diagram

Default visual pattern for a technical X Article:
- one cover image
- one overall architecture / concept map near the beginning when useful
- local mechanism diagrams only where prose alone is weaker

Use `visual-story` for the cover or narrative image.
Use `visual-explain` for architecture, process, comparison, state, or evidence diagrams.

Generate article visuals one by one. Do not combine multiple planned figures into one collage unless the article explicitly needs a single multi-panel figure.

A local diagram should explain the current section rather than summarize the whole article.

Good local diagrams:
- lifecycle transition
- source-to-skill compilation path
- authoring vs runtime boundary
- before/after architecture
- evidence loop
- step-level workflow
- temporal state update
- policy / permission gate
- state -> summary / retrieval split

A diagram should communicate one concept clearly:
- minimal crossing lines
- obvious hierarchy
- enough whitespace
- readable labels
- no decorative complexity

Do not put section numbers into image titles by default. Article sections may move during editing; visual titles should remain semantically valid.

### 7. Draft section by section

Do not write the entire article in one pass if the topic is structurally complex.

Recommended loop:

`thesis -> evidence map -> overall structure -> section 1 -> review -> section 2 -> review -> ...`

After each section, check:
- Did it advance the thesis?
- Did it add a mechanism, example, or evidence?
- Is there unnecessary repetition?
- Does the next section follow naturally?
- Does this section need a diagram?

### 8. Run a compression pass

After the full draft exists, edit for article density rather than completeness.

Remove:
- repeated explanations of the same architecture
- repeated disclaimers once the evidence boundary is already clear
- side branches that are interesting but not necessary
- English labels that have a natural Chinese equivalent and add no precision
- conclusion-like sentences repeated at the end of several sections
- sections that only make the article look comprehensive

Prefer one strong concrete example over several abstract explanations.

If a pipeline can be expressed naturally in Chinese, prefer Chinese while retaining technical terms where translation would reduce precision.

### 9. End by moving one level up

The ending should not merely summarize the article.

Prefer one of:
- a higher-order model
- a reusable principle
- an architectural implication
- a new boundary
- the next question the model exposes

Example:
`Book-to-Skill is not the destination. It is one input adapter into a broader Capability Compiler.`

A strong ending often returns to the opening observation and shows why it now means something different.

The final section should make the reader see the earlier material differently.

### 10. Prepare the publishing package

Before moving `Preparing -> Ready`, prepare the article as it will actually be published.

Include:
- title
- article description
- cover image
- body
- body visuals
- insertion points
- source links / citations as needed
- optional launch post

For X Article publishing, treat UI constraints as observed product constraints unless X documents them officially.

Current observed constraints from the editor:
- cover image: design for approximately `5:2`
- article description: keep within `256 characters`

These may change. Re-check the editor when publishing rather than treating them as permanent platform guarantees.

Keep critical cover text and visuals inside a central safe area because crops can vary across surfaces.

If a launch post is needed after the article is finished, use `x-post` to produce the teaser. Do not let short-post conventions determine the long-form article structure.

## Article template

Use this only as a default, not a rigid format.

1. Concrete observation / trigger
2. The key judgment
3. Overall diagram
4. Mechanism / architecture
5. Why the obvious alternative is insufficient
6. Evidence / example / counterexample
7. Higher-order model
8. Implication / next question

## Preparing checklist

Before moving `Preparing -> Ready`, verify:

- [ ] Thesis is one sentence and non-generic
- [ ] Existing work is the primary source
- [ ] Facts, source claims, observations, inference, and unknowns are distinguishable where relevant
- [ ] Claim -> evidence provenance is clear for important factual claims
- [ ] Article has one structural spine
- [ ] Overall diagram exists if the topic is architecture-heavy
- [ ] Each visual answers one reader question
- [ ] Visuals are generated separately unless a multi-panel figure is intentional
- [ ] Image titles do not depend on unstable section numbering
- [ ] Each section advances the thesis
- [ ] No section exists only to sound complete
- [ ] No major claim depends on invented evidence
- [ ] Research has stopped once sufficient
- [ ] Compression pass removed repeated mechanisms and side branches
- [ ] Ending moves to a higher-order model or implication
- [ ] Publishing package includes title, description, cover, visuals, and insertion points
- [ ] Current X editor constraints have been re-checked if publishing now

## Final editing pass

Remove:
- generic AI phrasing
- repeated conclusions
- empty transition sentences
- excessive headings
- claims stronger than the evidence
- unnecessary background the target reader likely knows

Tighten:
- opening
- thesis
- section transitions
- diagram captions
- article description
- final higher-order conclusion

Keep:
- concrete observations
- technical precision
- useful ambiguity where evidence is incomplete
- distinctive judgments
- examples from real work

## Output

When asked to prepare an article, produce in this order:

1. `Thesis`
2. `Research Brief / Evidence Map`
3. `Structure`
4. `Visual Plan`
5. `Draft` or section-by-section draft
6. `Publishing Package`
7. `Ready Checklist`

When the user asks only for the next step, do not automatically generate the full article.

## Success criteria

A good X Article should:
- expose a real judgment
- be rooted in actual work
- teach a reusable mechanism
- contain enough evidence to be credible
- keep fact and inference boundaries visible
- be visually self-explanatory
- sound like a technically opinionated human wrote it
- survive compression without losing the thesis
- be ready for the actual X publishing surface
- create an asset that can be resurfaced later
