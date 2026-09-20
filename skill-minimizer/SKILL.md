---
name: skill-minimizer
description: Minimize a SKILL.md under the sufficient-and-necessary principle while preserving intended behavior.
---

# Skill Minimizer

## Goal

Reduce a skill to the smallest instruction set that preserves its intended behavior.

Optimize for **behavioral compression**, not tokens or line count. A rule is necessary only if removing or weakening it can materially change valid behavior, create ambiguity, or break a required contract.

## Process

### 1. Extract the contract

Identify what must survive:

- trigger and purpose
- required input/output behavior
- correctness, safety, or external constraints
- decision, tool, or ordering constraints
- hard prohibitions and meaningful exceptions
- domain/style behavior that differs from normal model behavior

Treat explanation, examples, templates, and repetition as evidence, not requirements.

### 2. Ablate

For each rule or section:

- Delete it if its removal does not change behavior.
- Delete or merge it if a stronger rule already implies it.
- Delete rationale unless it resolves ambiguity.
- Replace lists with a general invariant only when coverage is unchanged.
- Keep an example only when the rule is otherwise underspecified.
- Preserve any unique constraint before shortening its wording.

Prefer one rule over several only when they are behaviorally equivalent. Do not trade clarity for terseness or introduce new behavior while simplifying.

### 3. Test sufficiency

Check the reduced skill against:

- a normal case
- an ambiguous case
- an important edge case
- a tempting failure case

If intended behavior is no longer determined, restore the smallest missing constraint. Use existing evals when available.

Stop when every remaining instruction has a distinct behavioral job.

## Output

Preserve required frontmatter/host structure and return the minimized skill directly unless analysis or a change log is requested.
