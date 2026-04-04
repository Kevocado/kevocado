#!/usr/bin/env python3
"""
update_readme.py
Re-ranks Kevocado's public GitHub repos by total commit count and rewrites
the <!-- TOP-REPOS-START --> … <!-- TOP-REPOS-END --> block in README.md.

Commit-count method
-------------------
GitHub's REST API doesn't expose a "total commit count" field directly.
We use the pagination trick:
  GET /repos/{owner}/{repo}/commits?per_page=1
If the response includes a `Link: …; rel="last"` header, the page number
in that URL equals the total number of commits.  If there is no "last"
link the response contains exactly one page (≤ 1 commit).

Repos with no commits are skipped from the ranking.
"""

import os
import re
import sys
import time
import urllib.request
import urllib.error
import json

OWNER = "Kevocado"
README_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "README.md")
TOP_N = 4

# Repos to skip (this profile repo itself)
SKIP_REPOS = {"kevocado"}

SECTION_START = "<!-- TOP-REPOS-START -->"
SECTION_END = "<!-- TOP-REPOS-END -->"

# Static metadata for known repos (description, language, highlights).
# The script updates *commit counts* dynamically; the prose is curated here
# so it stays readable even when the script runs in CI without interactive edits.
REPO_META = {
    "OpenClaw-Applicant-Bot": {
        "description": "Autonomous job-application agent that fills and submits forms across job boards with human-in-the-loop approval for top-tier companies.",
        "languages": "Python · Docker · n8n · Playwright · Gemini Pro",
        "highlights": [
            "Distributed architecture: VPS gateway + macOS Playwright execution node over Tailscale",
            "Tier-based routing: auto-submit for standard roles, Telegram gatekeeper for MBB/Big-4",
            "Resume & cover-letter knowledge base fed to Gemini Pro for context-aware form filling",
            "Google Sheets integration for real-time application tracking",
        ],
    },
    "SP500-Predictor": {
        "description": "Prediction-market edge finder for Kalshi (SPX, QQQ, BTC, ETH) combining LightGBM ML models, multi-source sentiment analysis, and a Bloomberg-style Streamlit dashboard.",
        "languages": "Python · Streamlit · LightGBM · Azure · Hugging Face",
        "highlights": [
            "Auto-retraining LightGBM regressors on feature drift for hourly and daily horizons",
            "Cloud model delivery via Hugging Face Hub; logs stored in Azure Blob Storage",
            "Composite sentiment scoring: Crypto Fear & Greed, VIX-derived, and price momentum",
            "Cross-venue arbitrage detection between Kalshi and PredictIt (>5% delta threshold)",
        ],
    },
    "algo-trade-hub-prod": {
        "description": "Production quantitative trading monorepo that discovers arbitrage edges in prediction markets using weather, macro, crypto, and sports data pipelines.",
        "languages": "Python · React · Vite · Supabase · PM2",
        "highlights": [
            "Hybrid architecture: Python daemon on VPS writes to Supabase; React terminal UI on Vercel reads it",
            "Covers Kalshi weather, macro (FRED), crypto momentum, and FPL sports arbitrage engines",
            "PM2 process management for resilient background scanning every 30 seconds",
            "Strict secret split: high-clearance backend tokens vs. public VITE_ frontend config",
        ],
    },
    "Stable-Coin-Analysis": {
        "description": "On-chain stablecoin analytics project studying cross-border remittance flows between Global North and South exchanges using BigQuery public blockchain data.",
        "languages": "SQL (BigQuery) · Python",
        "highlights": [
            "Queries USDT/USDC on-chain transfer data to compare L1 vs L2 remittance costs",
            "Geographic exchange classification (Global North vs South) for flow analysis",
            "Transfer-size histogram and stablecoin-preference breakdowns by region",
            "Collaborative project with University of Illinois CS team",
        ],
    },
}


def gh_request(path: str, token: str) -> tuple:
    """Return (parsed_json_or_None, headers_dict) for a GitHub API path."""
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read())
            headers = dict(resp.headers)
            return body, headers
    except urllib.error.HTTPError as exc:
        print(f"  HTTP {exc.code} for {url}", file=sys.stderr)
        return None, {}


def get_commit_count(owner: str, repo: str, token: str) -> int:
    """Return exact total commit count using the Link-header pagination trick."""
    path = f"/repos/{owner}/{repo}/commits?per_page=1"
    _, headers = gh_request(path, token)
    link = headers.get("Link", "")
    if not link:
        # 0 or 1 commit; try fetching to see
        body, _ = gh_request(path, token)
        return len(body) if body else 0
    # Parse rel="last" page number
    match = re.search(r'page=(\d+)>; rel="last"', link)
    if match:
        return int(match.group(1))
    return 1


def list_public_repos(owner: str, token: str) -> list:
    repos = []
    page = 1
    while True:
        data, _ = gh_request(f"/users/{owner}/repos?per_page=100&page={page}", token)
        if not data:
            break
        repos.extend(data)
        if len(data) < 100:
            break
        page += 1
    return repos


def build_section(ranked: list) -> str:
    lines = [SECTION_START, ""]
    lines.append("## 🏆 Featured Projects")
    lines.append("")
    lines.append("*Auto-ranked by total commit count · updated weekly by GitHub Actions*")
    lines.append("")

    for i, (repo_name, count, html_url) in enumerate(ranked, start=1):
        meta = REPO_META.get(repo_name, {})
        desc = meta.get("description", "_No description available._")
        langs = meta.get("languages", "")
        highlights = meta.get("highlights", [])

        medal = ["🥇", "🥈", "🥉", "4️⃣"][i - 1] if i <= 4 else f"{i}."
        lines.append(f"### {medal} [{repo_name}]({html_url})")
        lines.append("")
        lines.append(desc)
        lines.append("")
        if langs:
            lines.append(f"**Stack:** {langs}")
            lines.append("")
        if highlights:
            for h in highlights:
                lines.append(f"- {h}")
            lines.append("")
        lines.append(f"*{count} commits*")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append(SECTION_END)
    return "\n".join(lines)


def update_readme(section_text: str) -> None:
    with open(README_PATH, "r", encoding="utf-8") as fh:
        content = fh.read()

    pattern = re.compile(
        re.escape(SECTION_START) + ".*?" + re.escape(SECTION_END),
        re.DOTALL,
    )
    if pattern.search(content):
        new_content = pattern.sub(section_text, content)
    else:
        new_content = content.rstrip() + "\n\n" + section_text + "\n"

    with open(README_PATH, "w", encoding="utf-8") as fh:
        fh.write(new_content)


def main():
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("Warning: GITHUB_TOKEN not set; unauthenticated requests are rate-limited to 60/hr.", file=sys.stderr)

    print(f"Listing public repos for {OWNER}…")
    repos = list_public_repos(OWNER, token)
    repos = [r for r in repos if r["name"].lower() not in SKIP_REPOS and not r.get("fork", False)]
    print(f"Found {len(repos)} non-fork public repos")

    counts = []
    for repo in repos:
        name = repo["name"]
        html_url = repo["html_url"]
        print(f"  Counting commits in {name}…", end=" ", flush=True)
        count = get_commit_count(OWNER, name, token)
        print(count)
        counts.append((name, count, html_url))
        time.sleep(0.25)  # stay well within rate limits

    ranked = sorted(counts, key=lambda x: x[1], reverse=True)[:TOP_N]
    print("\nTop repos:")
    for name, count, _ in ranked:
        print(f"  {name}: {count}")

    section = build_section(ranked)
    update_readme(section)
    print(f"\nREADME.md updated at {os.path.abspath(README_PATH)}")


if __name__ == "__main__":
    main()
