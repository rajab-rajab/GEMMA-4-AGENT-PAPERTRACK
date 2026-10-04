# Typed Evidence Graphs for Reliable Local Code Repair

This repository is the evidence archive for Rajab Baig's Gemma 4 Developer
Agent Paper Track research project. It publishes the screening, held-out, and
safe-abstention evidence bundles together with the final report.

## What this repository contains

- `Typed-Evidence-Graphs-Final-Report.docx` — the final project report.
- `Gemma4-Heldout-Final-Evidence.zip` — the frozen held-out evidence archive.
- `P3` through `P9` held-out evidence ZIPs — case-level historical evidence.
- `C06` through `C13` screening evidence ZIPs — prospective candidate-screening
  records.
- `V01`, `V02`, and `V03C` ZIPs — non-actionable and safe-abstention controls.
- `gemma4-prospective-v01-envfix01-*` ZIPs — environment-fix validation
  evidence for the prospective cases.

## Research status and scope

The published evidence supports reproducible local red/green screening of
historical bug cases: the selected test fails on the buggy revision and passes
on the known fixed revision. The material is intended to document the protocol
and case evidence, not to claim completed Gemma repair-agent experiments.

The current project state is a validated research setup. The next stage is a
separate, preregistered evaluation of agent conditions and safe abstention.

## Downloading the large held-out archive

`Gemma4-Heldout-Final-Evidence.zip` is stored with Git LFS because it is larger
than GitHub's regular Git file limit. After cloning the repository, run:

```bash
git lfs install
git lfs pull
```

## Integrity note

The held-out archive is published once. A duplicate local copy with the same
SHA-256 value was intentionally not uploaded again.

## Related project

The project uses typed evidence graphs to make local code-repair evaluation
traceable: bug reports, revisions, tests, candidate patches, and verification
results are treated as structured evidence rather than as an unverified model
response.
