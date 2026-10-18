---
name: change-request
description: Draft or review concise change requests handed to a Coding Agent, preserving explicit actions, responsibility boundaries, and verifiable outcomes without prescribing implementation.
---

# Change Request

A CR transfers **intent and required outcomes** from outside a Coding Agent; the Coding Agent independently reality-checks the current repository, chooses the implementation, and verifies it. Distinguish an **execution request** (direction decided) from a **decision proposal** (direction undecided). Never downgrade a concrete execution request into an invitation to clarify or assess.

## Workflow

1. **Extract intent:** target, explicit must-do operations, desired result, relevant dependencies/consumers, preserved capabilities, and decisions delegated to the Coding Agent. Named operations (e.g., *remove X*) must survive summarization.
2. **Establish boundaries and sequence:** identify ownership/invariants when relevant; order dependent work logically (e.g., establish principles → review violations → fix violations). Reviewing is not a substitute for fixing when a fix was requested.
3. **Ground selectively:** use available context and inspect only material unknowns. Separate observations from assumptions. Require the Coding Agent to recheck mutable technical facts rather than copying extensive research into the CR.
4. **Write the request:** lead with concrete operations on named targets. State mandatory fixes; leave other technical solutions to the Coding Agent. Bound review/remediation to the target and relevant dependency chain, not the entire repository unless requested.
5. **Minimize:** include only context needed to preserve intent, resolve ambiguity, or constrain risk. Do not implement, commit, or publish unless requested.

## Default output

For a recipient with repository access/context, prefer a short CR (typically 100–200 words); expand only when necessary. No mandatory section count.

- **Scope:** target, relevant dependencies/consumers, exclusions.
- **Actions:** ordered changes; retain each explicitly required operation. State whether findings from a review must be fixed or merely reported.
- **Constraints:** what cannot regress, ownership boundaries, non-goals.
- **Acceptance:** observable resulting state and verification evidence.
- **Handoff:** Coding Agent reality check → implementation choice → changes → verification.

For undecided proposals, add the decision and minimal evidence/trade-offs. **Self-contained** means the request is understandable without prior chat, not that it reproduces source code, investigation, or mutable repository facts.

## Final check

- Is there a concrete **operation + target + expected result**, not just “clarify/optimize/refactor”?
- Are explicit must-do changes retained, with prerequisites → review → remediation correctly ordered?
- Is review scope bounded by relevant dependencies, and is the disposition of findings clear?
- Are required outcomes separate from suggested implementation details?
- Can the Coding Agent verify completion without weakening existing safeguards?
- Can any sentence be deleted without changing the handoff? If yes, delete it.