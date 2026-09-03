# FinRadar AI — Strategic Deployment Plan

**Project:** FinRadar AI  
**Business Context:** Medium-sized investment research / wealth-management firm  
**Core Use Cases:**

1. Financial News Triage & Prioritization
2. Risk & Regulatory Alerting

---

## 1. Deployment Strategy

FinRadar should move through a controlled deployment path:

```text
POC
 |
 v
Working MVP
 |
 v
Controlled Pilot
 |
 v
Full Deployment
 |
 v
Optional Scale
```

The system should not move directly from MVP to production.

Each phase should demonstrate sufficient business value, technical reliability, risk control, and compliance readiness before the next phase begins.

---

## 2. POC and MVP Status

### Round 1 POC

The n8n workflow demonstrated that financial news can be:

- Analysed by a LLM
- Classified into structured fields
- Assigned a priority
- Routed to either a High Priority Alert or Standard Queue

### Round 2 MVP

The working FinRadar MVP adds:

- Gradio user interface
- Marketaux live public financial news
- Manual public-news fallback
- GPT-5 Mini analysis
- Structured output
- Risk Type classification
- Deterministic escalation logic
- Human-review requirement
- Basic error handling
- Systematic accuracy and consistency evaluation

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

These results are based on small validation sets and are not production
guarantees.

---

## 3. Controlled Pilot

### Objective

Validate FinRadar in a real analyst workflow before production deployment.

### Proposed Pilot Scope

- 5–10 analysts
- 6–8 weeks
- Public financial news only
- Limited companies or sectors
- No automated trading
- No investment recommendations
- Mandatory human review
- No client portfolio integration

### Pilot Measurements

The pilot should measure:

- Analyst triage time
- Priority accuracy
- Risk Type accuracy
- Escalation accuracy
- False-negative risk alerts
- Processing reliability
- User adoption
- Cost per analysis

---

## 4. Pilot-to-Full Greenlight Criteria

Full deployment should proceed only if agreed targets are met.

| KPI | Proposed Greenlight Threshold |
|---|---:|
| Analyst triage-time reduction | ≥ 40% |
| Priority Accuracy | ≥ 80% |
| Risk Type Accuracy | ≥ 85% |
| Escalation Accuracy | ≥ 90% |
| Processing success rate | ≥ 95% |
| Human review of high-risk alerts | 100% |
| Critical unresolved compliance issues | 0 |
| Material security incidents | 0 |

If the criteria are not met, the system should remain in pilot and be
improved before wider deployment.

---

## 5. Full Deployment

A production version should add controls that are not part of the current MVP.

These include:

- Enterprise authentication
- Role-based access control
- Centralised logging
- Prompt and model version tracking
- Secure secrets management
- Production monitoring
- Audit trail
- Formal retention policy
- Incident response
- Compliance approval
- Vendor management
- Formal user training
- Change-management process

The production workflow should remain:

```text
Financial News
      |
      v
FinRadar AI
      |
      v
Structured Analysis
      |
      v
Risk / Escalation Rules
      |
      v
Human Analyst
      |
      v
Human Decision
```

---

## 6. Timeline and Milestones

| Phase | Estimated Duration | Main Milestone |
|---|---|---|
| POC | Completed | n8n workflow proved the concept |
| MVP | Completed | Live FinRadar application and evaluation |
| Pilot | 6–8 weeks | Real analyst testing and KPI measurement |
| Full Deployment | 2–4 months after pilot approval | Enterprise production rollout |
| Optional Scale | After production validation | More users, markets, integrations |

### Pilot Milestones

**Weeks 1–2**

- Pilot environment
- Security configuration
- Analyst training
- Baseline time measurement

**Weeks 3–6**

- Analyst usage
- Accuracy monitoring
- Error analysis
- User feedback

**Weeks 7–8**

- KPI assessment
- Compliance review
- ROI update
- Go / No-Go decision

---

## 7. Go-to-Market and Commercialisation

FinRadar could be commercialised as a **B2B SaaS product**.

### Target Buyers

Potential customers include:

- Investment research firms
- Wealth-management firms
- Asset-management teams
- Risk teams
- Compliance teams

Likely economic buyers include:

- Head of Research
- COO
- CTO
- Head of Risk
- Head of Compliance

### Sales Channel

The recommended initial channel is:

> **Paid pilot → measured business case → annual subscription**

Other possible channels include:

- Direct B2B sales
- Consulting partnerships
- Financial-services industry networks
- Strategic technology partnerships

### Pricing Concept

Illustrative pricing:

**Paid Pilot:** €8,000–€15,000

**Annual Subscription:** €20,000–€50,000

Final pricing would depend on:

- Number of users
- News volume
- Data-provider cost
- Integration requirements
- Support level

These figures are planning assumptions and require market validation.

---

## 8. Differentiation

FinRadar is not intended to compete only as another financial-news feed.

Its differentiator is:

> **Transforming raw financial news into a structured, risk-aware analyst
> workflow.**

Key differentiators include:

- Financial-news taxonomy
- Priority classification
- Risk Type classification
- Deterministic escalation
- Human-review design
- FiQA-based offline evaluation
- Live Marketaux news
- Compliance-aware architecture

The product is designed to reduce repetitive first-pass work rather than replace analysts.

---

## 9. Stakeholder Communication

### CEO / Management

Focus on:

- ROI
- Time savings
- Pilot results
- Business risk
- Go / No-Go decision

### Legal / Compliance

Focus on:

- EU AI Act
- GDPR
- Human oversight
- Vendor risk
- Model limitations

### CTO / Technology

Focus on:

- Architecture
- Security
- API reliability
- Monitoring
- Model and prompt changes

### Analysts / Operations

Focus on:

- How to use FinRadar
- Known limitations
- How to correct outputs
- Escalation process
- Workflow impact

---

## 10. KPIs by Phase

### POC

- End-to-end workflow works
- Structured AI output produced
- Routing demonstrated

### MVP

- Live news retrieval works
- AI analysis works
- Risk alerting works
- Basic error handling works
- Accuracy and consistency measured

### Pilot

- Analyst time reduction
- Classification accuracy
- Escalation accuracy
- False-negative rate
- Adoption
- Reliability
- Cost per analysis

### Production

- Monthly active analysts
- News items processed
- Analyst time saved
- System availability
- Correction rate
- Security incidents
- Compliance incidents
- Cost per item

---

## 11. Future Development

After successful production deployment, FinRadar could expand to:

- Multiple news providers
- Company watchlists
- Historical analysis
- Additional languages
- Analyst feedback loops
- Team alert queues
- Internal research integrations

A future version could also introduce a controlled LangChain / LangGraph agentic layer for ambiguous cases that require multi-step investigation.

The current MVP intentionally uses a simpler prompt-and-rule architecture because it is easier to evaluate, audit, and control.

---

## 12. Strategic Recommendation

The recommended next step is:

> **Run a controlled analyst pilot, measure real business value and model
> performance, complete compliance and security reviews, and only then decide
> whether to proceed to full production deployment.**

This phased approach balances:

- Business value
- Technical reliability
- Regulatory compliance
- Human oversight

while preserving the core principle:

> **AI assists — humans decide.**