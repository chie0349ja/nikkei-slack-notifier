"""Slack Incoming Webhook で送信"""

from __future__ import annotations

import os

import requests


def send_to_slack(text: str, webhook_url: str | None = None) -> None:
    """Slack Incoming Webhook にメッセージを送信する。"""
    url = webhook_url or os.environ.get("SLACK_WEBHOOK_URL")
    if not url:
        raise ValueError("SLACK_WEBHOOK_URL が設定されていません")

    response = requests.post(
        url,
        json={"text": text},
        timeout=30,
    )
    response.raise_for_status()
