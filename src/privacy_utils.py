from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

SENSITIVE_TYPES = {
    "Location",
    "Health Data",
    "Contacts",
    "Photos",
    "Search History",
    "Identifiers",
    "User Content",
}

TERM_EXPLANATIONS = {
    "Identifiers": "Identifiers are values that can single you out across sessions or services, such as device IDs or advertising IDs.",
    "Diagnostics": "Diagnostics usually means crash logs, performance logs, or technical information used to debug the app.",
    "Usage Data": "Usage data describes how you interact with the app, such as screens visited or features used.",
    "Linked": "Linked means the data can be connected back to your identity or account.",
    "Shared": "Shared means the data may be sent to third parties such as advertisers, analytics providers, or business partners.",
    "Self Reported": "Self reported means the label is provided by the developer, so users may still question completeness or accuracy."
}


def load_apps(path: str | Path) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)



def app_to_dataframe(app: Dict[str, Any]) -> pd.DataFrame:
    df = pd.DataFrame(app["data_collected"])
    if df.empty:
        return pd.DataFrame(columns=["type", "purpose", "shared", "linked", "sensitive"])
    return df



def compute_privacy_metrics(app: Dict[str, Any]) -> Dict[str, Any]:
    items = app["data_collected"]
    total_items = len(items)
    sensitive_count = sum(1 for x in items if x.get("sensitive") or x.get("type") in SENSITIVE_TYPES)
    shared_count = sum(1 for x in items if x.get("shared"))
    linked_count = sum(1 for x in items if x.get("linked"))
    advertising_count = sum(1 for x in items if "advert" in x.get("purpose", "").lower())
    analytics_count = sum(1 for x in items if "analytic" in x.get("purpose", "").lower())

    # Weighted prototype score, not a formal privacy metric.
    score = (
        total_items * 10
        + sensitive_count * 12
        + shared_count * 15
        + linked_count * 8
        + advertising_count * 18
        + analytics_count * 6
        + (8 if app.get("self_reported", True) else 0)
    )
    score = min(round(score, 1), 100)

    if score >= 70:
        level = "High"
    elif score >= 40:
        level = "Moderate"
    else:
        level = "Low"

    return {
        "score": score,
        "level": level,
        "total_items": total_items,
        "sensitive_count": sensitive_count,
        "shared_count": shared_count,
        "linked_count": linked_count,
        "advertising_count": advertising_count,
        "analytics_count": analytics_count,
    }



def plain_language_summary(app: Dict[str, Any]) -> str:
    metrics = compute_privacy_metrics(app)
    parts = []
    parts.append(
        f"{app['app_name']} shows a {metrics['level'].lower()} privacy exposure profile in this prototype."
    )

    if metrics["total_items"] == 0:
        parts.append("The label does not list any collected data types.")
    else:
        parts.append(
            f"The label lists {metrics['total_items']} data categories, including {metrics['sensitive_count']} categories that may be sensitive."
        )

    if metrics["shared_count"] > 0:
        parts.append(
            f"It indicates that {metrics['shared_count']} data categories may be shared with third parties."
        )
    else:
        parts.append("It does not indicate third-party sharing in the listed categories.")

    if metrics["advertising_count"] > 0:
        parts.append("Some collected data appears to be used for advertising related purposes.")

    if app.get("self_reported", True):
        parts.append("Because the label is self reported by the developer, users may still want stronger verification or external evidence.")

    return " ".join(parts)



def generate_recommendations(app: Dict[str, Any]) -> List[str]:
    metrics = compute_privacy_metrics(app)
    recs: List[str] = []

    if metrics["shared_count"] > 0:
        recs.append("Show a clearer split between data used inside the app and data shared with outside parties.")
    if metrics["advertising_count"] > 0:
        recs.append("Flag advertising related collection more prominently because users often react strongly to it.")
    if metrics["sensitive_count"] > 0:
        recs.append("Add plain-language explanations for sensitive categories so users understand why each one is needed.")
    if app.get("self_reported", True):
        recs.append("Add a verification badge or audit status to reduce user distrust in self-reported labels.")

    recs.append("Show the amount of data practice at a glance because users often care about how much data is collected overall.")
    recs.append("Offer a short plain-language summary before the detailed label to reduce jargon and scanning effort.")
    return recs



def get_term_help_table() -> pd.DataFrame:
    rows = [{"Term": k, "Plain-language explanation": v} for k, v in TERM_EXPLANATIONS.items()]
    return pd.DataFrame(rows)



def compare_apps(apps: List[Dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for app in apps:
        m = compute_privacy_metrics(app)
        rows.append(
            {
                "App": app["app_name"],
                "Category": app["category"],
                "Platform": app["platform"],
                "Risk score": m["score"],
                "Risk level": m["level"],
                "Data categories": m["total_items"],
                "Sensitive": m["sensitive_count"],
                "Shared": m["shared_count"],
                "Linked": m["linked_count"],
            }
        )
    return pd.DataFrame(rows).sort_values(by=["Risk score", "Shared", "Sensitive"], ascending=False)
