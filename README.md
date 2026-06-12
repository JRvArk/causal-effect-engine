# Causal Effect Engine

A heterogeneous treatment-effect engine that estimates not just *whether* an intervention works but *for whom*, validates those estimates rigorously, and serves targeting decisions through an API.

**Headline result:** an observational pipeline that recovers the experimental benchmark from the LaLonde/NSW dataset — the classic test of whether causal estimation actually works.

---

## What it does

| Layer | Description |
|---|---|
| **Research core** | Ingest data, encode a causal DAG, estimate average and heterogeneous treatment effects, stress-test with refutation and sensitivity analysis |
| **Decision layer** | Rank units by estimated treatment effect (uplift) to target interventions at the people they actually help |
| **Serving** | `/effect` (estimate an effect for a configuration) and `/recommend` (rank who to treat) endpoints, containerized |

---

## Datasets

| Dataset | Purpose |
|---|---|
| **LaLonde / NSW** | Observational + experimental versions; headline validation: observational pipeline recovers the RCT answer |
| **IHDP** (semi-synthetic) | True CATEs known; used to compute PEHE and rank CATE estimators |
| **Criteo Uplift** (~25M rows) | Scale demo and targeting product; evaluated with Qini/AUUC |
| **Hillstrom MineThatData** | Smaller uplift dataset for prototyping |

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

- **Experimental benchmark** — LaLonde observational pipeline vs. the RCT answer
- **Semi-synthetic ground truth** — PEHE on IHDP/ACIC where true CATEs are known
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
| Serving | FastAPI + Docker |
| Demo UI | Streamlit |
| Testing | pytest |
| Config | pydantic-settings + YAML |

---

## Repo structure

```
causal-effect-engine/
├── data/
│   ├── raw/                        # LaLonde, IHDP, Criteo, etc.
│   ├── processed/
│   └── db/                         # DuckDB file
├── notebooks/
│   ├── 01_eda_overlap.ipynb        # Outcome EDA + propensity overlap checks
│   ├── 02_ate_ladder.ipynb         # Naive → IPW → AIPW → DML comparison
│   ├── 03_cate_models.ipynb        # Meta-learners vs. causal forest
│   └── 04_validation.ipynb         # LaLonde benchmark + PEHE + refutation
├── src/
│   ├── ingestion/
│   │   └── load_datasets.py
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
├── tests/
├── configs/
│   └── config.yaml
├── Dockerfile
├── requirements.txt
└── research_memo.md
```

---

## Build order

1. Ingestion + EDA with an overlap lens (LaLonde → DuckDB; propensity overlap)
2. DAG + identification module
3. ATE ladder (naive → IPW → AIPW → DML, side by side)
4. LaLonde benchmark — observational DML vs. experimental result
5. CATE layer — meta-learners + causal forest; validate with PEHE on IHDP
6. Refutation + sensitivity suite
7. Uplift + targeting on Criteo; evaluate with Qini/AUUC
8. FastAPI `/effect` and `/recommend`, containerized and deployed
9. Research memo

---

## Showcase-ready checklist

- [ ] Observational pipeline recovers the LaLonde experimental benchmark
- [ ] CATE models validated on IHDP via PEHE
- [ ] Refutation + sensitivity suite implemented and reported
- [ ] Uplift demo on Criteo with a Qini curve
- [ ] Deployed API with working `/effect` and `/recommend` endpoints
- [ ] 2–4 page research memo
- [ ] Clean repo: tests, reproducible config, no magic numbers

---

## Key references

- Cunningham, *Causal Inference: The Mixtape*
- Huntington-Klein, *The Effect*
- Hernán & Robins, *Causal Inference: What If*
- Chernozhukov et al. (2018) — Double/Debiased Machine Learning
- Wager & Athey (2018) — Causal forests
- Künzel et al. (2019) — Meta-learners (X-learner)
- VanderWeele & Ding — E-value for sensitivity analysis
