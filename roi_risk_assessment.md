# FinRadar AI — ROI and Risk Assessment

## Round 2 Capstone

**Project:** FinRadar AI  
**Business Context:** Medium-sized investment research / wealth-management firm  
**Use Cases:**

1. Financial News Triage & Prioritization
2. Risk & Regulatory Alerting

---

# Part A — ROI Assessment

## 1. Purpose

This business case estimates the potential financial value of deploying FinRadar AI in a medium-sized investment research or wealth-management firm.

The calculation is based on transparent planning assumptions rather than claimed production results.

The MVP has demonstrated technical functionality and classification performance, but no real company pilot has yet measured actual employee time savings.

Therefore, all productivity benefits below should be validated during a controlled pilot.

---

## 2. Business Value Hypothesis

FinRadar is expected to create value mainly by reducing the amount of analyst time spent on repetitive first-pass financial-news review.

The system can automatically provide:

- Target identification
- Business Area classification
- Topic classification
- Sentiment classification
- Priority classification
- Risk Type classification
- Concise summarisation
- Risk-sensitive escalation

This allows analysts to spend more time on deeper research and less time performing repetitive news triage.

Potential benefits that are **not monetised** in this ROI model include:

- Faster detection of regulatory or legal events
- Reduced probability of missing material news
- More consistent triage
- Improved analyst workflow
- Better documentation of review decisions

These benefits are excluded from the financial calculation to avoid overstating the business case.

---

## 3. Core ROI Assumptions

The following assumptions represent a hypothetical medium-sized firm.

| Assumption | Base Case |
|---|---:|
| Number of analysts using FinRadar | 8 |
| Current news-triage time per analyst | 1.5 hours/day |
| Working days per year | 220 |
| Loaded analyst cost | €60/hour |
| Base-case time reduction | 30% |
| Pilot success target | 40% time reduction |
| AI analyses per working day | approximately 400 |
| Evaluation / production principle | Human review required |

The 30% productivity assumption is intentionally lower than the 40% pilot success target to make the base-case ROI more conservative.

---

## 4. Quantified Annual Business Value

### Current Annual News-Triage Time

Formula:

```text
8 analysts
× 1.5 hours/day
× 220 working days
= 2,640 analyst hours/year
```

### Base-Case Time Saved

Assuming a 30% reduction:

```text
2,640 hours
× 30%
= 792 hours saved/year
```

### Annual Productivity Value

```text
792 hours
× €60/hour
= €47,520/year
```

### Base-Case Annual Business Value

**€47,520**

This represents recovered analyst capacity rather than guaranteed cash savings.

The organisation may realise this value through:

- Increased research capacity
- More companies covered per analyst
- Faster review of important news
- Reduced repetitive manual work

---

## 5. Upfront Costs

The following costs estimate what would be required to move from the current capstone MVP into a controlled company pilot.

| Upfront Cost | Assumption | Cost |
|---|---:|---:|
| MVP-to-pilot engineering and integration | 120 hours × €80 | €9,600 |
| Security, privacy and compliance review | 40 hours × €100 | €4,000 |
| Analyst user testing and training | 24 hours × €60 | €1,440 |
| Project management and rollout configuration | 40 hours × €80 | €3,200 |
| Contingency | 10% of implementation labour | €1,824 |
| **Total Upfront Cost** | | **€20,064** |

These are planning assumptions and should be replaced by actual supplier or internal-company rates before procurement.

---

## 6. Ongoing Annual Costs

### Marketaux

The MVP currently uses Marketaux for live public financial news.

The free plan is sufficient for the capstone MVP.

For a pilot or production environment, a paid plan is more appropriate.

The current Marketaux Basic list price is approximately:

**$29/month**

For ROI planning, FinRadar allocates approximately:

**€350/year**

for the live-news API.

The final production plan should be selected based on actual request volume and service requirements.

---

### OpenAI API

The current MVP uses:

**GPT-5 Mini**

Current list pricing is based on token usage.

For planning purposes, assume:

```text
400 analyses/day
× 220 working days
= 88,000 analyses/year
```

Illustrative average AI request:

```text
1,200 input tokens
200 output tokens
```

Estimated annual token volume:

```text
Input:
88,000 × 1,200
= 105.6 million input tokens

Output:
88,000 × 200
= 17.6 million output tokens
```

At current GPT-5 Mini list pricing, the direct token cost remains relatively small compared with employee and infrastructure costs.

A conservative annual budget allowance of:

**€150/year**

is therefore used for OpenAI API usage in this base case.

Actual cost must be monitored during the pilot.

---

### Other Ongoing Costs

| Ongoing Cost | Annual Budget |
|---|---:|
| Marketaux API | €350 |
| OpenAI API | €150 |
| Cloud application hosting | €1,800 |
| Monitoring and logging | €1,200 |
| Maintenance and support | €3,840 |
| Annual security/compliance review | €1,500 |
| **Total Annual Ongoing Cost** | **€8,840** |

Cloud, monitoring, maintenance and review costs are planning assumptions, not vendor quotations.

---

## 7. 12-Month ROI

### Total 12-Month Cost

```text
Upfront Cost
€20,064

+

Annual Ongoing Cost
€8,840

=

€28,904
```

### 12-Month Benefit

```text
€47,520
```

### Net Benefit

```text
€47,520 - €28,904
= €18,616
```

### ROI Formula

```text
ROI =
(Net Benefit / Total Cost)
× 100
```

### 12-Month ROI

```text
€18,616 / €28,904
× 100

= 64.4%
```

**Estimated 12-Month ROI: 64.4%**

---

## 8. 36-Month ROI

### Total 36-Month Cost

```text
Upfront Cost:
€20,064

+

3 years × €8,840 ongoing cost:
€26,520

=

€46,584
```

### Total 36-Month Benefit

```text
3 × €47,520
= €142,560
```

### Net Benefit

```text
€142,560 - €46,584
= €95,976
```

### 36-Month ROI

```text
€95,976 / €46,584
× 100

= 206.0%
```

**Estimated 36-Month ROI: 206.0%**

---

## 9. Break-Even Analysis

Average monthly productivity value:

```text
€47,520 / 12
= €3,960/month
```

Average monthly ongoing cost:

```text
€8,840 / 12
≈ €737/month
```

Approximate monthly net benefit after operating costs:

```text
€3,960 - €737
≈ €3,223/month
```

Break-even:

```text
€20,064 upfront cost
/
€3,223 monthly net benefit

≈ 6.2 months
```

**Estimated break-even point: approximately 6 months**

---

## 10. ROI Sensitivity Analysis

Time savings are the most important business-case assumption.

Therefore, three scenarios are considered.

| Scenario | Time Reduction | Annual Value | 12-Month ROI | 36-Month ROI | Approx. Break-Even |
|---|---:|---:|---:|---:|---:|
| Conservative | 20% | €31,680 | 9.6% | 104.0% | 10.5 months |
| Base Case | 30% | €47,520 | 64.4% | 206.0% | 6.2 months |
| Pilot Target | 40% | €63,360 | 119.2% | 308.0% | 4.4 months |

This sensitivity analysis shows that the project remains potentially economically viable even if actual productivity gains are below the 40% pilot target.

However, these values must be validated with real analyst usage data.

---

## 11. ROI Interpretation

The business case should not be interpreted as a guaranteed financial return.

The largest uncertainty is not the AI API cost.

The largest uncertainty is:

**How much analyst time FinRadar actually saves in a real workflow.**

Therefore, the pilot should explicitly measure:

```text
Baseline analyst triage time
vs
FinRadar-assisted triage time
```

A full deployment decision should be based on measured pilot results rather than the planning assumptions in this document.

---

# Part B — Risk Assessment

## 12. Risk Scoring Method

Each risk is evaluated using:

### Likelihood

```text
1 = Rare
2 = Unlikely
3 = Possible
4 = Likely
5 = Almost Certain
```

### Impact

```text
1 = Minimal
2 = Minor
3 = Moderate
4 = Major
5 = Severe
```

### Risk Score

```text
Risk Score = Likelihood × Impact
```

### Interpretation

```text
1–4   = Low
5–9   = Medium
10–15 = High
16–25 = Critical
```

---

## 13. Risk Matrix

| # | Category | Risk | Likelihood | Impact | Score | Level | Mitigation |
|---|---|---|---:|---:|---:|---|---|
| 1 | Technical | AI misclassifies financial news or produces an incorrect summary | 3 | 4 | 12 | High | Structured outputs, benchmark evaluation, regression testing, human analyst review |
| 2 | Operational | A genuinely material risk event is assigned insufficient priority and is not escalated | 3 | 5 | 15 | High | Human review, monitoring of false negatives, clearer severity thresholds, larger labelled risk test set |
| 3 | Ethical | Analysts become over-reliant on AI classifications or treat outputs as authoritative | 3 | 4 | 12 | High | Analyst training, visible disclaimers, mandatory human review, no autonomous investment decisions |
| 4 | Regulatory / Privacy | Public news may contain personal data about executives or other individuals | 2 | 4 | 8 | Medium | Data minimisation, retention controls, GDPR review, processor review, data-subject-rights process |
| 5 | Regulatory | Incorrect assessment of applicable AI regulatory obligations could create compliance gaps | 2 | 4 | 8 | Medium | Legal/compliance review, maintain technical documentation, transparency controls, periodic regulatory reassessment |
| 6 | Technical / Operational | Marketaux or OpenAI API outage prevents normal processing | 3 | 3 | 9 | Medium | Manual public-news fallback, API error handling, retry logic, service monitoring and incident procedures |
| 7 | Technical | Model, API, or prompt changes alter classification behaviour | 3 | 4 | 12 | High | Version control, documented prompts, regression evaluation before changes, monitoring of accuracy and consistency |
| 8 | Operational | Financial taxonomy contains ambiguous boundaries such as Regulatory vs Compliance or Low vs Medium priority | 3 | 3 | 9 | Medium | Refine taxonomy definitions, labelled examples, human review, recurring error analysis |

---

## 14. Highest-Priority Risks

### Risk 1 — Incorrect AI Classification

The model can misunderstand an article, assign the wrong sentiment or priority, or produce an inaccurate summary.

This risk cannot be completely eliminated.

Current controls include:

- Structured output schema
- Prompt engineering
- FiQA benchmark evaluation
- Risk and Priority evaluation
- Consistency evaluation
- Human analyst review

Production deployment should add continuous monitoring and larger regression datasets.

---

### Risk 2 — Missed Escalation

A false negative is particularly important because a significant legal, regulatory, fraud, financial, or operational event could be incorrectly treated as routine.

The current small evaluation set achieved:

**100% escalation accuracy on 15 labelled cases.**

However, this should not be interpreted as proof of perfect real-world performance.

The consistency evaluation also found one operational-disruption example where priority changed between Medium and High across repeated runs.

This demonstrates the need for further severity calibration.

---

### Risk 3 — Automation Bias

Even when the AI is intended only as an assistant, analysts may begin to trust its classifications without sufficient independent review.

FinRadar therefore uses the operating principle:

> **AI assists — humans decide.**

No investment, legal, compliance, or trading decision should be made automatically from a FinRadar output.

---

## 15. Existing MVP Risk Controls

The current MVP already includes several risk controls:

- Public financial information only
- No client portfolio data
- No investment advice
- No trading capability
- No automated investment decisions
- Structured AI output
- Deterministic escalation logic
- Human-review requirement
- Manual input fallback
- API error handling
- Systematic accuracy evaluation
- Repeated-run consistency evaluation

These controls reduce risk but do not make the MVP production-ready.

---

## 16. Risk Acceptance for Pilot

A controlled pilot may proceed if:

- The system remains advisory only.
- Human analyst review is mandatory.
- Public financial information remains the primary input.
- High-risk outputs are logged and reviewed.
- Accuracy and false-negative rates continue to be measured.
- Security, GDPR and AI regulatory reviews are completed.
- Vendor agreements and data-processing arrangements are reviewed.
- The pilot has a defined stop or rollback process if material problems occur.

---

## 17. Pilot-to-Production Greenlight Criteria

Before full deployment, FinRadar should meet defined thresholds such as:

| KPI | Proposed Greenlight Threshold |
|---|---:|
| Analyst triage-time reduction | ≥ 40% |
| Priority Accuracy | ≥ 80% |
| Risk Type Accuracy | ≥ 85% |
| Escalation Accuracy | ≥ 90% |
| Processing success rate | ≥ 95% |
| Human review of high-risk alerts | 100% |
| Critical unresolved compliance issues | 0 |

These thresholds should be reassessed after the pilot using real operational
data.

---

## 18. Overall Business Case Conclusion

FinRadar presents a potentially attractive business case because the largest expected benefit comes from recovered analyst time, while direct AI inference costs are relatively low.

Under the base-case assumptions:

```text
12-Month ROI: 64.4%

36-Month ROI: 206.0%

Break-Even: approximately 6.2 months
```

The financial case is nevertheless highly dependent on actual analyst productivity gains.

Therefore, the recommended decision is not immediate full deployment.

The recommended next step is:

**Run a controlled pilot, measure real analyst time savings and model performance, complete compliance review, and use those results to make the full-deployment decision.**