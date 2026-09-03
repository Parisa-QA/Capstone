# FinRadar AI — MVP Documentation

**Author:** Parisa Dehghani  
**Project:** FinRadar AI — Round 2 Capstone

## 1. MVP Purpose

FinRadar AI is a working analyst-facing application for:

1. Financial News Triage & Prioritization
2. Risk & Regulatory Alerting

The MVP analyses public financial news and returns structured AI outputs to help analysts identify which items may require attention first.

The system follows the principle:

> **AI Assists — Humans Decide**

FinRadar does not provide investment advice, make trading decisions, or execute trades.

---

## 2. Technology Stack

The MVP uses:

- **Gradio** — analyst-facing web application
- **Marketaux API** — live public financial-news source
- **OpenAI GPT-5 Mini** — structured AI analysis
- **Weekly Earnings API** — current-week earnings calendar
- **Python** — application and business logic
- **Requests** — external API calls
- **python-dotenv** — environment-variable management

Round 1 also used FiQA, n8n, LangSmith, and Tableau as supporting evaluation, automation, monitoring, and analytics tools.

FiQA is used as an offline benchmark and was not used to train or fine-tune GPT-5 Mini.

---

## 3. MVP Architecture

```text
Marketaux Live News
        |
        v
    Gradio App
        |
        v
   GPT-5 Mini
        |
        v
Structured AI Output
        |
        +--> Target
        +--> Business Area
        +--> Topic
        +--> Sentiment
        +--> Priority
        +--> Risk Type
        +--> Summary
        |
        v
Deterministic Escalation Rule
        |
   +----+----+
   |         |
   v         v
Standard    High Priority /
Review       Risk Alert
   |         |
   +----+----+
        |
        v
Human Analyst
```

A manual public-news input is available as a fallback if the live-news API is unavailable.

The Weekly Earnings Calendar is displayed separately as additional analyst context and is not automatically sent to the AI model.

---

## 4. User Workflow

### Live News

1. Enter a ticker such as `AAPL`, `MSFT`, or `TSLA`.
2. Click **Fetch Latest News**.
3. FinRadar retrieves three recent Marketaux articles.
4. Select one article.
5. Review the article details and original source.
6. Click **Analyze Selected News with AI**.
7. GPT-5 Mini returns structured analysis.
8. FinRadar applies the escalation rule.
9. The analyst reviews either:
   - **Standard Analyst Review**, or
   - **High Priority / Risk Alert**.

For the same ticker, **Load More News** retrieves the next batch of articles.

Changing the ticker resets the search.

### Manual Public News

The user can paste a public financial headline or short description into the **Manual Public News** tab.

This provides a fallback when live news is unavailable.

### Weekly Earnings Calendar

The MVP also displays current-week earnings announcements from Monday to Friday, separated into:

- Pre Market
- After Market

The calendar can be refreshed manually.

---

## 5. AI Output and Escalation

FinRadar returns:

- Target
- Business Area
- Topic
- Sentiment
- Priority
- Risk Type
- Summary

Priority values are:

- Low
- Medium
- High

Risk Type values are:

- Regulatory
- Legal
- Fraud
- Financial Risk
- Operational Risk
- Compliance
- None

FinRadar combines the AI classification with deterministic escalation logic.

Examples of escalation conditions include:

- High Priority
- Fraud risk
- Negative Regulatory risk
- Negative Legal risk
- Negative Compliance risk

AI output does not automatically become an investment, legal, or compliance decision.

Human review remains mandatory.

---

## 6. Basic Error Handling

The MVP includes basic error handling for:

- Empty ticker input
- Missing API credentials
- Marketaux timeout or request failure
- Invalid API responses
- No news returned
- No article selected
- OpenAI analysis failure
- Earnings API failure

If Marketaux is unavailable, the analyst can continue using the Manual Public News tab.

---

## 7. Testing and Evaluation

The MVP was systematically evaluated using FiQA and a manually labelled risk and priority test set.

| Metric | Result |
|---|---:|
| Alias-Aware Target Accuracy | 80.0% |
| Business Area Accuracy | 90.0% |
| Sentiment Accuracy | 66.7% |
| Priority Accuracy | 86.7% |
| Risk Type Accuracy | 93.3% |
| Escalation Accuracy | 100.0% |
| Full Categorical Consistency | 80.0% |

These results are based on relatively small validation sets and are not production guarantees.

Known evaluation limitations include Neutral sentiment, multi-entity Target ambiguity, overlapping risk categories, and borderline Priority decisions.

---

## 8. How to Run the MVP

From the project root:

```bash
python -m pip install -r mvp/requirements.txt
```

Then run:

```bash
python mvp/app.py
```

The local application normally starts at:

```text
http://127.0.0.1:7860
```

The root `.env` file must contain:

```env
MARKETAUX_API_KEY=your_real_key
OPENAI_API_KEY=your_real_key
```

API keys must never be committed to GitHub.

The repository should contain `.env.example` with placeholder values only.

---

## 9. MVP Limitations and Production Gap

The current MVP does not include:

- Enterprise authentication
- Role-based access control
- Production audit logging
- Centralised monitoring
- Formal retention policies
- Production incident response
- Large-scale regression datasets
- Client portfolio integration
- Automated trading

Additional limitations include:

- LLM outputs can vary between repeated runs.
- Third-party APIs may become temporarily unavailable.
- The MVP processes public financial information only.
- Human review remains required.

A production version would require stronger security, monitoring, governance, compliance approval, and larger-scale testing.

---

## 10. Conclusion

FinRadar AI demonstrates a complete end-to-end workflow:

```text
Public Financial News
        |
        v
AI Analysis
        |
        v
Structured Classification
        |
        v
Risk / Priority Escalation
        |
        v
Human Analyst Review
```

The Round 2 MVP extends the Round 1 proof of concept with live financial news, a user-facing interface, risk-sensitive escalation, manual fallback, weekly earnings context, and systematic evaluation.

The recommended next step is a controlled analyst pilot before production deployment.