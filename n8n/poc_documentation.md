# Automation POC Documentation

## POC Name

**AI Financial News Triage POC**

## Automation Tool

n8n

## AI Model

OpenAI `gpt-5-mini`

---

## Purpose

The POC demonstrates how AI can support first-level financial-news triage.

Instead of requiring an analyst to manually classify every new financial item, the workflow sends the text to an AI model and produces structured output.

---

## Workflow

The Round 1 workflow is:

**Manual Trigger → Input Field → OpenAI → Structured Output → IF Priority Rule → Analyst Queue**

The AI analyzes the financial text and returns:

- target
- business_area
- topic
- sentiment
- priority
- summary

---

## Business Areas

The AI must select one of:

- Corporate
- Stock
- Market
- Economy

---

## Priority Levels

The AI returns:

- Low
- Medium
- High

High-priority items include material negative or risk-sensitive information that may require immediate analyst attention.

---

## Routing Logic

The n8n IF node checks:

`priority == High`

If true:

**High Priority Alert**

If false:

**Standard Analyst Queue**

---

## High-Priority Test

Test sentence:

> Tesla faces a major regulatory investigation over alleged fraud, raising the risk of significant financial penalties.

The AI returned:

- Target: Tesla
- Business Area: Corporate
- Topic: Regulatory
- Sentiment: Negative
- Priority: High

The workflow correctly routed the item to:

**High Priority Alert**

This demonstrates the intended escalation logic.

---

## Why This POC Fits the Use Case

The workflow addresses a real analyst workflow problem:

Financial information arrives continuously, but not all items require the same level of attention.

The POC shows that AI can:

1. Read financial information
2. Convert unstructured text into structured data
3. Assign priority
4. Route information automatically
5. Keep the final decision with a human analyst

---

## Production Limitations

The Round 1 POC is not a production system.

Current limitations include:

- Manual trigger
- No live financial-news API
- No persistent analyst database
- No production authentication or access-control design
- Limited evaluation sample
- No automated feedback loop
- Human review is still required
- No autonomous investment decisions

---

## Recommended Production Evolution

A future workflow could use:

**Live Financial API → n8n → OpenAI → Structured Classification → Priority Routing → Analyst Review → Monitoring**

The system should remain human-in-the-loop.

---

## Safety Principle

The POC is intended for financial information triage only.

It does not:

- Recommend investments
- Predict stock prices
- Execute trades
- Replace analyst judgment