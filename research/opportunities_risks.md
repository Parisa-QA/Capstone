# BI Dashboard Documentation

## Dashboard

**AI Financial News Intelligence Dashboard**

## BI Tool

Tableau Public

Tableau was used as the agreed BI alternative for the Round 1 project.

---

## Purpose

The dashboard analyzes the offline FiQA dataset before introducing AI automation.

The goal is to understand:

- Overall sentiment patterns
- Distribution of financial information by business area
- Important financial topics
- Frequently mentioned companies and targets

The dashboard supports the transition from data analysis to AI use-case selection.

---

## Data Source

Primary dataset:

**FiQA 2018 financial sentiment dataset**

Dataset:

`TheFinAI/fiqa-sentiment-classification`

Total records:

**1,173**

---

## Main Dashboard Metrics

### Total Items

**1,173**

Shows the total number of financial text records analyzed.

---

### Average Sentiment

Approximately:

**0.122**

Provides an overall view of the direction of sentiment in the dataset.

---

### Positive Items

**635**

Number of records categorized as Positive using the project-defined sentiment threshold.

---

### Negative Items

**321**

Number of records categorized as Negative using the project-defined sentiment threshold.

---

### Sentiment Distribution

The dashboard compares:

- Positive
- Neutral
- Negative

Distribution:

- Positive: 635
- Negative: 321
- Neutral: 217

---

### Business Area Distribution

Main areas:

- Stock: 647
- Corporate: 479
- Market: 40
- Economy: 7

This shows that most FiQA records in this project relate to stock-level or company-level information.

---

### Average Sentiment by Topic

The dashboard compares the average FiQA sentiment score across financial topics.

Only topics with at least 10 records are shown to reduce noise from very small categories.

Examples of relatively negative topics include:

- Risks
- Legal

Examples of more positive topics include:

- Options
- Fundamentals
- M&A
- Dividend Policy

---

### Top Targets by Mentions

The dashboard identifies frequently represented financial targets.

Examples include:

- AAPL
- TSLA
- FB
- SPY
- Tesco
- AstraZeneca

This helps identify which companies or financial entities are most represented in the offline dataset.

---

## Filters

The dashboard includes interactive filters for:

### Business Area

Allows stakeholders to focus on:

- Stock
- Corporate
- Market
- Economy

### Sentiment Category

Allows users to focus on:

- Positive
- Neutral
- Negative

The filters are applied across the relevant worksheets using the same data source.

---

## Sentiment Methodology

FiQA provides a continuous sentiment score between -1 and +1.

For dashboard visualization, this project creates:

- Positive: score > +0.2
- Negative: score < -0.2
- Neutral: score between -0.2 and +0.2 inclusive

Important:

**This three-class categorization is project-defined and is not an official FiQA sentiment label.**

---

## Stakeholder Relevance

The dashboard supports investment-research stakeholders by helping answer:

- What kind of financial information is most common?
- Which topics have stronger positive or negative sentiment?
- Which entities appear most frequently?
- Where could automated AI triage provide value?

---

## Navigation

1. Open the Tableau dashboard.
2. Review the KPI cards at the top.
3. Use the Sentiment Category filter to isolate sentiment groups.
4. Use the Business Area filter to analyze specific financial domains.
5. Review Topic and Target charts for deeper patterns.

---

## Round 1 Limitation

The dashboard uses historical offline FiQA data.

It does not currently represent a live financial-news feed.

A future pilot could connect a live financial API and combine real-time information with the same analytical framework.