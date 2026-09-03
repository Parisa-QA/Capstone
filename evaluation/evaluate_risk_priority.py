import os
import json
import sys
import time
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI


# =========================================================
# Paths and configuration
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

client = OpenAI(api_key=OPENAI_API_KEY)

MODEL_NAME = "gpt-5-mini"


INPUT_FILE = (
    PROJECT_ROOT
    / "evaluation"
    / "risk_priority_test_cases.csv"
)

RESULTS_FILE = (
    PROJECT_ROOT
    / "evaluation"
    / "risk_priority_evaluation_results.csv"
)

METRICS_FILE = (
    PROJECT_ROOT
    / "evaluation"
    / "risk_priority_evaluation_metrics.csv"
)


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

    for attempt in range(
        1,
        max_attempts + 1
    ):

        try:
            return analyze_news(
                news_text
            ), ""

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
                time.sleep(2 * attempt)

    return None, error


# =========================================================
# Load test cases
# =========================================================

df = pd.read_csv(INPUT_FILE,
    keep_default_na=False)
results = []

print()
print("=" * 60)
print("FinRadar AI — Risk & Priority Evaluation")
print("=" * 60)
print(f"Model: {MODEL_NAME}")
print(f"Test cases: {len(df)}")
print("=" * 60)
print()


# =========================================================
# Evaluation loop
# =========================================================

for index, row in df.iterrows():

    print(
        f"[{index + 1}/{len(df)}] "
        f"Evaluating case "
        f"{row['case_id']}..."
    )

    result, error = call_with_retry(
        row["news_text"]
    )

    if result is None:

        record = {
            "case_id":
                row["case_id"],

            "news_text":
                row["news_text"],

            "expected_priority":
                row["expected_priority"],

            "pred_priority": "",

            "expected_risk_type":
                row["expected_risk_type"],

            "pred_risk_type": "",

            "expected_escalation":
                row[
                    "expected_escalation"
                ],

            "pred_escalation": "",

            "priority_correct":
                False,

            "risk_type_correct":
                False,

            "escalation_correct":
                False,

            "error":
                error,
        }

    else:

        pred_priority = (
            result["priority"]
        )

        pred_risk_type = (
            result["risk_type"]
        )

        pred_escalation = (
            requires_escalation(
                result
            )
        )

        expected_escalation = (
            str(
                row[
                    "expected_escalation"
                ]
            ).strip().lower()
            == "true"
        )

        record = {
            "case_id":
                row["case_id"],

            "news_text":
                row["news_text"],

            "expected_priority":
                row["expected_priority"],

            "pred_priority":
                pred_priority,

            "expected_risk_type":
                row["expected_risk_type"],

            "pred_risk_type":
                pred_risk_type,

            "expected_escalation":
                expected_escalation,

            "pred_escalation":
                pred_escalation,

            "priority_correct":
                str(
                    pred_priority
                ).strip().lower()
                ==
                str(
                    row[
                        "expected_priority"
                    ]
                ).strip().lower(),

            "risk_type_correct":
                str(
                    pred_risk_type
                ).strip().lower()
                ==
                str(
                    row[
                        "expected_risk_type"
                    ]
                ).strip().lower(),

            "escalation_correct":
                pred_escalation
                ==
                expected_escalation,

            "error": "",
        }

    results.append(record)

    pd.DataFrame(
        results
    ).to_csv(
        RESULTS_FILE,
        index=False
    )

    time.sleep(0.5)


# =========================================================
# Metrics
# =========================================================

results_df = pd.DataFrame(results)

successful_df = results_df[
    results_df["error"] == ""
].copy()

priority_accuracy = (
    successful_df[
        "priority_correct"
    ].mean()
    * 100
)

risk_accuracy = (
    successful_df[
        "risk_type_correct"
    ].mean()
    * 100
)

escalation_accuracy = (
    successful_df[
        "escalation_correct"
    ].mean()
    * 100
)


metrics = pd.DataFrame(
    {
        "Metric": [
            "Priority Accuracy",
            "Risk Type Accuracy",
            "Escalation Accuracy",
            "Successful Evaluations",
            "Errors",
        ],

        "Value": [
            round(
                priority_accuracy,
                1
            ),
            round(
                risk_accuracy,
                1
            ),
            round(
                escalation_accuracy,
                1
            ),
            len(successful_df),
            len(results_df)
            - len(successful_df),
        ],
    }
)

metrics.to_csv(
    METRICS_FILE,
    index=False
)


# =========================================================
# Results
# =========================================================

print()
print("=" * 60)
print(
    "RISK & PRIORITY "
    "EVALUATION RESULTS"
)
print("=" * 60)

print(
    f"Priority Accuracy: "
    f"{priority_accuracy:.1f}%"
)

print(
    f"Risk Type Accuracy: "
    f"{risk_accuracy:.1f}%"
)

print(
    f"Escalation Accuracy: "
    f"{escalation_accuracy:.1f}%"
)

print(
    f"Successful evaluations: "
    f"{len(successful_df)}/"
    f"{len(results_df)}"
)

print()

print(
    "Saved:",
    RESULTS_FILE
)

print(
    "Saved:",
    METRICS_FILE
)

print("=" * 60)