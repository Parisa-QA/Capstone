# FinRadar AI — EU AI Act Compliance Assessment

**Project:** FinRadar AI  
**Use Cases:** Financial News Triage & Prioritization; Risk & Regulatory Alerting  
**Assessment:** Preliminary capstone compliance assessment  
**Date:** September 2026

> This document is an educational compliance assessment and is not legal advice. A production deployment should be reviewed by qualified Legal and Compliance professionals.

---

## 1. System Overview

FinRadar AI is an analyst-facing financial-news intelligence application.

It uses public financial news and a pretrained language model to produce:

- Target
- Business Area
- Topic
- Sentiment
- Priority
- Risk Type
- Summary
- Escalation status

The system supports analysts with first-pass news review.

FinRadar does **not**:

- Execute trades
- Recommend buying or selling securities
- Predict stock prices
- Make portfolio decisions
- Provide personalised investment advice
- Determine individual creditworthiness
- Make autonomous legal or compliance decisions

The operating principle is:

> **AI assists — humans decide.**

---

# 2. EU AI Act Risk Classification

## Step 1 — Is FinRadar an AI System?

Yes.

FinRadar uses a pretrained AI model to infer classifications and summaries from financial-news text.

The outputs are used to support an analyst workflow.

---

## Step 2 — Is FinRadar a Prohibited AI Practice?

No prohibited practice has been identified under the current scope.

FinRadar does not perform activities such as:

- Social scoring
- Manipulative behavioural techniques
- Biometric identification
- Biometric categorisation
- Emotion recognition
- Predictive policing

Therefore:

**FinRadar is not classified as a prohibited AI practice.**

---

## Step 3 — Is FinRadar High-Risk Under Article 6 / Annex I?

FinRadar is not intended to operate as a safety component of a regulated product such as medical equipment, machinery, aviation systems, or other regulated physical products.

Therefore, the Annex I product-safety route does not currently apply.

---

## Step 4 — Is FinRadar High-Risk Under Annex III?

Annex III includes sensitive uses such as:

- Biometrics
- Critical infrastructure
- Education
- Employment
- Access to essential services
- Individual creditworthiness assessment
- Law enforcement
- Migration and border control
- Administration of justice

FinRadar does not perform any of these functions.

Particular attention was given to financial services because some AI systems used to assess the creditworthiness of natural persons are classified asHigh-Risk.

However, FinRadar does **not**:

- Assess personal creditworthiness
- Establish individual credit scores
- Approve or reject loans
- Determine eligibility for financial services

It analyses public financial news for professional analysts.

### Preliminary Classification

> **Based on its current intended purpose, FinRadar does not appear to be
> a High-Risk AI System under Article 6 and Annex III.**

The appropriate description is:

**Non-high-risk AI system with relevant transparency, governance and human-oversight obligations.**

This classification should be reassessed if the intended purpose changes.

---

# 3. Relevant EU AI Act Requirements

Although FinRadar is not currently assessed as High-Risk, several requirements and governance principles remain relevant.

## 3.1 Transparency — Article 50

FinRadar directly presents AI-generated classifications and summaries to human analysts.

Users should clearly understand that AI is involved.

The current MVP already provides several transparency controls:

- The product is explicitly called **FinRadar AI**
- The UI identifies OpenAI as the AI analysis layer
- The interface states that human review is required
- The interface states that FinRadar does not provide investment advice

A production version should also display a clear notice such as:

> **This application uses artificial intelligence to classify and summarise
> financial news. AI-generated outputs may contain errors and require human
> analyst review.**

AI-generated analysis should remain distinguishable from the original financial-news source.

---

## 3.2 AI Literacy — Article 4

Employees using FinRadar should receive appropriate AI training.

Analysts should understand:

- What FinRadar can and cannot do
- That AI outputs may be incorrect
- That the model is probabilistic
- That Neutral sentiment is currently a weaker classification area
- That some risk categories can overlap
- That priority classification may vary in borderline cases
- That high-impact outputs require human review
- That FinRadar does not provide investment advice

Technical staff should additionally understand:

- Prompt versioning
- Model versioning
- API security
- Evaluation methodology
- Error handling
- Monitoring
- Regression testing

---

## 3.3 Human Oversight

Human oversight is a core FinRadar control.

The workflow is:

```text
Public Financial News
        |
        v
    FinRadar AI
        |
        v
Structured Classification
        |
        v
Deterministic Escalation Rule
        |
        v
   Human Analyst
        |
        v
   Human Decision
```

Analysts must be able to:

- Review the original article
- Reject an AI classification
- Correct a classification
- Manually escalate an item
- Report incorrect outputs

AI output must not automatically become an investment, legal, or compliance decision.

---

# 4. Conformity Assessment Summary

## Current Position

Based on the current intended purpose, FinRadar is not assessed as a High-Risk AI System.

Therefore, a formal High-Risk conformity assessment is **not currently identified as mandatory** for this MVP.

This conclusion depends on the system remaining within its current scope.

---

## Why the Assessment Still Matters

The classification should be reviewed if FinRadar is expanded.

Examples that would require a new regulatory assessment include:

- Individual credit scoring
- Decisions affecting access to financial services
- Employee evaluation
- Client-level profiling for regulated decisions
- Automated investment decisions
- Autonomous trading
- Significant changes to intended purpose

Operating in the financial sector alone does not automatically make the system High-Risk; the intended purpose of the AI system is critical to the classification.

---

## If FinRadar Became High-Risk

If a future version falls within a High-Risk category, a more extensive compliance programme may be required.

This could include:

- Formal risk-management processes
- Data-governance controls
- Technical documentation
- Record keeping and logging
- Human-oversight controls
- Accuracy and robustness testing
- Cybersecurity measures
- Quality-management processes
- Registration requirements
- Conformity assessment
- Post-market monitoring

The exact requirements would need to be determined for the future intended purpose.

---

## Capstone Conformity Review

| Assessment Question | FinRadar Assessment |
|---|---|
| AI system? | Yes |
| Prohibited practice identified? | No |
| Annex I product-safety system? | No |
| Annex III High-Risk use identified? | No |
| Human users interact with AI outputs? | Yes |
| Transparency relevant? | Yes |
| AI literacy relevant? | Yes |
| Human oversight required by system design? | Yes |
| Formal High-Risk conformity assessment currently identified? | No |
| Reassessment required after material scope change? | Yes |

---

# 5. Technical Documentation Skeleton

The following documentation should be maintained for FinRadar.

## 5.1 System Identification

- System name and version
- Business owner
- Technical owner
- Compliance owner
- Environment
- AI model and version
- Prompt version

## 5.2 Intended Purpose

- Target users
- Business problem
- Supported use cases
- Inputs
- Outputs
- Human-review requirement

## 5.3 Out-of-Scope Uses

- Investment advice
- Automated trading
- Automated investment decisions
- Individual creditworthiness assessment
- Employee evaluation
- Autonomous compliance decisions
- Client-portfolio processing in the current MVP

## 5.4 Architecture

```text
Marketaux
   |
   v
Gradio Application
   |
   v
GPT-5 Mini
   |
   v
Structured AI Output
   |
   v
Deterministic Escalation
   |
   v
Human Analyst
```

The manual public-news input should also be documented as an operational fallback.

## 5.5 Data Sources

### FiQA

Purpose:

- Offline benchmark
- Prompt evaluation
- Target evaluation
- Business Area evaluation
- Sentiment evaluation

FiQA was not used to train or fine-tune GPT-5 Mini in this project.

### Marketaux

Purpose:

- Live public financial-news source for the MVP

## 5.6 AI and Prompt Documentation

Maintain:

- Model name
- System prompt
- Structured output schema
- Prompt version
- Change history
- Reason for changes
- Evaluation results before and after material changes

## 5.7 Evaluation Evidence

Maintain:

- FiQA benchmark results
- Target error analysis
- Sentiment confusion matrix
- Priority accuracy
- Risk Type accuracy
- Escalation accuracy
- Consistency evaluation
- Known limitations

## 5.8 Known Limitations

Current limitations include:

- Neutral sentiment is more difficult to classify
- Multi-entity headlines can create Target ambiguity
- Low vs Medium priority can be subjective
- Medium vs High severity can vary in borderline cases
- Regulatory and Compliance labels can overlap
- Third-party APIs may become unavailable
- AI output is probabilistic

## 5.9 Human Oversight

Document:

- Who reviews alerts
- Who may override classifications
- How errors are reported
- Who owns escalation decisions
- Which outputs require mandatory review

## 5.10 Security and Monitoring

Production controls should cover:

- API-key protection
- Authentication
- Access controls
- Logging
- Prompt/model version tracking
- Error monitoring
- Incident response
- Data retention
- Vendor dependency

API keys must never be committed to the Git repository.

---

# 6. Current Compliance Gaps

| Area | MVP Status | Production Need |
|---|---|---|
| AI disclosure | Implemented | Maintain clearly |
| Human review | Implemented | Formal procedure |
| Evaluation | Implemented | Larger continuous testing |
| Prompt documentation | In code | Version-controlled register |
| Authentication | Not implemented | Enterprise authentication |
| Audit logging | Limited | Formal audit logs |
| AI literacy training | Not formalised | Staff training programme |
| Incident management | Not formalised | Formal response procedure |
| Legal approval | Capstone assessment only | Formal Legal/Compliance review |
| Monitoring | Limited | Production monitoring |

---

# 7. Pilot Compliance Conditions

A controlled FinRadar pilot should proceed only with:

1. Public financial information as the primary input.
2. A limited group of trained analysts.
3. Mandatory human review.
4. No autonomous investment decisions.
5. No automated trading.
6. Logging and review of incorrect high-impact outputs.
7. Ongoing monitoring of false negatives.
8. Defined escalation ownership.
9. GDPR review.
10. Legal and Compliance approval before production expansion.

---

# 8. Conclusion

FinRadar is designed as an AI-assisted analyst-support system rather than an autonomous financial decision system.

Based on its current intended purpose, the capstone assessment does not identify FinRadar as a High-Risk AI System under Article 6 and Annex III.

However, responsible deployment still requires:

- Transparency
- AI literacy
- Human oversight
- Documentation
- Security
- Monitoring
- Change management
- Legal and Compliance review

The compliance position should therefore be stated as:

> **FinRadar has been designed with EU AI Act requirements and governance
> principles in mind, but formal Legal and Compliance review is required
> before production deployment.**

The system should not be described as EU certified, regulator-approved, or fully compliant.

---

# 9. Official Sources

This assessment is based primarily on:

- Regulation (EU) 2024/1689 — Artificial Intelligence Act
- European Commission — Annex III / High-Risk AI guidance
- European Commission — Article 50 Transparency Guidelines
- European Commission — Article 4 AI Literacy guidance

The latest official guidance should be reviewed again before production deployment.