#!/usr/bin/env python3
"""Regenerate the profile board SVGs and the shipping-log table in README.md.

Pulls live data from the GitHub CLI, so the board reflects whatever was actually
pushed most recently. Run it locally or let .github/workflows/refresh-profile.yml
run it on a schedule.

    python scripts/build_profile.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

USER = "JonathanSolvesProblems"
ROOT = Path(__file__).resolve().parent.parent
ROWS = 6
NAME_MAX = 44

# Geometry. Columns are spaced for a ~8.4px monospace advance at 14px so the
# board survives whatever monospace font the viewer's OS resolves.
W = 900
PAD = 32
ROW_H = 36
ROWS_TOP = 148
COL_DATE, COL_NAME, COL_STACK, COL_STATUS = 32, 150, 560, 742
H = ROWS_TOP + ROWS * ROW_H + 60

MONO = "ui-monospace,'Cascadia Mono','SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

DARK = {
    "bg": "#0B0F14", "panel": "#111820", "rule": "#1C2733", "flap": "#0E141B",
    "title": "#E6EDF3", "muted": "#7D8590", "accent": "#FFB020",
    "live": "#3FB950", "dim": "#4A5560",
}
LIGHT = {
    "bg": "#FFFFFF", "panel": "#F6F8FA", "rule": "#D8DEE4", "flap": "#EEF1F4",
    "title": "#1F2328", "muted": "#636C76", "accent": "#9A6700",
    "live": "#1A7F37", "dim": "#8C959F",
}


def sh(args: list[str]) -> str:
    out = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        sys.exit(f"command failed: {' '.join(args)}\n{out.stderr.strip()}")
    return out.stdout


# Public and real, but not worth one of six board slots: policy pages, scratch
# repos, anything where a push says nothing about the work. Edit freely; every
# other public repo is picked up automatically.
EXCLUDE = {
    "cooldown-privacy",
    USER,  # this repo: the board must not report on itself, or every scheduled
           # refresh promotes the refresh commit to the top row forever
    f"{USER}-profile-archive",  # abandoned first attempt at this repo. Now private,
                                # so the isPrivate filter already drops it; kept here
                                # so it stays off the board if it is ever made public
}


def fetch_repos() -> list[dict]:
    raw = sh(["gh", "repo", "list", USER, "--limit", "300", "--json",
              "name,description,primaryLanguage,pushedAt,isFork,isPrivate,url"])
    repos = [r for r in json.loads(raw)
             if not r["isFork"] and not r["isPrivate"] and r["name"] not in EXCLUDE]
    repos.sort(key=lambda r: r["pushedAt"], reverse=True)
    return repos


def fetch_contributions() -> int | None:
    """Contribution calendar, or None if the token cannot read it.

    The default Actions token often can't, so this must not be fatal: the board
    simply drops that tally rather than failing the whole refresh.
    """
    q = ("query($u:String!){user(login:$u){contributionsCollection"
         "{contributionCalendar{totalContributions}}}}")
    out = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={q}", "-F", f"u={USER}"],
        capture_output=True, text=True, encoding="utf-8",
    )
    if out.returncode != 0:
        print(f"note: contribution tally unavailable ({out.stderr.strip()[:120]})")
        return None
    try:
        return (json.loads(out.stdout)["data"]["user"]["contributionsCollection"]
                ["contributionCalendar"]["totalContributions"])
    except (KeyError, TypeError, json.JSONDecodeError):
        print("note: contribution tally missing from response")
        return None


def lang_of(repo: dict) -> str:
    return (repo.get("primaryLanguage") or {}).get("name") or "—"


# Markup and config that GitHub happily reports as a repo's "primary language"
# because a build artifact or a vendored bundle outweighs the actual source.
INCIDENTAL = {"HTML", "CSS", "SCSS", "Less", "Dockerfile", "Makefile", "Shell", "Batchfile"}


def resolve_stack(repo: dict) -> str:
    """The language the repo is actually written in.

    primaryLanguage is a byte count, so a checked-in bundle or a docs folder can
    outrank the source. Prefer the largest non-incidental language and only fall
    back to markup when that is genuinely all there is.
    """
    out = subprocess.run(
        ["gh", "api", f'repos/{USER}/{repo["name"]}/languages'],
        capture_output=True, text=True, encoding="utf-8",
    )
    if out.returncode != 0:
        return lang_of(repo)
    try:
        langs: dict[str, int] = json.loads(out.stdout)
    except json.JSONDecodeError:
        return lang_of(repo)
    if not langs:
        return lang_of(repo)
    real = {k: v for k, v in langs.items() if k not in INCIDENTAL}
    pool = real or langs
    return max(pool, key=pool.get)


def build_svg(repos: list[dict], stats: dict, c: dict, theme: str) -> str:
    rows = repos[:ROWS]
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    p: list[str] = []
    p.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="Shipping board for {USER}: the {ROWS} most recently pushed projects.">'
    )
    p.append(f'<rect width="{W}" height="{H}" rx="10" fill="{c["bg"]}"/>')
    p.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="9.5" '
             f'fill="none" stroke="{c["rule"]}"/>')

    # Masthead.
    p.append(f'<text x="{PAD}" y="46" font-family="{MONO}" font-size="21" font-weight="700" '
             f'letter-spacing="3" fill="{c["title"]}">JONATHAN ANDREI</text>')
    p.append(f'<text x="{W-PAD}" y="46" font-family="{MONO}" font-size="12" '
             f'letter-spacing="1.5" text-anchor="end" fill="{c["muted"]}">SHIPPING BOARD</text>')
    p.append(f'<text x="{PAD}" y="76" font-family="{MONO}" font-size="14.5" '
             f'fill="{c["accent"]}">I build software that actually ships.</text>')

    # Column rules and headings.
    p.append(f'<line x1="{PAD}" y1="98" x2="{W-PAD}" y2="98" stroke="{c["rule"]}"/>')
    heads = [(COL_DATE, "PUSHED"), (COL_NAME, "PROJECT"),
             (COL_STACK, "STACK"), (COL_STATUS, "STATUS")]
    for x, label in heads:
        p.append(f'<text x="{x}" y="126" font-family="{MONO}" font-size="11" '
                 f'letter-spacing="1.6" fill="{c["dim"]}">{label}</text>')

    # Board rows, drawn as flaps: a panel with a hairline across its midline.
    for i, r in enumerate(rows):
        y = ROWS_TOP + i * ROW_H
        mid = y + ROW_H / 2
        base = y + ROW_H / 2 + 5
        p.append(f'<rect x="{PAD}" y="{y}" width="{W-2*PAD}" height="{ROW_H-6}" rx="3" '
                 f'fill="{c["panel"] if i % 2 == 0 else c["flap"]}"/>')
        p.append(f'<line x1="{PAD}" y1="{mid-3}" x2="{W-PAD}" y2="{mid-3}" '
                 f'stroke="{c["bg"]}" stroke-width="1" opacity="0.55"/>')

        date = r["pushedAt"][:10]
        name = r["name"]
        if len(name) > NAME_MAX:
            name = name[: NAME_MAX - 1] + "…"

        p.append(f'<text x="{COL_DATE+8}" y="{base}" font-family="{MONO}" font-size="13" '
                 f'fill="{c["muted"]}">{escape(date)}</text>')
        p.append(f'<text x="{COL_NAME}" y="{base}" font-family="{MONO}" font-size="13.5" '
                 f'font-weight="600" fill="{c["title"]}">{escape(name)}</text>')
        p.append(f'<text x="{COL_STACK}" y="{base}" font-family="{MONO}" font-size="13" '
                 f'fill="{c["accent"]}">{escape(r["stack"])}</text>')

        if i == 0:
            # Newest push gets a live indicator; everything below it has landed.
            p.append(f'<circle cx="{COL_STATUS+5}" cy="{base-4}" r="4" fill="{c["live"]}">'
                     f'<animate attributeName="opacity" values="1;0.25;1" dur="2.4s" '
                     f'repeatCount="indefinite"/></circle>')
            p.append(f'<text x="{COL_STATUS+18}" y="{base}" font-family="{MONO}" '
                     f'font-size="13" fill="{c["live"]}">LATEST</text>')
        else:
            p.append(f'<text x="{COL_STATUS}" y="{base}" font-family="{MONO}" font-size="13" '
                     f'fill="{c["dim"]}">SHIPPED</text>')

    # Footer tallies.
    fy = ROWS_TOP + ROWS * ROW_H + 16
    p.append(f'<line x1="{PAD}" y1="{fy}" x2="{W-PAD}" y2="{fy}" stroke="{c["rule"]}"/>')
    parts = [f'{stats["repos"]} REPOSITORIES', f'{stats["langs"]} LANGUAGES']
    if stats["contributions"] is not None:
        parts.append(f'{stats["contributions"]:,} CONTRIBUTIONS THIS YEAR')
    tally = "   ·   ".join(parts)
    p.append(f'<text x="{PAD}" y="{fy+30}" font-family="{MONO}" font-size="12" '
             f'letter-spacing="1.1" fill="{c["muted"]}">{escape(tally)}</text>')
    p.append(f'<text x="{W-PAD}" y="{fy+30}" font-family="{MONO}" font-size="11" '
             f'text-anchor="end" fill="{c["dim"]}">jonathansolvesproblems.com</text>')
    p.append('</svg>')

    out = ROOT / "assets" / f"board-{theme}.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(p), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}  ({generated})")
    return "\n".join(p)


def build_readme(repos: list[dict], stats: dict) -> None:
    """Rewrite only the region between the SHIPPING-LOG markers."""
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")

    lines = ["| Project | What it is | Stack |", "| --- | --- | --- |"]
    for r in repos[:ROWS]:
        desc = (r.get("description") or "").strip().replace("|", "\\|")
        if len(desc) > 96:
            desc = desc[:95].rstrip() + "…"
        lines.append(f'| **[{r["name"]}]({r["url"]})** | {desc or "—"} | {r["stack"]} |')

    block = "\n".join(lines)
    new = re.sub(
        r"(<!-- SHIPPING-LOG:START -->).*?(<!-- SHIPPING-LOG:END -->)",
        lambda m: f"{m.group(1)}\n{block}\n{m.group(2)}",
        text,
        flags=re.S,
    )
    if new == text and "SHIPPING-LOG:START" not in text:
        sys.exit("README.md is missing the SHIPPING-LOG markers")
    readme.write_text(new, encoding="utf-8")
    print("wrote README.md")


def main() -> None:
    repos = fetch_repos()
    for r in repos[:ROWS]:
        r["stack"] = resolve_stack(r)
    stats = {
        "repos": len(repos),
        "langs": len({lang_of(r) for r in repos} - {"—"}),
        "contributions": fetch_contributions(),
    }
    contrib = "unavailable" if stats["contributions"] is None else f"{stats['contributions']:,}"
    print(f"{stats['repos']} repos · {stats['langs']} languages · {contrib} contributions")
    build_svg(repos, stats, DARK, "dark")
    build_svg(repos, stats, LIGHT, "light")
    build_readme(repos, stats)


if __name__ == "__main__":
    main()
