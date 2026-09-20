---
name: meta-research
description: Graph-guided research that expands beyond obvious keywords to discover missing entities, relations, time links, and evidence until important research frontiers are covered.
---

# Meta Research

Use this skill for deep research where missing a highly relevant source would materially weaken the result.

## Goal

Maximize **research coverage**, not search volume.

Search answers known queries. Graph expansion discovers the queries you did not know to ask.

## Input

- Research question
- Known entities or sources, if any
- Time / scope / source constraints, if any

## Method

### 1. Seed

Extract the initial research graph from the question:

- entities: product, person, team, company, institution, technology, concept, paper, repository, event, source
- relations: created_by, founded_by, works_at, worked_at, coauthored_with, mentored_by, built_on, inspired_by, preceded_by, competes_with, published_in, presented_at, discussed_in, evaluated_by
- time: before, after, contemporary, pre-launch, post-launch

Keep the ontology lightweight. Add a type or relation only when it can create a useful search direction.

### 2. Expand

Generate search frontiers through four complementary modes:

1. **Lexical** — names, aliases, terminology, exact phrases.
2. **Semantic** — underlying concepts, mechanisms, problems, alternatives.
3. **Relational** — connected people, teams, companies, collaborators, prior work, talks, papers, institutions.
4. **Temporal** — predecessors, pre-launch material, historical evolution, later follow-ups.

Do not expand every edge. Prefer edges that can change the interpretation of the research question.

### 3. Rank frontiers

Prioritize each candidate frontier by:

`relevance × source_potential × novelty × entity_importance ÷ graph_distance`

Prefer first-party and primary evidence when available.

Typical high-value paths:

- product → creator → prior talks / papers / posts
- company → team → prior work
- concept → predecessor / competing concept
- launch → pre-launch material
- claim → independent evaluation / criticism

### 4. Search and update

For each high-priority frontier:

- search
- retrieve the best evidence
- extract new entities, relations, claims, dates, and aliases
- update the graph
- create new frontiers only when they add plausible information value

Keep **claim → evidence** provenance explicit.

### 5. Coverage check

Do not ask “have I searched enough?” Ask “which important graph frontiers remain uncovered?”

Check relevant dimensions such as:

- product / artifact
- mechanism
- creator / team
- company / institution
- prior work / intellectual lineage
- pre-launch history
- competitors / alternatives
- independent validation
- criticism / failure cases
- temporal evolution

Only include dimensions relevant to the question.

### 6. Stop

Stop when both are true:

1. important frontiers are covered;
2. new expansions have low marginal information gain.

Do not continue through weak relations merely because the graph permits them.

### 7. Synthesize

Answer the research question, not the graph.

Distinguish:

- verified facts
- source claims
- inference
- unresolved uncertainty

Surface any source that materially changes the interpretation, even if it was found through an indirect relation.

## Failure modes

Avoid:

- keyword-only research
- treating launch date as the beginning of the idea
- over-expanding low-value relations
- counting documents instead of measuring coverage
- stopping after confirming an early hypothesis
- confusing lexical relevance with conceptual relevance
- mixing inference with sourced fact

## Minimal working loop

```text
question
  ↓
seed entities + relations + time
  ↓
lexical + semantic + relational + temporal expansion
  ↓
rank frontier
  ↓
search / retrieve evidence
  ↓
update graph
  ↓
coverage + saturation check
  ↺ until covered
  ↓
synthesis
```

## Final quality test

Before finishing, ask:

> What important source, entity, relationship, or earlier/later event could still change my interpretation?

If a plausible high-value frontier exists, research it before concluding.
