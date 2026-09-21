---
name: x-post
description: Write or rewrite technical X posts in a concise, human, thinking-in-public style.
---

# X Post

## Goal

Write like a technical person thinking in public, not a content marketer.

Priority:
1. preserve the user's actual thought and technical meaning
2. use the shortest form that fully carries it
3. prefer mechanism, boundary, or observed result over generic importance
4. preserve uncertainty and useful roughness
5. polish only for clarity

Never make the thought sound smarter, more certain, or more complete than it is.

## Input

- **Draft:** preserve thesis, stance, terminology, uncertainty, numbers, and useful roughness; mostly delete and compress.
- **Source/link/screenshot:** keep only necessary context, then write the user's delta: interpretation, implication, question, or experiment. Do not mainly summarize.
- **Topic:** find the smallest non-obvious claim worth posting.

Follow the user's language. Keep established English technical terms when natural. No fixed target length.

## Style

Start from the observation or judgment. No article-style setup.

Choose the smallest structure that works:

```text
observation → inference
experiment → result → hypothesis / next step
source → interpretation → implication
claim → mechanism → example / contrast
current pattern → changed boundary → consequence
context → key question → possible paths
```

One useful sentence is enough.

Prefer concrete system behavior: who decides, what becomes code/rules, what stays probabilistic, where state/feedback/verification lives, what boundary moves, and what becomes the bottleneck.

For Agent/workflow topics, distinguish deterministic execution from model judgment when relevant. Use short pipelines when clearer than prose.

Use bullets only for real categories or steps. Use arrows, equations, parentheses, and numbers only when they carry information.

Keep natural uncertainty (`可能`、`看起来`、`感觉`、`似乎`、`应该`、`我的理解是`) when evidence is incomplete. Never invent certainty or numbers.

Uneven paragraphs, side thoughts, abrupt endings, and unresolved questions are allowed. Do not force a conclusion.

For source reactions, add at most one useful step beyond the source: a hidden constraint, changed boundary, engineering connection, workflow implication, verification need, or key question. If there is no real interpretation, prefer a short question or experiment note over invented insight.

Replies should normally be one or two sentences. Do not turn them into mini essays.

## Anti-AI pass

Remove:
- broad setup such as `随着……`
- generic importance claims and marketing language without mechanism
- `首先 / 其次 / 最后`, `核心洞察`, `关键启示`, `一句话总结`
- empty transitions, repeated summaries, slogan endings
- fake certainty and engagement bait such as `你怎么看？`
- decorative hashtags/emojis unless requested
- excessive `不是 A，而是 B`
- artificial symmetry or mandatory three-item lists
- source summary that outweighs the user's thought
- explanation added only to make the post feel complete

Prefer concrete behavior over abstract nouns and natural wording over editorial polish.

## Final check

Ask only:
1. What is the one thing this post says?
2. Can anything be deleted without losing it?
3. If source-based, what did it add?
4. Is certainty proportional to evidence?
5. Would a technical peer plausibly type this directly into X?

If anything can still be deleted, delete it.

## Output

Return only the finished post unless the user explicitly asks for analysis, alternatives, hashtags, or images.
