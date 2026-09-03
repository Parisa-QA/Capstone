import os
import json
import base64
import html
from pathlib import Path
from datetime import datetime, timedelta
from urllib.parse import urlparse

import gradio as gr
import requests
from dotenv import load_dotenv
from openai import OpenAI


# =========================================================
# Configuration
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MVP_DIR = Path(__file__).resolve().parent
ENV_FILE = PROJECT_ROOT / ".env"
LOGO_FILE = MVP_DIR / "assets" / "finradar_logo.png"

load_dotenv(ENV_FILE)

MARKETAUX_API_KEY = os.getenv("MARKETAUX_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MARKETAUX_URL = "https://api.marketaux.com/v1/news/all"
EARNINGS_URL = (
    "https://northalpha.taila42da8.ts.net/"
    "assets/earnings/thisWeek"
)

openai_client = (
    OpenAI(api_key=OPENAI_API_KEY)
    if OPENAI_API_KEY
    else None
)


def image_to_data_uri(path):
    """
    Convert a local image into a data URI for inline HTML usage.
    """

    if not path.exists():
        return ""

    encoded = base64.b64encode(
        path.read_bytes()
    ).decode("utf-8")

    return "data:image/png;base64," + encoded


LOGO_URI = image_to_data_uri(LOGO_FILE)


# =========================================================
# Structured Output Schema
# =========================================================

FINANCIAL_ANALYSIS_SCHEMA = {
    "name": "financial_news_analysis",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "target": {
                "type": "string"
            },
            "business_area": {
                "type": "string",
                "enum": [
                    "Corporate",
                    "Stock",
                    "Market",
                    "Economy"
                ]
            },
            "topic": {
                "type": "string",
                "enum": [
                    "Regulatory",
                    "M&A",
                    "Risks",
                    "Strategy",
                    "Sales",
                    "Price Action",
                    "Technical Analysis",
                    "Legal",
                    "Appointment",
                    "Market",
                    "Financial",
                    "Dividend Policy",
                    "Coverage",
                    "Signal",
                    "Fundamentals",
                    "Reputation",
                    "Other"
                ]
            },
            "sentiment": {
                "type": "string",
                "enum": [
                    "Positive",
                    "Neutral",
                    "Negative"
                ]
            },
            "priority": {
                "type": "string",
                "enum": [
                    "Low",
                    "Medium",
                    "High"
                ]
            },
            "risk_type": {
                "type": "string",
                "enum": [
                    "Regulatory",
                    "Legal",
                    "Fraud",
                    "Financial Risk",
                    "Operational Risk",
                    "Compliance",
                    "None"
                ]
            },
            "summary": {
                "type": "string"
            }
        },
        "required": [
            "target",
            "business_area",
            "topic",
            "sentiment",
            "priority",
            "risk_type",
            "summary"
        ],
        "additionalProperties": False
    }
}


SYSTEM_PROMPT = """
You are FinRadar AI, an AI assistant for financial-news triage.

Your job is to analyze PUBLIC financial news for investment-research
analysts.

You do NOT provide investment advice, trading recommendations,
price predictions, or buy/sell decisions.

TARGET:
Identify the primary company, security, institution, ETF, market,
or financial entity most directly affected by the news.

If several companies appear, choose the primary subject of the news.
Do not return a list of multiple targets unless absolutely unavoidable.

BUSINESS AREA:
Corporate = company-level events such as management, strategy,
M&A, legal, regulatory, sales, financial results, reputation.

Stock = share-price behavior, technical analysis, market signals,
coverage, options, or trading-related information.

Market = broader financial-market developments.

Economy = macroeconomic developments.

SENTIMENT:
Classify the overall financial tone as:
Positive, Neutral, or Negative.

PRIORITY:
High = material negative or risk-sensitive events that may require
immediate analyst attention, including serious regulatory action,
fraud, major litigation, severe financial loss, crisis, or other
material risks.

Medium = meaningful but non-urgent developments such as M&A,
earnings developments, strategic changes, approvals, or significant
market movements.

Low = routine commentary, minor developments, or low-impact
information.

Do NOT classify a routine positive regulatory approval as High
unless there is a material risk or urgency.

RISK TYPE:
Regulatory = investigation, enforcement action, sanction,
regulatory threat, or material regulatory issue.

Legal = lawsuit, court action, major legal dispute, or legal exposure.

Fraud = fraud, accounting manipulation, deception, or serious fraud
allegations.

Financial Risk = major loss, liquidity concern, solvency concern,
earnings warning, or material financial deterioration.

Operational Risk = major disruption, cyber incident, supply failure,
production failure, or similar operational event.

Compliance = material compliance failure or compliance investigation.

None = no material risk category is present.

SUMMARY:
Return one concise, factual sentence based only on the provided news.
Do not invent facts.
"""


# =========================================================
# Marketaux Helpers
# =========================================================

def get_source_name(source):
    if isinstance(source, dict):
        return (
            source.get("name")
            or source.get("domain")
            or source.get("id")
            or "Unknown source"
        )

    return source or "Unknown source"


def get_first(item, *keys, default=None):
    """
    Return the first non-empty value found in the supplied keys.
    """

    if not isinstance(item, dict):
        return default

    for key in keys:
        value = item.get(key)

        if value not in (None, ""):
            return value

    return default


def extract_earnings_items(payload):
    """
    Support several common API response structures.
    """

    if isinstance(payload, list):
        return payload

    if not isinstance(payload, dict):
        return []

    for key in [
        "data",
        "earnings",
        "results",
        "events",
        "items",
    ]:
        value = payload.get(key)

        if isinstance(value, list):
            return value

    return []


def parse_earnings_date(value):
    """
    Convert a common ISO/date value to datetime.
    """

    if not value:
        return None

    value = str(value).strip()

    try:
        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )
    except ValueError:
        pass

    for date_format in [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
    ]:
        try:
            return datetime.strptime(
                value,
                date_format,
            )
        except ValueError:
            continue

    return None


def infer_session_from_datetime(dt, raw_session=""):
    """
    Infer pre-market vs after-market from the earnings timestamp.
    """

    normalized = normalize_session(raw_session)

    if normalized != "Unspecified":
        return normalized

    if not dt:
        return "Unspecified"

    minutes = dt.hour * 60 + dt.minute

    if minutes >= 16 * 60:
        return "After Market"

    if minutes <= 12 * 60 + 30:
        return "Pre Market"

    return "Unspecified"


def normalize_session(value):
    """
    Normalize different API names for earnings timing.
    """

    value = str(
        value or ""
    ).strip().lower()

    if any(
        word in value
        for word in [
            "pre",
            "before",
            "bmo",
            "before market",
        ]
    ):
        return "Pre Market"

    if any(
        word in value
        for word in [
            "after",
            "post",
            "amc",
            "after market",
        ]
    ):
        return "After Market"

    return "Unspecified"


def normalize_earnings_item(item):
    """
    Convert the endpoint object into the fields FinRadar needs.
    """

    raw_date = get_first(
        item,
        "earningDate",
        "earning_date",
        "date",
        "earnings_date",
        "earningsDate",
        "report_date",
        "reportDate",
        "datetime",
    )

    parsed_date = parse_earnings_date(
        raw_date
    )

    symbol = get_first(
        item,
        "symbol",
        "ticker",
        "stock",
        default="",
    )

    company = get_first(
        item,
        "name",
        "company",
        "company_name",
        "companyName",
        default=symbol,
    )

    raw_session = get_first(
        item,
        "session",
        "time",
        "timing",
        "market_session",
        "marketSession",
        "when",
        default="",
    )

    logo = get_first(
        item,
        "logo",
        "logo_url",
        "logoUrl",
        "image",
        "image_url",
        default="",
    )

    return {
        "date": parsed_date,
        "symbol": str(symbol or ""),
        "company": str(company or ""),
        "session": infer_session_from_datetime(
            parsed_date,
            raw_session,
        ),
        "logo": str(logo or ""),
    }


def get_current_trading_week_label(reference_date=None):
    if reference_date is None:
        reference_date = datetime.now().astimezone().date()

    start_of_week = (
        reference_date
        - timedelta(days=reference_date.weekday())
    )
    end_of_week = start_of_week + timedelta(days=4)

    return (
        f"DATE: {start_of_week.strftime('%b %d, %Y')} - "
        f"{end_of_week.strftime('%b %d, %Y')}"
    ).upper()


def earnings_company_html(item):
    symbol = html.escape(
        item["symbol"] or ""
    ) or "Unknown"

    company = html.escape(
        item["company"] or ""
    ) or symbol

    logo = (item["logo"] or "").strip()

    logo_html = ""

    if logo.startswith(
        ("https://", "http://")
    ):
        safe_logo = html.escape(
            logo,
            quote=True,
        )

        logo_html = f"""
        <img
            class="earnings-logo"
            src="{safe_logo}"
            alt="{symbol}"
        />
        """
    else:
        initials = html.escape(
            (symbol[:3] or company[:3] or "A").upper()
        )
        logo_html = f"""
        <div class="earnings-logo earnings-logo-fallback">
            {initials}
        </div>
        """

    fallback = symbol or company or "Company"

    return f"""
    <div class="earnings-company">
        {logo_html}

        <div class="earnings-company-text">
            <strong>{fallback}</strong>
            <span>{company}</span>
        </div>
    </div>
    """


def build_earnings_calendar_html(payload=None, *, loading=False, error=None):
    if error:
        safe_error = html.escape(str(error))
        return f"""
        <div class="earnings-calendar">
            <div class="earnings-error">
                Unable to load the earnings calendar.<br>
                <small>{safe_error}</small>
            </div>
        </div>
        """

    if loading:
        return """
        <div class="earnings-calendar">
            <div class="earnings-empty">
                Loading this week's earnings calendar...
            </div>
        </div>
        """

    raw_items = extract_earnings_items(
        payload
    )

    earnings = []

    for raw_item in raw_items:
        if not isinstance(raw_item, dict):
            continue

        item = normalize_earnings_item(
            raw_item
        )

        if item["date"]:
            earnings.append(item)

    if not earnings:
        return """
        <div class="earnings-calendar">
            <div class="earnings-empty">
                No earnings events were returned for this week.
            </div>
        </div>
        """

    weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
    ]

    grouped = {
        day: {
            "Pre Market": [],
            "After Market": [],
            "Unspecified": [],
        }
        for day in weekdays
    }

    ordered_earnings = sorted(
        earnings,
        key=lambda item: (
            item["date"],
            item["symbol"],
            item["company"],
            item["session"],
        ),
    )

    for item in ordered_earnings:
        day_name = item["date"].strftime("%A")

        if day_name not in grouped:
            continue

        grouped[day_name][item["session"]].append(item)

    date_label = get_current_trading_week_label()

    columns = ""

    for day in weekdays:
        pre_items = "".join(
            earnings_company_html(item)
            for item in grouped[day]["Pre Market"]
        )
        after_items = "".join(
            earnings_company_html(item)
            for item in grouped[day]["After Market"]
        )
        unspecified_items = "".join(
            earnings_company_html(item)
            for item in grouped[day]["Unspecified"]
        )

        if not pre_items:
            pre_items = '<div class="earnings-none">—</div>'

        if not after_items:
            after_items = '<div class="earnings-none">—</div>'

        extra = ""

        if unspecified_items:
            extra = f"""
            <div class="earnings-session">
                <div class="earnings-session-title">
                    Time TBD
                </div>
                {unspecified_items}
            </div>
            """

        columns += f"""
        <div class="earnings-day">
            <div class="earnings-day-title">
                {day}
            </div>
            <div class="earnings-session">
                <div class="earnings-session-title">
                    Pre Market
                </div>
                {pre_items}
            </div>
            <div class="earnings-session">
                <div class="earnings-session-title">
                    After Market
                </div>
                {after_items}
            </div>
            {extra}
        </div>
        """

    return f"""
    <div class="earnings-calendar">
        <div class="earnings-calendar-header">
            <div>
                <div class="earnings-title">
                    Earnings Calendar
                </div>
                <div class="earnings-subtitle">
                    Scheduled earnings announcements for the current trading week.
                </div>
            </div>
            <div class="earnings-date">
                {date_label}
            </div>
        </div>
        <div class="earnings-week">
            {columns}
        </div>
    </div>
    """


def fetch_weekly_earnings():
    try:
        response = requests.get(
            EARNINGS_URL,
            timeout=25,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        return build_earnings_calendar_html(error=exc)
    except ValueError:
        return build_earnings_calendar_html(
            error="The earnings endpoint returned an invalid JSON response."
        )

    return build_earnings_calendar_html(payload)


def format_published_at(value):
    if not value:
        return "Unknown"

    try:
        dt = datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )

        return dt.strftime(
            "%d %b %Y, %H:%M UTC"
        )

    except ValueError:
        return value


def get_selected_article(selected_article, articles):
    if not selected_article or not articles:
        return None

    try:
        article_index = int(
            selected_article.split(".", 1)[0]
        ) - 1

        return articles[article_index]

    except (ValueError, IndexError):
        return None


def safe_external_url(value):
    """
    Allow only normal HTTP/HTTPS external links.
    """
    url = str(value or "").strip()

    try:
        parsed = urlparse(url)
    except ValueError:
        return ""

    if (
        parsed.scheme.lower() not in {"http", "https"}
        or not parsed.netloc
    ):
        return ""

    return url


def safe_article_text(value, fallback=""):
    """
    Escape external article text before rendering it in Markdown.
    """
    text = str(value or fallback)

    # Keep external content as plain text and collapse unusual whitespace.
    text = " ".join(text.split())

    # Escape HTML first.
    text = html.escape(
        text,
        quote=False,
    )

    # Neutralize common Markdown formatting / link syntax.
    for marker in (
        "\\",
        "`",
        "*",
        "_",
        "[",
        "]",
        "#",
    ):
        text = text.replace(
            marker,
            "\\" + marker,
        )

    return text


def article_markdown(selected_article, articles):
    article = get_selected_article(
        selected_article,
        articles
    )

    if not article:
        return "Select a news article to view its details."

    title = safe_article_text(
        article.get("title"),
        "Untitled article"
    )

    description = safe_article_text(
        article.get("description")
        or article.get("snippet"),
        "No description available."
    )

    published_at = safe_article_text(
        format_published_at(
            article.get("published_at")
        ),
        "Unknown"
    )

    source = safe_article_text(
        get_source_name(
            article.get("source")
        ),
        "Unknown source"
    )

    url = safe_external_url(
        article.get("url")
    )

    output = f"""
### {title}

**Source:** {source}  
**Published:** {published_at}

{description}
"""

    if url:
        safe_url = html.escape(
            url,
            quote=True
        )

        output += (
            "\n\n"
            f'<a href="{safe_url}" '
            f'target="_blank" '
            f'rel="noopener noreferrer">'
            f'Open original article'
            f'</a>'
        )

    return output


def handle_article_selection(selected_article, articles):
    if not selected_article:
        return (
            "Select a news article to view its details.",
            gr.update(visible=False),
        )

    return (
        article_markdown(
            selected_article,
            articles
        ),
        gr.update(visible=True),
    )


def reset_fetch_state(symbol):
    """
    Reset the news pagination UI when the user edits the ticker.
    """

    return (
        gr.update(value="Fetch Latest News"),
        1,
        gr.update(visible=False),
        gr.update(choices=[], value=None),
        [],
        "Enter a ticker and click **Fetch Latest News**.",
        ANALYSIS_PLACEHOLDER,
        "No news batch loaded yet.",
        gr.update(visible=False),
        gr.update(visible=False),
    )


def article_to_analysis_text(article):
    if not article:
        return ""

    title = article.get("title", "")

    description = (
        article.get("description")
        or article.get("snippet")
        or ""
    )

    return f"""
Headline:
{title}

Description:
{description}
""".strip()


# =========================================================
# Marketaux Live News
# =========================================================

def fetch_marketaux_news(symbol, current_page, last_symbol):
    symbol = (symbol or "").strip().upper()

    if not symbol:
        return (
            gr.update(
                choices=[],
                value=None,
                visible=False,
            ),
            [],
            "⚠️ Please enter a ticker symbol, for example `TSLA`.",
            ANALYSIS_PLACEHOLDER,
            "Enter a ticker and click **Fetch Latest News**.",
            1,
            "",
            gr.update(value="Fetch Latest News"),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False)
        )

    if not MARKETAUX_API_KEY:
        return (
            gr.update(
                choices=[],
                value=None,
                visible=False,
            ),
            [],
            "❌ Marketaux API key was not found.",
            ANALYSIS_PLACEHOLDER,
            "Enter a ticker and click **Fetch Latest News**.",
            1,
            "",
            gr.update(value="Fetch Latest News"),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False)
        )

    # Start again from page 1 when the ticker changes.
    if symbol != last_symbol:
        page = 1
    else:
        page = current_page

    params = {
        "api_token": MARKETAUX_API_KEY,
        "symbols": symbol,
        "filter_entities": "true",
        "language": "en",
        "limit": 3,
        "page": page,
    }

    try:
        response = requests.get(
            MARKETAUX_URL,
            params=params,
            timeout=25,
        )

        response.raise_for_status()

        payload = response.json()

    except requests.RequestException as exc:
        print("Marketaux request error:", exc)
        return (
            gr.update(
                choices=[],
                value=None,
                visible=False,
            ),
            [],
            "⚠️ Live financial news is temporarily unavailable. "
            "Please try again or use the Manual Public News tab.",
            ANALYSIS_PLACEHOLDER,
            "Enter a ticker and click **Fetch Latest News**.",
            page,
            last_symbol,
            gr.update(value="Fetch Latest News"),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False)
        )

    except ValueError:
        return (
            gr.update(
                choices=[],
                value=None,
                visible=False,
            ),
            [],
            "❌ Marketaux returned an invalid response.",
            ANALYSIS_PLACEHOLDER,
            "Enter a ticker and click **Fetch Latest News**.",
            page,
            last_symbol,
            gr.update(value="Fetch Latest News"),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False)
        )

    articles = payload.get("data", [])

    if not articles:
        return (
            gr.update(
                choices=[],
                value=None,
                visible=False,
            ),
            [],
            f"No recent news was found for **{symbol}**.",
            ANALYSIS_PLACEHOLDER,
            f"No news batch loaded yet for {symbol}.",
            1,
            "",
            gr.update(value="Fetch Latest News"),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False)
        )

    choices = []

    for index, article in enumerate(
        articles,
        start=1
    ):
        title = article.get(
            "title",
            "Untitled article"
        )

        choices.append(
            f"{index}. {title}"
        )

    next_page = page + 1
    start_article = ((page - 1) * 3) + 1
    end_article = start_article + len(articles) - 1
    button_text = "Load More News"

    page_message = (
        f"**Showing batch {page} for {symbol} "
        f"— articles {start_article}–{end_article}**"
    )

    return (
        gr.update(
            choices=choices,
            value=None,
            visible=True,
        ),
        articles,
        "Select a news article to view its details.",
        ANALYSIS_PLACEHOLDER,
        page_message,
        next_page,
        symbol,
        gr.update(value=button_text),
        gr.update(visible=False),
        gr.update(visible=True),
        gr.update(visible=True)
    )


# =========================================================
# OpenAI Analysis
# =========================================================

def analyze_financial_text(financial_text):
    financial_text = (
        financial_text or ""
    ).strip()

    if not financial_text:
        return ANALYSIS_PLACEHOLDER

    if not OPENAI_API_KEY or not openai_client:
        return """
        <div class="analysis-empty">
            <div class="analysis-empty-icon">!</div>
            <div class="analysis-empty-title">
                OpenAI API key was not found.
            </div>
            <div class="analysis-empty-text">
                Check your .env file.
            </div>
        </div>
        """

    try:
        response = (
            openai_client.chat.completions.create(
                model="gpt-5-mini",
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": financial_text
                    }
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema":
                        FINANCIAL_ANALYSIS_SCHEMA
                }
            )
        )

        content = (
            response
            .choices[0]
            .message
            .content
        )

        result = json.loads(content)

    except Exception as exc:
        safe_error = html.escape(
            f"{type(exc).__name__}: {exc}"
        )
        return f"""
        <div class="analysis-empty">
            <div class="analysis-empty-icon">!</div>
            <div class="analysis-empty-title">
                AI analysis failed
            </div>
            <div class="analysis-empty-text">
                {safe_error}
            </div>
        </div>
        """

    return format_analysis(result)


def analyze_selected_article(
    selected_article,
    articles
):
    article = get_selected_article(
        selected_article,
        articles
    )

    if not article:
        return ANALYSIS_PLACEHOLDER

    financial_text = article_to_analysis_text(
        article
    )

    return analyze_financial_text(
        financial_text
    )


# =========================================================
# Deterministic Risk / Escalation Rule
# =========================================================

def requires_escalation(result):
    priority = result.get(
        "priority",
        ""
    )

    risk_type = result.get(
        "risk_type",
        "None"
    )

    sentiment = result.get(
        "sentiment",
        "Neutral"
    )

    if priority == "High":
        return True

    if risk_type == "Fraud":
        return True

    if (
        risk_type
        in {
            "Regulatory",
            "Legal",
            "Compliance"
        }
        and sentiment == "Negative"
    ):
        return True

    return False


def format_analysis(result):
    target = html.escape(
        str(result.get("target", "Unknown"))
    )
    business_area = html.escape(
        str(result.get("business_area", "Unknown"))
    )
    topic = html.escape(
        str(result.get("topic", "Unknown"))
    )
    sentiment = html.escape(
        str(result.get("sentiment", "Unknown"))
    )
    priority = html.escape(
        str(result.get("priority", "Unknown"))
    )
    risk_type = html.escape(
        str(result.get("risk_type", "None"))
    )
    summary = html.escape(
        str(result.get("summary", ""))
    ).replace("\n", "<br>")

    escalation = requires_escalation(result)

    if escalation:
        card_class = "risk"
        status_icon = "!"
        status_title = "HIGH PRIORITY / RISK ALERT"
        status_subtitle = "Immediate analyst review required."
    else:
        card_class = "standard"
        status_icon = "✓"
        status_title = "STANDARD ANALYST REVIEW"
        status_subtitle = "No immediate escalation rule was triggered."

    sentiment_class = ""
    if sentiment.lower() == "positive":
        sentiment_class = "value-positive"
    elif sentiment.lower() == "negative":
        sentiment_class = "value-negative"

    priority_class = ""
    if priority.lower() == "high":
        priority_class = "value-high"
    elif priority.lower() == "medium":
        priority_class = "value-medium"
    elif priority.lower() == "low":
        priority_class = "value-low"

    return f"""
<div class="analysis-card {card_class}">
    <div class="analysis-status">
        <div class="analysis-status-icon">
            {status_icon}
        </div>

        <div>
            <div class="analysis-status-title">
                {status_title}
            </div>
            <div class="analysis-status-subtitle">
                {status_subtitle}
            </div>
        </div>
    </div>

    <div class="analysis-grid">
        <div class="analysis-label">Target</div>
        <div class="analysis-value">{target}</div>

        <div class="analysis-label">Business Area</div>
        <div class="analysis-value">{business_area}</div>

        <div class="analysis-label">Topic</div>
        <div class="analysis-value">{topic}</div>

        <div class="analysis-label">Sentiment</div>
        <div class="analysis-value {sentiment_class}">
            {sentiment}
        </div>

        <div class="analysis-label">Priority</div>
        <div class="analysis-value {priority_class}">
            {priority}
        </div>

        <div class="analysis-label">Risk Type</div>
        <div class="analysis-value">{risk_type}</div>

        <div class="analysis-label">Summary</div>
        <div class="analysis-value analysis-summary">
            {summary}
        </div>
    </div>
</div>
"""


HEADER_HTML = f"""
<div class="fr-header">
    <div class="fr-brand">
        <div class="fr-logo-shell">
            <img
                src="{LOGO_URI}"
                class="fr-logo"
                alt="FinRadar AI logo"
            />
        </div>

        <div class="fr-product-name">
            FinRadar AI
        </div>
    </div>

    <div class="fr-header-text">
        <div class="fr-subtitle">
            Financial News Intelligence for Analysts
        </div>

        <div class="fr-trust-line">
            AI Assists — Humans Decide
        </div>
    </div>
</div>
"""


ANALYSIS_PLACEHOLDER = """
<div class="analysis-empty">
    <div class="analysis-empty-icon">✦</div>
    <div class="analysis-empty-title">AI Analysis Results</div>
    <div class="analysis-empty-text">
        Select a news article and run the AI analysis
        to see the structured FinRadar result.
    </div>
</div>
"""


FINRADAR_CSS = """
/* =========================================================
   FinRadar AI - Light Financial UI
   ========================================================= */

:root {
    color-scheme: light !important;

    --fr-bg: #f6f8fb;
    --fr-card: #ffffff;
    --fr-card-soft: #f8fafc;

    --fr-text: #0f172a;
    --fr-muted: #64748b;

    --fr-border: #dbe3ee;

    --fr-blue: #1677e8;
    --fr-blue-dark: #0b5fc2;
    --fr-blue-soft: #eff6ff;

    --fr-teal: #0891b2;

    --fr-green: #15803d;
    --fr-green-soft: #f0fdf4;

    --fr-red: #dc2626;
    --fr-red-soft: #fff5f5;

    --fr-amber: #d97706;
}

html,
body {
    background: var(--fr-bg) !important;
    color: var(--fr-text) !important;
}

.gradio-container {
    background: var(--fr-bg) !important;
    color: var(--fr-text) !important;
    font-family:
        Inter,
        ui-sans-serif,
        system-ui,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif !important;
    max-width: 1600px !important;
    margin: 0 auto !important;
    padding-bottom: 40px !important;
}

.fr-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 36px;
    background: #ffffff;
    border: 1px solid var(--fr-border);
    border-radius: 16px;
    padding: 18px 24px;
    margin-bottom: 18px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
}

.fr-brand {
    display: flex;
    align-items: center;
    gap: 14px;
}

.fr-logo {
    width: 68px;
    height: 68px;
    object-fit: contain;
    border-radius: 50%;
}

.fr-product-name {
    font-size: 32px;
    line-height: 1.1;
    font-weight: 750;
    color: #0f2747;
    white-space: nowrap;
}

.fr-header-text {
    flex: 1;
    border-left: 1px solid var(--fr-border);
    padding-left: 28px;
}

.fr-subtitle {
    font-size: 22px;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 4px;
}

.fr-trust-line {
    font-size: 18px;
    font-weight: 700;
    color: var(--fr-blue);
}

.fr-workspace-card,
.fr-analysis-panel {
    background: var(--fr-card);
    border: 1px solid var(--fr-border);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 2px 7px rgba(15, 23, 42, 0.035);
}

.fr-section-title {
    font-size: 19px;
    font-weight: 700;
    color: var(--fr-text);
    margin-bottom: 5px;
}

.fr-section-help {
    font-size: 16px;
    color: #475569;
    margin-bottom: 14px;
}

.gradio-container input,
.gradio-container textarea {
    background: #ffffff !important;
    color: var(--fr-text) !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 9px !important;
}

.gradio-container input:focus,
.gradio-container textarea:focus {
    border-color: var(--fr-blue) !important;
    box-shadow: 0 0 0 3px rgba(22, 119, 232, 0.10) !important;
}

.gradio-container label {
    color: #334155 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

.fr-fetch-btn button {
    font-size: 14px !important;
    font-weight: 700 !important;
    min-height: 46px !important;
    padding: 0 22px !important;
}

.fr-analyze-btn button {
    background: linear-gradient(135deg, #1677e8, #0867c9) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    min-height: 48px !important;
    box-shadow: 0 4px 12px rgba(22, 119, 232, 0.18) !important;
}

.fr-analyze-btn button:hover {
    background: linear-gradient(135deg, #0b6fd8, #0558ad) !important;
}

.fr-news-list {
    background: var(--fr-card-soft);
    border: 1px solid var(--fr-border);
    border-radius: 12px;
    padding: 10px 12px;
    margin-bottom: 16px;
}

.fr-article-card {
    background: #ffffff;
    border: 1px solid var(--fr-border);
    border-radius: 12px;
    padding: 18px;
    margin-top: 12px;
    margin-bottom: 16px;
}

.fr-article-card h3 {
    color: var(--fr-text) !important;
    font-size: 19px !important;
}

.fr-article-card p {
    color: #334155 !important;
    font-size: 15px !important;
    line-height: 1.65 !important;
}

.fr-article-card a {
    color: var(--fr-blue) !important;
    font-weight: 600;
}

.fr-analysis-heading {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 3px;
    font-size: 19px;
    font-weight: 700;
    color: var(--fr-text);
}

.fr-analysis-caption {
    font-size: 15px;
    color: #64748b;
    margin-bottom: 16px;
}

.analysis-empty {
    border: 1px dashed #cbd5e1;
    border-radius: 12px;
    background: #f8fafc;
    padding: 38px 24px;
    text-align: center;
    color: var(--fr-muted);
}

.analysis-empty-icon {
    font-size: 27px;
    color: var(--fr-blue);
    margin-bottom: 8px;
}

.analysis-empty-title {
    font-size: 17px;
    font-weight: 700;
    color: #334155;
    margin-bottom: 5px;
}

.analysis-empty-text {
    font-size: 14px;
}

.analysis-card {
    border-radius: 13px;
    padding: 18px;
    overflow: hidden;
}

.analysis-card.standard {
    background: var(--fr-green-soft);
    border: 1px solid #86c99a;
}

.analysis-card.risk {
    background: var(--fr-red-soft);
    border: 1px solid #ef8c8c;
}

.analysis-status {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 17px;
}

.analysis-status-icon {
    width: 37px;
    height: 37px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 20px;
    font-weight: 800;
    flex-shrink: 0;
}

.standard .analysis-status-icon {
    background: #dcfce7;
    color: var(--fr-green);
}

.risk .analysis-status-icon {
    background: #fee2e2;
    color: var(--fr-red);
}

.analysis-status-title {
    font-size: 17px;
    font-weight: 800;
    margin-bottom: 3px;
}

.standard .analysis-status-title {
    color: var(--fr-green);
}

.risk .analysis-status-title {
    color: var(--fr-red);
}

.analysis-status-subtitle {
    color: #475569;
    font-size: 14px;
}

.analysis-grid {
    display: grid;
    grid-template-columns: minmax(130px, 36%) 1fr;
    background: white;
    border: 1px solid rgba(148, 163, 184, 0.45);
    border-radius: 9px;
    overflow: hidden;
}

.analysis-label,
.analysis-value {
    padding: 11px 13px;
    border-bottom: 1px solid #e2e8f0;
    font-size: 14px;
    line-height: 1.45;
}

.analysis-label {
    background: #f8fafc;
    font-weight: 700;
    color: #334155;
    border-right: 1px solid #e2e8f0;
}

.analysis-value {
    color: var(--fr-text);
    font-weight: 550;
}

.analysis-summary {
    line-height: 1.6;
}

.value-positive {
    color: var(--fr-green);
    font-weight: 700;
}

.value-negative {
    color: var(--fr-red);
    font-weight: 700;
}

.value-high {
    color: var(--fr-red);
    font-weight: 750;
}

.value-medium {
    color: var(--fr-amber);
    font-weight: 700;
}

.value-low {
    color: var(--fr-green);
    font-weight: 700;
}

.gradio-container [role="tab"] {
    font-weight: 650 !important;
}

footer {
    display: none !important;
}

.earnings-calendar {
    background: #ffffff !important;
    border: 1px solid #dbe3ee !important;
    border-radius: 16px !important;
    padding: 20px !important;
    margin-top: 18px !important;
    color: #0f172a !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06) !important;
}

.earnings-calendar-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 18px;
}

.earnings-title {
    color: #0f172a !important;
    font-size: 20px !important;
    font-weight: 750 !important;
    line-height: 1.25 !important;
}

.earnings-subtitle {
    color: #64748b !important;
    font-size: 14px !important;
    margin-top: 4px !important;
}

.earnings-date {
    color: #0b5fc2 !important;
    background: #eff6ff !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 999px !important;
    padding: 7px 12px !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    white-space: nowrap;
}

.earnings-week {
    display: grid !important;
    grid-template-columns: repeat(5, minmax(170px, 1fr)) !important;
    background: #ffffff !important;
    border: 1px solid #dbe3ee !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

.earnings-day {
    background: #ffffff !important;
    color: #0f172a !important;
    min-height: 280px !important;
    border-right: 1px solid #dbe3ee !important;
}

.earnings-day:last-child {
    border-right: none !important;
}

.earnings-day-title {
    background: #102c4c !important;
    color: #ffffff !important;
    text-align: center !important;
    padding: 11px 8px !important;
    font-size: 14px !important;
    font-weight: 750 !important;
    letter-spacing: 0.01em !important;
}

.earnings-session {
    background: #ffffff !important;
    color: #0f172a !important;
    padding: 12px 10px !important;
    border-bottom: 1px solid #e8edf4 !important;
}

.earnings-session:last-child {
    border-bottom: none !important;
}

.earnings-session-title {
    display: inline-block !important;
    color: #0b5fc2 !important;
    background: #eff6ff !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 6px !important;
    padding: 4px 7px !important;
    margin-bottom: 10px !important;
    font-size: 11px !important;
    font-weight: 750 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
}

.earnings-day > .earnings-session:nth-of-type(2) .earnings-session-title {
    color: #0f766e !important;
    background: #f0fdfa !important;
    border-color: #99f6e4 !important;
}

.earnings-company {
    display: flex !important;
    align-items: center !important;
    gap: 9px !important;
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 9px !important;
    padding: 8px !important;
    margin-bottom: 7px !important;
    color: #0f172a !important;
    transition: border-color 0.15s ease, background 0.15s ease, transform 0.15s ease !important;
}

.earnings-company:hover {
    background: #f1f5f9 !important;
    border-color: #93c5fd !important;
    transform: translateY(-1px);
}

.earnings-logo {
    width: 32px !important;
    height: 32px !important;
    flex-shrink: 0 !important;
    object-fit: contain !important;
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 7px !important;
    padding: 3px !important;
}

.earnings-logo-fallback {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: #e0f2fe !important;
    color: #0284c7 !important;
    font-size: 10px !important;
    font-weight: 800 !important;
    text-align: center !important;
}

.earnings-company-text {
    display: flex !important;
    flex-direction: column !important;
    min-width: 0 !important;
    color: #0f172a !important;
}

.earnings-company-text strong {
    color: #0f172a !important;
    font-size: 13px !important;
    font-weight: 750 !important;
    line-height: 1.3 !important;
}

.earnings-company-text span {
    color: #64748b !important;
    font-size: 11px !important;
    margin-top: 2px !important;
    line-height: 1.3 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}

.earnings-none {
    color: #94a3b8 !important;
    background: transparent !important;
    text-align: center !important;
    font-size: 15px !important;
    padding: 14px 5px !important;
}

.earnings-error {
    color: #b91c1c !important;
    background: #fff5f5 !important;
    border: 1px solid #fecaca !important;
    border-radius: 10px !important;
    padding: 18px !important;
    font-size: 14px !important;
}

.earnings-empty {
    color: #64748b !important;
    background: #f8fafc !important;
    border: 1px dashed #cbd5e1 !important;
    border-radius: 10px !important;
    padding: 24px !important;
    text-align: center !important;
    font-size: 14px !important;
}

.earnings-calendar *,
.earnings-calendar div,
.earnings-calendar span,
.earnings-calendar strong {
    text-shadow: none !important;
}

.earnings-refresh-btn {
    max-width: 180px !important;
}

.earnings-refresh-btn button {
    font-size: 13px !important;
    font-weight: 700 !important;
    min-height: 38px !important;
}

@media (max-width: 1050px) {
    .earnings-week {
        grid-template-columns: 1fr !important;
    }

    .earnings-day {
        min-height: auto !important;
        border-right: none !important;
        border-bottom: 1px solid #dbe3ee !important;
    }

    .earnings-calendar-header {
        flex-direction: column !important;
    }
}

/* =========================================================
   Final UI Overrides
   ========================================================= */

html,
body,
body > gradio-app,
gradio-app,
.gradio-container,
main,
.main,
.wrap {
    width: 100% !important;
    min-height: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    background: #f4f7fb !important;
    color: #0f172a !important;
}

.gradio-container {
    max-width: none !important;
    padding: 18px 24px 36px !important;
}

.fr-header {
    background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%) !important;
    border: 1px solid #dbe3ee !important;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06) !important;
}

.fr-brand {
    gap: 18px !important;
}

.fr-logo-shell {
    position: relative !important;
    width: 100px !important;
    height: 100px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: 50% !important;
    background: radial-gradient(
        circle at 30% 30%,
        #3b82f6 0%,
        #1677e8 52%,
        #0b5fc2 100%
    ) !important;
    box-shadow:
        0 0 0 1px rgba(59, 130, 246, 0.32),
        0 0 0 7px rgba(219, 234, 254, 0.92),
        0 14px 30px rgba(22, 119, 232, 0.16) !important;
    overflow: hidden !important;
}

.fr-logo-shell::after {
    content: "" !important;
    position: absolute !important;
    inset: 9px !important;
    border-radius: 50% !important;
    border: 1px solid rgba(255, 255, 255, 0.34) !important;
    animation: finradarRadarPulse 3.2s ease-in-out infinite !important;
    pointer-events: none !important;
}

.fr-logo {
    width: 90px !important;
    height: 90px !important;
    object-fit: contain !important;
    border-radius: 50% !important;
    position: relative !important;
    z-index: 1 !important;
}

@keyframes finradarRadarPulse {
    0% {
        transform: scale(0.92);
        opacity: 0.2;
    }

    50% {
        transform: scale(1);
        opacity: 0.8;
    }

    100% {
        transform: scale(1.06);
        opacity: 0.08;
    }
}

.fr-product-name {
    font-size: 33px !important;
    color: #0f2747 !important;
    letter-spacing: -0.03em !important;
}

.fr-subtitle {
    font-size: 21px !important;
    color: #1f2937 !important;
    font-weight: 700 !important;
}

.fr-trust-line {
    font-size: 17px !important;
    color: #0b5fc2 !important;
    letter-spacing: 0.01em !important;
    font-weight: 700 !important;
}

.fr-header-text {
    padding-left: 24px !important;
    border-left: 1px solid #dbe3ee !important;
}

.fr-section-title {
    font-size: 20px !important;
    color: #0f172a !important;
}

.fr-section-help {
    color: #475569 !important;
    font-size: 15px !important;
}

.fr-workspace-card,
.fr-analysis-panel {
    background: rgba(255, 255, 255, 0.98) !important;
    border: 1px solid #dbe3ee !important;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05) !important;
}

[role="tablist"] {
    background: #ffffff !important;
    border: 1px solid #dbe3ee !important;
    border-radius: 14px !important;
    padding: 6px !important;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04) !important;
}

button[role="tab"] {
    color: #475569 !important;
    border-radius: 10px !important;
    border: none !important;
    background: transparent !important;
}

button[role="tab"]:hover {
    background: #eff6ff !important;
    color: #0b5fc2 !important;
}

button[role="tab"][aria-selected="true"] {
    background: #1677e8 !important;
    color: #ffffff !important;
    box-shadow: 0 6px 16px rgba(22, 119, 232, 0.18) !important;
}

.fr-field-label {
    color: #334155 !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    margin-bottom: 8px !important;
}

.fr-field-label-spacer {
    visibility: hidden !important;
}

.fr-ticker-input,
.fr-ticker-input input {
    width: 100% !important;
}

.fr-ticker-input input {
    min-height: 46px !important;
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    color: #0f172a !important;
}

.fr-news-list {
    background: #f8fafc !important;
    border: 1px solid #dbe3ee !important;
    border-radius: 12px !important;
    padding: 10px 12px !important;
}

.fr-news-list:not(:has(input[type="radio"])) {
    display: none !important;
}

.fr-news-list label,
.fr-news-list span {
    color: #0f172a !important;
    white-space: normal !important;
}

.fr-news-list input[type="radio"] {
    accent-color: #1677e8 !important;
}

.fr-news-list label {
    align-items: flex-start !important;
    gap: 10px !important;
    padding: 8px 6px !important;
}

.fr-news-list label:hover {
    background: #eff6ff !important;
}

.fr-news-list input[type="radio"]:checked + span,
.fr-news-list input[type="radio"]:checked ~ span {
    color: #0b5fc2 !important;
    font-weight: 700 !important;
}

.fr-article-card {
    background: #ffffff !important;
    border: 1px solid #dbe3ee !important;
    border-radius: 14px !important;
    color: #0f172a !important;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04) !important;
}

.fr-article-card,
.fr-article-card * {
    text-shadow: none !important;
}

.analysis-empty {
    background: #f8fafc !important;
    border: 1px dashed #cbd5e1 !important;
    color: #64748b !important;
}

.analysis-card.standard {
    background: #f0fdf4 !important;
    border: 1px solid #86efac !important;
}

.analysis-card.risk {
    background: #fff5f5 !important;
    border: 1px solid #fca5a5 !important;
}

.analysis-status-title,
.analysis-label,
.analysis-value {
    color: #0f172a !important;
}

.analysis-status-positive,
.value-positive,
.value-low {
    color: #15803d !important;
}

.analysis-status-negative,
.value-negative,
.value-high {
    color: #dc2626 !important;
}

.value-medium {
    color: #d97706 !important;
}

.analysis-grid {
    border-color: #dbe3ee !important;
}

.analysis-label {
    background: #f8fafc !important;
}

.analysis-summary {
    color: #0f172a !important;
}

.fr-analysis-panel .analysis-empty,
.fr-analysis-panel .analysis-card {
    width: 100% !important;
}

.fr-analyze-btn button {
    box-shadow: 0 10px 20px rgba(22, 119, 232, 0.16) !important;
}

.fr-fetch-btn button {
    min-height: 46px !important;
    width: 100% !important;
    padding: 0 18px !important;
    font-size: 14px !important;
    font-weight: 700 !important;
}

.earnings-heading-row {
    display: flex !important;
    align-items: flex-start !important;
}

.earnings-heading-title {
    color: #0f172a !important;
    font-size: 20px !important;
    font-weight: 800 !important;
}

.earnings-heading-help {
    color: #64748b !important;
    font-size: 14px !important;
    margin-top: 4px !important;
}

.earnings-refresh-col {
    display: flex !important;
    align-items: flex-start !important;
    justify-content: flex-end !important;
}

.earnings-refresh-btn button {
    font-weight: 700 !important;
}

.earnings-day {
    min-height: 0 !important;
}

.earnings-calendar {
    margin-bottom: 0 !important;
}

footer {
    display: none !important;
}

@media (max-width: 1000px) {
    .gradio-container {
        padding: 14px 14px 28px !important;
    }

    .fr-header {
        flex-direction: column !important;
        align-items: flex-start !important;
    }

    .fr-header-text {
        border-left: none !important;
        padding-left: 0 !important;
    }

    .fr-logo-shell {
        width: 78px !important;
        height: 78px !important;
    }

    .fr-logo {
        width: 72px !important;
        height: 72px !important;
    }

    .fr-product-name {
        font-size: 26px !important;
    }

    .fr-section-title {
        font-size: 18px !important;
    }

    .earnings-heading-row,
    .earnings-refresh-col {
        width: 100% !important;
    }

    .earnings-refresh-col {
        justify-content: flex-start !important;
        margin-top: 10px !important;
    }
}

/* =========================================================
   FINAL NEWS SELECTOR FIX
   ========================================================= */

#finradar-news-selector {
    background: #f8fafc !important;
    color: #0f172a !important;
    border: 1px solid #dbe3ee !important;
    border-radius: 12px !important;
    padding: 10px !important;
    --checkbox-label-background-fill: #ffffff;
    --checkbox-label-background-fill-hover: #eff6ff;
    --checkbox-label-background-fill-selected: #eaf4ff;
    --checkbox-label-text-color: #172033;
    --checkbox-label-text-color-selected: #0f172a;
    --checkbox-label-border-color: #d8e1ec;
    --checkbox-label-border-color-hover: #7fb8f4;
}

#finradar-news-selector label {
    background: #ffffff !important;
    color: #172033 !important;
    border: 1px solid #d8e1ec !important;
    border-radius: 9px !important;
    padding: 12px 14px !important;
    margin: 6px 0 !important;
    box-shadow: none !important;
}

#finradar-news-selector label span {
    color: #172033 !important;
    font-size: 15px !important;
    font-weight: 650 !important;
    line-height: 1.45 !important;
}

#finradar-news-selector label:hover {
    background: #eff6ff !important;
    color: #0f172a !important;
    border-color: #7fb8f4 !important;
}

#finradar-news-selector label:hover span {
    color: #0f172a !important;
}

#finradar-news-selector label:has(
    input[type="radio"]:checked
) {
    background: #eaf4ff !important;
    color: #0f172a !important;
    border: 2px solid #1677e8 !important;
    box-shadow:
        0 0 0 2px
        rgba(22, 119, 232, 0.08) !important;
}

#finradar-news-selector label:has(
    input[type="radio"]:checked
) span {
    color: #0f172a !important;
}

#finradar-news-selector input[type="radio"] {
    accent-color: #1677e8 !important;
}

/* =========================================================
   AI PANEL HEIGHT FIX
   ========================================================= */

.fr-analysis-panel {
    align-self: flex-start !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
}

.fr-analysis-panel > div {
    min-height: 0 !important;
}

/* =========================================================
   BUTTON COLOR OVERRIDE
   ========================================================= */

.fr-fetch-btn button,
.earnings-refresh-btn button,
.fr-analyze-btn button {
    background: #1677E8 !important;
    background-color: #1677E8 !important;
    color: #ffffff !important;
    border-color: #1677E8 !important;
}

.fr-fetch-btn button:hover,
.earnings-refresh-btn button:hover,
.fr-analyze-btn button:hover {
    background: #0B5FC2 !important;
    background-color: #0B5FC2 !important;
    color: #ffffff !important;
    border-color: #0B5FC2 !important;
}

/* =========================================================
   FINAL SELECTED NEWS STYLE
   ========================================================= */

#finradar-news-selector label {
    background: #ffffff !important;
    color: #172033 !important;
    border: 1px solid #d8e1ec !important;
    border-radius: 9px !important;
    box-shadow: none !important;
}

#finradar-news-selector label span {
    color: #172033 !important;
}

#finradar-news-selector label:hover {
    background: #eff6ff !important;
    border-color: #93c5fd !important;
}

#finradar-news-selector label:has(
    input[type="radio"]:checked
) {
    background: #1677E8 !important;
    background-color: #1677E8 !important;
    color: #ffffff !important;
    border: 2px solid #1677E8 !important;
    box-shadow:
        0 3px 8px
        rgba(22, 119, 232, 0.22) !important;
}

#finradar-news-selector label:has(
    input[type="radio"]:checked
) span {
    color: #ffffff !important;
}

#finradar-news-selector label:has(
    input[type="radio"]:checked
):hover {
    background: #1677E8 !important;
    background-color: #1677E8 !important;
    color: #ffffff !important;
    border-color: #1677E8 !important;
}

#finradar-news-selector input[type="radio"] {
    accent-color: #1677E8 !important;
}

#finradar-news-selector label:has(
    input[type="radio"]:checked
) input[type="radio"] {
    accent-color: #ffffff !important;
}

/* =========================================================
   FINAL AI ANALYSIS WIDTH FIX
   ========================================================= */

.fr-analysis-panel {
    width: 100% !important;
    min-width: 0 !important;
    align-self: flex-start !important;
    padding: 22px !important;
}

.fr-analysis-panel .analysis-card {
    width: 100% !important;
    max-width: none !important;
    box-sizing: border-box !important;
    padding: 16px !important;
}

.fr-analysis-panel .analysis-grid {
    width: 100% !important;
    max-width: none !important;
    grid-template-columns: minmax(190px, 28%) minmax(0, 1fr) !important;
    box-sizing: border-box !important;
}

.analysis-card {
    padding: 16px !important;
}

.analysis-status {
    margin-bottom: 14px !important;
}

.analysis-label {
    min-width: 0 !important;
    font-size: 15px !important;
    padding: 12px 14px !important;
}

.analysis-value {
    min-width: 0 !important;
    font-size: 15px !important;
    padding: 12px 16px !important;
    overflow-wrap: normal !important;
    word-break: normal !important;
}

.analysis-summary {
    line-height: 1.55 !important;
    white-space: normal !important;
    word-break: normal !important;
    overflow-wrap: break-word !important;
}

"""


# =========================================================
# Gradio UI
# =========================================================

with gr.Blocks(
    title="FinRadar AI",
    css=FINRADAR_CSS,
    theme=gr.themes.Soft(),
    fill_width=True,
) as demo:

    gr.HTML(
        HEADER_HTML
    )

    with gr.Tabs():
        with gr.Tab(
            "◉ Live News"
        ):
            with gr.Row(
                equal_height=False
            ):
                with gr.Column(
                    scale=5,
                    min_width=460,
                    elem_classes=[
                        "fr-workspace-card"
                    ],
                ):
                    gr.HTML(
                        """
                        <div class="fr-section-title">
                            Live Financial News
                        </div>

                        <div class="fr-section-help">
                            Fetch public financial news,
                            select an article, and analyze it
                            with FinRadar AI.
                        </div>
                        """
                    )

                    articles_state = gr.State([])
                    page_state = gr.State(1)
                    last_symbol_state = gr.State("")

                    with gr.Row():
                        with gr.Column(scale=5):
                            gr.HTML(
                                """
                                <div class="fr-field-label">
                                    Ticker / Company Symbol
                                </div>
                                """
                            )

                            ticker_input = gr.Textbox(
                                label=None,
                                show_label=False,
                                container=False,
                                placeholder=(
                                    "Enter a ticker, e.g. AAPL, MSFT, TSLA"
                                ),
                                elem_classes=[
                                    "fr-ticker-input"
                                ],
                            )

                        with gr.Column(
                            scale=2,
                            min_width=180,
                        ):
                            gr.HTML(
                                """
                                <div class="fr-field-label fr-field-label-spacer">
                                    &nbsp;
                                </div>
                                """
                            )

                            fetch_button = gr.Button(
                                "Fetch Latest News",
                                variant="primary",
                                min_width=180,
                                elem_classes=[
                                    "fr-fetch-btn"
                                ],
                            )

                    news_results_group = gr.Column(
                        visible=False
                    )

                    with news_results_group:
                        gr.HTML(
                            """
                            <div class="fr-section-title"
                                 style="margin-top:16px;">
                                Latest Financial News
                            </div>
                            """
                        )

                        article_selector = gr.Radio(
                            choices=[],
                            value=None,
                            label=None,
                            show_label=False,
                            container=False,
                            visible=False,
                            interactive=True,
                            elem_id="finradar-news-selector",
                            elem_classes=[
                                "fr-news-list"
                            ],
                        )

                        page_status = gr.Markdown(
                            visible=False
                        )

                        article_details = gr.Markdown(
                            "Select a news article to view its details.",
                            elem_classes=[
                                "fr-article-card"
                            ],
                        )

                        analyze_live_button = gr.Button(
                            "✦  Analyze Selected News with AI",
                            variant="primary",
                            visible=False,
                            elem_classes=[
                                "fr-analyze-btn"
                            ],
                        )

                analysis_results_group = gr.Column(
                    visible=False,
                    scale=7,
                    min_width=680,
                    elem_classes=[
                        "fr-analysis-panel"
                    ],
                )

                with analysis_results_group:
                    gr.HTML(
                        """
                        <div class="fr-analysis-heading">
                            ✦ AI Analysis Results
                        </div>

                        <div class="fr-analysis-caption">
                            AI-generated insights for
                            the selected financial news.
                        </div>
                        """
                    )

                    live_analysis = gr.HTML(
                        value=ANALYSIS_PLACEHOLDER
                    )

            ticker_input.change(
                fn=reset_fetch_state,
                inputs=ticker_input,
                outputs=[
                    fetch_button,
                    page_state,
                    analyze_live_button,
                    article_selector,
                    articles_state,
                    article_details,
                    live_analysis,
                    page_status,
                    news_results_group,
                    analysis_results_group,
                ],
                show_progress="hidden",
            )

            fetch_button.click(
                fn=fetch_marketaux_news,
                inputs=[
                    ticker_input,
                    page_state,
                    last_symbol_state,
                ],
                outputs=[
                    article_selector,
                    articles_state,
                    article_details,
                    live_analysis,
                    page_status,
                    page_state,
                    last_symbol_state,
                    fetch_button,
                    analyze_live_button,
                    news_results_group,
                    analysis_results_group,
                ],
                show_progress="hidden",
            )

            article_selector.change(
                fn=handle_article_selection,
                inputs=[
                    article_selector,
                    articles_state,
                ],
                outputs=[
                    article_details,
                    analyze_live_button,
                ],
                show_progress="hidden",
            )

            analyze_live_button.click(
                fn=analyze_selected_article,
                inputs=[
                    article_selector,
                    articles_state,
                ],
                outputs=live_analysis,
                show_progress="full",
            )

        with gr.Tab(
            "▤ Manual Public News"
        ):
            with gr.Row():
                with gr.Column(
                    scale=5,
                    min_width=460,
                    elem_classes=[
                        "fr-workspace-card"
                    ],
                ):
                    gr.HTML(
                        """
                        <div class="fr-section-title">
                            Manual Public News
                        </div>

                        <div class="fr-section-help">
                            Paste a public financial
                            headline or short news
                            description for analysis.
                        </div>
                        """
                    )

                    manual_input = gr.Textbox(
                        label="Public Financial News",
                        lines=8,
                        placeholder=(
                            "Paste a public financial "
                            "headline or short news "
                            "description here..."
                        ),
                    )

                    manual_button = gr.Button(
                        "✦  Analyze News with AI",
                        variant="primary",
                        elem_classes=[
                            "fr-analyze-btn"
                        ],
                    )

                with gr.Column(
                    scale=7,
                    min_width=680,
                    elem_classes=[
                        "fr-analysis-panel"
                    ],
                ):
                    gr.HTML(
                        """
                        <div class="fr-analysis-heading">
                            ✦ AI Analysis Results
                        </div>

                        <div class="fr-analysis-caption">
                            Structured FinRadar analysis
                            for the submitted public news.
                        </div>
                        """
                    )

                    manual_analysis = gr.HTML(
                        value=ANALYSIS_PLACEHOLDER
                    )

            manual_button.click(
                fn=analyze_financial_text,
                inputs=manual_input,
                outputs=manual_analysis,
                show_progress="full",
            )

    with gr.Row():
        with gr.Column(
            scale=8,
            elem_classes=["earnings-heading-row"],
        ):
            gr.HTML(
                """
                <div class="earnings-heading-title">
                    Weekly Earnings Calendar
                </div>

                <div class="earnings-heading-help">
                    Upcoming company earnings announcements
                    for the current trading week.
                </div>
                """
            )

        with gr.Column(
            scale=2,
            min_width=220,
            elem_classes=["earnings-refresh-col"],
        ):
            refresh_earnings_button = gr.Button(
                "↻ Refresh Earnings",
                variant="primary",
                min_width=200,
                elem_classes=[
                    "earnings-refresh-btn"
                ],
            )

    earnings_calendar = gr.HTML(
        value=build_earnings_calendar_html(
            loading=True
        )
    )

    refresh_earnings_button.click(
        fn=fetch_weekly_earnings,
        inputs=None,
        outputs=earnings_calendar,
        show_progress="minimal",
    )

    demo.load(
        fn=fetch_weekly_earnings,
        inputs=None,
        outputs=earnings_calendar,
        show_progress="minimal",
    )

if __name__ == "__main__":
    launch_options = {}

    if LOGO_FILE.exists():
        launch_options["favicon_path"] = str(LOGO_FILE)

    demo.launch(**launch_options)
