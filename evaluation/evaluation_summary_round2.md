# FinRadar AI — Round 2 Evaluation Summary

## 1. Evaluation Objective

The purpose of this evaluation is to systematically assess the accuracy,
stability, and limitations of the prompt-engineered FinRadar AI MVP.

The MVP uses a pretrained OpenAI model (`gpt-5-mini`) with a custom
financial-news system prompt and structured output schema.

No model training or fine-tuning was performed.

FiQA is used as an offline benchmark dataset for evaluating the model
against labelled financial text, while a separate manually labelled
test set is used to evaluate the new Round 2 priority and risk taxonomy.

The evaluation therefore covers:

- Target identification
- Business Area classification
- Sentiment classification
- Priority classification
- Risk Type classification
- Escalation decision
- Output consistency across repeated runs

---

## 2. Evaluation Architecture

The evaluation uses the exact prompt, schema, and escalation logic
implemented in the working FinRadar MVP.

```text
FiQA labelled data
        |
        v
Current FinRadar Prompt
        |
        v
GPT-5 Mini
        |
        v
Structured Classification
        |
        +--> Target
        +--> Business Area
        +--> Topic
        +--> Sentiment
        +--> Priority
        +--> Risk Type
        |
        v
Deterministic Escalation Rule
        |
        +--> Standard Analyst Review
        |
        +--> High Priority / Risk Alert
```

This ensures that the evaluation tests the same AI behaviour used by
the application rather than a separate evaluation-only prompt.

---

## 3. FiQA Benchmark Evaluation

### Dataset

A balanced benchmark of 30 FiQA samples was used:

- 10 Negative
- 10 Neutral
- 10 Positive

The same benchmark sample previously used during Round 1 was retained
to allow comparison between prompt iterations.

### Results

| Metric | Result |
|---|---:|
| Strict Target Accuracy | 23.3% |
| Alias-Aware Target Accuracy | 80.0% |
| Business Area Accuracy | 90.0% |
| Sentiment Accuracy | 66.7% |
| Successful API Calls | 30 / 30 |

### Sentiment Confusion Matrix

| Actual / Predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| Negative | 9 | 1 | 0 |
| Neutral | 6 | 3 | 1 |
| Positive | 0 | 2 | 8 |

The model performs strongly on clearly Negative and Positive examples,
while Neutral sentiment remains the most difficult class.

---

## 4. Target Identification Error Analysis

Strict string matching produced a low Target Accuracy of 23.3%.

A manual error analysis showed that this number substantially
underestimates practical entity identification performance.

The 23 strict mismatches were classified as follows:

| Error Type | Count |
|---|---:|
| Alias / name expansion | 17 |
| Entity-selection disagreement | 5 |
| Potential annotation mismatch | 1 |

Examples of alias differences include:

- `TSLA` vs `Tesla, Inc. (TSLA)`
- `FB` vs `Facebook (ticker: FB)`
- `MSFT` vs `Microsoft (MSFT)`
- `EXPE` vs `Expedia Group (EXPE)`
- `GSK` vs `GlaxoSmithKline (GSK)`

These predictions identify the correct business entity but fail a strict
text-equality comparison.

After recognising only clear alias/name-expansion cases as equivalent,
the Alias-Aware Target Accuracy is:

**80.0%**

Five remaining cases involve genuine ambiguity in multi-entity news,
where FiQA and FinRadar selected different primary targets.

One FiQA example was also flagged as a potential annotation mismatch:
a headline concerning a Smiths Group CEO appointment contains a FiQA
target labelled as `Morrissons`.

For transparency, both strict and alias-aware metrics are retained.

---

## 5. Priority and Risk Evaluation

FiQA does not contain ground-truth labels for the FinRadar-specific
Priority and Risk Type taxonomy.

Therefore, a separate manually labelled set of 15 financial-news test
cases was created.

The test cases cover:

### Priority

- Low
- Medium
- High

### Risk Type

- None
- Regulatory
- Legal
- Fraud
- Financial Risk
- Operational Risk
- Compliance

### Results

| Metric | Result |
|---|---:|
| Priority Accuracy | 86.7% |
| Risk Type Accuracy | 93.3% |
| Escalation Accuracy | 100.0% |
| Successful API Calls | 15 / 15 |

The strongest operational result was the escalation layer.

All 15 test cases were correctly routed to either:

- Standard Analyst Review
- High Priority / Risk Alert

This is important because escalation is the main operational outcome
of FinRadar's Risk & Regulatory Alerting use case.

---

## 6. Risk and Priority Error Analysis

Two Priority mismatches were identified.

### Case 7 — Small Sales Increase

Expected:

`Medium`

Predicted:

`Low`

The distinction is subjective because the news described only a small
increase in sales and did not indicate material urgency.

### Case 13 — CFO Appointment

Expected:

`Medium`

Predicted:

`Low`

This represents a boundary between routine corporate information and
a meaningful management event.

One Risk Type mismatch was identified.

### Case 10 — Anti-Money-Laundering Investigation

Expected:

`Compliance`

Predicted:

`Regulatory`

Both classifications are semantically plausible because the news
contains both a compliance failure and a regulatory investigation.

Despite the classification difference, the system correctly escalated
the case as requiring analyst attention.

---

## 7. Consistency Evaluation

Accuracy alone does not measure whether an AI system produces stable
results.

To evaluate consistency, 10 representative test cases were selected
and each case was analysed three times using the exact same FinRadar
prompt.

Total AI calls:

**30**

### Results

| Field | Consistency |
|---|---:|
| Business Area | 100.0% |
| Topic | 100.0% |
| Sentiment | 100.0% |
| Priority | 90.0% |
| Risk Type | 90.0% |
| Escalation | 90.0% |
| Full Categorical Consistency | 80.0% |
| Successful API Calls | 30 / 30 |

Full categorical consistency means that all evaluated categorical
outputs remained identical across all three runs for a test case.

Eight of the ten cases achieved full categorical consistency.

---

## 8. Consistency Error Analysis

Two cases showed variation.

### Case 8 — Operational Disruption

Risk Type remained consistent:

`Operational Risk | Operational Risk | Operational Risk`

However, Priority varied:

`Medium | High | Medium`

This caused escalation to vary:

`False | True | False`

This indicates that severity calibration for operational disruptions
should be improved before production deployment.

### Case 10 — AML Compliance Investigation

Priority remained stable:

`High | High | High`

Escalation also remained stable:

`True | True | True`

Risk Type varied between:

`Regulatory | Compliance | Compliance`

This reflects overlap between the Regulatory and Compliance categories.

Importantly, the operational escalation decision remained stable.

---

## 9. Key Findings

The evaluation indicates that FinRadar performs strongly in several
areas:

- Business Area classification is highly accurate.
- Positive and Negative sentiment are identified more reliably than
  Neutral sentiment.
- Alias-aware entity identification performs substantially better than
  strict string matching.
- Priority classification reached 86.7%.
- Risk Type classification reached 93.3%.
- The deterministic escalation layer achieved 100% accuracy on the
  labelled risk test set.
- Business Area, Topic, and Sentiment were fully consistent across
  repeated consistency tests.

The evaluation also identified meaningful limitations:

- Neutral sentiment classification remains difficult.
- Primary-target selection can be ambiguous in multi-entity headlines.
- Low vs Medium and Medium vs High priority boundaries require further
  calibration.
- Regulatory and Compliance categories can overlap.
- One operational-risk test showed inconsistent escalation because the
  underlying Priority prediction changed between runs.

---

## 10. Production Recommendations

Before production deployment, the following improvements are recommended:

1. Expand the labelled financial-news evaluation set.
2. Define clearer severity thresholds for Low, Medium, and High priority.
3. Refine the distinction between Regulatory and Compliance risks.
4. Introduce an entity-alias mapping or entity-resolution layer.
5. Continue monitoring Neutral sentiment performance.
6. Add regression tests whenever the system prompt is modified.
7. Evaluate performance on larger volumes of live Marketaux news.
8. Add human review for all high-impact classifications and alerts.

---

## 11. Conclusion

The evaluation demonstrates that prompt engineering is sufficient to
produce a functional and measurable financial-news intelligence MVP
without training or fine-tuning a new model.

FiQA serves as an offline benchmark for validating established
financial-news classifications, while the custom risk test set evaluates
the additional FinRadar taxonomy required for the Round 2 use cases.

The results also demonstrate why human oversight remains necessary.

FinRadar is designed to assist analysts with prioritisation and risk
detection rather than replace human judgement or make autonomous
investment decisions.