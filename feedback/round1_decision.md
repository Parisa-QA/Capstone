# Round 1 Decision

## Feedback Summary

The Round 1 presentation and feedback confirmed that the financial-news intelligence problem was relevant and technically feasible, but the project scope needed to remain focused for Round 2.

The main feedback and resulting decisions were:

- Keep the project focused on a maximum of two core AI use cases.
- Preserve the strongest Round 1 capability: Financial News Triage & Prioritization.
- Strengthen the business value by adding Risk & Regulatory Alerting as the second use case.
- Do not continue with the Analyst Daily Briefing use case.
- Move beyond the Round 1 proof of concept by building a working analyst-facing MVP.
- Keep human review central and avoid autonomous investment decision-making.

---

## Decision

**CHANGE — use-case scope refined; industry retained**

The financial-services / investment-research context was retained.

The Round 2 project focuses on two use cases:

1. **Financial News Triage & Prioritization**
2. **Risk & Regulatory Alerting**

The previously considered **Analyst Daily Briefing** use case was removed from scope.

---

## Why

The Round 1 POC demonstrated that AI-assisted financial-news triage was technically feasible.

Round 1 evidence included:

- Business Area Accuracy: 93.3%
- Strict Target Accuracy: 66.7%
- Sentiment Accuracy: 66.7%
- Execution Errors: 0 / 30
- Successful High Priority routing in n8n
- LangSmith trace-level monitoring evidence

However, Round 1 also showed several limitations:

- The evaluation sample was small.
- Target extraction and sentiment classification required further testing.
- The workflow used manual input rather than live financial news.
- The POC was a workflow demonstration rather than an analyst-facing product.
- Human review remained necessary.

Based on the feedback and these limitations, Round 2 focused on a smaller, clearer scope with stronger evaluation, governance, compliance, and business justification.

---

## What Changed for Round 2

### Use Cases

Round 1 considered:

1. Financial News Triage & Prioritization
2. Analyst Daily Briefing
3. Risk & Regulatory Alerting

Round 2 retained only:

1. Financial News Triage & Prioritization
2. Risk & Regulatory Alerting

The Daily Briefing use case was removed.

### MVP

The Round 1 n8n proof of concept evolved into a working Gradio-based FinRadar AI MVP with:

- Live public financial news from Marketaux
- Structured AI analysis using GPT-5 Mini
- Priority classification
- Risk classification
- Deterministic escalation rules
- Manual public-news fallback
- News pagination
- Weekly Earnings Calendar
- Human-in-the-loop review

### Evaluation

Round 2 expanded testing beyond the original Round 1 benchmark.

The final evaluation includes:

- FiQA benchmark testing
- Alias-aware target evaluation
- Risk and Priority evaluation
- Escalation evaluation
- Repeated-run consistency testing

### Governance and Business Readiness

Round 2 also added:

- ROI and risk assessment
- EU AI Act compliance assessment
- GDPR documentation
- Strategic deployment plan
- Explicit pilot success criteria
- Scope and production limitations

---

## Round 2 Focus

### POC Improvements

The Round 1 POC remains as evidence that the core automation concept works.

Round 2 does not replace that evidence; it extends the concept into a working MVP with live financial-news input and stronger risk handling.

### MVP Scope

The core Round 2 workflow is:

**Live Financial News  
→ Article Selection  
→ AI Classification  
→ Priority & Risk Analysis  
→ Deterministic Escalation  
→ Human Analyst Review**

The system remains an analyst-assistance tool.

It does not:

- Make investment decisions
- Provide investment advice
- Execute trades
- Predict asset prices
- Replace analyst judgment

### Compliance / ROI / Strategy Priorities

Round 2 prioritises:

- Transparent human oversight
- Honest evaluation of model limitations
- EU AI Act assessment
- GDPR data-flow and rights analysis
- Explicit ROI assumptions
- Risk mitigation
- Controlled pilot deployment before production

---

## Final Round 2 Direction

The recommendation is to proceed with a **controlled analyst pilot**, not immediate full production deployment.

The pilot should validate:

- Operational time savings
- Priority accuracy
- Risk classification accuracy
- Escalation reliability
- Processing reliability
- Human-review effectiveness
- Compliance and governance controls

The guiding principle remains:

> **AI Assists — Humans Decide.**