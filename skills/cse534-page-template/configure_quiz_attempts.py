#!/usr/bin/env python3
"""
Configure Canvas quiz attempt policy (multiple attempts + keep highest score).

Usage examples:
    python3 configure_quiz_attempts.py --attempts -1 --title "Lecture 1 Quiz - GIS Overview and Geospatial Data Types"
    python3 configure_quiz_attempts.py --attempts -1 --title-contains "Lecture" --apply
    python3 configure_quiz_attempts.py --all --apply

Defaults:
  - Dry run unless --apply is provided
  - scoring_policy set to keep_highest

Environment variables:
  CANVAS_ACCESS_TOKEN (required)
  CANVAS_BASE_URL (optional, default: https://miamioh.instructure.com)
  CANVAS_COURSE_ID (required unless --course-id provided)
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from typing import Iterable, List

from canvasapi import Canvas

try:
    from dotenv import find_dotenv, load_dotenv

    dotenv_path = find_dotenv(usecwd=True)
    if dotenv_path:
        load_dotenv(dotenv_path)
    else:
        load_dotenv()
except Exception:
    pass


@dataclass
class QuizPolicy:
    attempts: int
    scoring_policy: str = "keep_highest"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--course-id", default=os.environ.get("CANVAS_COURSE_ID"))
    parser.add_argument("--canvas-url", default=os.environ.get("CANVAS_BASE_URL", "https://miamioh.instructure.com"))
    parser.add_argument("--token", default=os.environ.get("CANVAS_ACCESS_TOKEN"))

    parser.add_argument(
        "--attempts",
        type=int,
        default=-1,
        help="Allowed attempts. Use -1 for unlimited attempts. Default: -1 (unlimited)",
    )

    parser.add_argument(
        "--scoring-policy",
        default="keep_highest",
        choices=["keep_highest", "keep_latest"],
        help="Canvas scoring policy for multiple attempts. Default: keep_highest",
    )

    parser.add_argument(
        "--title",
        action="append",
        default=[],
        help="Exact quiz title to update. Repeat for multiple quizzes.",
    )
    parser.add_argument(
        "--title-contains",
        default="",
        help="Update quizzes whose titles contain this case-insensitive fragment.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Update all quizzes in the course.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes. Without this flag, only prints planned updates.",
    )

    args = parser.parse_args()

    if not args.token:
        print("ERROR: CANVAS_ACCESS_TOKEN not set and --token not provided.")
        sys.exit(1)
    if not args.course_id:
        print("ERROR: CANVAS_COURSE_ID not set and --course-id not provided.")
        sys.exit(1)
    if args.attempts == 0 or args.attempts < -1:
        print("ERROR: --attempts must be -1 (unlimited) or a positive integer.")
        sys.exit(1)
    if not args.all and not args.title and not args.title_contains:
        print("ERROR: choose one selector: --all, --title, or --title-contains.")
        sys.exit(1)

    return args


def selected(quiz_title: str, exact_titles: List[str], title_contains: str, all_quizzes: bool) -> bool:
    if all_quizzes:
        return True
    if quiz_title in exact_titles:
        return True
    if title_contains and title_contains.lower() in quiz_title.lower():
        return True
    return False


def iter_selected_quizzes(course, args: argparse.Namespace) -> Iterable:
    for quiz in course.get_quizzes():
        if selected(quiz.title, args.title, args.title_contains, args.all):
            yield quiz


def main() -> None:
    args = parse_args()

    canvas = Canvas(args.canvas_url, args.token)
    course = canvas.get_course(args.course_id)
    policy = QuizPolicy(attempts=args.attempts, scoring_policy=args.scoring_policy)

    matches = list(iter_selected_quizzes(course, args))
    if not matches:
        print("No quizzes matched the selector.")
        return

    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"Mode: {mode}")
    print(f"Course: {args.course_id}")
    print(f"Target policy: attempts={policy.attempts}, scoring_policy={policy.scoring_policy}")
    print(f"Matched quizzes: {len(matches)}")

    for quiz in matches:
        before_attempts = getattr(quiz, "allowed_attempts", None)
        before_policy = getattr(quiz, "scoring_policy", None)

        print("-" * 72)
        print(f"Quiz: {quiz.title}")
        print(f"  before: attempts={before_attempts}, scoring_policy={before_policy}")

        if args.apply:
            quiz.edit(
                quiz={
                    "allowed_attempts": policy.attempts,
                    "scoring_policy": policy.scoring_policy,
                }
            )
            refreshed = course.get_quiz(quiz.id)
            print(
                "  after: "
                f"attempts={getattr(refreshed, 'allowed_attempts', None)}, "
                f"scoring_policy={getattr(refreshed, 'scoring_policy', None)}"
            )


if __name__ == "__main__":
    main()
