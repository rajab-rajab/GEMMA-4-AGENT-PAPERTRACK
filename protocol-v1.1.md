# Experiment protocol v1.1 - planning, before agent runs

Research question: Can a typed evidence graph improve Gemma 4 E4B Q4_0 bug repair relative to ordinary search, holding model, tools, context, and budgets fixed?

## Scope

15 total issues: 3 pilot (P1 PySnooper, P2 tqdm, P4 HTTPie) and 12 held-out evaluation issues. P3, P5, and P6 are eligible evaluation candidates, but the 12-case list must be completed and frozen before the first pilot-driven method change. These six candidates were screened for red/green reproducibility only; no agent model has attempted any. Select nine further cases across additional repositories and issue years. Log all exclusions before agent runs. This is an exploratory study; report issue-level outcomes and uncertainty.

## Conditions

A: Issue text, ordinary code search/read/edit, and the same test feedback.
B: A plus automatically extracted typed file/symbol/import/call/test/trace evidence graph retrieval.
C: B plus typed edit checks that reject references to nonexistent symbols or unsupported file changes.

The benchmark's fixed revision and gold regression tests remain outside the agent-readable checkout. Apply candidate patches to clean pre-fix checkouts for independent verification. Both buggy and fixed reference tests must be established before agent execution.

## Model and budgets

Planned model: official Gemma 4 E4B instruction tuned QAT Q4_0 GGUF, on one Kaggle T4 via pinned llama.cpp. Record model SHA-256, inference commit, GPU, CUDA, quantization, prompt template, seed and sampler parameters. Pilot defaults: 16,384 context tokens; at most 8,000 generated tokens, 30 tool calls, two edit/test cycles, and 30 minutes per issue. Freeze practical budgets after the three pilot cases and before the 12 evaluation cases. Run each condition from an independent clean checkout. Count graph retrieval toward the same agent budgets; report graph build time separately and in total time.

## Pass and analysis

Pass only if the bug is confirmed before the patch, the hidden regression test passes afterward, the relevant existing suite has no new failures, and test files were not altered by the agent. Timeouts, invalid patches, and unverifiable runs count as failures. Primary comparison B vs A paired by issue; secondary C vs B. Report per-issue results, paired win/loss/tie counts, pass rates with uncertainty intervals, latency, token/tool use, and failure cases. Do not claim general performance improvements from a 12-issue held-out set.

The former one-page PDF planned six pilot and 24 held-out issues. This v1.1 changes the sample to the user's 15-issue scope before any agent experiment. It does not claim any model run or paper result.
