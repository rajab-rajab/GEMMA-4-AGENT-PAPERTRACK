# Submission Guide

## Project

**Typed Evidence Graphs for Reliable Local Code Repair** is a research setup
for evaluating whether a local Gemma 4 coding agent can make reliable repair
decisions using structured evidence.

The core idea is to represent a repair task as typed, traceable evidence:
issue description, source revision, failing test, candidate patch, and
independent verification result. This supports an evaluation of agent behavior
that is more auditable than judging a patch by plausibility alone.

## What has been validated

- Six historical public-repository bug cases were screened with a local
  red/green workflow.
- For each screened case, the selected test fails against the known buggy
  revision and passes against the known fixed revision.
- The evidence bundles, frozen held-out archive, and final report are included
  in this repository.
- `notebooks/01_kaggle_smoke.ipynb` provides a reproducible Gemma 4 runtime
  setup and smoke-test path for Kaggle.

## What is not claimed

This repository does not claim completed Gemma repair-agent runs, completed
A/B/C condition results, or general performance improvements. A model response
from the notebook is an environment check, not a successful code repair.

## Evaluation plan

The planned study compares three conditions while holding the model, tools,
context, and budget constant:

1. **A — ordinary repair workflow:** issue text, code search/read/edit, and
   test feedback.
2. **B — evidence-graph retrieval:** condition A plus typed file, symbol,
   import, call, test, and trace evidence.
3. **C — typed edit checks:** condition B plus checks that reject nonexistent
   symbol references and unsupported file changes.

The fixed revision and hidden regression tests remain outside the agent-readable
workspace. Candidate patches are verified against independent clean checkouts.
See `protocol-v1.1.md` for the full preregistered plan.

## Materials for judges

- `Typed-Evidence-Graphs-Final-Report.docx` — final report.
- `README.md` — archive contents and Git LFS guidance.
- `REPRODUCIBILITY.md` — local and Kaggle setup instructions.
- `cases.json` — screened-case registry.
- `evidence ZIP files` — case-level and frozen evidence records.
