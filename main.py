"""1回実行エントリーポイント"""

from __future__ import annotations

import sys

from dotenv import load_dotenv

from notifier import send_to_slack
from scraper import collect_all
from summarizer import generate_summary


def run() -> None:
    load_dotenv()

    print("データ収集中...")
    data = collect_all()

    print("サマリー生成中...")
    summary = generate_summary(data)

    print("Slack 送信中...")
    send_to_slack(summary)

    print("完了")


if __name__ == "__main__":
    try:
        run()
    except Exception as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        sys.exit(1)
