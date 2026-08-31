# Data Source Selection

## Data Strategy

The project follows the recommended sequence:

1. **Offline first**
2. **Live API**
3. **Hybrid approach**

This reduces implementation risk and makes early testing repeatable.

## Options Considered

### Option A — FiQA 2018

**Advantages**
- Finance-specific NLP dataset
- Publicly available
- Includes sentiment score
- Includes target/company information
- Includes financial aspect/topic labels
- Suitable for repeatable offline testing
- Suitable for dashboard analysis
- No dependency on external API availability

### Option B — Live Financial APIs

Examples reviewed:
- Finnhub
- Alpha Vantage
- Financial Modeling Prep
- Marketaux

**Advantages**
- Current financial information
- Suitable for future real-time workflows
- Better fit for production or pilot integration

**Limitations for Round 1**
- API limits or possible cost
- Data changes continuously
- Harder to reproduce the same evaluation
- Additional integration complexity
- Increased dependency on external services

## Final Selection

**FiQA was selected as the primary Round 1 dataset.**

### Reasons
1. It is specifically designed for financial NLP.
2. It contains structured fields useful for dashboard analysis.
3. It includes sentiment scores and financial targets.
4. It allows repeatable offline testing.
5. It supports evaluation of the AI POC.
6. It avoids dependency on live APIs during early prototyping.

## Project-Specific Sentiment Categorization

FiQA provides a continuous sentiment score from **-1 to +1**.

For dashboard visualization, the project derives three categories:

- **Positive:** score > +0.2
- **Negative:** score < -0.2
- **Neutral:** score between -0.2 and +0.2 inclusive

This is a **project-defined visualization threshold**, not an official FiQA label.

## Future Direction

**FiQA Offline Validation → Live Financial API → Hybrid Architecture**
