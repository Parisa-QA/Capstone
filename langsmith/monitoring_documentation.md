# LangSmith Monitoring Documentation

## Purpose

LangSmith was used to provide trace-level observability for the AI component of the Financial News Triage POC.

Monitoring is important because an AI workflow should not be treated as a black box.

---

## What Was Monitored

For individual AI runs, LangSmith provides visibility into:

- User input
- System prompt
- Model output
- Model used
- Latency
- Token usage
- Estimated cost
- Trace status

---

## Sample Trace

A Round 1 trace using `gpt-5-mini` showed approximately:

- Latency: 5.43 seconds
- Tokens: 534
- Estimated cost: approximately $0.0008 for the traced run

The trace also showed the complete input and AI-generated classification.

---

## Why Monitoring Matters

Observability supports:

### Transparency

The input, prompt, and model output can be inspected.

### Debugging

Incorrect classifications can be investigated at the individual-run level.

### Performance Monitoring

Latency can be tracked over time.

### Cost Monitoring

Token usage and estimated cost can be inspected.

### Prompt Governance

Changes to prompts can be evaluated before production deployment.

---

## Evaluation Insight

Round 1 included a prompt iteration experiment.

Evaluation v1:

- Sentiment Accuracy: 66.7%

Evaluation v2:

- Sentiment Accuracy: 56.7%

The new prompt appeared logically reasonable but reduced sentiment accuracy by 10 percentage points.

The change was rejected.

This demonstrates why prompt changes should be evaluated rather than assumed to improve performance.

---

## Production Recommendation

In a production pilot, monitoring should include:

- Classification accuracy
- High-priority recall
- False alerts
- Latency
- Errors
- Token usage
- Cost
- Analyst corrections

Human feedback could later be used to improve prompts and evaluation datasets.

---

## Governance Principle

Monitoring supports the principle:

**AI assists — humans decide.**

The analyst remains responsible for validating important financial information.