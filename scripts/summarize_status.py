#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "anthropic",
#     "python-dotenv",
# ]
# ///
"""Fetch GitHub Project status updates, summarize with Claude, and post back."""

import argparse
import json
import subprocess
import sys

import anthropic
from dotenv import load_dotenv

load_dotenv()

PROJECT_NODE_ID = "PVT_kwHOCHvKyc4BOPfE"

UPDATES_QUERY = """
query($cursor: String) {
  user(login: "e-straight") {
    projectV2(number: 2) {
      id
      statusUpdates(first: 100, orderBy: {field: CREATED_AT, direction: DESC}, after: $cursor) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          id
          body
          status
          createdAt
          creator {
            login
          }
          startDate
          targetDate
        }
      }
    }
  }
}
"""

POST_MUTATION = """
mutation($projectId: ID!, $body: String!, $status: ProjectV2StatusUpdateStatus!) {
  createProjectV2StatusUpdate(input: {projectId: $projectId, body: $body, status: $status}) {
    statusUpdate {
      id
      createdAt
    }
  }
}
"""


def gh_graphql(query: str, variables: dict | None = None) -> dict:
    """Execute a GraphQL query via the gh CLI."""
    payload = json.dumps({"query": query, "variables": variables or {}})
    result = subprocess.run(
        ["gh", "api", "graphql", "--input", "-"],
        input=payload,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def fetch_status_updates() -> list[dict]:
    """Fetch all status updates from the project, paginating if needed."""
    all_updates = []
    cursor = None

    while True:
        variables = {}
        if cursor:
            variables["cursor"] = cursor

        data = gh_graphql(UPDATES_QUERY, variables)
        project = data["data"]["user"]["projectV2"]
        updates_data = project["statusUpdates"]

        all_updates.extend(updates_data["nodes"])

        if updates_data["pageInfo"]["hasNextPage"]:
            cursor = updates_data["pageInfo"]["endCursor"]
        else:
            break

    # Reverse so they're in chronological order (oldest first)
    all_updates.reverse()
    return all_updates


def format_updates_for_prompt(updates: list[dict]) -> str:
    """Format status updates as a numbered list for the LLM prompt."""
    lines = []
    for i, u in enumerate(updates, 1):
        creator = u.get("creator", {}).get("login", "unknown")
        status = u.get("status") or "INACTIVE"
        created = u.get("createdAt", "")[:10]
        body = (u.get("body") or "").strip()

        header = f"[{i}] {created} | {status} | @{creator}"
        if u.get("startDate") or u.get("targetDate"):
            header += f" | {u.get('startDate', '?')} → {u.get('targetDate', '?')}"

        lines.append(header)
        if body:
            lines.append(body)
        lines.append("")

    return "\n".join(lines)


def summarize(updates_text: str) -> str:
    """Send status updates to Claude and return a markdown summary."""
    client = anthropic.Anthropic()

    prompt = f"""You are summarizing the status update history for a GitHub Project board called "Elijah Backlog".

Below are all the status updates posted to the project, in chronological order. Each entry includes the date, status enum (ON_TRACK, AT_RISK, OFF_TRACK, INACTIVE, COMPLETE), the creator, and the body text.

Produce a concise markdown summary of the project's progress. Focus on:
- Key milestones and accomplishments
- Current status and trajectory
- Any risks or blockers mentioned
- What's coming next

Keep it to 2-4 short paragraphs. Use plain markdown (no H1 headers). Start directly with the summary content.

---

{updates_text}"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def post_status_update(body: str, status: str = "ON_TRACK") -> dict:
    """Post a new status update to the project."""
    data = gh_graphql(
        POST_MUTATION,
        {"projectId": PROJECT_NODE_ID, "body": body, "status": status},
    )
    return data["data"]["createProjectV2StatusUpdate"]["statusUpdate"]


def main():
    parser = argparse.ArgumentParser(
        description="Summarize GitHub Project status updates and post a new one."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print summary but do not post it.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="dump_json",
        help="Print raw status updates as JSON and exit.",
    )
    args = parser.parse_args()

    updates = fetch_status_updates()

    if not updates:
        print("No status updates found.", file=sys.stderr)
        sys.exit(1)

    if args.dump_json:
        print(json.dumps(updates, indent=2))
        return

    updates_text = format_updates_for_prompt(updates)
    print(f"Fetched {len(updates)} status update(s). Summarizing...\n", file=sys.stderr)

    summary = summarize(updates_text)
    print(summary)

    if args.dry_run:
        print("\n[dry-run] Summary was NOT posted.", file=sys.stderr)
        return

    result = post_status_update(summary)
    print(
        f"\nPosted status update: {result['id']} (created {result['createdAt']})",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
