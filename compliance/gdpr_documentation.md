# FinRadar AI — GDPR Documentation

**Project:** FinRadar AI  
**System:** Financial News Intelligence for Analysts  
**Data Scope:** Primarily public financial information  
**Assessment:** Capstone-level privacy assessment

> This document is an educational GDPR assessment and is not legal advice.
> A production deployment should be reviewed by Legal, Compliance, or the
> organisation's Data Protection Officer.

---

## 1. GDPR Scope and Data Flow

FinRadar primarily processes public financial-news information.

However, public news may still contain personal data, for example:

- Names of CEOs and executives
- Directors
- Public officials
- Lawyers
- Employees mentioned in financial news

Therefore, GDPR should still be considered even though the MVP intentionally avoids private customer and portfolio information.

### Data Flow

```text
Marketaux
Public Financial News
        |
        v
FinRadar Gradio App
        |
        v
Selected Headline + Description
        |
        v
OpenAI API
        |
        v
AI Classification
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
Deterministic Escalation
        |
        v
Human Analyst Review
```

FinRadar also provides a manual public-news input as a fallback.

The MVP does not intentionally process:

- Client portfolios
- Customer records
- Private emails
- Employee records
- Internal confidential documents
- Personal investment profiles

This limited scope supports the GDPR principle of **data minimisation**.

---

## 2. Processing Activities Register

A simplified record of processing activities for the proposed pilot is shown below.

| Processing Activity | Purpose | Data | Proposed Legal Basis | Retention | Recipients |
|---|---|---|---|---|---|
| Retrieve public financial news | Provide relevant news to analysts | Public news content | Legitimate interests, subject to assessment | Temporary / minimum necessary | Authorised analysts |
| AI analysis | Classify and summarise financial news | Headline, description, possible public personal data | Legitimate interests, subject to balancing test | Minimum necessary | OpenAI service and authorised analysts |
| Risk and priority classification | Support news triage | News content and AI-generated metadata | Legitimate interests | Limited pilot period | Analysts / relevant reviewers |
| Technical logging | Reliability and troubleshooting | Error and system metadata | Legitimate interests | Short operational period | Technical staff |

For production use, the organisation should formally confirm the lawful basis.

If **Legitimate Interests** is used, a Legitimate Interests Assessment should consider:

1. Purpose
2. Necessity
3. Impact on individuals

The system should process only the information required for the financial-news analysis task.

---

## 3. Short DPIA

### Highest-Risk Processing Activity

The highest privacy risk identified is:

> Sending public financial-news content that may contain identifiable
> individuals to a third-party AI service for automated analysis.

For example, news may refer to a named CEO involved in:

- Litigation
- Regulatory investigation
- Fraud allegations
- Compliance failures

An incorrect AI summary could potentially misrepresent that individual.

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---:|---:|---|
| Incorrect AI statement about a named individual | 3 | 4 | Human review and original-source verification |
| Unnecessary personal data sent to AI provider | 2 | 3 | Data minimisation |
| Excessive retention | 2 | 3 | Defined retention and deletion policy |
| Unauthorised access | 2 | 4 | Authentication and access control |
| International transfer without suitable safeguards | 2 | 4 | Vendor and transfer assessment |

### Existing Controls

The MVP reduces privacy risk through:

- Public-news-only scope
- No client portfolio data
- Limited text sent to the AI model
- Human analyst review
- Original article available to the analyst
- No autonomous decision-making
- No investment advice
- No permanent database required for the core MVP

A formal DPIA should be completed before production if the organisation determines that the processing is likely to create high risk for individuals.

---

## 4. Data Subject Rights

If FinRadar stores personal data, the organisation should be able to support relevant GDPR rights.

These may include:

- Right of access
- Right to rectification
- Right to erasure
- Right to restriction
- Right to object
- Other applicable GDPR rights

### Example

If an AI-generated record incorrectly states something about a named company executive, the organisation should have a process to:

1. Locate the stored record.
2. Review the original source.
3. Correct or delete the inaccurate record where required.
4. Record the action taken.

Because FinRadar relies on human review and does not independently make legally significant decisions about individuals, the MVP is not intended to operate as an autonomous decision-making system.

---

## 5. Third-Party Providers and Cross-Border Transfers

FinRadar currently uses two important external services.

### Marketaux

**Purpose:** Live public financial-news provider.

Before production use, the organisation should review:

- Privacy terms
- Security controls
- Hosting location
- Retention
- Subprocessors
- Contractual conditions

### OpenAI

**Purpose:** AI analysis and structured classification.

Before production deployment, the organisation should review the applicable:

- Data Processing Agreement
- Data-retention settings
- Security documentation
- Processing locations
- Subprocessors
- International-transfer arrangements

FinRadar should not assume specific contractual terms without reviewing the actual enterprise or API agreement used by the organisation.

### Cross-Border Transfers

If personal data is transferred outside the European Economic Area, the organisation should confirm that an appropriate GDPR transfer mechanism is available.

Depending on the vendor arrangement, this may include:

- Adequacy decisions
- Standard Contractual Clauses
- Other appropriate safeguards
- Transfer assessment where required

Vendor selection should therefore consider privacy and security as well as technical capability.

---

## 6. GDPR Controls and Conclusion

### Existing MVP Controls

FinRadar currently includes several privacy-by-design choices:

- Public financial information only
- No client or portfolio integration
- Data minimisation
- Human review
- No autonomous investment decisions
- API keys stored in `.env`
- `.env` excluded from Git
- Basic API error handling

### Production Gaps

Before production deployment, the organisation should add or formalise:

- Approved lawful basis
- Legitimate Interests Assessment if applicable
- Data-retention schedule
- Data-subject-rights procedure
- Vendor and DPA review
- International-transfer assessment
- Enterprise authentication
- Role-based access control
- Audit logging
- Security monitoring
- Privacy incident-response procedure

### Conclusion

FinRadar deliberately reduces privacy exposure by using public financial information and excluding client and portfolio data from the MVP.

However, public financial news may contain personal data, so GDPR remains relevant.

The recommended approach is:

> **Proceed with a limited public-data pilot only after lawful-basis,
> vendor, data-transfer, retention, and privacy-governance reviews have been
> completed.**

Human review and data minimisation should remain mandatory throughout the pilot and any future production deployment.