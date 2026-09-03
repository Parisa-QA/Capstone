import os
import re
import json
import sys
import time
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI


# =========================================================
# Project paths
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")


# =========================================================
# Import EXACT current FinRadar prompt + schema
# =========================================================

from mvp.app import SYSTEM_PROMPT, FINANCIAL_ANALYSIS_SCHEMA


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY was not found in the root .env file."
    )

client = OpenAI(api_key=OPENAI_API_KEY)

MODEL_NAME = "gpt-5-mini"


# =========================================================
# Files
# =========================================================

INPUT_FILE = (
    PROJECT_ROOT
    / "evaluation"
    / "fiqa_evaluation_v1_results.csv"
)

RESULTS_FILE = (
    PROJECT_ROOT
    / "evaluation"
    / "fiqa_evaluation_v3_results.csv"
)

METRICS_FILE = (
    PROJECT_ROOT
    / "evaluation"
    / "fiqa_evaluation_v3_metrics.csv"
)

CONFUSION_FILE = (
    PROJECT_ROOT
    / "evaluation"
    / "fiqa_sentiment_confusion_matrix_v3.csv"
)


# =========================================================
# Helpers
# =========================================================

def normalize_target(value):
    """
    Strict normalization used for Target comparison.

    Examples:
    TSLA == $TSLA
    SAB Miller == SABMiller

    But:
    ARM Holdings != ARM Holdings plc
    """

    if pd.isna(value):
        return ""

    value = str(value).lower()

    # Remove everything except letters and numbers
    value = re.sub(r"[^a-z0-9]", "", value)

    return value


def call_finradar(sentence):
    """
    Run the EXACT current FinRadar prompt on one FiQA sentence.
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": sentence,
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": FINANCIAL_ANALYSIS_SCHEMA,
        },
    )

    content = response.choices[0].message.content

    return json.loads(content)


def call_with_retry(sentence, max_attempts=3):

    for attempt in range(1, max_attempts + 1):

        try:
            return call_finradar(sentence), ""

        except Exception as exc:

            print(
                f"Attempt {attempt} failed: "
                f"{type(exc).__name__}: {exc}"
            )

            if attempt < max_attempts:
                time.sleep(2 * attempt)

    return None, f"{type(exc).__name__}: {exc}"


# =========================================================
# Load SAME 30-sample benchmark
# =========================================================

df = pd.read_csv(INPUT_FILE)

evaluation_df = df[
    [
        "_id",
        "sentence",
        "actual_target",
        "actual_business_area",
        "actual_sentiment",
    ]
].copy()

print()
print("=" * 60)
print("FinRadar AI — Evaluation v3")
print("=" * 60)
print(f"Model: {MODEL_NAME}")
print(f"Samples: {len(evaluation_df)}")
print("=" * 60)
print()


# =========================================================
# Run evaluation
# =========================================================

results = []

for index, row in evaluation_df.iterrows():

    print(
        f"[{index + 1}/{len(evaluation_df)}] "
        f"Evaluating ID {row['_id']}..."
    )

    result, error = call_with_retry(
        row["sentence"]
    )

    if result is None:

        record = {
            "_id": row["_id"],
            "sentence": row["sentence"],

            "actual_target":
                row["actual_target"],

            "actual_business_area":
                row["actual_business_area"],

            "actual_sentiment":
                row["actual_sentiment"],

            "pred_target": "",
            "pred_business_area": "",
            "pred_topic": "",
            "pred_sentiment": "",
            "pred_priority": "",
            "pred_risk_type": "",
            "pred_summary": "",

            "error": error,

            "target_correct": False,
            "business_area_correct": False,
            "sentiment_correct": False,
        }

    else:

        pred_target = result["target"]

        pred_business_area = (
            result["business_area"]
        )

        pred_sentiment = result["sentiment"]

        target_correct = (
            normalize_target(
                row["actual_target"]
            )
            ==
            normalize_target(
                pred_target
            )
        )

        business_area_correct = (
            str(
                row["actual_business_area"]
            ).strip().lower()
            ==
            str(
                pred_business_area
            ).strip().lower()
        )

        sentiment_correct = (
            str(
                row["actual_sentiment"]
            ).strip().lower()
            ==
            str(
                pred_sentiment
            ).strip().lower()
        )

        record = {
            "_id": row["_id"],
            "sentence": row["sentence"],

            "actual_target":
                row["actual_target"],

            "actual_business_area":
                row["actual_business_area"],

            "actual_sentiment":
                row["actual_sentiment"],

            "pred_target":
                pred_target,

            "pred_business_area":
                pred_business_area,

            "pred_topic":
                result["topic"],

            "pred_sentiment":
                pred_sentiment,

            "pred_priority":
                result["priority"],

            "pred_risk_type":
                result["risk_type"],

            "pred_summary":
                result["summary"],

            "error": "",

            "target_correct":
                target_correct,

            "business_area_correct":
                business_area_correct,

            "sentiment_correct":
                sentiment_correct,
        }

    results.append(record)

    # Save continuously so progress is not lost
    pd.DataFrame(results).to_csv(
        RESULTS_FILE,
        index=False,
    )

    time.sleep(0.5)


# =========================================================
# Calculate Accuracy
# =========================================================

results_df = pd.DataFrame(results)

successful_df = results_df[
    results_df["error"] == ""
].copy()

total_successful = len(successful_df)

if total_successful == 0:
    raise ValueError(
        "No successful evaluations were completed."
    )


target_accuracy = (
    successful_df["target_correct"].mean()
    * 100
)

business_area_accuracy = (
    successful_df[
        "business_area_correct"
    ].mean()
    * 100
)

sentiment_accuracy = (
    successful_df[
        "sentiment_correct"
    ].mean()
    * 100
)


metrics_df = pd.DataFrame(
    {
        "Metric": [
            "Strict Target Accuracy",
            "Business Area Accuracy",
            "Sentiment Accuracy",
            "Successful Evaluations",
            "Errors",
        ],

        "Value": [
            round(target_accuracy, 1),
            round(
                business_area_accuracy,
                1
            ),
            round(
                sentiment_accuracy,
                1
            ),
            total_successful,
            len(results_df)
            - total_successful,
        ],
    }
)

metrics_df.to_csv(
    METRICS_FILE,
    index=False,
)


# =========================================================
# Sentiment Confusion Matrix
# =========================================================

sentiment_order = [
    "Negative",
    "Neutral",
    "Positive",
]

confusion_matrix = pd.crosstab(
    successful_df["actual_sentiment"],
    successful_df["pred_sentiment"],
)

confusion_matrix = (
    confusion_matrix
    .reindex(
        index=sentiment_order,
        columns=sentiment_order,
        fill_value=0,
    )
)

confusion_matrix.to_csv(
    CONFUSION_FILE
)


# =========================================================
# Final output
# =========================================================

print()
print("=" * 60)
print("FINRADAR AI — EVALUATION v3 RESULTS")
print("=" * 60)

print(
    f"Strict Target Accuracy: "
    f"{target_accuracy:.1f}%"
)

print(
    f"Business Area Accuracy: "
    f"{business_area_accuracy:.1f}%"
)

print(
    f"Sentiment Accuracy: "
    f"{sentiment_accuracy:.1f}%"
)

print(
    f"Successful evaluations: "
    f"{total_successful}/"
    f"{len(results_df)}"
)

print()

print("Sentiment Confusion Matrix:")
print(confusion_matrix)

print()
print("Files saved:")
print(RESULTS_FILE)
print(METRICS_FILE)
print(CONFUSION_FILE)

print("=" * 60)