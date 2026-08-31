# AI Financial News Intelligence — Round 1 Capstone  

**Author:** Parisa Dehghani  
**Project:** AI Consultant & Integration Capstone — Round 1

## Project Overview

This capstone explores how AI can support financial and investment research teams by reducing the manual effort required to review, classify, summarize, and prioritize financial news.

The proposed solution is an **AI-assisted Financial News Triage system**.

The system is designed to support analysts and improve information triage. It is **not intended to make autonomous investment decisions, provide investment advice, or execute trades**.

---

## Business Problem

Investment research analysts may need to review large volumes of financial headlines, news, and market commentary.

Manual review can be:

- Time-consuming
- Difficult to prioritize consistently
- Repetitive
- Prone to missed high-risk information

The main opportunity is to use AI as a first-level triage layer before analyst review.

---

## Project Approach

The project follows an offline-first implementation strategy:

**Offline Data → Dashboard → AI Opportunities → POC → Evaluation → Monitoring → Live API → Hybrid Architecture**

Round 1 focuses on validating the concept before introducing a live financial-news API.

---

## Data Source

The primary offline dataset is the **FiQA 2018 financial sentiment dataset**.

Dataset used:

`TheFinAI/fiqa-sentiment-classification`

Total records:

**1,173**

Important fields:

- sentence
- target
- aspect
- score
- type
- split

Derived fields created for this project:

- Business_Area
- Topic
- Sentiment_Category

FiQA provides a continuous sentiment score from -1 to +1.

For dashboard visualization, this project derives sentiment categories using:

- Positive: score > +0.2
- Negative: score < -0.2
- Neutral: score between -0.2 and +0.2 inclusive

This categorization is project-defined and is not an official FiQA label.

---

## BI Dashboard

The Round 1 BI dashboard was created using **Tableau Public** as the agreed BI alternative.

The dashboard includes:

- Total financial items
- Average sentiment
- Positive items
- Negative items
- Financial sentiment distribution
- Business area distribution
- Average sentiment by topic
- Top targets by mentions

The dashboard is used to understand historical patterns in the offline FiQA dataset before designing the AI workflow.

See:

`dashboard/dashboard_documentation.md`

Interactive Tableau Public dashboard:

[View the AI Financial News Intelligence Dashboard on Tableau Public](https://public.tableau.com/app/profile/parisa.dehghani/viz/AIFinancialNewsIntelligence-Round1/AIFinancialNewsIntelligenceDashboard)


---

## AI Use Cases

Three AI use cases were considered:

1. AI Financial News Triage & Prioritization
2. AI Analyst Daily Briefing
3. Risk & Regulatory Alerting

The selected Round 1 POC is:

**AI Financial News Triage & Prioritization**

It was selected because it combines high business value, good public-data availability, measurable outputs, and relatively low implementation complexity.

---

## Automation POC

The POC was created in **n8n** and uses the OpenAI API.

Workflow:

**Manual Input → OpenAI → Structured Output → Priority Rule → Alert / Standard Analyst Queue**

The AI produces:

- Target
- Business Area
- Topic
- Sentiment
- Priority
- Summary

High-priority items are routed to an immediate analyst-review path.

Standard items are routed to the normal analyst queue.

See:

`n8n/poc_documentation.md`

---

## Monitoring

**LangSmith** is used for trace-level observability.

The monitoring setup allows inspection of:

- Input
- System prompt
- Model output
- Latency
- Token usage
- Estimated cost
- Individual AI traces

This provides transparency into how the AI component behaves and supports debugging and future governance.

See:

`langsmith/monitoring_documentation.md`

---

## Evaluation

A balanced sample of **30 records** was selected from the FiQA test split:

- 10 Positive
- 10 Neutral
- 10 Negative

Evaluation v1 results:

| Metric | Accuracy |
|---|---:|
| Business Area Accuracy | 93.3% |
| Strict Target Accuracy | 66.7% |
| Sentiment Accuracy | 66.7% |
| Execution Errors | 0 / 30 |

A second prompt version was tested to improve sentiment classification.

Sentiment accuracy decreased from:

**66.7% → 56.7%**

The change was therefore rejected.

This demonstrates the importance of evaluation and regression testing before deploying prompt or model changes.

Evaluation files are stored in:

`evaluation/`

---

## Human-in-the-Loop Principle

The system follows the principle:

**AI assists — humans decide.**

Analysts remain responsible for reviewing outputs and making investment-related decisions.

The AI should not autonomously:

- Buy or sell financial assets
- Make investment decisions
- Provide investment recommendations
- Replace analyst judgment

---

## Round 1 Recommendation

The recommendation is:

**GO for a controlled pilot — NOT for autonomous investment decision-making.**

The POC demonstrates technical feasibility, but target extraction and sentiment classification require further improvement before production use.

The recommended next stage is a controlled pilot with:

- Live financial data
- Human review
- Expanded evaluation
- Monitoring
- Governance
- Clear success KPIs

---

## Repository Structure

```text
CAPSTONE/
├── cost_estimation/
│   └── cost_timeline.md
│
├── dashboard/
│   ├── dashboard_documentation.md
│   └── dashboard assets / screenshots
│
├── data/
│   └── fiqa_powerbi_ready.csv
│
├── evaluation/
│   ├── fiqa_evaluation_v1_metrics.csv
│   ├── fiqa_evaluation_v1_results.csv
│   └── fiqa_prompt_iteration_comparison.csv
│
├── feedback/
│   └── round1_decision.md
│
├── langsmith/
│   ├── langsmith-trace.png
│   └── monitoring_documentation.md
│
├── n8n/
│   ├── AI Financial News Triage POC.json
│   ├── n8n-workflow.png
│   ├── high-priority-test.png
│   └── poc_documentation.md
│
├── presentation/
│   └── Round 1 presentation
│
├── research/
│   ├── 01_research_summary.md
│   ├── 02_sources.md
│   ├── 03_data_source_selection.md
│   ├── 04_live_api_options.md
│   ├── opportunities_risks.md
│   └── use_cases.md
│
├── .env.example
├── README.md
└── requirements.txt