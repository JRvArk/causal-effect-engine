# Research Memo

## Question

*State the causal question precisely: what is the effect of [treatment] on [outcome] for [population]?*

## Identification strategy

**Causal DAG:** *(diagram or description of assumed DAG)*

**Key assumptions:**
- Unconfoundedness / ignorability: ...
- Positivity (overlap): ...
- SUTVA: ...

**Adjustment set:** *(variables adjusted for and why)*

**What would break this?** *(the honest paragraph about violations)*

---

## Data

| | |
|---|---|
| Dataset | |
| N (treated / control) | |
| Outcome | |
| Treatment | |
| Key covariates | |
| Period | |

**Overlap check:** *(propensity score overlap plot; any trimming?)*

**Balance diagnostics:** *(SMDs before/after weighting or matching)*

---

## Estimates

| Estimator | ATE | 95% CI | Notes |
|---|---|---|---|
| Naive difference | | | |
| IPW | | | |
| AIPW | | | |
| Double ML | | | |
| Experimental benchmark | 1794 | — | LaLonde (1986) |

**Preferred estimate:** Double ML — *[justify choice]*

---

## Heterogeneous effects

*(CATE estimators, PEHE on IHDP, key subgroup findings)*

---

## Robustness

**Refutation tests:**
- Placebo treatment: ...
- Random common cause: ...
- Subset stability: ...

**Sensitivity analysis:**
- E-value: the effect survives unless a confounder has risk ratio > X with both treatment and outcome
- Robustness value (RV): ...

---

## Targeting results (Criteo)

*(Qini curve, AUUC, uplift-by-decile table)*

---

## Limitations

1. ...
2. ...

---

## Conclusion

*One paragraph. What the effect appears to be, how robust it is, what would be needed to overturn it.*
