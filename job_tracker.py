"""Job Application Tracker - a small CLI tool to manage job applications.

I built this while job hunting in Japan to keep track of applications
sent through different platforms (Indeed, doda, LinkedIn, Workport).

Data is stored in a local JSON file (data.json).
Only the Python standard library is used.
"""

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).with_name("data.json")

STATUSES = ["applied", "screening", "interview", "offer", "rejected", "withdrawn"]


@dataclass
class Application:
    company: str
    position: str
    platform: str
    applied_on: str  # YYYY-MM-DD
    status: str = "applied"
    note: str = ""


class Tracker:
    def __init__(self, data_file: Path = DATA_FILE):
        self.data_file = data_file
        self.applications: list[Application] = []
        self.load()

    def load(self) -> None:
        if self.data_file.exists():
            rows = json.loads(self.data_file.read_text(encoding="utf-8"))
            self.applications = [Application(**row) for row in rows]

    def save(self) -> None:
        rows = [asdict(app) for app in self.applications]
        self.data_file.write_text(
            json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def add(self, app: Application) -> None:
        if app.status not in STATUSES:
            raise ValueError(f"status must be one of: {', '.join(STATUSES)}")
        self.applications.append(app)
        self.save()

    def update_status(self, index: int, status: str) -> Application:
        if status not in STATUSES:
            raise ValueError(f"status must be one of: {', '.join(STATUSES)}")
        app = self.applications[index]
        app.status = status
        self.save()
        return app

    def stats(self) -> dict[str, int]:
        counts = {status: 0 for status in STATUSES}
        for app in self.applications:
            counts[app.status] += 1
        counts["total"] = len(self.applications)
        return counts


def cmd_add(args: argparse.Namespace) -> None:
    tracker = Tracker()
    app = Application(
        company=args.company,
        position=args.position,
        platform=args.platform,
        applied_on=args.date or date.today().isoformat(),
        note=args.note or "",
    )
    tracker.add(app)
    print(f"Added: {app.company} / {app.position} ({app.platform})")


def cmd_list(args: argparse.Namespace) -> None:
    tracker = Tracker()
    if not tracker.applications:
        print("No applications yet.")
        return
    for i, app in enumerate(tracker.applications):
        if args.status and app.status != args.status:
            continue
        print(
            f"[{i}] {app.applied_on}  {app.company}  {app.position}"
            f"  ({app.platform})  -> {app.status}"
        )


def cmd_update(args: argparse.Namespace) -> None:
    tracker = Tracker()
    app = tracker.update_status(args.index, args.status)
    print(f"Updated: {app.company} -> {app.status}")


def cmd_stats(args: argparse.Namespace) -> None:
    tracker = Tracker()
    counts = tracker.stats()
    for status in STATUSES:
        print(f"{status:10}: {counts[status]}")
    print(f"{'total':10}: {counts['total']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Track your job applications")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add a new application")
    p_add.add_argument("company")
    p_add.add_argument("position")
    p_add.add_argument("platform", help="e.g. Indeed, doda, LinkedIn, Workport")
    p_add.add_argument("--date", help="applied date YYYY-MM-DD (default: today)")
    p_add.add_argument("--note", default="")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="list applications")
    p_list.add_argument("--status", choices=STATUSES, help="filter by status")
    p_list.set_defaults(func=cmd_list)

    p_update = sub.add_parser("update", help="update the status of an application")
    p_update.add_argument("index", type=int, help="index shown by the list command")
    p_update.add_argument("status", choices=STATUSES)
    p_update.set_defaults(func=cmd_update)

    p_stats = sub.add_parser("stats", help="show counts by status")
    p_stats.set_defaults(func=cmd_stats)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
