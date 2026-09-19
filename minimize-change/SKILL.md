---
name: minimize-change
description: Ensure completed changes are sufficient and necessary before commit.
---

# Minimize Change

Minimize change scope, not line count. Preserve correctness and readability.

1. **Establish scope.** Read the task and acceptance criteria. Identify
   related staged, unstaged, and new files. Preserve unrelated work.

2. **Check sufficiency.** Confirm the requested behavior and documented
   usage, preserving required existing behavior. Resolve unclear contracts
   instead of accumulating exceptions for observed outputs. Passing tests
   alone does not establish completeness.

3. **Check necessity.** For each task-related change, ask:
   “Could this be omitted or narrowed without compromising requirements,
   correctness, readability, or verification?”
   If yes, remove or narrow it. Judge complexity across the whole change,
   including supporting code and dependencies. Avoid unrelated cleanup
   and speculative abstractions.

4. **Verify.** Review the final diff, including staged and new files.
   Run relevant checks against the changed boundaries; mocks alone do not
   establish integration success. Recheck affected behavior after edits
   and restore necessary changes if verification fails.

Never weaken requirements, tests, or safeguards merely to obtain a pass
or shrink the diff. Do not commit unless explicitly requested.

Report briefly: what changed during minimization, verification results,
and any unresolved gaps or checks not run.
