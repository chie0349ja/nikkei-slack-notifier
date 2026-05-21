"""データ収集（Yahoo Finance / NHK RSS / Reuters RSS）"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

import feedparser
import yfinance as yf


@dataclass
class CollectedData:
    timestamp: str
    nikkei: dict[str, Any] = field(default_factory=dict)
    nhk_news: list[dict[str, str]] = field(default_factory=list)
    reuters_news: list[dict[str, str]] = field(default_factory=list)


NHK_RSS_URL = "https://www3.nhk.or.jp/rss/news/cat0.xml"
REUTERS_JP_RSS_URL = "https://feeds.reuters.com/reuters/JPBusinessNews"
NIKKEI_TICKER = "^N225"


def fetch_yahoo_finance() -> dict[str, Any]:
    """日経平均株価（^N225）の最新データを取得する。"""
    ticker = yf.Ticker(NIKKEI_TICKER)
    info = ticker.info
    history = ticker.history(period="2d")

    if history.empty:
        return {
            "symbol": NIKKEI_TICKER,
            "name": info.get("shortName", "日経平均"),
            "price": None,
            "change": None,
            "change_percent": None,
        }

    latest = history.iloc[-1]
    previous = history.iloc[-2] if len(history) > 1 else latest
    price = float(latest["Close"])
    change = price - float(previous["Close"])
    change_percent = (change / float(previous["Close"])) * 100 if previous["Close"] else 0.0

    return {
        "symbol": NIKKEI_TICKER,
        "name": info.get("shortName", "日経平均"),
        "price": round(price, 2),
        "change": round(change, 2),
        "change_percent": round(change_percent, 2),
    }


def _parse_rss(url: str, limit: int = 5) -> list[dict[str, str]]:
    feed = feedparser.parse(url)
    items: list[dict[str, str]] = []

    for entry in feed.entries[:limit]:
        items.append(
            {
                "title": entry.get("title", "").strip(),
                "link": entry.get("link", "").strip(),
                "published": entry.get("published", entry.get("updated", "")).strip(),
            }
        )

    return items


def fetch_nhk_rss(limit: int = 5) -> list[dict[str, str]]:
    """NHK 主要ニュース RSS を取得する。"""
    return _parse_rss(NHK_RSS_URL, limit=limit)


def fetch_reuters_rss(limit: int = 5) -> list[dict[str, str]]:
    """Reuters 日本ビジネスニュース RSS を取得する。"""
    return _parse_rss(REUTERS_JP_RSS_URL, limit=limit)


def collect_all(
    nhk_limit: int = 5,
    reuters_limit: int = 5,
) -> CollectedData:
    """全ソースからデータを収集する。"""
    return CollectedData(
        timestamp=datetime.now(timezone.utc).isoformat(),
        nikkei=fetch_yahoo_finance(),
        nhk_news=fetch_nhk_rss(limit=nhk_limit),
        reuters_news=fetch_reuters_rss(limit=reuters_limit),
    )
