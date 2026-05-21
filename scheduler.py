"""常駐プロセス版スケジューラー"""

from __future__ import annotations

import os
import sys
import time

import schedule
from dotenv import load_dotenv

from main import run


def _interval_minutes() -> int:
    raw = os.environ.get("SCHEDULE_INTERVAL_MINUTES", "60")
    try:
        return max(1, int(raw))
    except ValueError:
        return 60


def start() -> None:
    load_dotenv()
    interval = _interval_minutes()

    print(f"スケジューラー起動: {interval} 分間隔で実行します")
    schedule.every(interval).minutes.do(run)
    run()

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        print("\n停止しました")
        sys.exit(0)
    except Exception as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        sys.exit(1)
