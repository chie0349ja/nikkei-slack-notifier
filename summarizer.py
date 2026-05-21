"""Claude API でサマリー生成"""

from __future__ import annotations

import json
import os

from anthropic import Anthropic

from scraper import CollectedData


def _format_data(data: CollectedData) -> str:
    return json.dumps(
        {
            "timestamp": data.timestamp,
            "nikkei": data.nikkei,
            "nhk_news": data.nhk_news,
            "reuters_news": data.reuters_news,
        },
        ensure_ascii=False,
        indent=2,
    )


def generate_summary(data: CollectedData, model: str = "claude-sonnet-4-20250514") -> str:
    """収集データから Slack 向けの日本語サマリーを生成する。"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY が設定されていません")

    client = Anthropic(api_key=api_key)
    prompt = f"""以下は日経平均株価と最新ニュースのデータです。
Slack 通知向けに、日本語で簡潔なサマリーを作成してください。

要件:
- 日経平均の現在値・前日比を冒頭に記載
- NHK と Reuters のニュースから重要なトピックを 3〜5 件ピックアップ
- 箇条書き中心、全体 400 文字程度
- 絵文字は使わない

データ:
{_format_data(data)}
"""

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text.strip()
