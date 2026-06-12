# Causal Effect Engine — Project Brief

**Thesis:** Build a heterogeneous treatment-effect engine — a system that estimates not just *whether* an intervention works but *for whom*, validates those estimates honestly, and serves "who to treat" decisions through an API. The causal core is econometrics and measurement; the heterogeneous-effect layer is genuine ML (estimating a quantity you can never directly observe); the serving layer fills the ingestion/deployment/cloud gap. Few people do all three well.

This document is self-contained. You should be able to execute the whole project from this file alone.

---

## 1. What you're building

A research-grade causal estimation core, with a decision-product layer on top:

- **Research core:** ingest data, encode a causal DAG and its assumptions, estimate average and heterogeneous treatment effects with modern estimators, and stress-test the result with refutation and sensitivity analysis.
- **Decision layer:** rank units by their estimated treatment effect ("uplift") so you can target an intervention at the people it actually helps.
- **Serving:** expose it through a `/effect` endpoint and a `/recommend` endpoint, containerized and deployed. **Estimators are fit offline and serialized with their config and data hash; the API loads artifacts at startup and never trains on demand.** This is the only design that works on a free-tier deployment and is the correct model-serving pattern to demonstrate.

Two ways to lean, pick by taste — but the plan below builds the product flavor on top of a research-grade core so you get both stories:
- **Decision-product flavor:** emphasize uplift/targeting. More commercial, more obviously ML.
- **Research-tool flavor:** emphasize rigorous effect estimation from messy observational data. Closer to quant research and policy work.

---

## 2. Datasets

| Dataset | Role in the project |
|---|---|
| **LaLonde / NSW** (job-training program) | Exists in both randomized and observational versions. The goal is not to simply "recover the experimental answer" — that framing is a hostage to fortune (Smith & Todd (2005) showed the result is highly sensitive to sample and specification). The real contribution is **characterizing when and why observational methods recover the experimental benchmark** — across comparison groups (CPS-1 vs. PSID), samples (LaLonde 1986 full sample vs. Dehejia & Wahba 1999 subsample), and estimators. This is a strictly better portfolio story: it shows you understand the debate, not just the trick. The benchmark itself is the Dehejia & Wahba (1999) experimental subsample estimate of **$1,794** (1978 earnings). |
| **IHDP** (Infant Health and Development Program, semi-synthetic) | True CATEs are known, so you can compute PEHE (precision in estimation of heterogeneous effects) and rank CATE estimators. **Important:** IHDP has 1000 simulated outcome replications. PEHE on a single replication is noisy enough that estimator rankings can flip between replications. Evaluate across the pre-registered replication set (see §4a); report mean ± std PEHE. |
| **Criteo Uplift** (~25M rows, real ad uplift) | Demonstrate scale and the targeting product; evaluate with Qini/AUUC. **Scale constraint:** causal forests on 25M rows won't fit laptop RAM or a free-tier deployment. Plan explicitly: DuckDB handles all 25M rows for feature engineering, aggregation, and uplift evaluation out-of-core — this *is* the ingestion-skills demonstration. Model training happens offline on a pre-registered stratified subsample (see §4a). |
| **Hillstrom MineThatData email** (optional) | A gentler uplift dataset to prototype on before Criteo. |

Recommended path: validate on LaLonde + IHDP (ground truth available), then demonstrate scale/realism on Criteo.

---

## 3. The methods ladder

Climb these in order. The point is to show you understand *why* each rung exists, not to use the fanciest one.

**0. Naive baseline.** Compare treated vs. untreated outcome means. Build it first so you can later show how badly confounding corrupts it. It's your strawman.

**1. Identification before estimation.** Draw the causal DAG. State the assumptions explicitly: unconfoundedness/ignorability, positivity (overlap), SUTVA. This step *is* the econometric mindset and is what signals you're not just throwing models at data.

**2. Average treatment effect (ATE).** Climb through the estimators to feel their tradeoffs:
   - Regression adjustment
   - Propensity-score methods: IPW, matching, stratification
   - Doubly-robust (AIPW): consistent if *either* the outcome model *or* the propensity model is right
   - Double/Debiased ML (DML): ML nuisance models with orthogonalization and cross-fitting for valid inference. The modern workhorse and the clean bridge between econometrics and ML.

**3. Heterogeneous effects (CATE).** The genuinely ML layer:
   - Meta-learners: S / T / X / R / DR learners
   - Causal forests
   - DML with treatment–feature interactions
   This layer powers the targeting product.

**4. When unconfoundedness fails (optional bonus modules).** If the data has the structure for it:
   - Difference-in-differences (panel data)
   - Instrumental variables
   - Regression discontinuity
   Squarely in the econometrics wheelhouse; makes the project feel complete.

---

## 4. Evaluation — the heart of the project

The fundamental problem of causal inference: you never observe both potential outcomes for the same unit, so you **cannot** just hold out a test set and compute error on real data. A model can predict outcomes well and estimate effects terribly. Spend disproportionate effort here — it is what separates a serious project from a toy.

Four honest strategies; use several together:

1. **Benchmark against experimental ground truth — honestly.** The benchmark is the Dehejia & Wahba (1999) experimental subsample estimate of **$1,794**. This is not a target to hit — it is a reference point for a diagnostic. Run the pipeline on both the DW subsample and the full LaLonde comparison groups (CPS-1 and PSID). Report all results; don't cherry-pick the specification that "works." The PSID divergence is expected and scientifically interesting, not a failure.
2. **Semi-synthetic data with known effects.** On IHDP, compute PEHE across multiple replications (see §4a).
3. **Refutation and sensitivity on real data.** Placebo-treatment tests, adding a random common cause, subset-stability, and sensitivity analysis quantifying how strong an unobserved confounder would need to be to overturn the result (E-values; the sensemakr / Cinelli–Hazlett approach). "Our effect survives unless a confounder is stronger than X" is how credible causal work is communicated.
4. **Uplift-specific metrics.** For the targeting layer: Qini curves, AUUC, uplift-by-decile.

---

## 4a. Pre-registered success criteria

Write these down **before running any estimators.** The project's entire credibility rests on not torturing the specification until it "works." This is the discipline that separates causal work from prediction work.

**LaLonde benchmark (milestone 4):**
- Primary estimator: Double ML with LightGBM nuisance models, 5-fold cross-fitting.
- Primary sample: Dehejia & Wahba (1999) experimental subsample + CPS-1 comparison group.
- **Success:** the DML 95% CI covers $1,794.
- **Informative non-success:** PSID comparison group estimate diverges further — this reproduces the Smith & Todd (2005) finding and is the *point*, not a bug.
- Do not re-specify after seeing results. Run once; report what you get; interpret honestly.

**IHDP PEHE (milestone 5):**
- Evaluate on replications 1–10 of the 1000 available (chosen before running).
- Report mean ± std PEHE per estimator across those 10 replications.
- Reference bar: a PEHE below ~2.0 is competitive for IHDP in the literature.

**Criteo uplift (milestone 7):**
- Training subsample: stratified random sample of 1M rows (50/50 treatment/control), drawn once and fixed.
- **Success:** Qini coefficient > 0 (positive lift vs. random targeting).

---

## 5. Tech stack

| Layer | Tool | Why |
|---|---|---|
| Identification + refutation | DoWhy | Enforces model → identify → estimate → refute; built-in refutation tests |
| Estimators (DML, forests, meta-learners) | EconML | Industrial-grade CausalForestDML, DRLearner, LinearDML, etc. |
| Uplift + Qini/AUUC | CausalML (Uber) | Meta-learners plus uplift evaluation metrics |
| IV / panel / DiD | linearmodels, statsmodels | Econometrics comfort zone for the bonus modules |
| Base ML learners | scikit-learn, LightGBM | Nuisance models inside DML/meta-learners |
| DAG encoding | NetworkX + graphviz | Express and visualize assumptions |
| Storage / ingestion | DuckDB + pandas | SQL on local files; out-of-core for Criteo scale |
| Model artifacts | joblib + manifest JSON | Serialize fitted estimators with config + data hash |
| Serving | FastAPI + Docker | /effect and /recommend, load artifacts at startup |
| Demo UI (optional) | Streamlit | Upload data, specify DAG, see effects |
| Deployment | Railway / Render free tier | Cloud exposure without AWS overhead yet |
| Testing + CI | pytest + GitHub Actions | Unit tests; CI runs pytest on every push |
| Config | pydantic-settings + YAML | Type-safe config; no magic numbers in code |

---

## 6. Repo structure

```
causal-effect-engine/
│
├── data/
│   ├── raw/                   # Downloaded datasets (gitignored; checksums in config)
│   ├── processed/
│   └── db/                    # DuckDB file
│
├── notebooks/
│   ├── 01_eda_overlap.ipynb        # Outcome EDA + propensity overlap checks
│   ├── 02_ate_ladder.ipynb         # Naive → IPW → AIPW → DML comparison
│   ├── 03_cate_models.ipynb        # Meta-learners vs. causal forest
│   └── 04_validation.ipynb         # LaLonde benchmark + PEHE + refutation
│
├── src/
│   ├── ingestion/
│   │   └── load_datasets.py        # Download from pinned URLs, verify SHA-256 → DuckDB
│   ├── identification/
│   │   ├── dag.py                  # Define DAG, encode assumptions
│   │   └── checks.py               # Positivity/overlap, balance diagnostics
│   ├── estimators/
│   │   ├── ate.py                  # IPW, matching, AIPW, DML wrappers
│   │   ├── cate.py                 # Meta-learners, causal forest
│   │   └── econometric.py          # IV, DiD, RDD (bonus)
│   ├── evaluation/
│   │   ├── benchmark.py            # Observational-vs-experimental (LaLonde)
│   │   ├── pehe.py                 # Semi-synthetic ground-truth error
│   │   ├── refutation.py           # Placebo, random cause, subset tests
│   │   ├── sensitivity.py          # E-values / unobserved-confounder bounds
│   │   └── uplift.py               # Qini, AUUC, uplift-by-decile
│   └── serve/
│       └── api.py                  # FastAPI: /effect, /recommend (loads serialized artifacts)
│
├── artifacts/                      # Serialized fitted models + manifest.json (gitignored)
├── tests/
├── .github/workflows/ci.yml        # pytest on every push
├── configs/
│   └── config.yaml                 # Dataset URLs, checksums, treatment/outcome/confounders
├── pyproject.toml
├── uv.lock
├── Dockerfile
└── research_memo.md
```

---

## 7. Build order / milestones

1. **Ingestion + EDA with an overlap lens.** Load LaLonde into DuckDB; plot propensity-score overlap. **Each loader must: (a) download from a pinned URL in `config.yaml`, (b) verify a SHA-256 checksum, (c) record source URL and license in a DuckDB metadata table.** This is the data-provenance baseline every quant reviewer will ask about.
2. **DAG + identification module.** Encode assumptions explicitly before any estimation.
3. **The ATE ladder.** Naive → IPW → AIPW → DML, side by side, on the same data. The comparison is the point.
4. **The LaLonde benchmark.** Run DML on the DW/CPS-1 combination; compare to the pre-registered criterion (§4a). Also run on PSID; report the divergence. Do not re-specify after seeing results.
5. **CATE layer.** Meta-learners and a causal forest; validate with mean ± std PEHE on IHDP replications 1–10 (§4a).
6. **Refutation + sensitivity suite.** Placebo tests, random common cause, E-values.
7. **Uplift + targeting on Criteo.** Load all 25M rows into DuckDB; do feature engineering in SQL; train on the pre-registered 1M-row stratified subsample; evaluate Qini/AUUC via SQL aggregation over the full dataset.
8. **Model artifact layer + serving.** Serialize fitted estimators with `joblib` and a `manifest.json` recording config hash, training-data hash, and fit timestamp. FastAPI loads artifacts at startup; `/effect` serves estimates; `/recommend` scores new units. Containerize and deploy.
9. **Research memo.** Written like a credible empirical paper: question, identification strategy, pre-registered criteria and actual results, robustness, limitations.

### Suggested first week (a concrete, motivating start)

- **Day 1:** Create the repo; set up the environment; pull LaLonde into DuckDB with checksum verification; plot propensity-score overlap.
- **Days 2–3:** Build the DAG/identification module and the naive baseline.
- **Days 4–5:** Implement the ATE ladder (IPW, AIPW, DML).
- **End-of-week milestone:** Your observational DML estimate vs. the experimental benchmark, written up in one page.

---

## 8. Pitfalls checklist

- **Bad controls / colliders.** Don't "control for everything." Conditioning on a post-treatment variable, mediator, or collider *induces* bias. A worked example of a control that *hurts* the estimate is a sophisticated touch.
- **Positivity violations.** Near-zero or near-one propensities make IPW weights explode. Diagnose and trim; don't ignore.
- **Prediction ≠ identification.** A high-R² outcome model says nothing about whether your effect is unbiased. Keep the two scorecards separate.
- **Over-trusting unconfoundedness.** The honest stance: "here's how strong a hidden confounder would need to be to change the conclusion." That's what the sensitivity module delivers.
- **IHDP replication variance.** PEHE on a single replication is noisy; estimator rankings flip. Always evaluate across the pre-registered replication set (§4a).
- **Specification search / garden of forking paths.** The pre-registered criteria in §4a exist to prevent this. Run the primary specification once; don't tune until it "works." Every re-specification must be logged as exploratory.
- **Data provenance.** "Where did this CSV come from?" is the first question a quant reviewer asks. Every loader must download from a pinned URL, verify a SHA-256 checksum, and record source + license. An unreproducible dataset negates a reproducible model.

---

## 9. Why this is also a quant-research muscle

Treatment-effect estimation is structurally the same problem as event studies (did this event *cause* the return move?), alpha/attribution analysis (is this signal causal or just correlated with a known factor?), and policy/regime analysis. Double ML shows up in modern empirical finance precisely because it gives valid inference with high-dimensional, ML-modeled nuisance. The project builds a quant-relevant skill while being a complete, deployable data-and-AI artifact.

---

## 10. Definition of "showcase-ready"

- LaLonde benchmark characterization complete: DML 95% CI result on DW/CPS-1 reported; PSID divergence documented and interpreted.
- Pre-registered success criteria (§4a) evaluated verbatim — no post-hoc re-specification.
- CATE models validated on IHDP replications 1–10 via mean ± std PEHE.
- Refutation + sensitivity suite implemented and reported.
- Criteo: DuckDB ingests all 25M rows out-of-core; model trains on the pre-registered 1M-row subsample; Qini curve and AUUC reported.
- Serialized model artifacts with `manifest.json`; deployed API with working `/effect` and `/recommend` endpoints.
- GitHub Actions CI: pytest passes on every push.
- A 2–4 page research memo.
- Clean repo: tests, reproducible config, data provenance verified, no magic numbers.

---

## 11. Reading list (canonical references)

Books:
- Cunningham, *Causal Inference: The Mixtape*
- Huntington-Klein, *The Effect*
- Hernán & Robins, *Causal Inference: What If*
- Pearl, *The Book of Why* (intuition) / *Causality* (formal)

Papers / methods:
- Rosenbaum & Rubin (1983) — propensity scores
- LaLonde (1986) — NSW experimental evaluation (the RCT)
- Dehejia & Wahba (1999) — propensity-score reanalysis; source of the $1,794 experimental subsample benchmark
- Smith & Todd (2005) — sensitivity of DW results to sample and specification; the necessary counterpoint
- Hill (2011) — BART for causal inference / IHDP
- Chernozhukov et al. (2018) — Double/Debiased Machine Learning
- Wager & Athey (2018) — causal forests
- Künzel et al. (2019) — meta-learners (X-learner)
- VanderWeele & Ding — the E-value for sensitivity analysis
- Cinelli & Hazlett (2020) — sensitivity analysis (sensemakr)

(Confirm exact titles/years as you go; these are well-known works but worth checking against the source.)
