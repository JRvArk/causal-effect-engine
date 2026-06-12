# Causal Effect Engine

> **Status: In development — 0 of 9 milestones complete.**

A heterogeneous treatment-effect engine that estimates not just *whether* an intervention works but *for whom*, validates those estimates rigorously, and serves targeting decisions through an API.

**Headline goal:** characterize when and why observational methods recover the experimental benchmark from the LaLonde/NSW dataset — across comparison groups (CPS-1 vs. PSID), samples (LaLonde 1986 vs. Dehejia & Wahba 1999 subsample), and estimators. This is the honest framing of "does observational causal inference work?" — the answer depends on the sample and specification, and documenting that is the result.

---

## Setup

```bash
# Install Python 3.12 and project dependencies
uv python install 3.12
uv sync --group dev --group notebook

# Run tests
uv run pytest

# Start the API (loads serialized artifacts from artifacts/)
uv run uvicorn src.serve.api:app --reload

# Or with Docker
docker build -t causal-effect-engine .
docker run -p 8000:8000 causal-effect-engine
```

> Most endpoints currently return `NotImplementedError` — the API scaffold is defined from day one so the serving contract is stable as the internals are built.

---

## What it does

| Layer | Description |
|---|---|
| **Research core** | Ingest data, encode a causal DAG, estimate average and heterogeneous treatment effects, stress-test with refutation and sensitivity analysis |
| **Decision layer** | Rank units by estimated treatment effect (uplift) to target interventions at the people they actually help |
| **Serving** | Estimators are fit offline and serialized with their config and data hash; `/effect` and `/recommend` load artifacts at startup — no on-demand training |

---

## Datasets

| Dataset | Purpose |
|---|---|
| **LaLonde / NSW** | Observational + experimental versions; benchmark is the Dehejia & Wahba (1999) estimate of $1,794 — tested across CPS-1 and PSID comparison groups with pre-registered success criteria |
| **IHDP** (semi-synthetic) | True CATEs known; PEHE evaluated across replications 1–10 to give stable estimator rankings (single-replication PEHE is too noisy) |
| **Criteo Uplift** (~25M rows) | DuckDB ingests all 25M rows out-of-core for feature engineering and evaluation; model trains on a pre-registered 1M-row stratified subsample; evaluated with Qini/AUUC |
| **Hillstrom MineThatData** | Optional — smaller uplift dataset for prototyping |

---

## Methods

The project climbs a deliberate methods ladder — each rung exists because the previous one fails in a specific, demonstrable way.

1. **Naive baseline** — treated vs. untreated means; the strawman that confounding corrupts
2. **Identification** — causal DAG, explicit assumptions (unconfoundedness, positivity, SUTVA)
3. **ATE estimators** — regression adjustment → IPW → AIPW (doubly robust) → Double/Debiased ML
4. **CATE / heterogeneous effects** — S/T/X/R/DR meta-learners, causal forests, DML with interactions
5. **Bonus modules** — DiD, IV, RDD for cases where unconfoundedness fails

---

## Evaluation

Causal evaluation is hard: you never observe both potential outcomes for the same unit, so a held-out test set cannot tell you if your effect estimate is right.

Four honest strategies used together:

- **Experimental benchmark** — LaLonde DML vs. the Dehejia & Wahba $1,794 estimate; success criteria pre-registered before running; PSID divergence documented (it is the Smith & Todd result and is expected)
- **Semi-synthetic ground truth** — mean ± std PEHE across IHDP replications 1–10
- **Refutation + sensitivity** — placebo-treatment tests, random common cause, E-values quantifying how strong an unobserved confounder must be to overturn the result
- **Uplift metrics** — Qini curves, AUUC, uplift-by-decile for the targeting layer

---

## Tech stack

| Layer | Tools |
|---|---|
| Identification + refutation | DoWhy |
| DML, causal forests, meta-learners | EconML |
| Uplift + Qini/AUUC | CausalML (Uber) |
| IV / DiD / RDD | linearmodels, statsmodels |
| Base ML learners | scikit-learn, LightGBM |
| DAG encoding | NetworkX + graphviz |
| Storage / ingestion | DuckDB + pandas |
| Model artifacts | joblib + manifest JSON |
| Serving | FastAPI + Docker |
| Demo UI | Streamlit |
| CI | GitHub Actions |
| Testing | pytest |
| Config | pydantic-settings + YAML |

---

## Repo structure

```
causal-effect-engine/
├── data/
│   ├── raw/                        # Downloaded datasets (gitignored; checksums in config)
│   ├── processed/
│   └── db/                         # DuckDB file
├── notebooks/
│   ├── 01_eda_overlap.ipynb        # Outcome EDA + propensity overlap checks
│   ├── 02_ate_ladder.ipynb         # Naive → IPW → AIPW → DML comparison
│   ├── 03_cate_models.ipynb        # Meta-learners vs. causal forest
│   └── 04_validation.ipynb         # LaLonde benchmark + PEHE + refutation
├── src/
│   ├── ingestion/
│   │   └── load_datasets.py        # Download from pinned URLs → verify SHA-256 → DuckDB
│   ├── identification/
│   │   ├── dag.py                  # Causal DAG + assumption encoding
│   │   └── checks.py               # Positivity/overlap, balance diagnostics
│   ├── estimators/
│   │   ├── ate.py                  # IPW, matching, AIPW, DML
│   │   ├── cate.py                 # Meta-learners, causal forest
│   │   └── econometric.py          # IV, DiD, RDD
│   ├── evaluation/
│   │   ├── benchmark.py            # Observational vs. experimental (LaLonde)
│   │   ├── pehe.py                 # Semi-synthetic ground-truth error
│   │   ├── refutation.py           # Placebo, random cause, subset tests
│   │   ├── sensitivity.py          # E-values / unobserved-confounder bounds
│   │   └── uplift.py               # Qini, AUUC, uplift-by-decile
│   └── serve/
│       └── api.py                  # FastAPI: /effect, /recommend
├── artifacts/                      # Serialized models + manifest.json (gitignored)
├── tests/
├── .github/workflows/ci.yml
├── configs/
│   └── config.yaml
├── pyproject.toml
├── uv.lock
├── Dockerfile
└── research_memo.md
```

---

## Build order

1. Ingestion + EDA (LaLonde → DuckDB; SHA-256 checksum; propensity overlap)
2. DAG + identification module
3. ATE ladder (naive → IPW → AIPW → DML, side by side)
4. LaLonde benchmark — DML vs. pre-registered criteria; PSID divergence documented
5. CATE layer — meta-learners + causal forest; mean ± std PEHE on IHDP replications 1–10
6. Refutation + sensitivity suite
7. Criteo — DuckDB ingests 25M rows; train on 1M-row subsample; Qini/AUUC
8. Model artifact layer + FastAPI serving, containerized and deployed
9. Research memo

---

## Results

*Populated as milestones complete.*

### ATE ladder — LaLonde (Dehejia & Wahba subsample + CPS-1)

| Estimator | ATE | 95% CI | Covers $1,794? |
|---|---|---|---|
| Naive difference | — | — | — |
| IPW | — | — | — |
| AIPW | — | — | — |
| Double ML | — | — | — |
| **Experimental benchmark (DW 1999)** | **$1,794** | — | reference |

### CATE — IHDP (replications 1–10)

| Estimator | Mean PEHE | Std PEHE |
|---|---|---|
| S-learner | — | — |
| T-learner | — | — |
| X-learner | — | — |
| DR-learner | — | — |
| Causal forest | — | — |

### Uplift — Criteo (1M-row training subsample)

*Qini curve and AUUC to be added at milestone 7.*

---

## Showcase-ready checklist

- [ ] LaLonde benchmark: DML 95% CI result on DW/CPS-1 reported; PSID divergence documented
- [ ] Pre-registered success criteria (see brief §4a) evaluated without post-hoc re-specification
- [ ] CATE models validated on IHDP replications 1–10 via mean ± std PEHE
- [ ] Refutation + sensitivity suite implemented and reported
- [ ] Criteo: DuckDB ingests 25M rows; Qini curve on 1M-row subsample
- [ ] Serialized model artifacts with `manifest.json`; deployed API
- [ ] GitHub Actions CI: pytest passes on every push
- [ ] 2–4 page research memo
- [ ] Clean repo: tests, reproducible config, data provenance verified, no magic numbers

---

## Key references

- Cunningham, *Causal Inference: The Mixtape*
- Huntington-Klein, *The Effect*
- Hernán & Robins, *Causal Inference: What If*
- LaLonde (1986) — NSW experimental evaluation
- Dehejia & Wahba (1999) — propensity-score reanalysis; source of the $1,794 benchmark
- Smith & Todd (2005) — sensitivity of DW results to sample and specification
- Chernozhukov et al. (2018) — Double/Debiased Machine Learning
- Wager & Athey (2018) — Causal forests
- Künzel et al. (2019) — Meta-learners (X-learner)
- VanderWeele & Ding — E-value for sensitivity analysis
