# Live Financial API Options

## Purpose

A live financial API is not required for the core Round 1 POC.

The project first validates the workflow using offline FiQA data.  
Live data can be added during a controlled pilot.

## Options Reviewed

### Finnhub
**Potential use:**  
Financial news and market information.

### Alpha Vantage
**Potential use:**  
Market data and financial news / sentiment-related endpoints.

### Financial Modeling Prep
**Potential use:**  
Company, market, and financial data.

### Marketaux
**Potential use:**  
Financial news aggregation.

## Round 1 Decision

The core POC remains **offline-first**.

Reasons:
- Faster implementation
- Repeatable testing
- Lower dependency on third-party services
- Easier comparison between model versions
- Better fit for a Round 1 proof of concept

## Recommended Next Phase

1. Validate the AI workflow offline
2. Select one live financial API
3. Add live ingestion to n8n
4. Keep human review in the workflow
5. Monitor quality, latency, token usage, and cost
6. Move toward a hybrid architecture if pilot KPIs are met
