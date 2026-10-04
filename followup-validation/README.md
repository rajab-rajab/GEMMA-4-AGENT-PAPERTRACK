# Follow-up validation cohort (v1)

This directory is deliberately separate from the frozen exploratory study
(`P3`, `P5`, `P6`, `P7`, `P8`, `P9`). It does not alter its protocol, traces,
or reported outcome.

## Purpose

Validate the three conditions on a larger prospective cohort and measure two
different outcomes:

1. **Repair success** on 12 newly screened Python defects.
2. **Safe abstention** on six cases where an edit is not justified.

No candidate may be promoted to evaluation until its buggy/fixed revisions,
relevant suite, hidden regression test, exclusion decision, and environment
record are frozen. The agent must never see the fixed commit or hidden test.

## Run plan

- 12 repair candidates × A/B/C = 36 runs.
- 6 abstention controls × A/B/C = 18 runs.
- Total: 54 runs, one preregistered run per condition/case.
- Keep model, prompt, temperature, seed, tool budget, token budget and verifier
  checkout fixed within a case, as in the frozen study.

`registry.json` is intentionally a screening registry, not fabricated evidence.
Replace `UNSELECTED` only after an independently recorded red/green screen.

## Required outcome fields

Every run needs a `result.json`, patch (when any), `trace.json`, verifier log,
and `failure-events.jsonl`. The failure-event log separates model reasoning,
tool use, edit validity, test execution, verifier outcome, and timeout failures.

Run `python scripts/validate_registry.py` before freezing the cohort and
`python -m unittest discover -s tests -v` to check the registry validator.
