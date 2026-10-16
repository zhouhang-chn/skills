---
name: repo-study
description: Investigate a repository's real implementation, dependencies, Git evolution, author rationale, independent evaluations, and reusable lessons. Use for studying, reverse-engineering, evaluating, or learning from a software or agent repository.
---

# Repo Study

**Goal:** Explain **what, how, why, evolution, evidence, limits, and transferable lessons**—not just the README. Match scope to the question: narrow requests follow relevant paths; deep studies complete the evidence loop.

1. **Pin scope and version.** Confirm repository/ref, head SHA and observation date. Inventory source tree, entrypoints, dependencies, docs, tests, examples, CI and releases. Distinguish public history from earlier/private development.
2. **Reverse-engineer the mechanism.** Trace `input → entrypoint → key modules/data and control flow → output`, reading implementation and import/config/runtime dependencies rather than trusting module names or docs. Walk through a real example. For large/inaccessible repos, prioritize and disclose uninspected areas.
3. **Verify behavior.** Inspect what tests, CI, audit scripts and demos actually check; safely execute only when feasible and relevant. Report commands and observed results. Never imply code ran, everything was read, or behavior was reproduced when it wasn't.
4. **Reconstruct changes** when relevant from early commits, tags, release notes, changelog, diffs, Issues, PRs and maintainer replies. Trace `failure/feedback → decision → change → validation/open problem`. Distinguish proposed, closed, and merged work; do not confuse launch with origin or popularity with quality.
5. **Cross-check outside the repo** when relevant: creator postmortems, independent reviews, real demos, comparisons, criticism and social discussion. Favor primary artifacts over reposts; qualify methodology, dates and sample sizes. Use `meta-research` for broad external discovery, not as a required subroutine.
6. **Synthesize causally.** Answer the user's goal with architecture, design rationale, evolution, strengths, failure modes, limitations and applicable patterns. Cite precise files/commits/PRs/issues/posts. Label **verified / reported / inferred / unknown**; separate the author's claims from independent evidence.

**Stop test:** Could a missing entrypoint, dependency, executable example, test, pivotal change, maintainer explanation or independent counterexample reverse a main conclusion? Investigate high-impact gaps, otherwise state uncertainty and stop when additional searching has low value.

Do not run untrusted code or change/publish to a repository without an appropriate purpose and authorization. Honor host-tool and citation rules.
