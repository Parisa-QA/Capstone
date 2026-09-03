"""
FinRadar AI - Consistency Evaluation

This script evaluates how consistently the FinRadar AI MVP classifies
the same financial-news inputs across repeated runs.

It uses the exact system prompt, structured output schema, and escalation
logic from the production MVP in mvp/app.py.

For each selected test case, the model is executed multiple times and
the consistency of the following categorical outputs is measured:

- Business Area
- Topic
- Sentiment
- Priority
- Risk Type
- Escalation Decision

The goal is to measure model stability and reproducibility as part of
the capstone's systematic prompt-engineering evaluation methodology.
"""
import os
import json
import sys
import time
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI


# =========================================================
# Configuration
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

from mvp.app import (
    SYSTEM_PROMPT,
    FINANCIAL_ANALYSIS_SCHEMA,
    requires_escalation,
)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY was not found."
    )


client = OpenAI(
    api_key=OPENAI_API_KEY
)

MODEL_NAME = "gpt-5-mini"

RUNS_PER_CASE = 3


INPUT_FILE = (
    PROJECT_ROOT
    / "evaluation"
    / "risk_priority_test_cases.csv"
)

RESULTS_FILE = (
    PROJECT_ROOT
    / "evaluation"
    / "consistency_evaluation_results.csv"
)

SUMMARY_FILE = (
    PROJECT_ROOT
    / "evaluation"
    / "consistency_evaluation_summary.csv"
)

METRICS_FILE = (
    PROJECT_ROOT
    / "evaluation"
    / "consistency_evaluation_metrics.csv"
)


# =========================================================
# Cases selected for consistency testing
# =========================================================

SELECTED_CASE_IDS = [
    1,   # Low / None
    2,   # Medium / None
    3,   # High / Regulatory
    4,   # High / Fraud
    6,   # High / Legal
    8,   # High / Operational Risk
    9,   # High / Financial Risk
    10,  # High / Compliance
    12,  # Low / None
    13,  # Appointment edge case
]


# =========================================================
# AI call
# =========================================================

def analyze_news(news_text):

    response = client.chat.completions.create(
        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": news_text,
            },
        ],

        response_format={
            "type": "json_schema",
            "json_schema":
                FINANCIAL_ANALYSIS_SCHEMA,
        },
    )

    content = (
        response
        .choices[0]
        .message
        .content
    )

    return json.loads(content)


def call_with_retry(
    news_text,
    max_attempts=3
):

    error = ""

    for attempt in range(
        1,
        max_attempts + 1
    ):

        try:

            result = analyze_news(
                news_text
            )

            return result, ""

        except Exception as exc:

            error = (
                f"{type(exc).__name__}: "
                f"{exc}"
            )

            print(
                f"Attempt {attempt} failed: "
                f"{error}"
            )

            if attempt < max_attempts:

                time.sleep(
                    2 * attempt
                )

    return None, error


# =========================================================
# Load test cases
# =========================================================

df = pd.read_csv(
    INPUT_FILE,
    keep_default_na=False
)

df = df[
    df["case_id"].isin(
        SELECTED_CASE_IDS
    )
].copy()


print()
print("=" * 65)
print(
    "FinRadar AI — Consistency Evaluation"
)
print("=" * 65)
print(f"Model: {MODEL_NAME}")
print(f"Cases: {len(df)}")
print(
    f"Runs per case: "
    f"{RUNS_PER_CASE}"
)
print(
    f"Total expected calls: "
    f"{len(df) * RUNS_PER_CASE}"
)
print("=" * 65)
print()


# =========================================================
# Run repeated tests
# =========================================================

results = []


for _, row in df.iterrows():

    case_id = int(
        row["case_id"]
    )

    news_text = row[
        "news_text"
    ]

    for run_number in range(
        1,
        RUNS_PER_CASE + 1
    ):

        print(
            f"Case {case_id} "
            f"— Run "
            f"{run_number}/"
            f"{RUNS_PER_CASE}"
        )

        result, error = (
            call_with_retry(
                news_text
            )
        )

        if result is None:

            record = {
                "case_id":
                    case_id,

                "run":
                    run_number,

                "news_text":
                    news_text,

                "target": "",

                "business_area": "",

                "topic": "",

                "sentiment": "",

                "priority": "",

                "risk_type": "",

                "escalation": "",

                "error":
                    error,
            }

        else:

            escalation = (
                requires_escalation(
                    result
                )
            )

            record = {
                "case_id":
                    case_id,

                "run":
                    run_number,

                "news_text":
                    news_text,

                "target":
                    result[
                        "target"
                    ],

                "business_area":
                    result[
                        "business_area"
                    ],

                "topic":
                    result[
                        "topic"
                    ],

                "sentiment":
                    result[
                        "sentiment"
                    ],

                "priority":
                    result[
                        "priority"
                    ],

                "risk_type":
                    result[
                        "risk_type"
                    ],

                "escalation":
                    escalation,

                "error": "",
            }

        results.append(
            record
        )

        pd.DataFrame(
            results
        ).to_csv(
            RESULTS_FILE,
            index=False
        )

        time.sleep(0.5)


# =========================================================
# Consistency calculations
# =========================================================

results_df = pd.DataFrame(
    results
)

successful_df = results_df[
    results_df["error"] == ""
].copy()


FIELDS = [
    "business_area",
    "topic",
    "sentiment",
    "priority",
    "risk_type",
    "escalation",
]


summary_rows = []


for case_id, group in (
    successful_df.groupby(
        "case_id"
    )
):

    row = {
        "case_id":
            case_id,

        "successful_runs":
            len(group),
    }

    all_fields_consistent = True

    for field in FIELDS:

        unique_values = (
            group[field]
            .astype(str)
            .nunique()
        )

        consistent = (
            unique_values == 1
            and len(group)
            == RUNS_PER_CASE
        )

        row[
            f"{field}_consistent"
        ] = consistent

        row[
            f"{field}_values"
        ] = " | ".join(
            group[field]
            .astype(str)
            .tolist()
        )

        if not consistent:

            all_fields_consistent = False

    row[
        "full_categorical_consistency"
    ] = all_fields_consistent

    summary_rows.append(
        row
    )


summary_df = pd.DataFrame(
    summary_rows
)

summary_df.to_csv(
    SUMMARY_FILE,
    index=False
)


# =========================================================
# Overall consistency metrics
# =========================================================

metric_rows = []


for field in FIELDS:

    metric_name = (
        field
        .replace("_", " ")
        .title()
        + " Consistency"
    )

    score = (
        summary_df[
            f"{field}_consistent"
        ].mean()
        * 100
    )

    metric_rows.append(
        {
            "Metric":
                metric_name,

            "Consistency (%)":
                round(
                    score,
                    1
                ),
        }
    )


full_consistency = (
    summary_df[
        "full_categorical_consistency"
    ].mean()
    * 100
)


metric_rows.append(
    {
        "Metric":
            "Full Categorical Consistency",

        "Consistency (%)":
            round(
                full_consistency,
                1
            ),
    }
)


metrics_df = pd.DataFrame(
    metric_rows
)

metrics_df.to_csv(
    METRICS_FILE,
    index=False
)


# =========================================================
# Terminal output
# =========================================================

print()
print("=" * 65)
print(
    "CONSISTENCY EVALUATION RESULTS"
)
print("=" * 65)


for _, row in (
    metrics_df.iterrows()
):

    print(
        f"{row['Metric']}: "
        f"{row['Consistency (%)']:.1f}%"
    )


print()

print(
    "Successful API calls: "
    f"{len(successful_df)}/"
    f"{len(results_df)}"
)

print()

print(
    "Files saved:"
)

print(
    RESULTS_FILE
)

print(
    SUMMARY_FILE
)

print(
    METRICS_FILE
)

print("=" * 65)