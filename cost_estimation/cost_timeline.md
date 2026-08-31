# Cost and Timeline Estimate

## Purpose

This document provides a rough-order-of-magnitude estimate for a controlled pilot of the AI Financial News Triage solution.

The numbers are planning estimates rather than a formal vendor quotation.

---

# Pilot Assumptions

| Assumption | Pilot Estimate |
|---|---|
| Organization | Medium-sized investment research / wealth-management firm |
| Initial users | Small analyst team |
| Monthly volume | Approximately 5,000 financial items |
| AI model | GPT-5 mini |
| Human review | Required |
| Initial data strategy | Offline first |
| Next data phase | Live financial API |
| Deployment approach | Controlled pilot |
| Autonomous investment decisions | Not allowed |

---

# AI Usage Estimate

A monitored Round 1 LangSmith trace showed an estimated AI cost of approximately:

**$0.0008 per example run**

Using this trace only as a rough planning reference:

5,000 items × $0.0008 ≈ **$4 per month**

Actual production cost will vary based on:

- Input length
- Output length
- Prompt size
- Model pricing
- Number of retries
- Processing volume

Therefore, the AI API itself is expected to be a relatively small part of the total pilot cost.

---

# Other Cost Categories

## Workflow Automation

n8n or an equivalent orchestration platform will be required.

Exact production cost depends on deployment model and workflow volume.

---

## Monitoring

LangSmith or equivalent observability tooling should be included to monitor:

- Inputs
- Outputs
- Latency
- Token usage
- Cost
- Errors

---

## BI Environment

Tableau Public is suitable for the Round 1 public/offline demonstration.

A production environment containing internal or sensitive data should use a private BI solution.

---

## Live Financial Data

Round 1 does not require a paid live-data provider.

A live financial-news API should be selected for the pilot based on:

- Coverage
- Latency
- Licensing
- API limits
- Data quality
- Price

---

# Main Cost Driver

The largest pilot cost is expected to be implementation effort rather than raw LLM usage.

Implementation work includes:

- Data integration
- Workflow development
- Testing
- Security
- Governance
- Evaluation
- Analyst validation

---

# Estimated Timeline

| Phase | Estimated Duration |
|---|---|
| Data review and dashboard | 3–5 days |
| AI workflow and structured output | 3–5 days |
| Evaluation and monitoring | 2–4 days |
| Live API integration | 3–5 days |
| Security, testing and governance | 3–5 days |
| Analyst pilot and feedback | 1–2 weeks |

## Total Pilot Estimate

**Approximately 4–6 weeks**

---

# Suggested Roadmap

## Week 1

Offline data analysis and dashboard.

## Week 2

AI workflow and automation POC.

## Week 3

Evaluation and monitoring.

## Week 4

Live financial API integration.

## Week 5

Testing, security, error handling and governance.

## Week 6

Small analyst pilot, feedback and go/no-go decision.

---

# Cost Recommendation

The recommendation is to avoid a large production investment before the pilot proves value.

Start with:

- Small analyst group
- Limited data volume
- Human review
- Monitoring
- Clear KPIs

Scale only if the pilot meets agreed quality and business-value targets.