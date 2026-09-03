**Author:** Parisa Dehghani  
**Project:** FinRadar AI — Round 2 Capstone

## This file covers requirements of Round 2:
1. business prolem
2. Company profile
3. Proposed AI solution
4. Stakeholders and ineterests
5. minimum 2 measurable success outcomes
6. what are out of scope
7. evolution from Round 1

# FinRadar AI — Use Case Definition

## Round 2 Capstone

**Project:** FinRadar AI  
**Subtitle:** Financial News Intelligence for Analysts  
**Tagline:** Detect what matters. Prioritize what needs attention.

This document defines the business problem, target company, proposed AI solution, stakeholders, measurable success outcomes, project scope, and evolution from Round 1.

The Round 2 of project focuses on two use cases:

1. Financial News Triage & Prioritization
2. Risk & Regulatory Alerting

---

## 1. Business Problem

Investment research and wealth-management analysts must review a large volume of financial news to identify information that may be relevant to companies, securities, markets, and potential risks.The current process is largely manual.

An analyst may need to:

- Read multiple financial-news sources.
- Identify which company or financial entity is affected.
- Determine the topic of the news.
- Interpret whether the financial tone is positive, neutral, or negative.
- Decide whether the item is routine or requires faster attention.
- Identify legal, regulatory, fraud, compliance, financial, or operational risks.
- Escalate important items to the appropriate analyst or compliance reviewer.

This creates several business problems.

### Information Overload

Analysts may need to review many news items even though only a smaller subset may require immediate attention.

### Inconsistent Prioritization

Different analysts may interpret the urgency of the same news differently.

### Delayed Risk Detection

Important regulatory, legal, fraud, compliance, financial, or operational risk events may be hidden among routine market news.

### Repetitive Manual Work

Analysts repeatedly perform similar classification and summarisation tasks before they can begin deeper analysis.

### Lack of Standardised Triage

Without a common taxonomy, news may be classified differently across teams.

**FinRadar AI** addresses this problem by providing a structured first-pass analysis of public financial news. The system does not replace professional judgement. 
Its purpose is to reduce repetitive triage work and help analysts identify which information deserves attention first.

---

## 2. Company Profile

### Target Company
The proposed solution is designed for a **medium-sized investment research or wealth-management firm**.

The company is assumed to have teams such as:

- Investment Research
- Portfolio Analysis
- Risk
- Legal and Compliance
- Operations
- Technology / IT
- Management

### Current State
The organisation currently relies on analysts to manually review financial news and identify relevant developments.

Typical information sources may include:

- Financial-news platforms
- Public company announcements
- Regulatory news
- Market commentary
- Financial websites
- Publicly available market information

The Round 2 MVP intentionally processes **public financial information only**.

It does not require access to:

- Client portfolios
- Customer records
- Private emails
- Internal company documents
- Employee records
- Confidential investment information

This limited data scope reduces implementation complexity and privacy risk during the MVP and pilot stages.

---

## 3. Proposed AI Solution

### Solution Name

**FinRadar AI**

### System Type

FinRadar is an **AI-assisted financial-news intelligence application** for analysts.

It is not designed primarily as a chatbot.
**The core product is a structured news triage, prioritisation, and risk-alert workflow**.

### Primary AI Capability

FinRadar uses a pre-trained language model (in this case GPT) with prompt engineering to analyse financial-news text.

The current MVP uses:

**OpenAI GPT-5 Mini**

No model training or fine-tuning is required for the current capstone.

The model receives a financial-news item and returns a structured classification.

### FinRadar Taxonomy

For each news item, the system produces:

- Target
- Business Area
- Topic
- Sentiment
- Priority
- Risk Type
- Summary

### Business Area

The available Business Area categories are:

- Corporate
- Stock
- Market
- Economy

### Sentiment

The available sentiment categories are:

- Positive
- Neutral
- Negative

### Priority

The available priority categories are:

- Low
- Medium
- High

### Risk Type

The available risk categories are:

- Regulatory
- Legal
- Fraud
- Financial Risk
- Operational Risk
- Compliance
- None

### Human Review

FinRadar is designed according to the principle:

**AI assists — humans decide.**

AI classifications are used to support analyst workflows.

The system does not make autonomous investment decisions.

---

### MVP Workflow

The Round 2 working MVP follows this process:

```text
Marketaux Live Financial News
            |
            v
      FinRadar AI
        Gradio App
            |
            v
       GPT-5 Mini
   Prompt Engineering
            |
            v
Structured AI Analysis
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
      +-----+------+
      |            |
      v            v
Standard       High Priority /
Review          Risk Alert
      |            |
      +-----+------+
            |
            v
       Human Analyst
```

---

### Live Data

The MVP uses **Marketaux** as the source of live public financial news.

A user can:

1. Enter a ticker such as `TSLA`, `AAPL`, or `MSFT`.
2. Fetch recent financial news.
3. Select an article.
4. Analyse the selected article using FinRadar AI.
5. Review the structured classification.
6. See whether the article requires escalation or not.

---

### Manual Fallback

The MVP also includes a manual public-news input.

This allows an analyst to paste a public financial headline or short news description directly into FinRadar.

This provides a basic operational fallback if the live news API is temporarily unavailable.

---

### Deterministic Escalation

The final alert decision is not based only on free-form AI output.

FinRadar combines model classification with a deterministic business rule.

For example, high-priority events and selected material risk conditions can trigger:

**HIGH PRIORITY / RISK ALERT**

Other items are routed to:

**STANDARD ANALYST REVIEW**

This hybrid design makes the escalation logic more transparent and controllable than relying only on the language model.

---

## 4. Stakeholders and Interests

FinRadar affects several business stakeholders.

### CEO / Senior Management

**Interest:**

- Business value
- Operational efficiency
- Controlled AI adoption
- Competitive advantage
- Return on investment
- Reputation and liability

Senior management needs evidence that FinRadar creates measurable value without introducing unacceptable organisational risk.

---

### Investment Analysts

**Interest:**

- Faster news review
- Less repetitive triage work
- Clearer prioritisation
- Concise summaries
- Identification of potentially important developments

Analysts are the **primary** users of the application.

FinRadar should support their work without replacing their professional judgement.

---

### Legal and Compliance Officer

**Interest:**

- Regulatory risk
- AI governance
- Human oversight
- Data protection
- Auditability
- Incorrect or misleading outputs
- Clear responsibility for decisions

Legal and Compliance teams need confidence that AI-generated classifications do not automatically become investment decisions or compliance conclusions.

---

### CTO / Technology Team

**Interest:**

- Technical architecture
- Reliability
- API security
- Model performance
- Monitoring
- Scalability
- Integration with existing systems
- Error handling

The technology team is responsible for ensuring that the prototype can evolve into a controlled production system.

---

### Operations Manager

**Interest:**

- Workflow efficiency
- Clear escalation paths
- Reduced manual processing
- Consistent analyst processes
- Adoption by operational teams

Operations needs the tool to improve the existing workflow rather than introduce unnecessary complexity.

---

### Risk Team

**Interest:**

- Early identification of risk-sensitive news
- Reliable classification
- Clear escalation rules
- Human review of high-impact events

FinRadar can support the Risk team by highlighting potentially material financial and operational developments.

---

## 5. Measurable Success Outcomes

The following are proposed **pilot success targets**.

They are not presented as already achieved business outcomes.

They should be measured during a controlled pilot.

### Outcome 1 — Reduce Manual News-Triage Time

**Target:**

Reduce average manual first-pass news-triage time by at least **40%**.

### Measurement

Compare:

```text
Average minutes per article without FinRadar
vs
Average minutes per article with FinRadar
```

The pilot should measure this using the same or comparable news samples.

---

### Outcome 2 — Maintain High Escalation Accuracy

**Target:**

At least **90% escalation accuracy** on a labelled validation set.

The current MVP evaluation achieved:

**100% escalation accuracy on 15 manually labelled test cases.**

This result is promising but is based on a small test set and should be validated on a larger pilot dataset.

---

### Outcome 3 — Risk Classification Performance

**Target:**

At least **85% Risk Type accuracy** during pilot validation.

The current MVP evaluation achieved:

**93.3% Risk Type accuracy on 15 manually labelled test cases.**

Further evaluation is required before production use.

---

### Outcome 4 — Priority Classification Performance

**Target:**

At least **80% Priority accuracy** during pilot validation.

The current MVP evaluation achieved:

**86.7% Priority accuracy on 15 manually labelled test cases.**

---

### Outcome 5 — Reliable System Operation

**Target:**

At least **95% successful processing rate** for supported news inputs during the pilot.

The current evaluation runs completed without API-processing failures:

- FiQA evaluation: 30 / 30 successful
- Risk and Priority evaluation: 15 / 15 successful
- Consistency evaluation: 30 / 30 successful

Production reliability would require a larger test volume and monitoring over time.

---

### Outcome 6 — Human Oversight

**Target:**

100% of high-priority or risk-alert items remain subject to human analyst review before any business or investment action is taken.

This is a mandatory operating principle of the proposed system.

---

## 6. Out of Scope

The following capabilities are intentionally outside the scope of the current FinRadar MVP.

### Investment Decisions

FinRadar does not:

- Recommend buying securities.
- Recommend selling securities.
- Make investment decisions.
- Execute trades.
- Rebalance portfolios.

---

### Investment Advice

FinRadar does not provide personalised investment advice.

Its classifications and summaries are intended only to support professional analyst review.

---

### Financial Prediction

The MVP does not:

- Predict stock prices.
- Forecast market returns.
- Generate trading signals for automated execution.
- Predict future portfolio performance.

---

### Private or Confidential Data

The current MVP does not intentionally process:

- Customer or client records
- Portfolio holdings
- Private emails
- Internal confidential documents
- Employee records
- Authentication credentials
- Private investment recommendations

The MVP focuses on public financial information.

---

### Autonomous Compliance Decisions

A `Regulatory`, `Legal`, or `Compliance` classification is not a final legal or compliance conclusion.

It is an alert to support human review.

---

### Model Training

Training or fine-tuning a new AI model is outside the core capstone scope.

The project focuses on:

- Prompt engineering
- Structured outputs
- Systematic evaluation
- Workflow integration
- Human oversight

---

### Full Production Infrastructure

The MVP does not currently include:

- Enterprise user authentication
- Role-based access control
- Production database architecture
- Enterprise audit logging
- High-availability infrastructure
- Full monitoring and incident response
- Automated integration with portfolio-management systems
- Production-scale security controls

These capabilities would be addressed during Pilot and Full Deployment phases.

---

## 7. Evolution from Round 1

FinRadar evolved substantially between Round 1 and Round 2.

### Round 1 — Offline Analysis and Proof of Concept

Round 1 focused on understanding the problem and validating the initial AI concept.

The project used the **FiQA financial sentiment dataset** as an offline labelled benchmark to understand how financial news is stractured and classfied and to evaluate the performance of the prompt-engineering AI system.

FiQA was used for:

- Understanding financial-news structure
- Analysing financial sentiment
- Developing the project taxonomy
- Building the Tableau dashboard
- Evaluating prompt performance
- Comparing prompt iterations

FiQA was **not used to train GPT-5 Mini** 

Instead, it served as an offline benchmark for prompt development and evaluation.

---

### Round 1 No-Code / Low-Code POC

An n8n workflow was created to demonstrate the automation concept.

The workflow:

```text
Manual Input
     |
     v
GPT-5 Mini
     |
     v
Structured Classification
     |
     v
Priority Decision
     |
 +---+---+
 |       |
High   Standard
Alert   Queue
```

This demonstrated that AI could classify financial news and support automated routing. However, the Round 1 POC was not a complete user-facing product.  

---

### Round 2 — Working MVP

Round 2 transforms the automation concept into a working analyst-facing application.

The main improvements are:

#### 1. Live Financial Data

Round 1:

`FiQA offline dataset`

Round 2:

`Marketaux live public financial news` using free api calls

---

#### 2. User-Facing Application

Round 1:

`n8n workflow POC`

Round 2:

`Gradio FinRadar AI application`

---

#### 3. Expanded AI Taxonomy

Round 1 primarily focused on:

- Target
- Business Area
- Topic
- Sentiment
- Priority
- Summary

Round 2 adds structured risk classification:

- Regulatory
- Legal
- Fraud
- Financial Risk
- Operational Risk
- Compliance
- None

---

#### 4. Second Use Case

Round 1 focused mainly on:

**Financial News Triage & Prioritization**

Round 2 adds:

**Risk & Regulatory Alerting**

The project intentionally focuses on only these two use cases.

---

#### 5. Hybrid Architecture

The project now follows a hybrid approach:

```text
OFFLINE VALIDATION
FiQA
  |
  v
Prompt Evaluation
  |
  +----------------------+
                         |
                         v
                  FinRadar AI
                         ^
                         |
                  LIVE OPERATION
                    Marketaux
```

FiQA provides the offline benchmark.

Marketaux provides live operational financial news.

GPT-5 Mini performs the prompt-engineered structured analysis.

---

#### 6. Systematic Evaluation

Round 2 introduces a more complete evaluation methodology.

The current evaluation includes:

- FiQA benchmark accuracy
- Target error analysis
- Alias-aware target accuracy
- Business Area accuracy
- Sentiment accuracy
- Priority accuracy
- Risk Type accuracy
- Escalation accuracy
- Repeated-run consistency testing
- Error and limitation analysis

Current key evaluation results include:

| Metric | Result |
|---|---:|
| Alias-Aware Target Accuracy | 80.0% |
| Business Area Accuracy | 90.0% |
| Sentiment Accuracy | 66.7% |
| Priority Accuracy | 86.7% |
| Risk Type Accuracy | 93.3% |
| Escalation Accuracy | 100.0% |
| Full Categorical Consistency | 80.0% |

These results are based on relatively small validation sets and should not be interpreted as production-level guarantees.

---

#### 7. Human Oversight

Round 2 makes the human-review requirement explicit.

The final principle is:

> **AI assists — humans decide.**

FinRadar identifies and prioritises potentially relevant news.

A human analyst remains responsible for interpretation, escalation, compliance review, and any subsequent business or investment decision.

---

## Conclusion

FinRadar AI addresses a practical financial-news workflow problem by combining live public news, prompt-engineered AI classification, deterministic escalation rules, and human analyst review.

The Round 2 MVP demonstrates that the initial Round 1 automation concept can be developed into a functional user-facing system without requiring model training or fine-tuning.

The project intentionally remains narrow in scope:

1. Financial News Triage & Prioritization
2. Risk & Regulatory Alerting

This focused scope allows the business value, technical performance, limitations, compliance considerations, and deployment strategy to be evaluated clearly before any production implementation.