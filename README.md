# FinRadar AI

**Author:** Parisa Dehghani  
**Project:** AI Consultant & Integration Capstone — Round 2

**Financial News Intelligence for Analysts**

> **AI Assists — Humans Decide**

FinRadar AI is an AI-assisted financial-news intelligence application designed for investment research and wealth-management teams.

The project focuses on two core use cases:

1. **Financial News Triage & Prioritization**
2. **Risk & Regulatory Alerting**

FinRadar helps analysts review public financial news more efficiently by producing structured classifications, summaries, priority levels, and risk alerts.

It does **not** provide investment advice, predict prices, make portfolio decisions, or execute trades.

---

## Project Evolution

FinRadar was developed in two stages.

### Round 1 — Discovery and Proof of Concept

Round 1 established the initial concept using:

- **FiQA** as an offline financial-sentiment benchmark
- **Tableau Public** for exploratory financial-news analysis
- **n8n** for a no-code/low-code automation POC
- **OpenAI GPT-5 Mini** for structured news classification
- **LangSmith** for Round 1 POC trace-level observability


The n8n POC demonstrated:

```text
Manual News Input
        |
        v
AI Classification
        |
        v
Priority Rule
        |
   +----+----+
   |         |
   v         v
Alert    Standard Queue
```

### Round 2 — FinRadar AI MVP

Round 2 extended the concept into a working analyst-facing application with:

- Live public financial news
- AI-powered structured analysis
- Risk and priority classification
- Deterministic escalation rules
- Manual public-news fallback
- News pagination
- Weekly Earnings Calendar
- Accuracy and consistency evaluation
- ROI and risk assessment
- EU AI Act and GDPR documentation
- Pilot and commercialisation strategy

---

## Working MVP

The FinRadar MVP is built with:

- **Python**
- **Gradio**
- **Marketaux API**
- **OpenAI GPT-5 Mini**
- **Weekly Earnings API**
- **Requests**
- **python-dotenv**

### Live News Workflow

```text
Ticker
  |
  v
Marketaux Live News
  |
  v
Select Article
  |
  v
GPT-5 Mini
  |
  v
Structured Classification
  |
  v
Deterministic Escalation
  |
  +-------------------+
  |                   |
  v                   v
Standard Review    Risk Alert
  |                   |
  +---------+---------+
            |
            v
       Human Analyst
```

The AI returns:

- Target
- Business Area
- Topic
- Sentiment
- Priority
- Risk Type
- Summary

A separate **Manual Public News** tab provides a fallback if the live-news service is unavailable.

The **Weekly Earnings Calendar** provides additional market context and is intentionally kept separate from the AI classification workflow.

---

## Human Oversight

FinRadar uses a human-in-the-loop operating model.

AI classification is combined with deterministic escalation logic for higher-risk cases.

Examples include:

- High Priority
- Fraud
- Negative Regulatory Risk
- Negative Legal Risk
- Negative Compliance Risk

The system supports analyst review rather than replacing professional judgment.

---

## Evaluation

FinRadar was evaluated using:

- FiQA benchmark samples
- Manually labelled Risk and Priority cases
- Repeated-run consistency testing

| Metric | Result |
|---|---:|
| Strict Target Accuracy | 23.3% |
| Alias-Aware Target Accuracy | 80.0% |
| Business Area Accuracy | 90.0% |
| Sentiment Accuracy | 66.7% |
| Priority Accuracy | 86.7% |
| Risk Type Accuracy | 93.3% |
| Escalation Accuracy | 100.0% |
| Full Categorical Consistency | 80.0% |

Strict Target Accuracy is lower because the benchmark requires exact string
matching, while the model often returns expanded company names instead of
ticker aliases (for example, a company name instead of its ticker symbol).

Alias-Aware Target Accuracy treats equivalent company names and ticker aliases
as matches.

These results come from relatively small evaluation sets and are **not production guarantees**.

See:

`evaluation/evaluation_summary_round2.md`

---

## Business Case

The Round 2 business case uses explicit planning assumptions rather than claiming realised company results.

Base-case estimates include:

- **12-month ROI:** 64.4%
- **36-month ROI:** 206.0%
- **Estimated break-even:** approximately 6.2 months

The business case also includes sensitivity analysis and a structured risk matrix.

See:

`roi_risk_assessment.md`

---

## Compliance and Governance

The project includes dedicated documentation for:

### EU AI Act

The current FinRadar use case is assessed as a **non-high-risk AI system under its present intended purpose**, subject to reassessment if the scope changes.

See:

`compliance/eu_ai_act_compliance.md`

### GDPR

The GDPR documentation covers:

- Data flows
- Processing purposes
- Proposed legal basis
- Retention
- Data-subject rights
- Third-party providers
- Cross-border considerations
- Short DPIA-style assessment

See:

`compliance/gdpr_documentation.md`

The project uses public financial information only and does not intentionally process client portfolio data or private customer records.

---

## Strategic Recommendation

FinRadar should progress through:

```text
POC
 |
 v
Working MVP
 |
 v
Controlled Analyst Pilot
 |
 v
Evaluation / Governance Review
 |
 v
Production Decision
```

Immediate full production deployment is **not** recommended.

The next step is a controlled analyst pilot with defined KPIs, human oversight, security review, monitoring, and compliance approval.

See:

`strategic_plan.md`

---

## Run the MVP

Install the MVP dependencies:

```bash
python -m pip install -r mvp/requirements.txt
```

Create a local `.env` file using `.env.example` as the template.

Required MVP credentials include:

```env
OPENAI_API_KEY=your_openai_api_key_here
MARKETAUX_API_KEY=your_marketaux_api_key_here
```

Then run:

```bash
python mvp/app.py
```

The local Gradio application normally starts at:

```text
http://127.0.0.1:7860
```

API keys must never be committed to Git.

---

## Main Project Documentation

| Area | File |
|---|---|
| Use Case & Scope | `use_case_definition.md` |
| MVP Documentation | `mvp/mvp_documentation.md` |
| Evaluation | `evaluation/evaluation_summary_round2.md` |
| ROI & Risk | `roi_risk_assessment.md` |
| Strategic Plan | `strategic_plan.md` |
| EU AI Act | `compliance/eu_ai_act_compliance.md` |
| GDPR | `compliance/gdpr_documentation.md` |
| n8n POC | `n8n/poc_documentation.md` |
| LangSmith Round 1 Monitoring | `langsmith/monitoring_documentation.md` |
| Round 1 Historical Notes | `capstone.md` |

---

## Repository Structure

```text
Capstone/
├── compliance/
├── dashboard/
├── data/
├── evaluation/
├── feedback/
├── langsmith/
├── mvp/
│   ├── app.py
│   ├── assets/
│   ├── screenshots/
│   ├── mvp_documentation.md
│   └── requirements.txt
├── n8n/
├── presentation/
├── research/
├── capstone.md
├── roi_risk_assessment.md
├── strategic_plan.md
├── use_case_definition.md
├── .env.example
├── .gitignore
└── README.md
```

---

## Scope Limitations

FinRadar currently excludes:

- Investment recommendations
- Automated trading
- Price prediction
- Portfolio decisions
- Private client documents
- Customer portfolio data
- Enterprise authentication
- Production audit databases

LLM outputs can vary, external APIs can become unavailable, and some financial-news categories remain ambiguous.

Human review therefore remains mandatory.

---

## Final Recommendation

FinRadar demonstrates that the original Round 1 automation concept can be developed into a functional AI-assisted financial-news intelligence application.

The project provides technical evidence, systematic evaluation, an ROI case, compliance analysis, and a deployment strategy.

The recommended decision is:

> **Proceed to a controlled analyst pilot — not autonomous production deployment.**

**AI Assists — Humans Decide**