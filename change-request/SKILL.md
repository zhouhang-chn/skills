---
name: change-request
description: Turn a confirmed problem or proposed change in a software/project workflow into an evidence-grounded, self-contained, decision-ready Change Request. Use when asked to investigate, draft, refine, or review a CR, architecture pivot, or workflow change proposal; do not use for routine implementation tasks or open-ended research without a change decision.
---

# Change Request

**Goal:** Produce the smallest **decision-ready change contract** that explains *why to change, what to change, what to preserve, and how to know it worked*. A CR is a proposal for approval—not a research dump, implementation diary, or authorization to implement.

## Workflow

Apply these steps proportionally. Reuse sufficiently verified work already in context; do not repeat research or manufacture process artifacts merely to satisfy the sequence.

1. **Frame the decision.** Identify the trigger, affected system, intended outcome, decision owner if known, and scope. Ask whether a real change is necessary: would correcting a misunderstanding, updating a small document, or leaving the system unchanged solve the issue? If no substantive decision remains, recommend **no CR**.
2. **Ground the problem.** Inspect the minimum relevant current sources—implementation, contracts, tests, configuration, workflows, history, incidents, or user-provided evidence. Trace material dependencies and constraints, including what is actually enforced versus only documented. Distinguish **observed / reported / inferred / unknown**. Cite precise paths, revisions, or examples where possible; do not present a draft, external analogy, or stale plan as existing behavior.
3. **Explore the smallest viable change.** Separate the underlying responsibility or invariant from candidate APIs, tools, files, and frameworks. Compare at least **status quo**, **minimal targeted change**, and any materially different alternative. Evaluate benefit, complexity, migration, compatibility, risk, and reversibility. Avoid speculative abstraction, tool proliferation, and scope creep.
4. **Converge on a proposal.** State one recommended decision and its rationale. Specify **change / preserve / defer** and affected boundaries. Record meaningful rejected alternatives and unresolved choices. If evidence cannot support a choice, label it as a decision to resolve or an assumption to validate—do not invent consensus or claim approval.
5. **Write a self-contained CR.** Lead with the decision requested. Explain essential context and causal reasoning within the document; links support claims and give access to deeper evidence, not substitute for the argument. Write implementation-facing requirements and observable acceptance criteria without prematurely dictating low-level code or creating a detailed task diary.
6. **Critique and hand off.** Review the proposal for necessity, independent readability, impact, compatibility, risk, testability, and alignment with repository governance. Tighten or remove weak requirements. Return a draft for review unless publication or implementation was explicitly requested. A proposed CR does not change project status or authorize code changes.

## CR output contract

Use the following **content**, not a rigid section count. Adapt the headings and depth to the change:

- **Decision requested:** a one-paragraph proposal, status (`Proposed` unless genuinely approved), and affected scope.
- **Problem and evidence:** current behavior, concrete failure/constraint, root cause where supportable, and consequences. Separate facts from hypotheses.
- **Desired outcome and boundaries:** measurable goal, invariants, non-goals, and what explicitly remains unchanged.
- **Proposed changes and rationale:** required behavior/contracts, responsibilities, alternatives and trade-offs; distinguish existing interfaces from proposed ones.
- **Adoption and risks:** affected components/owners, compatibility or migration strategy, sequencing only where dependencies matter, rollback/mitigation as relevant.
- **Acceptance:** observable conditions and evidence surfaces for proving them, including regression safeguards and intentionally deferred work.
- **References:** concise sources/provenance, preferably grouped after the explanation. Link precisely where verification requires it.

A small CR may fit on one page. A cross-cutting architecture change may need more detail. Do not create additional research, design, implementation-plan, or checklist files by default. If the user wants a separate implementation plan, derive it **after** the decision is accepted or explicitly request it as a draft.

## Review gates

Before delivery, answer all six from the CR itself:

1. **Problem:** Is there an evidenced problem or an explicit change goal, rather than a preferred technology in search of a use case?
2. **Reasoning:** Why this choice over the status quo and the strongest alternative?
3. **Boundary:** What changes, stays, and is deferred—and who owns each responsibility?
4. **Truthfulness:** Are existing facts, proposed interfaces, assumptions, and approval/delivery states unmistakably distinct?
5. **Execution:** Could implementers carry out a bounded change without guessing major contracts or inventing extra scope?
6. **Acceptance:** Can reviewers disprove an unsupported completion claim through concrete checks, including preservation of existing behavior?

**Standalone test:** Hide hyperlinks and historical references. Can an unfamiliar reviewer still understand the problem, decision, rationale, constraints, and success condition? If not, repair the explanation, not the link list. Self-contained does **not** mean duplicating logs, schemas, or mutable status ledgers; keep their canonical ownership intact.

## Stop and failure rules

- **No sufficient evidence:** investigate high-impact gaps; otherwise issue a clearly qualified draft with explicit verification questions. Do not imply code was read, tests ran, or a proposal was validated if they were not.
- **No meaningful change decision:** report that a CR is unnecessary; suggest the smaller action.
- **Material alternatives unresolved:** surface the decision and recommendation; do not disguise uncertainty with implementation detail.
- **Out-of-scope implementation:** stop at a proposal unless explicitly asked to implement, commit, open a PR, or update governance. Never silently mutate the repository.
- **Historical decision records:** do not rewrite old rationales or turn planned work into delivered work; add a dated decision/update and point to canonical implementation evidence when a CR is later adopted.

**Handoff:** Summarize the proposed decision, the strongest supporting evidence, key trade-off, unanswered blocker (if any), and what action—review, approval, further investigation, or implementation—is actually next.
