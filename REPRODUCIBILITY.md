# Reproducibility Guide

## Local red/green validation

Use Python 3.8 in a virtual environment. Install the dependency set for the
case you are reproducing, then run the validation script. For example, the
`P2` tqdm case uses:

```bash
python -m pip install -r requirements-tqdm-pilot.txt
python scripts/reproduce.py --case P2 --python /absolute/path/to/python --output ./results/P2
```

The script clones only public repositories listed in `cases.json`, checks out
the known buggy and fixed revisions in isolated worktrees, runs the selected
test in each, and saves logs and metadata under the chosen output directory.

Historical HTTPie cases require their matching requirements file and the
consistent `--noconftest` handling documented in the project README.

## Kaggle Gemma 4 smoke test

1. Create a Kaggle Notebook with **GPU T4 x2**.
2. Upload or attach this repository as a Kaggle Dataset input.
3. Attach the official Gemma 4 E4B instruction-tuned QAT Q4_0 GGUF model.
4. Open `notebooks/01_kaggle_smoke.ipynb`.
5. Set `PROJECT_ZIP` to the attached project ZIP and, if needed, set
   `MODEL_GGUF` to the attached `.gguf` file.
6. Run cells in order. Enable Internet when package and public-source downloads
   are required.
7. Save the notebook version and the generated
   `/kaggle/working/gemma4-repair-results` output.

The notebook verifies the environment, builds GPU-enabled llama.cpp, starts a
Gemma 4 model on GPU 0, and records runtime metadata and a model response. It
does not execute or claim a completed bug repair.

## Large archive retrieval

The frozen held-out archive is stored in Git LFS. After cloning, retrieve it
with:

```bash
git lfs install
git lfs pull
```

## Research safeguards

Do not place the gold regression test or fixed patch inside the agent-readable
workspace. Verify all candidate patches independently on clean pre-fix
checkouts, and treat timeouts, invalid patches, altered test files, and
unverifiable runs as failures.
